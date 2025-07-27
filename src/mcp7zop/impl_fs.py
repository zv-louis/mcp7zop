# encoding : utf-8

import os
from pathlib import Path

# -------------------------------------------------------------------------------------------
# get if the specified path exists
def path_is_exist(path: str | os.PathLike) -> bool:
    """
    Check if the specified path exists.
    """
    return Path(path).exists()

# -------------------------------------------------------------------------------------------
# get info of specified path
def get_path_item_info_impl(path: str | os.PathLike) -> dict[str, str]:
    """
    Get file and directory info of specified path.
    """
    ps_path = Path(path).resolve()
    if not ps_path.exists():
        raise FileNotFoundError(f"Path not found: {ps_path}")
    item_info = {}
    if ps_path.is_file():
        item_info["type"] = "file"
    elif ps_path.is_dir():
        item_info["type"] = "directory"
    elif ps_path.is_symlink():
        item_info["type"] = "symlink"
    else:
        raise ValueError(f"Unsupported path type: {ps_path}")
    st = ps_path.stat()
    item_info["name"] = str(ps_path.name)
    item_info["size"] = str(st.st_size)
    item_info["mtime"] = str(st.st_mtime)
    item_info["path"] = str(ps_path.resolve())
    return item_info

# -------------------------------------------------------------------------------------------
# get file and directory list of specified path
def get_dir_item_list_impl(path: str | os.PathLike) -> list[dict[str, str]]:
    """
    Get file and directory list of specified path.
    """
    ps_path = Path(path).resolve()
    if not ps_path.exists():
        raise FileNotFoundError(f"Path not found: {ps_path}")

    item_list = []
    if not ps_path.is_dir():
        raise ValueError(f"Specified path is not a directory: {ps_path}")
    for item in ps_path.iterdir():
        #Skip . and ..
        if item.name in ('.', '..'):
            continue
        else:
            item_info = get_path_item_info_impl(item)
            item_list.append(item_info)

    return item_list
