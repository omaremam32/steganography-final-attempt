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
                            chars = []
                            for i in range(0, len(bits), 8):
                                byte_bits = bits[i:i+8]
                                if len(byte_bits) < 8:
                                    break
                                byte_str = "".join("1" if b else "0" for b in byte_bits)
                                chars.append(chr(int(byte_str, 2)))
                                return "".join(chars)
                            def get_bmp_pixel_data_offset(image_data: bytearray) -> int:
                                if len(image_data) < 14:
                                    return BMP_HEADER_SIZE
                                offset = int.from_bytes(image_data[10:14], byteorder="little", signed=False)
                                return offset if offset > 0 else BMP_HEADER_SIZE
                            def validate_bmp_24bit_uncompressed(image_data: bytearray) -> tuple:
                                if len(image_data) < BMP_HEADER_SIZE:
                                    return (False, "File is too small to be a valid BMP.", BMP_HEADER_SIZE, None, None)
                                if image_data[0:2] != b"BM":
                                    return (False, "Not a BMP file (missing 'BM' signature).", BMP_HEADER_SIZE, None, None)
                                pixel_offset = get_bmp_pixel_data_offset(image_data)
                                dib_size = int.from_bytes(image_data[14:18], "little")
                                if dib_size < 40:
                                    return (False, "Unsupported BMP format (DIB header too small).", pixel_offset, None, None)
                                bpp = int.from_bytes(image_data[28:30], "little")
                                compression = int.from_bytes(image_data[30:34], "little")
                                if bpp != 24:
                                    return (False, f"Unsupported BMP bit-depth: {bpp}. Please use 24-bit BMP.", pixel_offset, bpp, compression)
                                if compression != 0:
                                    return (False, "Unsupported BMP compression. Please use uncompressed (BI_RGB) BMP.", pixel_offset, bpp, compression)
                                if pixel_offset >= len(image_data):
                                    return (False, "Corrupt BMP (pixel data offset out of range).", pixel_offset, bpp, compression)
                                