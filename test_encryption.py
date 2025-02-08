from src.services.encryption import encrypt_data, decrypt_data

if __name__ == "__main__":
    test_data = "MySecretPassword123!"
    encrypted = encrypt_data(test_data)
    print(f"Encrypted: {encrypted}")

    decrypted = decrypt_data(encrypted)
    print(f"Decrypted: {decrypted}")