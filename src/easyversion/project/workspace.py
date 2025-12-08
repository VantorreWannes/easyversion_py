from dataclasses import dataclass, field
import json
from pathlib import Path

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
        if not self.versions:
            return ProjectWorkspace(new_dir, self.file_store, [])

        if version_index == -1:
            version_slice = self.versions
        else:
            version_slice = self.versions[:version_index]

        versions: list[ProjectVersion] = [v.clone() for v in version_slice]

        last_project_version: ProjectVersion = versions[-1]

        last_project_version.restore(new_dir, self.file_store)

        return ProjectWorkspace(new_dir, self.file_store, versions)

    def to_json(self) -> str:
        return json.dumps(unstructure(self))

    @classmethod
    def from_json(cls, json_data: str) -> ProjectWorkspace:
        return structure(json.loads(json_data), ProjectWorkspace)
