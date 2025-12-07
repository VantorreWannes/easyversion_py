from typing import LiteralString


from pathlib import Path
from pytest import fixture

from easyversion import FileStore, ProjectVersion, ProjectWorkspace


@fixture
def workspace_dir(tmp_path: Path) -> Path:
    dir = tmp_path / "workspace"
    dir.mkdir()
    return dir


@fixture
def file_store(tmp_path: Path) -> FileStore:
    return FileStore(tmp_path / "file_store")


@fixture
def project_version() -> ProjectVersion:
    return ProjectVersion(None)


@fixture
def project_workspace(workspace_dir: Path, file_store: FileStore) -> ProjectWorkspace:
    return ProjectWorkspace(workspace_dir, file_store)


@fixture
def json_data() -> LiteralString:
    return '{"dir": "/tmp/pytest-of-wannes/pytest-61/test_to_json0/workspace", "file_store": {"dir": "/tmp/pytest-of-wannes/pytest-61/test_to_json0/file_store"}, "versions": [{"comment": "Hello World!", "files": {"temp/temp.txt": 6486659796661480009679813770337136512253847759462969237328633784501934220200}}]}'


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
