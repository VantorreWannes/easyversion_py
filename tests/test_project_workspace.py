from pathlib import Path
from easyversion import FileStore
from easyversion.project.workspace import ProjectWorkspace


def test_init(workspace_dir: Path, file_store: FileStore) -> None:
    workspace = ProjectWorkspace(workspace_dir, file_store)
    assert workspace.dir == workspace_dir
    assert workspace.versions == []


def test_save(project_workspace: ProjectWorkspace, rel_file_in_dir: Path) -> None:
    project_workspace.save()
    assert len(project_workspace.versions) == 1


def test_split(
    project_workspace: ProjectWorkspace, rel_file_in_dir: Path, tmp_path: Path
) -> None:
    split_one = project_workspace.split(tmp_path, 0)
    assert len(split_one.versions) == 0

    project_workspace.save()

    split_one = project_workspace.split(tmp_path, 0)
    assert len(split_one.versions) == 0

    split_one = project_workspace.split(tmp_path, 1)
    assert len(split_one.versions) == 1


def test_to_json(project_workspace: ProjectWorkspace, rel_file_in_dir: Path) -> None:
    project_workspace.save("Hello world!")
    json_data = project_workspace.to_json()
    parsed_workspace = ProjectWorkspace.from_json(json_data)
    assert json_data == parsed_workspace.to_json()
