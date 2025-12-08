# EasyVersion — User Guide

EasyVersion lets you take quick snapshots of a project folder and later recreate the folder exactly as it was. You don’t need Git or any developer tools to use it.

You will download a prebuilt app and run a few simple commands:

- save: capture the current state of your folder
- list: see your saved snapshots
- split: create a new folder that matches a chosen snapshot (non-destructive)
- clean: remove local EasyVersion metadata for the current folder

--------------------------------------------------------------------------------

## 1) Download the app

- Download the prebuilt binary for your operating system from the project’s releases page.
  - Windows: file ends with `.exe` (example: `ev.exe`)
  - macOS / Linux: file has no extension (example: `ev`)
- Place it somewhere convenient (e.g., your Desktop or a Tools folder). Optionally, add it to your system PATH so you can run it from anywhere.

Tip (macOS/Linux): If the file isn’t executable yet, you can make it executable:

```bash
chmod +x ./ev
```

--------------------------------------------------------------------------------

## 2) Use it on your project

Open a terminal/shell in your project’s folder (the folder you want to snapshot). Then run:

- Save a snapshot (you can add a comment):

```bash
# macOS/Linux
./ev save -m "Initial snapshot"

# Windows (Command Prompt or PowerShell)
.\ev.exe save -m "Initial snapshot"
```

- List snapshots:

```bash
# macOS/Linux
./ev list

# Windows
.\ev.exe list
```

- Split (recreate a chosen snapshot into a new folder):

```bash
# Create a new folder with the state at version 1
# macOS/Linux
./ev split ./MyProject_v1 -v 1

# Windows
.\ev.exe split .\MyProject_v1 -v 1
```

- Clean EasyVersion metadata for this folder (removes local workspace config only):

```bash
# macOS/Linux
./ev clean

# Windows
.\ev.exe clean
```

### Logging

Use global verbosity before the subcommand:

- macOS/Linux: `./ev -v INFO list`
- Windows: `.\ev.exe -v DEBUG save -m "Investigating logs"`

Notes:

- Two different `-v` flags:
  - Global `-v/--verbosity` controls logging and must come before the subcommand.
  - Split’s `-v/--version` selects the snapshot index.

--------------------------------------------------------------------------------

## Safety and behavior

- Save only reads your files and writes compressed copies to an internal content store. It does not modify your working folder.
- Split creates the destination folder exactly like the chosen snapshot. If the destination exists, it will be removed and recreated.
- List prints available versions starting at 1. If you omit `-v` with split, the latest version is used.
- Clean only removes the local workspace configuration file for the current folder; it does not delete your snapshots in the content store.

--------------------------------------------------------------------------------

## Where EasyVersion stores data

EasyVersion keeps your project folder untouched except when you run split to a destination you choose. Internal data is stored under your user configuration/data directories:

- Workspace configs (per source folder): platform-specific config directory
- Content store (compressed files): platform-specific data directory under a `file_store` subfolder

Typical locations (may vary by system settings):

- Linux
  - Config: `~/.config/easyversion`
  - Data: `~/.local/share/easyversion/file_store`
  - Logs: `~/.config/easyversion`
- macOS
  - Config: `~/Library/Application Support/easyversion`
  - Data: `~/Library/Application Support/easyversion/file_store`
  - Logs: `~/Library/Application Support/easyversion`
- Windows
  - Config: `%APPDATA%\wannesvantorre\easyversion`
  - Data: `%LOCALAPPDATA%\wannesvantorre\easyversion\file_store`
  - Logs: `%APPDATA%\wannesvantorre\easyversion`

--------------------------------------------------------------------------------

## Uninstall and data cleanup

- To uninstall the app, delete the `ev` (or `ev.exe`) file you downloaded.
- Optional: remove local EasyVersion data for all projects by deleting the directories listed above (this will permanently remove saved snapshots):
  - On Linux/macOS, remove the config and data folders shown in “Where EasyVersion stores data”.
  - On Windows, remove the `%APPDATA%\wannesvantorre\easyversion` and `%LOCALAPPDATA%\wannesvantorre\easyversion\file_store` folders.
- To reset a single project’s local metadata without deleting snapshots, run `clean` in that project folder:

  ```bash
  # macOS/Linux
  ./ev clean
  # Windows
  .\ev.exe clean
  ```

Warning: Deleting the data directory (the content store) will remove all snapshots for all projects. This cannot be undone.

--------------------------------------------------------------------------------

## 3) Tips and troubleshooting

- If you see “permission denied” on macOS/Linux, run:

```bash
chmod +x ./ev
```

- If you see “command not found”, make sure you’re calling it with `./ev` (macOS/Linux) or `.\ev.exe` (Windows) from the folder that contains the file. Or add the app to your PATH.

- If you see “No versions saved.” when listing, create a snapshot first with `save`.

--------------------------------------------------------------------------------

## Where to go next

- Technical docs for developers (building from source, running tests): see [DEVELOPERS.md](DEVELOPERS.md)
