from pathlib import Path
from .file import FileStore
from .project import ProjectVersion, ProjectWorkspace

__all__: list[str] = ["FileStore", "ProjectVersion", "ProjectWorkspace"]


def work(folder: Path, data: str) -> None:
    file_one = folder / "FileOne.txt"
    nested_folder = folder / "Nested"
    file_two = nested_folder / "FileTwo.txt"

    folder.mkdir(parents=True, exist_ok=True)
    file_one.write_text(data)
    nested_folder.mkdir(parents=True, exist_ok=True)
    file_two.write_text(data)


def main() -> None:
    FILE_STORE_DIR = Path("/home/wannes/Documenten/EVTests/EVCache")

    WORK_DIR_ONE = Path("/home/wannes/Documenten/EVTests/WorkspaceOne/")
    WORK_DIR_TWO = Path("/home/wannes/Documenten/EVTests/WorkspaceTwo/")

    file_store = FileStore(FILE_STORE_DIR)

    workspace_one = ProjectWorkspace(WORK_DIR_ONE, file_store)

    work(WORK_DIR_ONE, "1")
    workspace_one.save("Version One")

    work(WORK_DIR_ONE, "2")
    workspace_one.save("Version Two")

    work(WORK_DIR_ONE, "3")
    workspace_one.save("Version Three")

    workspace_two = workspace_one.split(WORK_DIR_TWO, 2)

    work(WORK_DIR_TWO, "Seperate Version")
    workspace_two.save("Seperate Version")
