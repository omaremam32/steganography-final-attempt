import os 
import sys
BMP_HEADER_SIZE = 54
STOP_MARKER = "@@@"
def file_exists(path: str) -> bool:
    return os.path.isfile(path)
def read_all_bytes(path: str) -> bytearray:
    with open(path, "rb") as f:
        return bytearray(f.read())