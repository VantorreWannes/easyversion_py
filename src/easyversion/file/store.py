import hashlib
import logging
from dataclasses import dataclass, field
from pathlib import Path
import zlib

logger = logging.getLogger(__name__)


@dataclass
class FileStore:
    dir: Path = field()

    def __post_init__(self) -> None:
        logger.debug("Ensuring file store directory exists: %s", self.dir)
        self.dir.mkdir(parents=True, exist_ok=True)

    def _path(self, file_id: int) -> Path:
        p = self.dir / f"{file_id}.ezfile"
        logger.debug("Resolved file_id=%s to path %s", file_id, p)
        return p

    def _blake_hash(self, data: bytes) -> int:
        digest = hashlib.blake2b(data, digest_size=32).digest()
        file_id = int.from_bytes(digest, byteorder="big", signed=False)
        logger.debug("Computed BLAKE2b id=%s for %d bytes", file_id, len(data))
        return file_id

    def _compress(self, data: bytes) -> bytes:
        compressed = zlib.compress(data)
        logger.debug("Compressed %d -> %d bytes", len(data), len(compressed))
        return compressed

    def _decompress(self, data: bytes) -> bytes:
        decompressed = zlib.decompress(data)
        logger.debug("Decompressed %d -> %d bytes", len(data), len(decompressed))
        return decompressed

    def add(self, data: bytes) -> int:
        file_id: int = self._blake_hash(data)
        save_path: Path = self._path(file_id)

        compressed_data = self._compress(data)
        save_path.write_bytes(compressed_data)

        logger.info("Stored file_id=%s at %s", file_id, save_path)
        return file_id

    def get(self, file_id: int) -> bytes:
        save_path = self._path(file_id)
        with open(save_path, "rb") as f:
            compressed = f.read()
        data = self._decompress(compressed)
        logger.info("Loaded file_id=%s from %s", file_id, save_path)
        return data
