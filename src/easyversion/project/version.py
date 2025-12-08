from dataclasses import dataclass, field
import os
from pathlib import Path
import shutil
import zlib


from easyversion.file import FileStore


@dataclass
class ProjectVersion:
    comment: str | None = None
    files: dict[Path, int] = field(default_factory=dict)

    def add_file(self, file_store: FileStore, root_dir: Path, sub_path: Path) -> int:
        file_id = file_store.add((root_dir / sub_path).read_bytes())
        self.files[sub_path] = file_id
        return file_id

    def add_dir(
        self, file_store: FileStore, root_dir: Path, sub_dir_path: Path | None = None
    ) -> None:
        base = root_dir / sub_dir_path if sub_dir_path is not None else root_dir
        for p in sorted(pp for pp in base.rglob("*") if pp.is_file()):
            self.add_file(file_store, root_dir, p.relative_to(root_dir))

    def restore(self, root_dir: Path, file_store: FileStore) -> None:
        if root_dir.exists():
            shutil.rmtree(root_dir)
        for rel, fid in self.files.items():
            abs_path = root_dir / rel
            abs_path.parent.mkdir(parents=True, exist_ok=True)
            data = file_store.get(fid)
            abs_path.write_bytes(data)

    def clone(self) -> ProjectVersion:
        return ProjectVersion(self.comment, self.files.copy())
