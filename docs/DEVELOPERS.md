# EasyVersion — Developer Guide

For developers and contributors. End‑user steps are in [USERS.md](docs/USERS.md).

--------------------------------------------------------------------------------

## Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) on PATH

--------------------------------------------------------------------------------

## Local development

```bash
uv sync
source .venv/path/to/activate   # .venv/bin/activate (Linux/macOS) or .venv\Scripts\activate (Windows)
uv tool install -e .
uvx easyversion --verbosity INFO list
```

- Console script: see [pyproject.toml](pyproject.toml) (`easyversion = "easyversion:main"`).
- CLI flags (including verbosity): see [USERS.md](docs/USERS.md).

--------------------------------------------------------------------------------

## Config/data locations

Resolved via platformdirs in the CLI:

- Constants: [APPNAME](src/easyversion/__init__.py:14), [APPAUTHOR](src/easyversion/__init__.py:15), [CONFIG_DIR](src/easyversion/__init__.py:16), [DATA_DIR](src/easyversion/__init__.py:17), [STORE_DIR](src/easyversion/__init__.py:18)
- Paths: [config_file_path()](src/easyversion/__init__.py:53)
- Load/save: [open_workspace()](src/easyversion/__init__.py:66), [save_workspace()](src/easyversion/__init__.py:57)
OS-specific directories: see [USERS.md](docs/USERS.md).

--------------------------------------------------------------------------------

## Build single‑file binary

```bash
uv sync
source .venv/path/to/activate
uv tool install pyinstaller
uvx pyinstaller --onefile --name ev --paths ".venv/path/to/site-packages" src/easyversion/__init__.py
```

- Output: `dist/ev` (or `ev.exe` on Windows).
- Ensure `--paths` points to your venv’s site‑packages.

--------------------------------------------------------------------------------

## Tests

```bash
uv run pytest
```

--------------------------------------------------------------------------------

## Project layout (reference)

- CLI: [main()](src/easyversion/__init__.py:150), [cmd_save()](src/easyversion/__init__.py:85), [cmd_list()](src/easyversion/__init__.py:95), [cmd_split()](src/easyversion/__init__.py:115), [cmd_clean()](src/easyversion/__init__.py:127)
- Content store: [FileStore](src/easyversion/file/store.py:11) — [add()](src/easyversion/file/store.py:39), [get()](src/easyversion/file/store.py:49)
- Version: [ProjectVersion](src/easyversion/project/version.py:11) — [add_file()](src/easyversion/project/version.py:15), [add_dir()](src/easyversion/project/version.py:22), [restore()](src/easyversion/project/version.py:34), [clone()](src/easyversion/project/version.py:43)
- Workspace: [ProjectWorkspace](src/easyversion/project/workspace.py:15) — [save()](src/easyversion/project/workspace.py:20), [split()](src/easyversion/project/workspace.py:34), [to_json()](src/easyversion/project/workspace.py:88), [from_json()](src/easyversion/project/workspace.py:99)
- Tests: [tests/](tests/)

--------------------------------------------------------------------------------

## Release checklist

- Bump version in [pyproject.toml](pyproject.toml).
- Build binaries for Linux/macOS/Windows.
- Smoke test: `save`, `list`, `split`, `clean` with `--verbosity INFO` and `--verbosity DEBUG`.
