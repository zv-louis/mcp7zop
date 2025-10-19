# Mcp7zOp

Mcp7zOp - A Local MCP server for operating 7-zip CUI interface

English | [日本語](README_ja.md)

<!-- TOC tocDepth:2..4 chapterDepth:2..6 -->

- [1. Overview](#1-overview)
- [2. Features](#2-features)
  - [2-1. Archive Operations](#2-1-archive-operations)
  - [2-2. File System Operations](#2-2-file-system-operations)
- [3. Requirements](#3-requirements)
  - [3-1. System Requirements](#3-1-system-requirements)
  - [3-2. 7-Zip Installation](#3-2-7-zip-installation)
- [4. Installation/Usage](#4-installationusage)
  - [4-1. Installing uv](#4-1-installing-uv)
  - [4-2. Adding Package to uv Environment](#4-2-adding-package-to-uv-environment)
  - [4-3. Registering as MCP Server](#4-3-registering-as-mcp-server)
- [5. Available Tools](#5-available-tools)
  - [`mcp7zop_make_archive`](#mcp7zop_make_archive)
  - [`mcp7zop_extract_archive`](#mcp7zop_extract_archive)
  - [`mcp7zop_get_archive_item_list`](#mcp7zop_get_archive_item_list)
  - [`mcp7zop_replace_archive_items`](#mcp7zop_replace_archive_items)
  - [`mcp7zop_remove_archive_items`](#mcp7zop_remove_archive_items)
  - [`mcp7zop_get_dir_item_list`](#mcp7zop_get_dir_item_list)
  - [`mcp7zop_get_path_item_info`](#mcp7zop_get_path_item_info)
  - [`mcp7zop_path_is_exist`](#mcp7zop_path_is_exist)
- [6. License](#6-license)

<!-- /TOC -->

## 1. Overview

Mcp7zOp is an MCP (Model Context Protocol) server for 7-Zip command line tool operations.  
It provides tools for file and directory archive creation, extraction, and manipulation using the installed 7-zip.

## 2. Features

### 2-1. Archive Operations

Uses the installed 7-Zip to perform the following operations:

- **Archive Creation**: Create 7z or zip archives from multiple files and directories
- **Archive Extraction**: Extract 7z or zip archives to a specified directory
- **Archive Item Listing**: Get a list of items in an archive file
- **Archive Item Addition/Replacement**: Add or replace files and directories in existing archives
- **Archive Item Removal**: Remove specified items from archives

### 2-2. File System Operations

Some environments may not allow file listing for folders outside the open project/workspace,
so some file system reference functions necessary for archive creation are also provided as tools.  

- **Directory Listing**: Get a list of items in a specified directory
- **Path Information**: Get detailed information about files or directories
- **Path Existence Check**: Check if a specified path exists

## 3. Requirements

### 3-1. System Requirements

- Python (>=3.10)
- 7-Zip (>=23.0)

### 3-2. 7-Zip Installation

Please install 7-Zip from the official website or official repository.

- [7-Zip Official Website](https://www.7-zip.org/)

After installing 7-Zip using the installer, configure the MCP server to use 7-Zip by one of the following methods:

**a. Make the 7z command available**

Add the directory containing the 7-Zip executable to your system's PATH environment variable.

**b. Use a configuration file**

Create a `${HOME}/.mcp7zop/config.json` file and specify the path to 7-Zip.

```json
{
    "7z_path": "/path/to/7z_executable"
}
```

## 4. Installation/Usage

### 4-1. Installing uv

This project uses uv as the package manager.  
Please install it from the following link.  

- [uv - https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

### 4-2. Adding Package to uv Environment

Add the mcp7zop package directly from the git repository to your uv environment.  
Since it installs using git, please execute the following command in an environment where the git command is available.  

```bash
uv tool install git+{repository_URL}
```

After installation, the mcp7zop command will be available.  
Try running the following command.  

```bash
mcp7zop
```

If the list of mcp tools is displayed, it has been installed correctly.

### 4-3. Registering as MCP Server

Register the command in the mcpServers of your Agent tool.  
The registration method for mcp servers varies by Agent tool, so please refer to the Agent documentation.  
Below is an example configuration file.

```json
{
    // Example configuration file for Agent tool
    // ** Please refer to the Agent documentation for configuration methods. **
    "mcpServers": { 
        "mcp7zop": {
            "type": "stdio",
            "command": "mcp7zop",
            "args": [
                "--mcp-server"
            ]
        }
    }
}
```

## 5. Available Tools

### `mcp7zop_make_archive`

Creates an archive from multiple files and directories.

**Parameters:**  

- `archive_path` (str): Path of the archive file to be created
- `input_pathes` (List[str]): List of file/directory paths to include in the archive

**Returns:** Path of the created archive file

### `mcp7zop_extract_archive`

Extracts an archive file.

**Parameters:**  

- `archive_path` (str): Path of the archive file to extract
- `extract_dir` (str): Directory where files will be extracted

**Returns:** List of extracted file paths

### `mcp7zop_get_archive_item_list`

Gets a list of items in an archive file.

**Parameters:**  

- `archive_path` (str): Path of the archive file to list items from

**Returns:** List of dictionaries containing item information

### `mcp7zop_replace_archive_items`

Adds or replaces files and directories in an archive.

**Parameters:**  

- `archive_path` (str): Path of the archive file to be updated
- `replace_pathes` (List[str]): List of file/directory paths to add or replace in the archive

**Returns:** Path of the updated archive file

### `mcp7zop_remove_archive_items`

Removes specified items from an archive.

**Parameters:**  

- `archive_path` (str): Path of the archive file to remove items from
- `remove_item_paths` (List[str]): List of item paths to be removed from the archive

**Returns:** Path of the updated archive file

### `mcp7zop_get_dir_item_list`

Gets a list of items in a directory.

**Parameters:**  

- `dir_path` (str): Path of the directory to list

**Returns:** List of dictionaries containing item names and types

### `mcp7zop_get_path_item_info`

Gets detailed information about a path.

**Parameters:**  

- `item_path` (str): Path of the item to get information about

**Returns:** Dictionary containing item information

### `mcp7zop_path_is_exist`

Checks if a path exists.

**Parameters:**  

- `item_path` (str): Path to check

**Returns:** True if the path exists, False otherwise

---

## 6. License

This project is released under the MIT License.  
See the [LICENSE](LICENSE) file for details.
