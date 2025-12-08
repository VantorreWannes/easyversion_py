from dataclasses import dataclass, field
import json
import logging
from pathlib import Path
import shutil

from cattrs import structure, unstructure
from easyversion.file import FileStore
from easyversion.project.version import ProjectVersion

logger = logging.getLogger(__name__)


@dataclass
class ProjectWorkspace:
    dir: Path
    file_store: FileStore
    versions: list[ProjectVersion] = field(default_factory=list)

    def save(self, comment: str | None = None) -> None:
        logger.info("Saving workspace at %s (comment=%r)", self.dir, comment)
        project_version = ProjectVersion(comment)
        project_version.add_dir(
            self.file_store,
            self.dir,
        )
        self.versions.append(project_version)
        logger.info(
            "Saved new version with %d file(s). Total versions now: %d",
            len(project_version.files),
            len(self.versions),
        )

    def split(
        self, new_dir: Path, version_index: int | None = None
    ) -> ProjectWorkspace:
        logger.info(
            "Splitting workspace %s into %s at version_index=%s",
            self.dir,
            new_dir,
            version_index,
        )
        version_index = len(self.versions) if version_index is None else version_index
        logger.debug(
            "Resolved version_index=%s (total available=%d)",
            version_index,
            len(self.versions),
        )

        if version_index > len(self.versions):
            logger.error(
                "Requested version_index %d exceeds available versions %d",
                version_index,
                len(self.versions),
            )
            raise IndexError()

        if version_index == 0:
            logger.error("Requested version_index 0 is invalid (1..N expected)")
            raise IndexError()

        versions = self.versions[:version_index]
        logger.debug("Prepared %d version(s) for new workspace", len(versions))

        if new_dir.exists():
            logger.debug("Removing existing directory before split: %s", new_dir)
            shutil.rmtree(new_dir)

        new_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("Created new directory for split: %s", new_dir)

        if versions:
            last_version = versions[-1]
            logger.info(
                "Restoring last version with %d file(s) into %s",
                len(last_version.files),
                new_dir,
            )
            last_version.restore(new_dir, self.file_store)

        logger.info(
            "Split complete. New workspace at %s with %d version(s)",
            new_dir,
            len(versions),
        )
        return ProjectWorkspace(new_dir, self.file_store, versions)

    def to_json(self) -> str:
        s = json.dumps(unstructure(self))
        logger.debug(
            "Serialized workspace %s with %d version(s) into %d bytes",
            self.dir,
            len(self.versions),
            len(s),
        )
        return s

    @classmethod
    def from_json(cls, json_data: str) -> ProjectWorkspace:
        ws = structure(json.loads(json_data), ProjectWorkspace)
        logger.debug(
            "Deserialized workspace %s with %d version(s)",
            ws.dir,
            len(ws.versions),
        )
        return ws
