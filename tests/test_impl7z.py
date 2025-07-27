# encoding : utf-8
import os
import pytest
import anyio
from pathlib import Path

from src.mcp7zop.impl_7z import *

# -------------------------------------------------------------------------------------------
# Test for mcp7zop_make_archive function
@pytest.mark.asyncio
async def test_make_archive():
    """
    Test the mcp7zop_make_archive function.
    """
    async with anyio.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        archive_path = temp_dir / "test_archive.7z"
        input_paths = [temp_dir / "test_file1.txt", temp_dir / "test_file2.txt"]

        # Create test files
        for path in input_paths:
            with open(path, 'w') as f:
                f.write("This is a test file.")

        # Call the mcp7zop_make_archive function
        try:
            result = await mcp7zop_make_archive_impl(archive_path, input_paths)
            assert isinstance(result, str)
            assert Path(result).exists()
        finally:
            # Clean up test files
            for path in input_paths:
                os.remove(path)
            if Path(archive_path).exists():
                os.remove(archive_path)


# -------------------------------------------------------------------------------------------
# test for extracting an archive
@pytest.mark.asyncio
async def test_extract_archive():
    """
    Test the mcp7zop_extract_archive function.
    """
    async with anyio.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        archive_path = temp_dir / "test_archive.7z"
        extract_dir = temp_dir / "extracted_files"
        input_paths = [temp_dir / "test_file1.txt", temp_dir / "test_file2.txt"]

        # Create test files and archive them
        for path in input_paths:
            with open(path, 'w') as f:
                f.write("This is a test file.")

        # Create the archive
        await mcp7zop_make_archive_impl(archive_path, input_paths)

        # Call the mcp7zop_extract_archive function
        extracted_files = await mcp7zop_extract_archive_impl(archive_path, extract_dir)

        assert isinstance(extracted_files, list)
        # making a list of the file names.
        outfile_names = [f.name for f in input_paths]
        for p in extracted_files:
            print(f"Extracted file: {p}")

        # check if the extracted files match the input files
        assert len(extracted_files) == len(outfile_names)

# -------------------------------------------------------------------------------------------
# test for listing items in the archive
@pytest.mark.asyncio
async def test_list_archive_items():
    """
    Test the mcp7zop_list_archive_items function.
    """
    async with anyio.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        archive_path = temp_dir / "test_archive.7z"
        input_paths = [temp_dir / "test_file1.txt", temp_dir / "test_file2.txt"]

        # Create test files and archive them
        for path in input_paths:
            with open(path, 'w') as f:
                f.write("This is a test file.")

        # Create the archive
        await mcp7zop_make_archive_impl(archive_path, input_paths)

        # Call the mcp7zop_list_archive_items function
        item_list = await mcp7zop_get_archive_item_list_impl(archive_path)

        assert isinstance(item_list, list)
        assert len(item_list) > 0
        for item in item_list:
            assert isinstance(item, dict)

# -------------------------------------------------------------------------------------------
# test for removing items from an archive
@pytest.mark.asyncio
async def test_remove_archive_items():
    """
    Test the mcp7zop_remove_archive_item function.
    """
    async with anyio.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        archive_path = temp_dir / "test_archive.7z"
        input_paths = [temp_dir / "test_file1.txt", temp_dir / "test_file2.txt"]

        # Create test files and archive them
        for path in input_paths:
            with open(path, 'w') as f:
                f.write("This is a test file.")

        # Create the archive
        await mcp7zop_make_archive_impl(archive_path, input_paths)

        # Call the mcp7zop_remove_archive_item function
        removed_files = await mcp7zop_remove_archive_item_impl(archive_path, [input_paths[0]])

        assert isinstance(removed_files, str)
        assert Path(removed_files).exists() # Check if the archive still exists
        # Check if the removed file is no longer in the archive
        item_list = await mcp7zop_get_archive_item_list_impl(archive_path)
        assert not any(item['Path'] == input_paths[0].name for item in item_list)
        # Check if the other file is still in the archive
        assert any(item['Path'] == input_paths[1].name for item in item_list)

# -------------------------------------------------------------------------------------------
# mcp tool for replacing items in an archive
@pytest.mark.asyncio
async def test_replace_archive_items():
    """
    Test the mcp7zop_replace_archive_items function.
    """
    async with anyio.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        archive_path = temp_dir / "test_archive.7z"
        input_paths = [temp_dir / "test_file1.txt", temp_dir / "test_file2.txt"]
        replace_paths = [temp_dir / "replace_file1.txt",
                         temp_dir / "replace_file2.txt"]

        # Create test files and archive them
        for path in input_paths:
            with open(path, 'w') as f:
                f.write("This is a test file.")

        # Create replacement files
        for path in replace_paths:
            with open(path, 'w') as f:
                f.write("This is a replacement file.")

        # Create the archive
        await mcp7zop_make_archive_impl(archive_path, input_paths)

        # change size of test_file1.txt to ensure it is replaced
        with open(input_paths[0], 'a') as f:
            f.write("Additional content to ensure replacement.")

        # add test_file1.txt to the replace_paths
        replace_paths.append(input_paths[0])

        # Call the mcp7zop_replace_archive_items function
        replaced_archive = await mcp7zop_replace_archive_items_impl(archive_path, replace_paths)

        assert isinstance(replaced_archive, str)
        assert Path(replaced_archive).exists()
        # Check if the replaced files are in the archive
        item_list = await mcp7zop_get_archive_item_list_impl(replaced_archive)
        for replace_path in replace_paths:
            assert any(item['Path'] == replace_path.name for item in item_list), \
                       f"Replaced file {replace_path.name} not found in the archive."
        # Check if test_file1.txt has been replaced with checking size
        for item in item_list:
            if item['Path'] == input_paths[0].name:
                assert item['Size'] != "0", \
                       "test_file1.txt was not replaced correctly in the archive."
                break

