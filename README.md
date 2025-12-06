# EasyVersion

A minimalist, high-performance Version Control System designed for **Artists, Musicians, and Game Developers**.

## Features

- **Save:** Saves the current state of the folder as a new version.
- **List:** Shows a list of all saved versions with their IDs and comments.
- **Split:** Creates a **new folder** containing the project exactly as it looked at a specified version.

```md
## ProjectWorkspace
- dir: DirectoryPath
- versions: List(ProjectVersion)

## ProjectVersion
- files: HashMap(Path, Hash)
- comment: Optional(Text)

## FileStore
- dir: DirectoryPath
```