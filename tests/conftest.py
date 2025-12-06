from pathlib import Path
from easyversion_py import FileStore
from pytest import TempPathFactory, fixture


@fixture
def temp_text_file(tmp_path: Path) -> Path:
    return tmp_path / "file.txt"


@fixture
def file_store_dir(tmp_path_factory: TempPathFactory) -> Path:
    return tmp_path_factory.mktemp("file_store")


@fixture
def workspace_dir(tmp_path_factory: TempPathFactory) -> Path:
    return tmp_path_factory.mktemp("workspace")


@fixture
def file_store(file_store_dir: Path) -> FileStore:
    return FileStore(file_store_dir)


@fixture
def data() -> bytes:
    return b"Hello world!"
