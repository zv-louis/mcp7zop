# encoding : utf-8

from typing import Annotated, Any
from pydantic import Field
from fastmcp import FastMCP
from .impl_fs import *
from .impl_7z import *

# FastMCP instance
mcp = FastMCP("Mcp7zOp")

# -------------------------------------------------------------------------------------------
# return the FastMCP instance
def get_mcp():
    return mcp

# -------------------------------------------------------------------------------------------
# mcp tool for creating an archive
@mcp.tool()
async def mcp7zop_make_archive(
        archive_path:  Annotated[str, Field(description="output archive path will be saved.")],
        input_pathes: Annotated[list[str], Field(description="Input file paths. Can be files or directories. If it is a single file or a single directory, this must to be a list with one item.")]
    ) -> str:
    """
    Create an archive file from the specified paths and return the archive path.

    Args:
        archive_path (str):
            Path where the archive will be saved.
            This path must be a file path of a supported archive format (e.g., .7z, .zip).
        input_pathes (list[str]):
            List of input file paths to be archived.
            If it is a single file or a single directory, this must to be a list with one item.
            If this path is a directory, directory itself and all its contents will be archived.
    Returns:
        str: the path to the created archive file.
    Raises:
        ValueError:
            If the specified archive path is not a file or if the archive format is unsupported.
        FileNotFoundError:
            If the specified archive file does not exist.
        Exception:
            If there is an error during the archive creation process.
    """
    ret = await mcp7zop_make_archive_impl(archive_path, input_pathes)
    return ret

# -------------------------------------------------------------------------------------------
# mcp tool for extracting an archive
@mcp.tool()
async def mcp7zop_extract_archive(
        archive_path: Annotated[str, Field(description="Path to the archive file to be extracted.")],
        extract_dir: Annotated[str, Field(description="Directory where the files will be extracted.")]
    ) -> list[str]:
    """
    Extract files from a 7z or zip archive and return the list of extracted file paths.

    Args:
        archive_path (str):
            Path to the archive file to be extracted.
            This path must be a file path of a supported archive format (e.g., .7z, .zip).
        extract_dir (str):
            Directory where the files will be extracted.
    Returns:
        list[str]: List of paths to the extracted files.
    Raises:
        ValueError:
            If the specified archive path is not a file or if the archive format is unsupported.
        FileNotFoundError:
            If the specified archive file does not exist.
        Exception:
            If there is an error during the extraction process.
    """
    ret = await mcp7zop_extract_archive_impl(archive_path, extract_dir)
    return ret

# -------------------------------------------------------------------------------------------
# mcp tool for listing items in an archive
@mcp.tool()
async def mcp7zop_get_archive_item_list(
        archive_path: Annotated[str, Field(description="Path to the archive file to list items from.")]
    ) -> list[dict[str, str]]:
    """
    List items in a 7z or zip archive.
    Args:
        archive_path (str):
            Path to the archive file to list items from.
            This path must be a file path of a supported archive format (e.g., .7z, .zip).
    Returns:
        list[dict[str,str]]: List of dictionaries containing item informations.
    Raises:
        ValueError:
            If the specified archive path is not a file or if the archive format is unsupported.
        FileNotFoundError:
            If the specified archive file does not exist.
        Exception:
            If there is an error during the listing process.
    """
    # Call the mcp7zop_list_archive_items_impl function
    ret = await mcp7zop_get_archive_item_list_impl(archive_path)
    return ret

# -------------------------------------------------------------------------------------------
# mcp tool for replacing items in an archive
@mcp.tool()
async def mcp7zop_replace_archive_items(
        archive_path:  Annotated[str, Field(description="target archive path will be updated.")],
        replace_pathes: Annotated[list[str], Field(description="Input file paths to be added or replaced in the archive. If it is a single file or a single directory, this must to be a list with one item. If this path is a directory, directory itself and all its contents will be replaced in the archive.")],
    ) -> str:
    """
    Replace items or Add items in a 7z or zip archive and return the archive path.
    Args:
        archive_path (str):
            Path to the archive file to be updated.
            This path must be a file path of a supported archive format (e.g., .7z, .zip).
        replace_pathes (list[str]):
            List of file paths to be added or replaced in the archive.
            If it is a single file or a single directory, this must to be a list with one item.
            If this path is a directory, directory itself and all its contents will be added or replaced in the archive.
    Returns:
        str: the path to the updated archive file.
    Raises:
        ValueError:
            If the specified archive path is not a file or if the archive format is unsupported.
        FileNotFoundError:
            If the specified archive file does not exist.
        Exception:
            If there is an error during the update process.
    """
    ret = await mcp7zop_replace_archive_items_impl(archive_path, replace_pathes)
    return ret

# -------------------------------------------------------------------------------------------
# mcp tool for removing items from an archive
@mcp.tool()
async def mcp7zop_remove_archive_items(
        archive_path: Annotated[str, Field(description="Path to the archive file to remove items from.")],
        remove_item_paths: Annotated[list[str], Field(description="List of item paths to be removed from the archive.")]
    ) -> str:
    """
    Remove items from a 7z or zip archive and return the archive path.
    Args:
        archive_path (str):
            Path to the archive file to remove items from.
            This path must be a file path of a supported archive format (e.g., .7z, .zip).
        remove_item_paths (list[str]):
            List of item paths to be removed from the archive.
            If it is a single path, this must to be a list with one item.
            If this path is a directory of the items, directory itself and all its contents will be removed in the archive.
    Returns:
        str: the path to the updated archive file.
    Raises:
        ValueError:
            If the specified archive path is not a file or if the archive format is unsupported.
        FileNotFoundError:
            If the specified archive file does not exist.
        Exception:
            If there is an error during the removal process.
    """
    ret = await mcp7zop_remove_archive_item_impl(archive_path, remove_item_paths)
    return ret


# -------------------------------------------------------------------------------------------
# mcp tool for getting directory item list
@mcp.tool()
async def mcp7zop_get_dir_item_list(
        dir_path: Annotated[str, Field(description="Path to the directory to list items from.")]
    ) -> list[dict[str, str]]:
    """
    Get a list of items in the specified directory.

    Args:
        dir_path (str):
            Path to the directory.
    Returns:
        list[dict[str,str]]: List of dictionaries containing item names and types.
    Raises:
        FileNotFoundError:
            If the specified directory does not exist.
        ValueError:
            If the specified path is not a directory.
    """
    return get_dir_item_list_impl(dir_path)

# -------------------------------------------------------------------------------------------
# mcp tool for getting path item info
@mcp.tool()
async def mcp7zop_get_path_item_info(
        item_path: Annotated[str, Field(description="Path to the item (file or directory) to get information about.")]
    ) -> dict[str, str]:
    """
    Get information about the specified path item.
    Args:
        item_path (str):
            Path to the item (file or directory).
    Returns:
        dict[str, str]: Dictionary containing item information.
    Raises:
        FileNotFoundError:
            If the specified path does not exist.
        ValueError:
            If the specified path is not a file, directory, or symlink.
    """
    return get_path_item_info_impl(item_path)

# -------------------------------------------------------------------------------------------
# mcp tool for checking if a path exists
@mcp.tool()
async def mcp7zop_path_is_exist(
        item_path: Annotated[str, Field(description="Path to check if it exists.")]
    ) -> bool:
    """
    Check if the specified path exists.

    Args:
        item_path (str):
            Path to check.
    Returns:
        bool: True if the path exists, False otherwise.
    """
    return path_is_exist(item_path)
