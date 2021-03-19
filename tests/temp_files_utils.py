from contextlib import AbstractContextManager
from pathlib import Path
from random import choices
from shutil import rmtree
from string import ascii_letters
from typing import Optional


class TempFile(AbstractContextManager):
    def __init__(self, base_dir: Optional[Path] = Path(__file__).parent):
        self.base_dir = base_dir

        self.temp_dir: Path = (base_dir / "temp")
        self.temp_dir.mkdir(exist_ok=True)

        self.temp_file_obj: Path = self.temp_dir / ''.join(choices(ascii_letters, k=16))
        self.temp_file_obj.touch(exist_ok=True)

    def __enter__(self) -> Path:
        return self.temp_file_obj

    def __exit__(self, exc_type, exc_value, traceback):
        rmtree(self.temp_dir)
