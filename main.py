def encrypt_char(char, shift1, shift2):
    """Encrypt a single character based on the custom rules"""
    if char.islower():
        # Lowercase letters
        if 'a' <= char <= 'm':  # First half (a-m)
            shift = (shift1 * shift2) % 26
            return chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:  # Second half (n-z)
            shift = (shift1 + shift2) % 26
            return chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
    
    elif char.isupper():
        # Uppercase letters
        if 'A' <= char <= 'M':  # First half (A-M)
            shift = shift1 % 26
            return chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        else:  # Second half (N-Z)
            shift = (shift2 ** 2) % 26
            return chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
    
    else:
        # Spaces, tabs, newlines, special characters, numbers remain unchanged
        return char


def decrypt_char(char, shift1, shift2):
    """Decrypt a single character by reversing the encryption rules"""
    if char.islower():
        # We need to figure out where this encrypted char came from
        # Try both decryption paths and see which gives us a char in the right range
        
        # Path 1: Assume it came from first half (a-m), so reverse forward shift
        shift = (shift1 * shift2) % 26
        candidate1 = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        
        # Path 2: Assume it came from second half (n-z), so reverse backward shift
        shift = (shift1 + shift2) % 26  
        candidate2 = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        
        # Return the candidate that falls in the correct original range
        if 'a' <= candidate1 <= 'm':
            return candidate1
        elif 'n' <= candidate2 <= 'z':
            return candidate2
        else:
            # Edge case: return the first candidate if neither fits perfectly
            return candidate1
    
    elif char.isupper():
        # Path 1: Assume it came from first half (A-M), so reverse backward shift
        shift = shift1 % 26
        candidate1 = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        
        # Path 2: Assume it came from second half (N-Z), so reverse forward shift
        shift = (shift2 ** 2) % 26
        candidate2 = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        
        # Return the candidate that falls in the correct original range
        if 'A' <= candidate1 <= 'M':
            return candidate1
        elif 'N' <= candidate2 <= 'Z':
            return candidate2
        else:
            # Edge case: return the first candidate if neither fits perfectly
            return candidate1
    
    else:
        # Spaces, tabs, newlines, special characters, numbers remain unchanged
        return char


def encrypt_file(input_filename, output_filename, shift1, shift2):
    """Encrypt the contents of input file and write to output file"""
    try:
        with open(input_filename, 'r', encoding='utf-8') as infile:
            content = infile.read()
        
        encrypted_content = ''.join(encrypt_char(char, shift1, shift2) for char in content)
        
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            outfile.write(encrypted_content)
            
        print(f"✓ Successfully encrypted '{input_filename}' to '{output_filename}'")
        return True
        
    except FileNotFoundError:
        print(f"✗ Error: Could not find file '{input_filename}'")
        return False
    except Exception as e:
        print(f"✗ Error during encryption: {e}")
        return False


def decrypt_file(input_filename, output_filename, shift1, shift2):
    """Decrypt the contents of input file and write to output file"""
    try:
        with open(input_filename, 'r', encoding='utf-8') as infile:
            content = infile.read()
        
        decrypted_content = ''.join(decrypt_char(char, shift1, shift2) for char in content)
        
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            outfile.write(decrypted_content)
            
        print(f"✓ Successfully decrypted '{input_filename}' to '{output_filename}'")
        return True
        
    except FileNotFoundError:
        print(f"✗ Error: Could not find file '{input_filename}'")
        return False
    except Exception as e:
        print(f"✗ Error during decryption: {e}")
        return False


def verify_decryption(original_filename, decrypted_filename):
    """Compare original and decrypted files to verify successful decryption"""
    try:
        with open(original_filename, 'r', encoding='utf-8') as orig_file:
            original_content = orig_file.read()
            
        with open(decrypted_filename, 'r', encoding='utf-8') as decr_file:
            decrypted_content = decr_file.read()
        
        if original_content == decrypted_content:
            print("🎉 SUCCESS: Decryption was successful! Files match perfectly.")
            return True
        else:
            print("❌ FAILURE: Decryption failed. Files do not match.")
            print(f"Original length: {len(original_content)}")
            print(f"Decrypted length: {len(decrypted_content)}")
            return False
            
    except FileNotFoundError as e:
        print(f"✗ Error: Could not find file for verification: {e}")
        return False
    except Exception as e:
        print(f"✗ Error during verification: {e}")
        return False


def main():
    """Main program function"""
    print("🔐 Custom Encryption/Decryption Program")
    print("=" * 40)
    
    # Get user input for shift values
    try:
        shift1 = int(input("Enter shift1 value: "))
        shift2 = int(input("Enter shift2 value: "))
    except ValueError:
        print("✗ Error: Please enter valid integer values for shifts.")
        return
    
    print(f"\nUsing shifts: shift1={shift1}, shift2={shift2}")
    print("-" * 40)
    
    # Step 1: Encrypt the file
    print("Step 1: Encrypting...")
    if not encrypt_file("raw_text.txt", "encrypted_text.txt", shift1, shift2):
        return
    
    # Step 2: Decrypt the encrypted file
    print("\nStep 2: Decrypting...")
    if not decrypt_file("encrypted_text.txt", "decrypted_text.txt", shift1, shift2):
        return
    
    # Step 3: Verify the decryption
    print("\nStep 3: Verifying...")
    verify_decryption("raw_text.txt", "decrypted_text.txt")


if __name__ == "__main__":
    main()