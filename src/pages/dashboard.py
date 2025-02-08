import tkinter as tk
from tkinter import messagebox
from src.services.encryption import encrypt_data, decrypt_data
from src.database.crud import add_password, get_passwords, update_password, delete_password

class DashboardPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard - Password Manager")
        self.root.geometry("800x600")

        # Title Label
        self.label_title = tk.Label(root, text="Password Manager Dashboard", font=("Arial", 16))
        self.label_title.pack(pady=20)

        # Input Fields
        self.frame_inputs = tk.Frame(root)
        self.frame_inputs.pack(pady=10)

        # URL Field
        self.label_url = tk.Label(self.frame_inputs, text="URL:")
        self.label_url.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_url = tk.Entry(self.frame_inputs, width=50)
        self.entry_url.grid(row=0, column=1, padx=5, pady=5)

        # Name Field
        self.label_name = tk.Label(self.frame_inputs, text="Name:")
        self.label_name.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_name = tk.Entry(self.frame_inputs, width=50)
        self.entry_name.grid(row=1, column=1, padx=5, pady=5)

        # Username Field
        self.label_username = tk.Label(self.frame_inputs, text="Username:")
        self.label_username.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_username = tk.Entry(self.frame_inputs, width=50)
        self.entry_username.grid(row=2, column=1, padx=5, pady=5)

        # Site Password Field
        self.label_password = tk.Label(self.frame_inputs, text="Site Password:")
        self.label_password.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_password = tk.Entry(self.frame_inputs, show="*", width=50)
        self.entry_password.grid(row=3, column=1, padx=5, pady=5)

        # Note Field
        self.label_note = tk.Label(self.frame_inputs, text="Note:")
        self.label_note.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.entry_note = tk.Entry(self.frame_inputs, width=50)
        self.entry_note.grid(row=4, column=1, padx=5, pady=5)

        # Buttons Frame
        self.frame_buttons = tk.Frame(root)
        self.frame_buttons.pack(pady=10)

        # Add Button
        self.button_add = tk.Button(self.frame_buttons, text="Add Password", command=self.add_password)
        self.button_add.grid(row=0, column=0, padx=5)

        # Edit Button
        self.button_edit = tk.Button(self.frame_buttons, text="Edit Password", command=self.edit_password)
        self.button_edit.grid(row=0, column=1, padx=5)

        # Delete Button
        self.button_delete = tk.Button(self.frame_buttons, text="Delete Password", command=self.delete_password)
        self.button_delete.grid(row=0, column=2, padx=5)

        # Listbox to Display Saved Passwords
        self.password_list = tk.Listbox(root, width=100, height=10)
        self.password_list.pack(pady=10)

        # Refresh Password List
        self.refresh_password_list()

    def add_password(self):
        """Add a new password to the database."""
        url = self.entry_url.get()
        name = self.entry_name.get()
        username = self.entry_username.get()
        site_password = self.entry_password.get()
        note = self.entry_note.get()

        if not url or not username or not site_password:
            messagebox.showerror("Error", "Please fill in all required fields (URL, Username, Site Password).")
            return

        # Encrypt the site password
        encrypted_password = encrypt_data(site_password)

        # Save to the database
        add_password(user_id=1, website=url, username=username, encrypted_password=encrypted_password)

        # Clear input fields
        self.clear_input_fields()

        # Refresh the password list
        self.refresh_password_list()
        messagebox.showinfo("Success", "Password added successfully!")

    def refresh_password_list(self):
        """Refresh the list of saved passwords."""
        self.password_list.delete(0, tk.END)
        passwords = get_passwords(user_id=1)
        for password_id, website, username, encrypted_password in passwords:
            decrypted_password = decrypt_data(encrypted_password)
            self.password_list.insert(tk.END, f"{password_id}: {website} | {username} | {decrypted_password}")


    def edit_password(self):
        """Edit an existing password."""
        selected_item = self.password_list.get(tk.ACTIVE)
        if not selected_item:
            messagebox.showerror("Error", "No password selected.")
            return

        # Extract password ID from the selected item
        password_id = int(selected_item.split(":")[0])

        # Retrieve current details from the database
        passwords = get_passwords(user_id=1)
        for pid, website, username, encrypted_password in passwords:
            if pid == password_id:
                decrypted_password = decrypt_data(encrypted_password)
                break

        # Populate input fields with current details
        self.entry_url.delete(0, tk.END)
        self.entry_url.insert(0, website)
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, "Name")  # Placeholder for now
        self.entry_username.delete(0, tk.END)
        self.entry_username.insert(0, username)
        self.entry_password.delete(0, tk.END)
        self.entry_password.insert(0, decrypted_password)
        self.entry_note.delete(0, tk.END)
        self.entry_note.insert(0, "Note")  # Placeholder for now

        # Update button functionality
        self.button_add.config(state=tk.DISABLED)
        self.button_edit.config(command=lambda: self.update_password(password_id))

    def update_password(self, password_id):
        """Update an existing password in the database."""
        url = self.entry_url.get()
        username = self.entry_username.get()
        site_password = self.entry_password.get()

        if not url or not username or not site_password:
            messagebox.showerror("Error", "Please fill in all required fields (URL, Username, Site Password).")
            return

        # Encrypt the updated site password
        encrypted_password = encrypt_data(site_password)

        # Update in the database
        update_password(password_id=password_id, website=url, username=username, encrypted_password=encrypted_password)

        # Clear input fields
        self.clear_input_fields()

        # Re-enable Add button and reset Edit button
        self.button_add.config(state=tk.NORMAL)
        self.button_edit.config(command=self.edit_password)

        # Refresh the password list
        self.refresh_password_list()
        messagebox.showinfo("Success", "Password updated successfully!")

    def delete_password(self):
        """Delete a selected password from the database."""
        selected_item = self.password_list.get(tk.ACTIVE)
        if not selected_item:
            messagebox.showerror("Error", "No password selected.")
            return

        # Extract password ID from the selected item
        password_id = int(selected_item.split(":")[0])

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this password?")
        if not confirm:
            return

        # Delete from the database
        delete_password(password_id=password_id)

        # Refresh the password list
        self.refresh_password_list()
        messagebox.showinfo("Success", "Password deleted successfully!")

    def clear_input_fields(self):
        """Clear all input fields."""
        self.entry_url.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_note.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardPage(root)
    root.mainloop()