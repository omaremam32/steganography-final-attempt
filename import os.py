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
def bits_to_text(bits: list) -> str:
    
    chars = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        if len(byte_bits) < 8:
            break
        byte_str = "".join("1" if b else "0" for b in byte_bits)
        chars.append(chr(int(byte_str, 2)))
    return "".join(chars)