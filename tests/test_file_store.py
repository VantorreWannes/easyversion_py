from easyversion import FileStore


def test_add(file_store: FileStore, data: bytes, file_id: int) -> None:
    file_id = file_store.add(data)
    assert file_id == file_id


def test_get(file_store: FileStore, data: bytes, file_id: int) -> None:
    recieved = file_store.get(file_id)
    assert recieved == data
