from easyversion import FileStore


def test_init(tmp_path) -> None:
    d = tmp_path / "store"
    file_store = FileStore(d)
    assert file_store.dir == d


def test_add_and_get(file_store: FileStore, data: bytes) -> None:
    file_id = file_store.add(data)
    assert file_store.get(file_id) == data
