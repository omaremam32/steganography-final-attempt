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
                f.write(data)
                def text_to_bits(text: str) -> list:
                    bits = []
                    for ch in text:
                        b = format(ord(ch), "08b")
                        for bit in b:
                            bits.append(1 if bit == "1" else 0)
                            return bits
                        def bits_to_text(bits: list) -> str: