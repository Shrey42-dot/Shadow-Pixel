# src/stego_utils.py

"""
Phase 1: Binary encoding utilities for Shadow-Pixel

This module handles:
- String <-> bytes conversion
- Bytes <-> bitstream conversion
- 32-bit length header packing and unpacking

No image or cryptography logic exists here.
"""

from typing import List


# -----------------------------
# Basic Bit Conversion Helpers
# -----------------------------

def string_to_bytes(text: str) -> bytes:
    """Convert UTF-8 string to bytes."""
    return text.encode("utf-8")


def bytes_to_string(data: bytes) -> str:
    """Convert bytes back to UTF-8 string."""
    return data.decode("utf-8")


def bytes_to_bits(data: bytes) -> List[int]:
    """
    Convert bytes to a list of bits (0/1).
    Each byte becomes 8 bits.
    """
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits


def bits_to_bytes(bits: List[int]) -> bytes:
    """
    Convert list of bits back to bytes.
    Length of bits must be divisible by 8.
    """
    if len(bits) % 8 != 0:
        raise ValueError("Bit length must be divisible by 8")

    result = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for bit in bits[i:i + 8]:
            byte = (byte << 1) | bit
        result.append(byte)

    return bytes(result)


# -----------------------------
# Length Header Logic (32-bit)
# -----------------------------

def int_to_32bit_bits(value: int) -> List[int]:
    """
    Convert integer to 32-bit big-endian bit list.
    """
    if value < 0 or value >= 2**32:
        raise ValueError("Value out of range for 32-bit integer")

    bits = []
    for i in range(31, -1, -1):
        bits.append((value >> i) & 1)
    return bits


def bits_to_int(bits: List[int]) -> int:
    """
    Convert bit list to integer.
    """
    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value


# -----------------------------
# Public Packing API
# -----------------------------

def pack_message(text: str) -> List[int]:
    """
    Convert a string into:
    [32-bit length header][message bits]
    """
    data_bytes = string_to_bytes(text)
    message_bits = bytes_to_bits(data_bytes)

    length_bits = int_to_32bit_bits(len(message_bits))
    return length_bits + message_bits


def unpack_message(bitstream: List[int]) -> str:
    """
    Extract message from:
    [32-bit length header][message bits]
    """
    if len(bitstream) < 32:
        raise ValueError("Bitstream too short to contain header")

    length_bits = bitstream[:32]
    message_length = bits_to_int(length_bits)

    message_bits = bitstream[32:32 + message_length]

    if len(message_bits) != message_length:
        raise ValueError("Incomplete message bits")

    data_bytes = bits_to_bytes(message_bits)
    return bytes_to_string(data_bytes)

# -----------------------------
# Phase 3: Image Capacity Logic
# -----------------------------

from PIL import Image


def calculate_image_capacity(image_path: str) -> int:
    """
    Calculate how many bits can be hidden in an image
    using 1 LSB per RGB channel.
    """
    with Image.open(image_path) as img:
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")

        width, height = img.size
        channels = 3  # Only RGB channels

        return width * height * channels


def validate_capacity(image_path: str, required_bits: int) -> None:
    """
    Ensure the image can hold the required number of bits.
    Raises ValueError if capacity is insufficient.
    """
    capacity = calculate_image_capacity(image_path)

    if required_bits > capacity:
        raise ValueError(
            f"Image capacity insufficient: "
            f"{capacity} bits available, "
            f"{required_bits} bits required"
        )

# -----------------------------
# Phase 4: LSB Embedding Engine
# -----------------------------

def embed_bits_into_image(
    image_path: str,
    output_path: str,
    bits: list[int]
) -> None:
    """
    Embed a list of bits into the LSBs of an image's RGB pixels.
    """
    validate_capacity(image_path, len(bits))

    with Image.open(image_path) as img:
        img = img.convert("RGB")
        pixels = list(img.getdata())

    bit_index = 0
    new_pixels = []

    for r, g, b in pixels:
        if bit_index < len(bits):
            r = (r & 0b11111110) | bits[bit_index]
            bit_index += 1
        if bit_index < len(bits):
            g = (g & 0b11111110) | bits[bit_index]
            bit_index += 1
        if bit_index < len(bits):
            b = (b & 0b11111110) | bits[bit_index]
            bit_index += 1

        new_pixels.append((r, g, b))

    stego_img = Image.new("RGB", img.size)
    stego_img.putdata(new_pixels)
    stego_img.save(output_path)


def extract_bits_from_image(
    image_path: str,
    num_bits: int
) -> list[int]:
    """
    Extract a specific number of bits from the LSBs of an image.
    """
    extracted_bits = []

    with Image.open(image_path) as img:
        img = img.convert("RGB")
        pixels = list(img.getdata())

    for r, g, b in pixels:
        if len(extracted_bits) < num_bits:
            extracted_bits.append(r & 1)
        if len(extracted_bits) < num_bits:
            extracted_bits.append(g & 1)
        if len(extracted_bits) < num_bits:
            extracted_bits.append(b & 1)

        if len(extracted_bits) >= num_bits:
            break

    return extracted_bits

# -----------------------------
# Phase 5: Full Secure Pipeline
# -----------------------------

from crypto_utils import encrypt_message, decrypt_message


def hide_secret_in_image(
    image_path: str,
    output_path: str,
    secret_text: str,
    password: str
) -> None:
    """
    Encrypt a secret message and hide it inside an image.
    """
    # Encrypt the secret
    encrypted_bytes = encrypt_message(secret_text, password)

    # Convert encrypted bytes to bits with length header
    encrypted_bits = bytes_to_bits(encrypted_bytes)
    length_bits = int_to_32bit_bits(len(encrypted_bits))
    full_bitstream = length_bits + encrypted_bits

    # Embed into image
    embed_bits_into_image(image_path, output_path, full_bitstream)


def reveal_secret_from_image(
    image_path: str,
    password: str
) -> str:
    """
    Extract and decrypt a hidden secret from an image.
    """
    # Extract header first
    header_bits = extract_bits_from_image(image_path, 32)
    message_length = bits_to_int(header_bits)

    # Extract encrypted payload
    encrypted_bits = extract_bits_from_image(
        image_path,
        32 + message_length
    )[32:]

    encrypted_bytes = bits_to_bytes(encrypted_bits)

    # Decrypt and return plaintext
    return decrypt_message(encrypted_bytes, password)
