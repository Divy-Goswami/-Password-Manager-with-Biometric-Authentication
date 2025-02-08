import os
from cryptography.fernet import Fernet

def generate_key():
    """Generate a new encryption key and save it to a file."""
    key = Fernet.generate_key()
    os.makedirs("src/assets/keys", exist_ok=True)  # Ensure the directory exists
    with open("src/assets/keys/encryption.key", "wb") as key_file:
        key_file.write(key)
    print("Encryption key generated and saved.")

def load_key():
    """Load the encryption key from the file."""
    try:
        with open("src/assets/keys/encryption.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        print("Encryption key not found. Generating a new key...")
        generate_key()
        return load_key()  # Retry loading the key after generating it

def encrypt_data(data):
    """Encrypt data using AES."""
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

def decrypt_data(encrypted_data):
    """Decrypt data using AES."""
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()