import sqlite3

def initialize_db():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect('src/database/vault.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            master_password_hash TEXT NOT NULL,
            biometric_data BLOB
        )
    ''')

    # Create passwords table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password_encrypted TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

def add_password(user_id, website, username, encrypted_password):
    """Add a new password to the database."""
    conn = sqlite3.connect('src/database/vault.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO passwords (user_id, website, username, password_encrypted)
            VALUES (?, ?, ?, ?)
        ''', (user_id, website, username, encrypted_password))
        conn.commit()
        print("Password added successfully to the database.")
    except Exception as e:
        print(f"Error adding password to the database: {e}")
    finally:
        conn.close()

def get_passwords(user_id):
    """Retrieve passwords for a specific user."""
    conn = sqlite3.connect('src/database/vault.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, website, username, password_encrypted FROM passwords WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_password(password_id, website, username, encrypted_password):
    """Update an existing password in the database."""
    conn = sqlite3.connect('src/database/vault.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE passwords
        SET website = ?, username = ?, password_encrypted = ?
        WHERE id = ?
    ''', (website, username, encrypted_password, password_id))
    conn.commit()
    conn.close()

def delete_password(password_id):
    """Delete a password from the database."""
    conn = sqlite3.connect('src/database/vault.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM passwords WHERE id = ?', (password_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
    print("Database initialized successfully.")