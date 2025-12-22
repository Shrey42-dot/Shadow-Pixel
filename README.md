# 🌑 Shadow-Pixel

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/Shrey42-dot/Shadow-Pixel)
**Invisible Cryptographic Steganography using AES-256-GCM and LSB Encoding**

Shadow-Pixel is a local, offline, security-focused steganography tool that allows you to hide strongly encrypted secrets inside ordinary images.
The output image appears visually identical to the original, yet secretly contains protected data that can only be recovered with the correct password.

This project deliberately combines modern authenticated cryptography with low-level image processing, packaged as a fully installable command-line tool, demonstrating real-world security engineering rather than toy encryption.

---
## ✨ Key Features

* 🔐 AES-256-GCM authenticated encryption
Confidentiality + integrity protection (tamper detection included)

* 🖼️ Invisible LSB steganography
Data embedded in the Least Significant Bits of RGB pixels

* 📦 Explicit bit-length encoding
Safe and deterministic extraction without data corruption

* 🧠 Automatic image capacity validation
Prevents overflow and broken stego-images

* 💻 Installable command-line interface (shadow-pixel)
Clean CLI with clear error handling

* 🚫 Fully offline by design
No APIs, no telemetry, no network access

* 🛡️ Tamper-resistant by default
Any modification to the image causes decryption failure

--- 

## 📸 Visual Demonstration

### ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎original.png‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ stego.png
<img width="265" height="190" alt="image" src="https://github.com/user-attachments/assets/c7bada75-7582-491f-8276-4f1103e0e107" />  
‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ 
<img width="265" height="190" alt="image" src="https://github.com/user-attachments/assets/da599478-5c18-44a2-b9e9-ea64fea99e84" />


Observation:
Both images look identical to the human eye.
However, the second image contains an AES-GCM encrypted secret embedded at the pixel level.

---

## 🧠 How Shadow-Pixel Works
High-Level Pipeline (Hiding)

            Plaintext Message
                    ↓
            AES-256-GCM Encryption
                    ↓
            Byte → Bit conversion + length header
                    ↓
            Image capacity validation
                    ↓
            LSB embedding into RGB pixels
                    ↓
            Stego Image (visually unchanged)

Extraction (Reverse Process)

            Stego Image
                    ↓
            LSB bit extraction
                    ↓
            Length header parsing
                    ↓
            AES-GCM decryption
                    ↓
            Original plaintext message

---

## 🔐 Security Model

            | Property       | Description                             |
            | -------------- | --------------------------------------- |
            | Encryption     | AES-256-GCM (authenticated encryption)  |
            | Integrity      | Any tampering causes decryption failure |
            | Authentication | Password-derived symmetric key          |
            | Stealth        | No visible image distortion             |
            | Offline Safety | No network or external dependencies     |

### Important:
Even if an attacker suspects steganography, the embedded data remains cryptographically secure.
This is not security-through-obscurity — it is real cryptography.

---

## 📦 Installation

Clone the repository and install locally:

            git clone https://github.com/Shrey42-dot/Shadow-Pixel.git
            cd Shadow-Pixel
            pip install -e .
            
Verify installation:

            shadow-pixel --help

---

## 🖥️ Command-Line Usage

Hide a Secret

            shadow-pixel hide \
            --image examples/original.png \
            --out examples/stego.png \
            --msg "Top secret message" \
            --key superpassword

Output:

            [+] Secret successfully hidden

Reveal a Secret

            shadow-pixel reveal \
            --image examples/stego.png \
            --key superpassword

Output:

            [+] Revealed secret:
            Top secret message

### As shown in the image below

<img width="1335" height="634" alt="Screenshot 2025-12-21 220927" src="https://github.com/user-attachments/assets/b47edce8-0a8a-402c-b836-cae8373278bf" />


---
## 🧮 Image Capacity
Shadow-Pixel embeds 1 bit per RGB channel (3 bits per pixel).

            | Image Resolution | Approx. Capacity |
            | ---------------- | ---------------- |
            | 800 × 600        | ~180 KB          |
            | 1920 × 1080      | ~750 KB          |
            | 3840 × 2160 (4K) | ~3 MB            |

Capacity is automatically validated before embedding.

--- 

## 🗂️ Project Structure

            Shadow-Pixel/
            ├── src/
            │   ├── __init__.py
            │   ├── cli.py            # CLI entry point & argument parsing
            │   ├── stego_utils.py    # LSB embedding, extraction & bit logic
            │   └── crypto_utils.py   # AES-GCM encryption & key handling
            ├── examples/
            │   ├── original.png
            │   └── stego.png
            ├── tests/                # Unit tests
            ├── pyproject.toml        # Build & CLI configuration
            ├── requirements.txt
            └── .gitignore

--- 
## 🧪 Core Modules Overview

### crypto_utils.py

* AES-256-GCM encryption & decryption

* Password-derived symmetric keys

* Built-in tamper detection

### stego_utils.py

* Bit/byte serialization

* Image capacity validation

* LSB embedding and extraction logic

* Secure end-to-end pipeline

### cli.py

* Installable CLI interface

* hide and reveal commands

* Clean error handling and help output

--- 
## 📚 Dependencies 
Runtime dependencies only:

            pillow>=10.0.0
            cryptography>=42.0.0

--- 

## ⚠️ What This Project Is NOT

* ❌ Not XOR-based encryption

* ❌ Not metadata hiding

* ❌ Not watermarking

* ❌ Not security-through-obscurity

This is real cryptography + real steganography.

--- 

## 🚀 Future Improvements (Optional)

* File-based payloads (not just text)

* Multi-bit LSB encoding

* Password-based key stretching (PBKDF2 / Argon2)

* Batch image support

* GUI frontend

--- 

## 👤 Author

### Shrey

Built as a cybersecurity + image processing portfolio project.
