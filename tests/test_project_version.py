from pathlib import Path
from easyversion_py import FileStore
from easyversion_py.project.version import ProjectVersion


def test_init(workspace_dir: Path):
    pv = ProjectVersion(workspace_dir, None)
    assert pv.root_dir == workspace_dir


def test_add_file(project_version: ProjectVersion, file_store: FileStore, rel_file: Path):
    project_version.add_file(file_store, rel_file)
    assert rel_file in project_version.files
    assert file_store.get(project_version.files[rel_file]) == b""


def test_add_folder(project_version: ProjectVersion, file_store: FileStore, rel_dir: Path, rel_file_in_dir: Path):
    project_version.add_dir(file_store, rel_dir)
    assert rel_file_in_dir in project_version.files
    assert file_store.get(project_version.files[rel_file_in_dir]) == b""


def test_clone_to(project_version: ProjectVersion, workspace_dir: Path):
    clone = project_version.clone_to(workspace_dir / "other")
    assert clone.root_dir == workspace_dir / "other"
    assert clone.comment == project_version.comment
    assert clone.files == project_version.files
    clone.files[Path("x")] = 1
    assert Path("x") not in project_version.files


def test_restore(project_version: ProjectVersion, file_store: FileStore, rel_file: Path, workspace_dir: Path):
    project_version.add_file(file_store, rel_file)
    abs_path = workspace_dir / rel_file
    abs_path.write_bytes(b"different")
    project_version.restore(file_store)
    assert abs_path.read_bytes() == b""
