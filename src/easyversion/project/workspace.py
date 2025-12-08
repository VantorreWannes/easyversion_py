from dataclasses import dataclass, field
import json
from pathlib import Path
import shutil

from cattrs import structure, unstructure
from easyversion.file import FileStore
from easyversion.project.version import ProjectVersion


@dataclass
class ProjectWorkspace:
    dir: Path
    file_store: FileStore
    versions: list[ProjectVersion] = field(default_factory=list)

    def save(self, comment: str | None = None) -> None:
        project_version = ProjectVersion(comment)
        project_version.add_dir(
            self.file_store,
            self.dir,
        )
        self.versions.append(project_version)

    def split(
        self, new_dir: Path, version_index: int | None = None
    ) -> ProjectWorkspace:
        version_index = len(self.versions) if version_index is None else version_index

        if version_index > len(self.versions):
            raise IndexError()

        if version_index == 0:
            raise IndexError()

        versions = self.versions[:version_index]

        if new_dir.exists():
            shutil.rmtree(new_dir)

        new_dir.mkdir(parents=True, exist_ok=True)

        if versions:
            last_version = versions[-1]
            last_version.restore(new_dir, self.file_store)

        return ProjectWorkspace(new_dir, self.file_store, versions)

    def to_json(self) -> str:
        return json.dumps(unstructure(self))

    @classmethod
    def from_json(cls, json_data: str) -> ProjectWorkspace:
        return structure(json.loads(json_data), ProjectWorkspace)
