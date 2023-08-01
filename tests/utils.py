from contextlib import AbstractContextManager
from functools import partial
from pathlib import Path
from random import choices
from shutil import rmtree
from string import ascii_letters


class TempFile(AbstractContextManager):
    def __init__(self):
        self.base_dir = Path(__file__).parent

        self.temp_dir: Path = (self.base_dir / "temp")
        self.temp_dir.mkdir(exist_ok=True)

        self.temp_file_obj: Path = (
            self.temp_dir / ''.join(choices(ascii_letters, k=16))
        )
        self.temp_file_obj.touch(exist_ok=True)

    def __enter__(self) -> Path:
        return self.temp_file_obj

    def __exit__(self, exc_type, exc_value, traceback):
        rmtree(self.temp_dir)


rm_temp_dir = partial(
    rmtree, Path(__file__).parent / "temp", ignore_errors=True
)
