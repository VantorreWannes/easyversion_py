from pathlib import Path
from easyversion import FileStore
from easyversion.project.version import ProjectVersion


def test_add_file(
    project_version: ProjectVersion,
    workspace_dir: Path,
    file_store: FileStore,
    rel_file: Path,
):
    project_version.add_file(file_store, workspace_dir, rel_file)
    assert rel_file in project_version.files
    assert file_store.get(project_version.files[rel_file]) == b""


def test_add_folder(
    project_version: ProjectVersion,
    file_store: FileStore,
    workspace_dir: Path,
    rel_dir: Path,
    rel_file_in_dir: Path,
):
    project_version.add_dir(file_store, workspace_dir, rel_dir)
    assert rel_file_in_dir in project_version.files
    assert file_store.get(project_version.files[rel_file_in_dir]) == b""


def test_clone(project_version: ProjectVersion):
    clone = project_version.clone()
    assert clone.comment == project_version.comment
    assert clone.files == project_version.files
    clone.files[Path("x")] = 1
    assert Path("x") not in project_version.files


def test_restore(
    project_version: ProjectVersion,
    file_store: FileStore,
    rel_file: Path,
    workspace_dir: Path,
):
    project_version.add_file(file_store, workspace_dir, rel_file)
    abs_path = workspace_dir / rel_file
    abs_path.write_bytes(b"different")
    project_version.restore(workspace_dir, file_store)
    assert abs_path.read_bytes() == b""
