import argparse
import os
from cryptography.fernet import Fernet

def generate_key(save_path):
    key = Fernet.generate_key()
    with open(save_path, 'wb') as key_file:
        key_file.write(key)
    print(f"Generated and saved key to {save_path}")
    return key

def load_key(path):
    with open(path, 'rb') as key_file:
        key = key_file.read()
    return key

def encrypt_file(file_path, output_path, key):
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)
        with open(output_path, 'wb') as file:
            file.write(encrypted_data)
        print("File encrypted successfully")
    except Exception as e:
        print(f"Error encrypting file: {str(e)}")

def decrypt_file(file_path, output_path, key):
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(data)
        with open(output_path, 'wb') as file:
            file.write(decrypted_data)
        print("File decrypted successfully")
    except Exception as e:
        print(f"Error decrypting file: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="File Encryption and Decryption Tool")
    parser.add_argument('--generate-key', type=str, help='Path to save the automatically generated encryption key')
    parser.add_argument('--encrypt', type=str, help='Path of the file to encrypt')
    parser.add_argument('--output', type=str, help='Output path for the encrypted file')
    parser.add_argument('--decrypt', type=str, help='Path of the file to decrypt')
    parser.add_argument('--decrypt-output', type=str, help='Output path for the decrypted file')
    parser.add_argument('--key', type=str, help='Path to the encryption key')

    args = parser.parse_args()

    if args.generate_key:
        generate_key(args.generate_key)

    if args.encrypt and args.output and args.key:
        key = load_key(args.key)
        encrypt_file(args.encrypt, args.output, key)

    if args.decrypt and args.decrypt_output and args.key:
        key = load_key(args.key)
        decrypt_file(args.decrypt, args.decrypt_output, key)

    else:
        print("No action specified or insufficient arguments. Use --help for more information.")

if __name__ == "__main__":
    main()
