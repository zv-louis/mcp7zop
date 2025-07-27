# encoding : utf-8
import os
import pytest
import anyio
from pathlib import Path

from src.mcp7zop.impl_fs import *

# -------------------------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_dir_item_list():
    """
    Test the get_dir_item_list function.
    """
    async with anyio.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        test_dir = temp_dir / "test_dir"
        test_dir.mkdir()

        # Create test files and directories
        (test_dir / "file1.txt").touch()
        (test_dir / "file2.txt").touch()
        (test_dir / "subdir").mkdir()

        item_list = get_dir_item_list_impl(test_dir)

        assert isinstance(item_list, list)
        assert len(item_list) == 3  # 2 files + 1 directory
        assert any(item['name'] == 'file1.txt' and item['type'] == "file" for item in item_list)
        assert any(item['name'] == 'file2.txt' and item['type'] == "file" for item in item_list)
        assert any(item['name'] == 'subdir' and item['type'] == "directory" for item in item_list)

@pytest.mark.asyncio
async def test_get_path_item_info():
    """
    Test the get_path_item_info function.
    """
    async with anyio.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        test_file = temp_dir / "test_file.txt"
        test_file.touch()

        item_info = get_path_item_info_impl(test_file)

        assert isinstance(item_info, dict)
        assert item_info['name'] == 'test_file.txt'
        assert item_info['type'] == 'file'
        assert item_info['size'] == '0'  # size of the empty file

# -------------------------------------------------------------------------------------------
# Test for checking if a path exists
@pytest.mark.asyncio
async def test_path_is_exist():
    """
    Test the path_is_exist function.
    """
    async with anyio.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        test_file = temp_dir / "test_file.txt"
        test_file.touch()

        assert path_is_exist(test_file) is True
        assert path_is_exist(temp_dir / "non_existent_file.txt") is False
    
