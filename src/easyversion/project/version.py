from dataclasses import dataclass, field
import logging
from pathlib import Path

from easyversion.file import FileStore

logger = logging.getLogger(__name__)


@dataclass
class ProjectVersion:
    comment: str | None = None
    files: dict[Path, int] = field(default_factory=dict)

    def add_file(self, file_store: FileStore, root_dir: Path, sub_path: Path) -> int:
        data = (root_dir / sub_path).read_bytes()
        file_id = file_store.add(data)
        self.files[sub_path] = file_id
        logger.debug("Added file %s (id=%s, %d bytes)", sub_path, file_id, len(data))
        return file_id

    def add_dir(
        self, file_store: FileStore, root_dir: Path, sub_dir_path: Path | None = None
    ) -> None:
        base = root_dir / sub_dir_path if sub_dir_path is not None else root_dir
        logger.info("Scanning directory %s for files to add", base)
        count = 0
        for p in sorted(pp for pp in base.rglob("*") if pp.is_file()):
            self.add_file(file_store, root_dir, p.relative_to(root_dir))
            count += 1
        suffix = f" from {sub_dir_path}" if sub_dir_path else ""
        logger.info("Added %d file(s) to version%s", count, suffix)

    def restore(self, root_dir: Path, file_store: FileStore) -> None:
        logger.info("Restoring %d file(s) into %s", len(self.files), root_dir)
        for rel, fid in self.files.items():
            abs_path = root_dir / rel
            abs_path.parent.mkdir(parents=True, exist_ok=True)
            data = file_store.get(fid)
            abs_path.write_bytes(data)
            logger.debug("Restored %s (id=%s, %d bytes)", rel, fid, len(data))

    def clone(self) -> ProjectVersion:
        cloned = ProjectVersion(self.comment, self.files.copy())
        logger.debug(
            "Cloned ProjectVersion with %d file(s), comment=%r",
            len(self.files),
            self.comment,
        )
        return cloned
