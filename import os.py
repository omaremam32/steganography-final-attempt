import os 
import sys
BMP_HEADER_SIZE = 54
STOP_MARKER = "@@@"
def file_exists(path: str) -> bool:
    return os.path.isfile(path)
def read_all_bytes(path: str) -> bytearray:
    with open(path, "rb") as f:
        return bytearray(f.read())
    def write_all_bytes(path: str, data: bytearray) -> None:
    with open(path, "wb") as f:
        f.write(data)
        def text_to_bits(text: str) -> list:
    bits = []
    for ch in text:
        binary = format(ord(ch), "08b")  # Convert character to 8-bit binary
        for bit in binary:
            bits.append(1 if bit == "1" else 0)
    return bits