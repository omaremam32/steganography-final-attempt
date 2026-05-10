import os
import sys
BMP_HEADER_SIZE = 54
STOP_MARKER = "@@@"
def file_exists(path: str) -> bool:
    def read_all_bytes(path: str) -> bytearray:
        with open(path, "rb") as f:
            return bytearray(f.read())
        def write_all_bytes(path: str, data: bytearray) -> None:
            with open(path, "wb") as f: