import hashlib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FileStore:
    dir: Path = field()

    def __post_init__(self) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)

    def _path(self, file_id: int) -> Path:
        return self.dir / f"{file_id}.ezfile"

    def _blake_hash(self, data: bytes) -> int:
        digest = hashlib.blake2b(data, digest_size=32).digest()
        return int.from_bytes(digest, byteorder="big", signed=False)

    def add(self, data: bytes) -> int:
        file_id: int = self._blake_hash(data)

        save_path: Path = self._path(file_id)

        save_path.write_bytes(data)

        return file_id

    def get(self, file_id: int) -> bytes:
        save_path = self._path(file_id)
        with open(save_path, "rb") as f:
            return f.read()
