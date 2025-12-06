from .file import FileStore
import os 

__all__ = ["FileStore"]


def main() -> None:
    for root, dirs, files in os.walk("/home/wannes/Documenten/personal/coding/python/easyversion_py/src/"):
        print(f"Root: {root}")
        print(f"Dirs: {dirs}")
        print(f"Files: {files}")
    
        
