import argparse
import hashlib
from pathlib import Path
from platformdirs import user_config_path, user_data_path

from easyversion.file import FileStore
from easyversion.project import ProjectWorkspace, ProjectVersion

__all__: list[str] = ["FileStore", "ProjectVersion", "ProjectWorkspace"]

APPNAME = "easyversion"
APPAUTHOR = "wannesvantorre"
CONFIG_DIR = user_config_path(APPNAME, APPAUTHOR)
DATA_DIR = user_data_path(APPNAME, APPAUTHOR)
STORE_DIR = DATA_DIR / "file_store"


def path_id(path: Path) -> int:
    digest = hashlib.blake2b(bytes(path), digest_size=32).digest()
    return int.from_bytes(digest, byteorder="big", signed=False)


def config_file_path(path: Path) -> Path:
    return CONFIG_DIR / f"{path_id(path)}.json"


def save_workspace(workspace: ProjectWorkspace):
    config_file: Path = config_file_path(workspace.dir)
    config_file.parent.mkdir(parents=True, exist_ok=True)
    config_file.write_text(workspace.to_json())


def open_workspace(dir: Path):
    config_file: Path = config_file_path(dir)
    try:
        json_data = config_file.read_text()
        return ProjectWorkspace.from_json(json_data)
    except FileNotFoundError:
        file_store = FileStore(STORE_DIR)
        return ProjectWorkspace(dir, file_store)


def cmd_save(comment: str | None):
    workspace: ProjectWorkspace = open_workspace(Path.cwd())
    workspace.save(comment)
    save_workspace(workspace)


def cmd_list() -> None:
    workspace: ProjectWorkspace = open_workspace(Path.cwd())
    if not workspace.versions:
        print("No versions saved.")
    else:
        for idx, v in enumerate(workspace.versions, start=1):
            cmt = f'"{v.comment}"' if v.comment else f""
            print(f"{idx}. {cmt}")


def cmd_split(dest_dir: Path, version: int) -> None:
    workspace: ProjectWorkspace = open_workspace(Path.cwd())
    new_ws = workspace.split(dest_dir, version)
    save_workspace(new_ws)


def resolve_command(args: argparse.Namespace):
    match args.command:
        case "save":
            cmd_save(args.comment)
        case "list":
            cmd_list()
        case "split":
            cmd_split(args.dir.resolve(), args.version)


def main() -> None:
    main_parser = argparse.ArgumentParser(
        prog="easyversion",
        description="Easy Version Control system",
        epilog="Designed for Artists, Musicians, and Game Developers",
    )

    subparsers = main_parser.add_subparsers(dest="command", required=True)

    save_parser = subparsers.add_parser("save", help="Save current state of a folder")
    save_parser.add_argument("-m", "--comment", default=None, help="Optional comment")

    list_parser = subparsers.add_parser("list", help="List saved versions")

    split_parser = subparsers.add_parser(
        "split", help="Create a new folder with the project state at a version"
    )
    split_parser.add_argument("dir", type=Path, help="Destination directory")
    split_parser.add_argument(
        "-v",
        "--version",
        type=int,
        default=-1,
        help="Version index (1..N). Defaults to latest",
    )

    args = main_parser.parse_args()
    resolve_command(args)


if __name__ == "__main__":
    main()
