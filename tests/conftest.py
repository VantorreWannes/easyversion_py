from pathlib import Path
from pytest import fixture

from easyversion_py import FileStore
from easyversion_py.project.version import ProjectVersion


@fixture
def workspace_dir(tmp_path: Path) -> Path:
    dir = tmp_path / "workspace"
    dir.mkdir()
    return dir


@fixture
def file_store(tmp_path: Path) -> FileStore:
    return FileStore(tmp_path / "file_store")


@fixture
def project_version(workspace_dir: Path) -> ProjectVersion:
    return ProjectVersion(workspace_dir, None)


@fixture
def data() -> bytes:
    return b"Hello world!"


@fixture
def rel_file(workspace_dir: Path) -> Path:
    file_path = workspace_dir / "temp.txt"
    file_path.write_bytes(b"")
    return file_path


@fixture
def rel_dir(workspace_dir: Path) -> Path:
    dir_path = Path("temp")
    (workspace_dir / dir_path).mkdir(parents=True, exist_ok=True)
    return dir_path


@fixture
def rel_file_in_dir(workspace_dir: Path, rel_dir: Path) -> Path:
    file_pth = rel_dir / "temp.txt"
    (workspace_dir / file_pth).write_bytes(b"")
    return file_pth
