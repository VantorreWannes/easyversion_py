from dataclasses import dataclass, field
from pathlib import Path

from easyversion_py.file import FileStore


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
        for p in sorted(
            pp for pp in base.rglob("*") if pp.is_file() and ".ev" not in pp.parts
        ):
            self.add_file(file_store, root_dir, p.relative_to(root_dir))

    def restore(self, root_dir: Path, file_store: FileStore) -> None:
        for rel, fid in self.files.items():
            abs_path = root_dir / rel
            abs_path.parent.mkdir(parents=True, exist_ok=True)
            abs_path.write_bytes(file_store.get(fid))

    def clone(self) -> ProjectVersion:
        return ProjectVersion(self.comment, self.files.copy())
