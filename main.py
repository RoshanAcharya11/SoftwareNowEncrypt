import sys
from typing import List, Tuple

# I have implemeted the encryption logic as per the requirements of the assignment.
def encrypt_file(src_path: str, enc_path: str, shift1: int, shift2: int) -> Tuple[str, List[int]]:
    """Here the function reads the plaintext file, and eencrpts with the shift rules.\
    The rule ID is also saved in the list.
    The encrypted text is saved into the encypted text file
    Finally the encrypted text and the list of rules needed for decrption is returned."""

    # This part reads the plaintext file
    with open(src_path, "r", encoding="utf-8") as file_in:
        plain_data = file_in.read()
    
    # This variable is used to store the encrpted text as the string is built.

    enc_buffer: List[str] = []

    # This variable is used to store the rule IDs for decryption reference
    applied_rules: List[int] = []

    #for loop goes through each character in the text

    for symbol in plain_data:
        # Here it is looking only at the lowercase letters
        if 'a' <= symbol <= 'z':
            if symbol <= 'm': # first half of the alphabet
                # I have implemented applied_rules(0) -> shift forward by (shift1 * shift2)
                idx_new = (ord(symbol) - ord('a') + (shift1 * shift2)) % 26

                # Encrpted character is being added to the buffer in the next step.
                enc_buffer.append(chr(idx_new + ord('a')))
                # finally the rule ID is added to the list.
                applied_rules.append(0)
            else:
                # Similar to the above implementation but for the second half of the alphabets with apllied_rules(1)
                idx_new = (ord(symbol) - ord('a') - (shift1 + shift2)) % 26
                enc_buffer.append(chr(idx_new + ord('a')))
                applied_rules.append(1)
        # Implementing for the capital letters
        elif 'A' <= symbol <= 'Z':
            # Implementing for the first half alphabets in capital letters
            if symbol <= 'M':
                # Using the applied_rules(2) -> shift backward by shift1
                idx_new = (ord(symbol) - ord('A') - shift1) % 26
                enc_buffer.append(chr(idx_new + ord('A')))
                applied_rules.append(2)
            else:
                # Similar to the above implementation but for the second half of the alphabets with apllied_rules(3)
                idx_new = (ord(symbol) - ord('A') + (shift2 ** 2)) % 26
                enc_buffer.append(chr(idx_new + ord('A')))
                applied_rules.append(3)

        else:
            # To finish it off I have implemented the no change rule for non-alphabetic characters with applied_rules(4)
            enc_buffer.append(symbol)
            applied_rules.append(4)
    # The code below joins the encrypted characters to form the final encrypted text.
    enc_text = "".join(enc_buffer)
    # The encrypted text is then written to the output file.
    with open(enc_path, "w", encoding="utf-8") as file_out:
        file_out.write(enc_text)
    # Finally the encrypted text and the list of rules is returned.
    return enc_text, applied_rules


"""
    I have implemented the decryption logic as per the requirements of the assignment.
"""

def decrypt_file(enc_path: str, dec_path: str, rulebook: List[int], shift1: int, shift2: int) -> str:
    """"
    This function reads the encrypted text file, and decrypts it using the provided rulebook and shift values.
    The decrypted text is saved into the decrypted text file.
    """

    # The encrpted file is read using the code below.
    with open(enc_path, "r", encoding="utf-8") as file_enc:
        enc_text = file_enc.read()
    # The code below is the safety check to ensure the lengths of the encrypted text and the rulebook match.
    if len(enc_text) != len(rulebook):
        raise ValueError("Encrypted text length and rules length do not match; cannot decrypt safely.")
    # This variable is used to store the decrypted text as the string is built.
    dec_buffer: List[str] = []
    # The for loop goes through each character in the encrypted text along with its corresponding rule from the rulebook.
    for i, symbol in enumerate(enc_text):
        # The mode variable stores the current rule to be applied.
        mode = rulebook[i]
        # The following conditional statements apply the appropriate decryption based on the rule.
        if mode == 0:
            # Decrypting for applied_rules(0) -> shift backward by (shift1 * shift2) hence reversing the encryption logic for first half of lowercase letters.
            idx = ord(symbol) - ord('a')
            orig_idx = (idx - (shift1 * shift2)) % 26
            # Finally the decrypted character is added to the buffer.
            dec_buffer.append(chr(orig_idx + ord('a')))
        # Decrypting for applied_rules(1) -> shift forward by (shift1 + shift2) hence reversing the encryption logic for second half of lowercase letters.
        elif mode == 1:
            # The index is calculated similarly to the above but with the forward shift.
            idx = ord(symbol) - ord('a')
            orig_idx = (idx + (shift1 + shift2)) % 26

            # Finally the decrypted character is added to the buffer.
            dec_buffer.append(chr(orig_idx + ord('a')))
        # Decrypting for applied_rules(2) -> shift forward by shift1 hence reversing the encryption logic for first half of capital letters.
        elif mode == 2:
            # The index is calculated similarly to the above but with the forward shift.
            idx = ord(symbol) - ord('A')
            # The original index is calculated by applying the reverse shift.
            orig_idx = (idx + shift1) % 26
            # Finally the decrypted character is added to the buffer.
            dec_buffer.append(chr(orig_idx + ord('A')))
        # Decrypting for applied_rules(3) -> shift backward by (shift2 ** 2) hence reversing the encryption logic for second half of capital letters.
        elif mode == 3:
            # The index is calculated similarly to the above but with the backward shift.
            idx = ord(symbol) - ord('A')
            # The original index is calculated by applying the reverse shift.
            orig_idx = (idx - (shift2 ** 2)) % 26
            
            dec_buffer.append(chr(orig_idx + ord('A')))
        # Below I implement the no change rule for non-alphabetic characters with applied_rules(4)
        else:
            # Non-alphabetic characters are added to the buffer without any change.
            dec_buffer.append(symbol)
    # The code below joins the decrypted characters to form the final decrypted text.
    dec_text = "".join(dec_buffer)
    # The decrypted text is then written to the output file.
    with open(dec_path, "w", encoding="utf-8") as file_dec:
        file_dec.write(dec_text)
    # Finally the decrypted text is returned.
    return dec_text

# This function verifies if two files have identical content.
def verify_files(path_a: str, path_b: str) -> bool:
    # It is reading the first file and add its content to txt_a
    with open(path_a, "r", encoding="utf-8") as f1:
        txt_a = f1.read()
    # It is reading the second file and add its content to txt_b
    with open(path_b, "r", encoding="utf-8") as f2:
        txt_b = f2.read()

    # Finally it compares the contents of both files and returns True if they are identical, otherwise False.
    return txt_a == txt_b


def main() -> None:
    # The main function handles user input and orchestrates the encryption, decryption, and verification processes.
    try:
        # Getting shift values from the user
        shift1 = int(input("Enter shift1: ").strip())
        shift2 = int(input("Enter shift2: ").strip())
    except ValueError:
        # Handle invalid input  
        print("Please enter valid integers for shift1 and shift2.", file=sys.stderr)
        return
    # File paths for plaintext, encrypted, and decrypted files
    file_plain = "raw_text.txt"
    file_enc = "encrypted_text.txt"
    file_dec = "decrypted_text.txt"

    try:
        # calling the encrypt_file function to encrypt the plaintext file,  the parameters plain file path, encrypted file path, shift1 and shift2 are passed.
        _, rulebook = encrypt_file(file_plain, file_enc, shift1, shift2)
        
        # The encrypted text file path is printed.
        print(f"Encrypted -> {file_enc}")
        # calling the decrypt_file function to decrypt the encrypted file, the parameters encrypted file path, decrypted file path, rulebook, shift1 and shift2 are passed.
        decrypt_file(file_enc, file_dec, rulebook, shift1, shift2)
        
        # The decrypted text file path is printed.
        print(f"Decrypted -> {file_dec}")

        # Verification step to check if the decrypted text matches the original plaintext.
        if verify_files(file_plain, file_dec):
            # If the files match, a success message is printed.
            print("Verification succeeded: decrypted text matches the original.")
        else:
            # If the files do not match, a failure message is printed.
            print("Verification failed: decrypted text does NOT match the original.")
    # Handling file not found errors
    except FileNotFoundError as e:
        print(f"File error: {e}. Make sure '{file_plain}' exists next to this script.", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
