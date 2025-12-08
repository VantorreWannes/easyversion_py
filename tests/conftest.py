from pathlib import Path
import zlib
from pytest import TempPathFactory, fixture

from easyversion import FileStore, ProjectVersion, ProjectWorkspace


@fixture
def workspace_dir(tmp_path: Path) -> Path:
    dir = tmp_path / "workspace"
    dir.mkdir()
    return dir


@fixture
def file_store(tmp_path_factory: TempPathFactory, data: bytes) -> FileStore:
    fs_base = tmp_path_factory.mktemp("file_store_base")
    file_store = FileStore(fs_base / "file_store")
    file_store.add(data)
    return file_store


@fixture
def project_version() -> ProjectVersion:
    return ProjectVersion(None)


@fixture
def project_workspace(workspace_dir: Path, file_store: FileStore) -> ProjectWorkspace:
    return ProjectWorkspace(workspace_dir, file_store)


@fixture
def data() -> bytes:
    return b"Hello world!"


@fixture
def compressed_data(data: bytes) -> bytes:
    return zlib.compress(data)


@fixture
def file_id() -> int:
    return 28827940057343428552633618170441716678452632871101695289607250431293174006633


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
