def encrypt_char(c, shift1, shift2):
    if c.islower():
        pos = ord(c) - ord('a')
        if pos <= 12:  # a-m
            shift = shift1 * shift2
            return chr((pos + shift) % 26 + ord('a'))
        else:  # n-z
            shift = shift1 + shift2
            return chr((pos - shift) % 26 + ord('a'))
    elif c.isupper():
        pos = ord(c) - ord('A')
        if pos <= 12:  # A-M
            shift = shift1
            return chr((pos - shift) % 26 + ord('A'))
        else:  # N-Z
            shift = shift2 ** 2
            return chr((pos + shift) % 26 + ord('A'))
    return c

def decrypt_char(c, shift1, shift2):
    if c.islower():
        pos = ord(c) - ord('a')
        if pos <= 12:  # Assume came from first half, reverse forward shift
            shift = shift1 * shift2
            return chr((pos - shift) % 26 + ord('a'))
        else:  # Assume came from second half, reverse backward shift
            shift = shift1 + shift2
            return chr((pos + shift) % 26 + ord('a'))
    elif c.isupper():
        pos = ord(c) - ord('A')
        if pos <= 12:  # Assume came from first half, reverse backward shift
            shift = shift1
            return chr((pos + shift) % 26 + ord('A'))
        else:  # Assume came from second half, reverse forward shift
            shift = shift2 ** 2
            return chr((pos - shift) % 26 + ord('A'))
    return c

def encrypt_file(shift1, shift2):
    with open("raw_text.txt", "r") as f:
        content = f.read()
    encrypted = "".join(encrypt_char(c, shift1, shift2) for c in content)
    with open("encrypted_text.txt", "w") as f:
        f.write(encrypted)

def decrypt_file(shift1, shift2):
    with open("encrypted_text.txt", "r") as f:
        content = f.read()
    decrypted = "".join(decrypt_char(c, shift1, shift2) for c in content)
    with open("decrypted_text.txt", "w") as f:
        f.write(decrypted)

def verify():
    with open("raw_text.txt", "r") as f:
        original = f.read()
    with open("decrypted_text.txt", "r") as f:
        decrypted = f.read()
    if original == decrypted:
        print("Decryption was successful.")
    else:
        print("Decryption was not successful.")

if __name__ == "__main__":
    while True:
        try:
            shift1 = int(input("Enter shift1: "))
            shift2 = int(input("Enter shift2: "))
            break
        except ValueError:
            print("Please enter integer values for shifts.")
    encrypt_file(shift1, shift2)
    decrypt_file(shift1, shift2)
    verify()