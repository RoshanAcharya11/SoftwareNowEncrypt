import sys
from typing import List, Tuple


def encrypt_file(src_path: str, enc_path: str, shift1: int, shift2: int) -> Tuple[str, List[int]]:
    with open(src_path, "r", encoding="utf-8") as file_in:
        plain_data = file_in.read()

    enc_buffer: List[str] = []
    applied_rules: List[int] = []

    for symbol in plain_data:
        if 'a' <= symbol <= 'z':
            if symbol <= 'm':
                idx_new = (ord(symbol) - ord('a') + (shift1 * shift2)) % 26
                enc_buffer.append(chr(idx_new + ord('a')))
                applied_rules.append(0)
            else:
                idx_new = (ord(symbol) - ord('a') - (shift1 + shift2)) % 26
                enc_buffer.append(chr(idx_new + ord('a')))
                applied_rules.append(1)

        elif 'A' <= symbol <= 'Z':
            if symbol <= 'M':
                idx_new = (ord(symbol) - ord('A') - shift1) % 26
                enc_buffer.append(chr(idx_new + ord('A')))
                applied_rules.append(2)
            else:
                idx_new = (ord(symbol) - ord('A') + (shift2 ** 2)) % 26
                enc_buffer.append(chr(idx_new + ord('A')))
                applied_rules.append(3)

        else:
            enc_buffer.append(symbol)
            applied_rules.append(4)

    enc_text = "".join(enc_buffer)

    with open(enc_path, "w", encoding="utf-8") as file_out:
        file_out.write(enc_text)

    return enc_text, applied_rules


def decrypt_file(enc_path: str, dec_path: str, rulebook: List[int], shift1: int, shift2: int) -> str:
    with open(enc_path, "r", encoding="utf-8") as file_enc:
        enc_text = file_enc.read()

    if len(enc_text) != len(rulebook):
        raise ValueError("Encrypted text length and rules length do not match; cannot decrypt safely.")

    dec_buffer: List[str] = []

    for i, symbol in enumerate(enc_text):
        mode = rulebook[i]

        if mode == 0:
            idx = ord(symbol) - ord('a')
            orig_idx = (idx - (shift1 * shift2)) % 26
            dec_buffer.append(chr(orig_idx + ord('a')))

        elif mode == 1:
            idx = ord(symbol) - ord('a')
            orig_idx = (idx + (shift1 + shift2)) % 26
            dec_buffer.append(chr(orig_idx + ord('a')))

        elif mode == 2:
            idx = ord(symbol) - ord('A')
            orig_idx = (idx + shift1) % 26
            dec_buffer.append(chr(orig_idx + ord('A')))

        elif mode == 3:
            idx = ord(symbol) - ord('A')
            orig_idx = (idx - (shift2 ** 2)) % 26
            dec_buffer.append(chr(orig_idx + ord('A')))

        else:
            dec_buffer.append(symbol)

    dec_text = "".join(dec_buffer)

    with open(dec_path, "w", encoding="utf-8") as file_dec:
        file_dec.write(dec_text)

    return dec_text


def verify_files(path_a: str, path_b: str) -> bool:
    with open(path_a, "r", encoding="utf-8") as f1:
        txt_a = f1.read()
    with open(path_b, "r", encoding="utf-8") as f2:
        txt_b = f2.read()
    return txt_a == txt_b


def main() -> None:
    try:
        shift1 = int(input("Enter shift1: ").strip())
        shift2 = int(input("Enter shift2: ").strip())
    except ValueError:
        print("Please enter valid integers for shift1 and shift2.", file=sys.stderr)
        return

    file_plain = "raw_text.txt"
    file_enc = "encrypted_text.txt"
    file_dec = "decrypted_text.txt"

    try:
        _, rulebook = encrypt_file(file_plain, file_enc, shift1, shift2)
        print(f"Encrypted -> {file_enc}")

        decrypt_file(file_enc, file_dec, rulebook, shift1, shift2)
        print(f"Decrypted -> {file_dec}")

        if verify_files(file_plain, file_dec):
            print("Verification succeeded: decrypted text matches the original.")
        else:
            print("Verification failed: decrypted text does NOT match the original.")

    except FileNotFoundError as e:
        print(f"File error: {e}. Make sure '{file_plain}' exists next to this script.", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
