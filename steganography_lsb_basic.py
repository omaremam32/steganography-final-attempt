"""
Image-Based Text Steganography (LSB) using BASIC Python only (no external libraries).

- Works with 24-bit uncompressed BMP files.
- Dual input methods: type message OR read from a .txt file.
- File existence checks for BMP image and text file.
- Color channel sequence awareness (BMP pixel bytes are stored as B, G, R).
- Smart looping: stop embedding/extracting as soon as done.
"""

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


def read_message_from_txt(txt_path: str) -> tuple:
    if not file_exists(txt_path):
        return (False, f"Error: Text file does not exist: {txt_path}")

    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            return (True, f.read())
    except Exception as e:
        return (False, f"Error: Could not read text file: {e}")


def validate_message(message: str) -> tuple:
    if message is None:
        return (False, "Error: Message is empty or invalid.")

    for ch in message:
        if ord(ch) > 255:
            return (False, "Error: Message contains unsupported characters. Please use normal English text.")
        if ord(ch) < 9 or (ord(ch) > 13 and ord(ch) < 32):
            return (False, "Error: Message contains invalid control characters.")

    return (True, "OK")


def text_to_bits(text: str) -> list:
    bits = []

    for ch in text:
        byte = format(ord(ch), "08b")
        for bit in byte:
            bits.append(1 if bit == "1" else 0)

    return bits


def bits_to_text(bits: list) -> str:
    chars = []

    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i + 8]

        if len(byte_bits) < 8:
            break

        byte_str = "".join("1" if bit else "0" for bit in byte_bits)
        chars.append(chr(int(byte_str, 2)))

    return "".join(chars)


def get_bmp_pixel_data_offset(image_data: bytearray) -> int:
    if len(image_data) < 14:
        return BMP_HEADER_SIZE

    offset = int.from_bytes(image_data[10:14], byteorder="little", signed=False)

    if offset > 0:
        return offset

    return BMP_HEADER_SIZE


def validate_bmp_24bit_uncompressed(image_data: bytearray) -> tuple:
    if len(image_data) < BMP_HEADER_SIZE:
        return (False, "File is too small to be a valid BMP.", BMP_HEADER_SIZE, None, None)

    if image_data[0:2] != b"BM":
        return (False, "Not a BMP file. Missing BM signature.", BMP_HEADER_SIZE, None, None)

    pixel_offset = get_bmp_pixel_data_offset(image_data)

    dib_size = int.from_bytes(image_data[14:18], "little")
    if dib_size < 40:
        return (False, "Unsupported BMP format. DIB header is too small.", pixel_offset, None, None)

    bpp = int.from_bytes(image_data[28:30], "little")
    compression = int.from_bytes(image_data[30:34], "little")

    if bpp != 24:
        return (False, f"Unsupported BMP bit-depth: {bpp}. Please use 24-bit BMP.", pixel_offset, bpp, compression)

    if compression != 0:
        return (False, "Unsupported BMP compression. Please use uncompressed BMP.", pixel_offset, bpp, compression)

    if pixel_offset >= len(image_data):
        return (False, "Corrupt BMP. Pixel data offset is out of range.", pixel_offset, bpp, compression)

    return (True, "OK", pixel_offset, bpp, compression)


def capacity_bits(image_data: bytearray, pixel_offset: int) -> int:
    return max(0, len(image_data) - pixel_offset)


def hide_message_bmp(input_bmp: str, message: str, output_bmp: str) -> str:
    if not file_exists(input_bmp):
        return f"Error: Input file does not exist: {input_bmp}"

    valid_msg, msg_result = validate_message(message)
    if not valid_msg:
        return msg_result

    image_data = read_all_bytes(input_bmp)

    ok, msg, pixel_offset, _, _ = validate_bmp_24bit_uncompressed(image_data)
    if not ok:
        return f"Error: {msg}"

    full_message = message + STOP_MARKER
    secret_bits = text_to_bits(full_message)

    cap = capacity_bits(image_data, pixel_offset)

    if len(secret_bits) > cap:
        return f"Error: Message is too long. Needs {len(secret_bits)} bits but image capacity is {cap} bits."

    bit_index = 0

    for i in range(pixel_offset, len(image_data)):
        if bit_index >= len(secret_bits):
            break

        current_byte = image_data[i]
        current_byte = current_byte & 0b11111110
        new_byte = current_byte | secret_bits[bit_index]

        image_data[i] = new_byte
        bit_index += 1

    write_all_bytes(output_bmp, image_data)

    return f"Success: Message hidden. Saved as {output_bmp} (embedded {bit_index} bits)."


def reveal_message_bmp(stego_bmp: str) -> str:
    if not file_exists(stego_bmp):
        return f"Error: Input file does not exist: {stego_bmp}"

    image_data = read_all_bytes(stego_bmp)

    ok, msg, pixel_offset, _, _ = validate_bmp_24bit_uncompressed(image_data)
    if not ok:
        return f"Error: {msg}"

    stop_bits = text_to_bits(STOP_MARKER)
    extracted_bits = []

    for i in range(pixel_offset, len(image_data)):
        lsb = image_data[i] & 0b00000001
        extracted_bits.append(lsb)

        if len(extracted_bits) >= len(stop_bits):
            if extracted_bits[-len(stop_bits):] == stop_bits:
                message_bits_only = extracted_bits[:-len(stop_bits)]
                return bits_to_text(message_bits_only)

    return "Error: Couldn't find the message. Stop marker not found."


def menu() -> None:
    print("=== Image Steganography (LSB) - Basic Python ===")
    print("Note: Use 24-bit uncompressed BMP images.")
    print("BMP stores pixel bytes in B, G, R order.")
    print("Each 24-bit BMP pixel contains 3 bytes: Blue, Green, and Red.")
    print("The program hides one secret bit in the least significant bit of each byte.")
    print()

    while True:
        print("Choose an option:")
        print("1) Hide a message (encode)")
        print("2) Extract a message (decode)")
        print("3) Exit")

        choice = input("Enter 1/2/3: ").strip()

        if choice == "1":
            input_bmp = input("Enter input BMP path: ").strip()

            if not file_exists(input_bmp):
                print("Error: Input image file does not exist.\n")
                continue

            print("Message input method:")
            print("1) Type the message")
            print("2) Read message from a .txt file")

            method = input("Enter 1/2: ").strip()

            if method == "1":
                message = input("Enter secret message: ")

            elif method == "2":
                txt_path = input("Enter text file path: ").strip()
                ok, result = read_message_from_txt(txt_path)

                if not ok:
                    print(result + "\n")
                    continue

                message = result

            else:
                print("Error: Invalid input method.\n")
                continue

            valid_msg, msg_result = validate_message(message)
            if not valid_msg:
                print(msg_result + "\n")
                continue

            output_bmp = input("Enter output BMP path (e.g., stego.bmp): ").strip()

            if output_bmp == "":
                output_bmp = "stego.bmp"

            result = hide_message_bmp(input_bmp, message, output_bmp)
            print(result + "\n")

        elif choice == "2":
            stego_bmp = input("Enter stego BMP path: ").strip()

            result = reveal_message_bmp(stego_bmp)

            print("\n--- Extracted Result ---")
            print(result)
            print("------------------------\n")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Error: Please enter 1, 2, or 3.\n")


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting...")
        sys.exit(0)