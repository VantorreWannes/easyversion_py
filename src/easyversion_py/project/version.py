from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from easyversion_py import FileStore


@dataclass
class ProjectVersion:
    root_dir: Path
    comment: str | None = None
    files: dict[Path, int] = field(default_factory=dict)

    def add_file(self, file_store: FileStore, sub_path: Path) -> int:
        file_id = file_store.add((self.root_dir / sub_path).read_bytes())
        self.files[sub_path] = file_id
        return file_id

    def add_dir(self, file_store: FileStore, sub_dir_path: Path) -> None:
        base = self.root_dir / sub_dir_path
        for p in sorted(
            pp for pp in base.rglob("*") if pp.is_file() and ".ev" not in pp.parts
        ):
            self.add_file(file_store, p.relative_to(self.root_dir))

    def restore(self, file_store: FileStore) -> None:
        for rel, fid in self.files.items():
            abs_path = self.root_dir / rel
            abs_path.parent.mkdir(parents=True, exist_ok=True)
            abs_path.write_bytes(file_store.get(fid))

    def clone_to(self, new_root_dir: Path) -> ProjectVersion:
        return ProjectVersion(new_root_dir, self.comment, self.files.copy())
