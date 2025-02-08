import sqlite3
from src.services.encryption import decrypt_data

def view_saved_passwords():
    """Fetch and display all saved passwords from the database."""
    conn = sqlite3.connect('src/database/vault.db')
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT id, website, username, password_encrypted FROM passwords WHERE user_id = ?', (1,))
        rows = cursor.fetchall()

        if not rows:
            print("No passwords found in the database.")
            return

        print("\nSaved Passwords:")
        for row in rows:
            password_id, website, username, encrypted_password = row
            decrypted_password = decrypt_data(encrypted_password)
            print(f"ID: {password_id}, Website: {website}, Username: {username}, Password: {decrypted_password}")

    except Exception as e:
        print(f"Error fetching passwords: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    view_saved_passwords()