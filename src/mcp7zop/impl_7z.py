# encoding : utf-8

import os
import sys
import shutil
import asyncio
import anyio
from pathlib import Path
from typing import Annotated 

from .config import get_config

# -------------------------------------------------------------------------------------------
# detect the path to the 7z executable
def detect_7z_path() -> Path:
    """
    Detect the path to the 7z executable.
    """
    exe_name = "7z.exe" if sys.platform == "nt" else "7z"
    # Check if 7z is in the system PATH
    cfg_7z_path = shutil.which(exe_name)
    if not cfg_7z_path:
        cfg = get_config()
        cfg_7z_path = cfg.get("7z_path", exe_name)
        if not cfg_7z_path:
            raise FileNotFoundError(f"7z executable not found at {cfg_7z_path}")
    return Path(cfg_7z_path).resolve()

# -------------------------------------------------------------------------------------------
# create or update an archive file from the specified paths
async def create_or_update_archive(archive_path: Path,
                                   input_paths: list[str | os.PathLike]) -> None:
    """
    Create or update an archive file from the specified paths.
    """
    cfg_7z_path = detect_7z_path()
    in_list = [str(p) for p in input_paths if Path(p).exists()]
    if not in_list:
        raise ValueError("No valid input paths provided for archiving.")
    else:
        process = await asyncio.create_subprocess_exec(
            cfg_7z_path,
            'a', "-ba", "-bd", "-sccUTF-8", "-y",
            str(archive_path), *input_paths,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        _, stderr = await process.communicate()
        if process.returncode != 0:
            raise Exception(f"Error creating archive: {stderr.decode(encoding='utf-8').strip()}")

# -------------------------------------------------------------------------------------------
# extract an archive file to the specified directory
async def extract_archive(archive_path: Path, extract_dir: Path) -> None:
    """
    Extract an archive file to the specified directory.
    """
    cfg_7z_path = detect_7z_path()
    if not archive_path.exists():
        raise FileNotFoundError(f"Archive file not found: {archive_path}")

    process = await asyncio.create_subprocess_exec(
        cfg_7z_path,
        'x', "-ba", "-bd", "-sccUTF-8", "-y",
        str(archive_path), f'-o{extract_dir}',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    _, stderr = await process.communicate()
    if process.returncode != 0:
        raise Exception(f"Error extracting archive: {stderr.decode(encoding='utf-8').strip()}")


# -------------------------------------------------------------------------------------------
# parse the content lines of an archive item
def parse_content_lines(content_lines: list[str]) -> (dict[str, str] | None):
    """
    Parse the content lines of an archive item.
    """
    result_item: dict[str, str] = None
    if content_lines:
        item_info = {}
        for line in content_lines:
            # split with '=' and strip spaces
            line_data = line.split('=', 1)
            if len(line_data) != 2:
                break
            key = line_data[0].strip()
            value = line_data[1].strip()
            item_info[key] = value
        if item_info:
            result_item = item_info
    return result_item

# -------------------------------------------------------------------------------------------
# list items in the archive
async def mcp7zop_get_archive_item_list_impl(
        archive_path: Annotated[str | os.PathLike, "Path to the archive file to list items from"]
    ) -> list[dict[str, str]]:
    """
    Extract an archive file to the specified directory.
    """
    cfg_7z_path = detect_7z_path()
    archive_path_obj = Path(archive_path)
    if not archive_path_obj.exists():
        raise FileNotFoundError(f"Archive file not found: {archive_path}")

    item_list = []
    async with anyio.TemporaryDirectory() as td:
        temp_dir = Path(td)
        # create file in the temp directory to store the list
        list_file = temp_dir / "list.txt"
        # open the file for writing
        async with await anyio.open_file(list_file, 'w', encoding='utf-8') as f:
            process = await asyncio.create_subprocess_exec(
                cfg_7z_path,
                'l', "-ba", "-slt", "-sccUTF-8", "-y",
                str(archive_path),
                stdout=f,
                stderr=asyncio.subprocess.PIPE
            )
            _, stderr = await process.communicate()
            if process.returncode != 0:
                raise Exception(f"Error listing archive: {stderr.decode(encoding='utf-8').strip()}")

        # read the list file and parse it
        async with await anyio.open_file(list_file, 'r', encoding='utf-8') as f:
            content_lines = []
            async for line in f:
                content = line.strip()
                if not content:
                    # if content is empty string, it is the end of an item
                    if content_lines:
                        item_info = parse_content_lines(content_lines)
                        if item_info:
                            item_list.append(item_info)
                        content_lines.clear()
                else:
                    # add the line to the content lines
                    content_lines.append(content)

        return item_list

# -------------------------------------------------------------------------------------------
# main implementation for creating an archive
async def mcp7zop_make_archive_impl(
        archive_path: Annotated[str | os.PathLike, "output archive path will be saved."],
        input_pathes: Annotated[list[str | os.PathLike], "input file paths"]
    ) -> str:
    """
    main implementation for creating or updating an archive
    """
    ret = ""
    ps_archive_path = Path(archive_path).resolve()
    if ps_archive_path.is_dir():
        raise ValueError(f"Archive path must be a file, not a directory: {ps_archive_path}")
    if ps_archive_path.exists():
        os.remove(ps_archive_path)  # remove the existing archive file if it exists

    # getting extension of the archive file
    suffix = ps_archive_path.suffix.lower()
    if suffix not in ['.7z', '.zip']:
        raise ValueError(f"Unsupported archive format: {suffix}. Supported formats are .7z and .zip.")
    # remove '.' from the suffix
    # archive_type = suffix[1:]

    async with anyio.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / f"temp_archive{suffix}"
        await create_or_update_archive(temp_path, input_pathes)
        shutil.move(temp_path, ps_archive_path)
        ret = str(ps_archive_path)

    return ret

# -------------------------------------------------------------------------------------------
# main implementation for creating an archive
async def mcp7zop_replace_archive_items_impl(
        archive_path: Annotated[str | os.PathLike, "output archive path will be saved."],
        replace_pathes: Annotated[list[str | os.PathLike], "input file paths to be replaced in the archive"],
    ) -> str:
    """
    main implementation for replacing items in an archive
    """
    ret = ""
    ps_archive_path = Path(archive_path).resolve()
    if ps_archive_path.is_dir() or not ps_archive_path.exists():
        raise FileNotFoundError(f"Archive file does not exist: {ps_archive_path}")

    # getting extension of the archive file
    suffix = ps_archive_path.suffix.lower()
    if suffix not in ['.7z', '.zip']:
        raise ValueError(f"Unsupported archive format: {suffix}. Supported formats are .7z and .zip.")
    # remove '.' from the suffix
    # archive_type = suffix[1:]

    await create_or_update_archive(ps_archive_path, replace_pathes)
    ret = str(ps_archive_path)
    return ret

# -------------------------------------------------------------------------------------------
# main implementation for extracting an archive
async def mcp7zop_extract_archive_impl(archive_path: str | os.PathLike,
                                       extract_dir: str | os.PathLike) -> list[str]:
    """
    main implementation for extracting an archive
    """
    retList = []
    ps_archive_path = Path(archive_path).resolve()
    if not ps_archive_path.exists():
        raise FileNotFoundError(f"Archive file not found: {ps_archive_path}")

    # getting extension of the archive file
    suffix = ps_archive_path.suffix.lower()
    if suffix not in ['.7z', '.zip']:
        raise ValueError(f"Unsupported archive format: {suffix}. Supported formats are .7z and .zip.")

    extract_dir = Path(extract_dir).resolve()
    if not extract_dir.exists():
        extract_dir.mkdir(parents=True, exist_ok=True)

    await extract_archive(archive_path=ps_archive_path, extract_dir=extract_dir)
    retList = [str(p.resolve()) for p in extract_dir.rglob('*') if p.is_file()]
    # return the list of extracted files.
    return retList

# -------------------------------------------------------------------------------------------
# mcp tool for  items in an archive
async def mcp7zop_remove_archive_item_impl(
        archive_path: Annotated[str | os.PathLike, "Path to the archive file to remove items from"],
        remove_item_paths: Annotated[list[str | os.PathLike], "list of item pathes to be removed from the archive"]
    ) -> str:
    """
    Remove items from an archive file.
    """
    ps_archive_path = Path(archive_path).resolve()
    if not ps_archive_path.exists():
        raise FileNotFoundError(f"Archive file not found: {ps_archive_path}")
    if not remove_item_paths:
        raise ValueError("No items to remove from the archive.")
    # getting extension of the archive file
    suffix = ps_archive_path.suffix.lower()
    if suffix not in ['.7z', '.zip']:
        raise ValueError(f"Unsupported archive format: {suffix}. Supported formats are .7z and .zip.")

    cfg_7z_path = detect_7z_path()
    process = await asyncio.create_subprocess_exec(
        cfg_7z_path,
        'd', "-ba", "-bd", "-sccUTF-8", "-y",
        str(ps_archive_path), *remove_item_paths,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    _, stderr = await process.communicate()
    if process.returncode != 0:
        raise Exception(f"Error removing items from archive: {stderr.decode(encoding='utf-8').strip()}")
    # return the path to the archive file
    return str(ps_archive_path)

