import os
from pathlib import Path
from typing import Tuple


def verify_file_permissions(path: Path, mask: int) -> Tuple[bool, int]:
    """
    Check that the file's permissions are properly restricted, as compared to the
    permission mask
    """
    if not path.exists():
        raise Exception(f"file {path} does not exist")

    mode = os.stat(path).st_mode & 0o777
    return (mode & mask == 0, mode)


def octal_mode_string(mode: int) -> str:
    return f"0{oct(mode)[-3:]}"
