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
def get_bmp_pixel_data_offset(image_data: bytearray) -> int:
    
    if len(image_data) < 14:
        return BMP_HEADER_SIZE
    offset = int.from_bytes(image_data[10:14], "little")
    return offset if offset > 0 else BMP_HEADER_SIZE
def validate_bmp_24bit_uncompressed(image_data: bytearray) -> tuple:
   
    if image_data[0:2] != b"BM":
        return (False, "Not a BMP file.", BMP_HEADER_SIZE, None, None)

    pixel_offset = get_bmp_pixel_data_offset(image_data)

    bpp = int.from_bytes(image_data[28:30], "little")         # Bits per pixel
    compression = int.from_bytes(image_data[30:34], "little") # Compression type

    if bpp != 24:
        return (False, "Image is not 24-bit BMP.", pixel_offset, bpp, compression)

    if compression != 0:
        return (False, "BMP file is compressed.", pixel_offset, bpp, compression)

    return (True, "OK", pixel_offset, bpp, compression)
def capacity_bits(image_data: bytearray, pixel_offset: int) -> int:
    
    return len(image_data) - pixel_offset
def hide_message_bmp(input_bmp: str, message: str, output_bmp: str) -> str:
    
    if not file_exists(input_bmp):
        return "Error: Input image file does not exist."

    image_data = read_all_bytes(input_bmp)
    ok, msg, pixel_offset, _, _ = validate_bmp_24bit_uncompressed(image_data)
    if not ok:
        return f"Error: {msg}"

    
    full_message = message + STOP_MARKER
    secret_bits = text_to_bits(full_message)

    if len(secret_bits) > capacity_bits(image_data, pixel_offset):
        return "Error: Message too long for the image."

    bit_index = 0

    
    for i in range(pixel_offset, len(image_data)):
        if bit_index >= len(secret_bits):
            break
        image_data[i] = (image_data[i] & 0b11111110) | secret_bits[bit_index]
        bit_index += 1

    write_all_bytes(output_bmp, image_data)
    return "Success: Message hidden successfully."
def reveal_message_bmp(stego_bmp: str) -> str:
    
    if not file_exists(stego_bmp):
        return "Error: Stego image does not exist."

    image_data = read_all_bytes(stego_bmp)
    ok, msg, pixel_offset, _, _ = validate_bmp_24bit_uncompressed(image_data)
    if not ok:
        return f"Error: {msg}"

    extracted_bits = []
    stop_bits = text_to_bits(STOP_MARKER)

    
    for i in range(pixel_offset, len(image_data)):
        extracted_bits.append(image_data[i] & 1)
        if extracted_bits[-len(stop_bits):] == stop_bits:
            return bits_to_text(extracted_bits[:-len(stop_bits)])

    return "Error: No hidden message found."
def menu():
    
    print("=== Image Steganography (LSB) ===")

    while True:
        print("1) Encode message")
        print("2) Decode message")
        print("3) Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            img = input("Enter input BMP path: ")
            msg = input("Enter secret message: ")
            out = input("Enter output BMP name: ") or "stego.bmp"
            print(hide_message_bmp(img, msg, out))

        elif choice == "2":
            img = input("Enter stego BMP path: ")
            print(reveal_message_bmp(img))

        elif choice == "3":
            break

        else:
            print("Invalid choice.")
            if __name__ == "__main__":
                menu()