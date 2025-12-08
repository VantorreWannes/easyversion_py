import argparse
import hashlib
import logging
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
LOG_FILE = CONFIG_DIR / "out.log"

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.addHandler(logging.FileHandler(LOG_FILE))


def parse_loglevel(value: str) -> int:
    v = value.strip()
    if v.isdigit():
        return int(v)
    name = v.upper()
    mapping = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "WARN": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "NOTSET": logging.NOTSET,
    }
    if name in mapping:
        return mapping[name]
    raise argparse.ArgumentTypeError(f"Invalid log level: {value}")


def setup_logging(level: int) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logger.debug("Logging initialized at level %s", logging.getLevelName(level))


def path_id(path: Path) -> int:
    digest = hashlib.blake2b(bytes(path), digest_size=32).digest()
    return int.from_bytes(digest, byteorder="big", signed=False)


def config_file_path(path: Path) -> Path:
    return CONFIG_DIR / f"{path_id(path)}.json"


def save_workspace(workspace: ProjectWorkspace):
    config_file: Path = config_file_path(workspace.dir)
    logger.debug("Ensuring config directory exists: %s", config_file.parent)
    config_file.parent.mkdir(parents=True, exist_ok=True)
    data = workspace.to_json()
    config_file.write_text(data)
    logger.info("Workspace config saved: %s (%d bytes)", config_file, len(data))


def open_workspace(dir: Path):
    config_file: Path = config_file_path(dir)
    try:
        logger.debug("Opening workspace from config: %s", config_file)
        json_data = config_file.read_text()
        ws = ProjectWorkspace.from_json(json_data)
        logger.info("Loaded workspace for %s with %d version(s)", dir, len(ws.versions))
        return ws
    except FileNotFoundError:
        logger.info(
            "No workspace config found at %s; initializing new workspace", config_file
        )
        file_store = FileStore(STORE_DIR)
        return ProjectWorkspace(dir, file_store)
    except Exception:
        logger.exception("Failed to load workspace configuration at %s", config_file)
        raise


def cmd_save(comment: str | None):
    logger.info('Command "save" invoked with comment=%r', comment)
    try:
        workspace: ProjectWorkspace = open_workspace(Path.cwd())
        workspace.save(comment)
        save_workspace(workspace)
    except Exception:
        logger.error("Save failed")


def cmd_list() -> None:
    logger.info('Command "list" invoked')
    try:
        workspace: ProjectWorkspace = open_workspace(Path.cwd())
        if not workspace.versions:
            print("No versions saved.")
            logger.debug("List: no versions in workspace %s", workspace.dir)
        else:
            logger.debug(
                "List: %d version(s) in workspace %s",
                len(workspace.versions),
                workspace.dir,
            )
            for idx, v in enumerate(workspace.versions, start=1):
                cmt = f'"{v.comment}"' if v.comment else f""
                print(f"{idx}. {cmt}")
    except Exception:
        logger.error("List failed")


def cmd_split(dest_dir: Path, version: int | None) -> None:
    logger.info(
        'Command "split" invoked with dest_dir=%s version=%s', dest_dir, version
    )
    try:
        workspace: ProjectWorkspace = open_workspace(Path.cwd())
        new_ws = workspace.split(dest_dir, version)
        save_workspace(new_ws)
    except Exception:
        logger.error("Split failed")


def cmd_clean() -> None:
    logger.info('Command "clean" invoked')
    try:
        config_file = config_file_path(Path.cwd())
        config_file.unlink(missing_ok=True)
        logger.info("Removed config file if present: %s", config_file)
    except Exception:
        logger.error("Clean failed")


def resolve_command(args: argparse.Namespace):
    logger.debug("Dispatching command: %s", args.command)
    match args.command:
        case "save":
            cmd_save(args.comment)
        case "list":
            cmd_list()
        case "split":
            cmd_split(args.dir.resolve(), args.version)
        case "clean":
            cmd_clean()


def main() -> None:
    main_parser = argparse.ArgumentParser(
        prog="easyversion",
        description="Easy Version Control system",
        epilog="Designed for Artists, Musicians, and Game Developers",
    )
    main_parser.add_argument(
        "-v",
        "--verbosity",
        default="WARNING",
        type=parse_loglevel,
        help="Logging level (CRITICAL, ERROR, WARNING, INFO, DEBUG or a numeric level)",
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
        default=None,
        help="Version index (1..N). Defaults to latest",
    )

    clean_parser = subparsers.add_parser("clean", help="Cleanup EV in this folder")

    args = main_parser.parse_args()
    setup_logging(args.verbosity)
    logger.debug("CLI arguments parsed: %s", args)
    try:
        resolve_command(args)
    except Exception:
        logger.exception("Unhandled error during command execution")


if __name__ == "__main__":
    main()
