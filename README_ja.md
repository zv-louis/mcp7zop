# Mcp7zOp

Mcp7zOp - A Local MCP server for operating 7-zip CUI interface

[English](README.md) | 日本語

<!-- TOC tocDepth:2..4 chapterDepth:2..6 -->

- [1. 概要](#1-概要)
- [2. 機能](#2-機能)
  - [2-1. アーカイブ操作](#2-1-アーカイブ操作)
  - [2-2. ファイルシステム操作](#2-2-ファイルシステム操作)
- [3. 必要環境](#3-必要環境)
  - [3-1. 動作要件](#3-1-動作要件)
  - [3-2. 7-Zipのインストール](#3-2-7-zipのインストール)
- [4. インストール/使用方法](#4-インストール使用方法)
  - [4-1. uvのインストール](#4-1-uvのインストール)
  - [4-2. uv環境へのパッケージ追加](#4-2-uv環境へのパッケージ追加)
  - [4-3. MCPサーバーとして登録](#4-3-mcpサーバーとして登録)
- [5. 提供されるtool一覧](#5-提供されるtool一覧)
  - [`mcp7zop_make_archive`](#mcp7zop_make_archive)
  - [`mcp7zop_extract_archive`](#mcp7zop_extract_archive)
  - [`mcp7zop_get_archive_item_list`](#mcp7zop_get_archive_item_list)
  - [`mcp7zop_replace_archive_items`](#mcp7zop_replace_archive_items)
  - [`mcp7zop_remove_archive_items`](#mcp7zop_remove_archive_items)
  - [`mcp7zop_get_dir_item_list`](#mcp7zop_get_dir_item_list)
  - [`mcp7zop_get_path_item_info`](#mcp7zop_get_path_item_info)
  - [`mcp7zop_path_is_exist`](#mcp7zop_path_is_exist)
- [6.ライセンス](#6ライセンス)

<!-- /TOC -->

## 1. 概要

Mcp7zOpは、7-Zipのコマンドラインツール操作を行うMCP (Model Context Protocol) サーバーです。  
インストールされている7-zipを利用してファイルとディレクトリのアーカイブ作成/展開/操作を行うツールを提供します。  

## 2. 機能

### 2-1. アーカイブ操作

インストールされている7-Zipを使用して、以下の操作を行います。

- **アーカイブ作成**: 複数のファイルやディレクトリから7zまたはzipアーカイブを作成
- **アーカイブ展開**: 7zやzipアーカイブを指定したディレクトリに展開
- **アーカイブ内容一覧**: アーカイブファイル内のアイテム一覧を取得
- **アーカイブアイテム追加・置換**: 既存のアーカイブにファイルやディレクトリを追加または置換
- **アーカイブアイテム削除**: アーカイブから指定したアイテムを削除

### 2-2. ファイルシステム操作

環境によっては、開いているプロジェクト/ワークスペースの外にあるフォルダのファイル一覧取得ができないことがあるため、
アーカイブ作成などに必要となる一部のファイルシステム参照機能もツールとして提供しています.  

- **ディレクトリ一覧**: 指定したディレクトリ内のアイテム一覧を取得
- **パス情報**: ファイルやディレクトリの詳細情報を取得
- **パス存在確認**: 指定したパスが存在するかチェック

## 3. 必要環境

### 3-1. 動作要件

- Python (>=3.10)
- 7-Zip  (>=23.0)

### 3-2. 7-Zipのインストール

7-Zipは、公式サイトや公式リポジトリからインストールしてください。  

- [7-Zip公式サイト](https://www.7-zip.org/)

インストーラーを実行して 7-Zip をインストール後、
以下のいずれかの方法でMCPサーバーが7-Zipを使用できるように設定します。  

**a. 7zコマンドを使用可能にする**  

7-Zipの実行ファイルのあるディレクトリをシステムのPATH環境変数に追加します。

**b. 設定ファイルを使用する**  

`${HOME}/.mcp7zop/config.json` ファイルを作成し、7-Zipのパスを指定します。  

```json
{
    "7z_path": "/path/to/7z_executable"
}
```

## 4. インストール/使用方法

### 4-1. uvのインストール

このプロジェクトはパッケージマネージャに uv を使用しています。  
下記よりインストールしてください.  

- [uv - https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

### 4-2. uv環境へのパッケージ追加

uv環境にgitリポジトリから直接 mcp7zop パッケージを追加します.  
gitを利用してインストールするため, gitコマンドが使用可能な環境で下記のコマンドを実行してください.  

```bash
uv tool install git+{リポジトリのURL}
```

インストール後、mcp7zop コマンドが利用できるようになります.  
以下のコマンドを実行してみます.  

```bash
mcp7zop
```

mcpツール一覧が表示されれば正常にインストールされています.

### 4-3. MCPサーバーとして登録

コマンドをAgentツールのmcpServersに登録します.  
mcpサーバの登録方法はAgentツールにより異なりますので, Agentのドキュメントを参照してください.  
以下は設定ファイル例です.

```json
{
    // Agentツールの設定ファイル例. 
    // ** 設定方法はAgentのドキュメントを参照してください。**
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

## 5. 提供されるtool一覧

### `mcp7zop_make_archive`

複数のファイルやディレクトリからアーカイブを作成します。

**パラメータ:**  

- `archive_path` (str): 作成するアーカイブファイルのパス
- `input_pathes` (List[str]): アーカイブに含めるファイル/ディレクトリのパス一覧

**戻り値:** 作成されたアーカイブファイルのパス

### `mcp7zop_extract_archive`

アーカイブファイルを展開します。

**パラメータ:**  

- `archive_path` (str): 展開するアーカイブファイルのパス
- `extract_dir` (str): ファイルを展開するディレクトリ

**戻り値:** 展開されたファイルのパス一覧

### `mcp7zop_get_archive_item_list`

アーカイブファイル内のアイテム一覧を取得します。

**パラメータ:**  

- `archive_path` (str): 一覧を取得するアーカイブファイルのパス

**戻り値:** アイテム情報を含む辞書のリスト

### `mcp7zop_replace_archive_items`

アーカイブにファイルやディレクトリを追加または置換します。

**パラメータ:**  

- `archive_path` (str): 更新するアーカイブファイルのパス
- `replace_pathes` (List[str]): アーカイブに追加または置換するファイル/ディレクトリのパス一覧

**戻り値:** 更新されたアーカイブファイルのパス

### `mcp7zop_remove_archive_items`

アーカイブから指定したアイテムを削除します。

**パラメータ:**  

- `archive_path` (str): アイテムを削除するアーカイブファイルのパス
- `remove_item_paths` (List[str]): アーカイブから削除するアイテムのパス一覧

**戻り値:** 更新されたアーカイブファイルのパス

### `mcp7zop_get_dir_item_list`

ディレクトリ内のアイテム一覧を取得します。

**パラメータ:**  

- `dir_path` (str): 一覧を取得するディレクトリのパス

**戻り値:** アイテム名とタイプを含む辞書のリスト

### `mcp7zop_get_path_item_info`

パスの詳細情報を取得します。

**パラメータ:**  

- `item_path` (str): 情報を取得するアイテムのパス

**戻り値:** アイテム情報を含む辞書

### `mcp7zop_path_is_exist`

パスの存在を確認します。

**パラメータ:**  

- `item_path` (str): 確認するパス

**戻り値:** パスが存在する場合True、そうでなければFalse

---

## 6.ライセンス

このプロジェクトはMITライセンスの下で公開されています。  
詳細は[LICENSE](LICENSE)ファイルを参照してください。  
