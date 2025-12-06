from pathlib import Path
from easyversion_py import FileStore


def test_init(file_store_dir: Path) -> None:
    file_store = FileStore(file_store_dir)
    assert file_store.dir == file_store_dir


def test_add(file_store: FileStore, data: bytes) -> None:
    file_id = file_store.add(data)
    assert (
        file_id
        == 28827940057343428552633618170441716678452632871101695289607250431293174006633
    )


def test_get(file_store: FileStore, data: bytes) -> None:
    file_id = file_store.add(data)
    new_data = file_store.get(file_id)
    assert new_data
