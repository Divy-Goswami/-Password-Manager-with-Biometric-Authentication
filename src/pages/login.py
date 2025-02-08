import tkinter as tk
from tkinter import messagebox
from src.services.biometrics import capture_face
from src.services.mfa import verify_otp

SECRET_KEY = "JBSWY3DPEHPK3PXP"

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Password Manager")
        self.root.geometry("400x300")

        # Label and Button for Facial Recognition
        self.label_face = tk.Label(root, text="Click below to start facial recognition:")
        self.label_face.pack(pady=10)

        self.button_face = tk.Button(root, text="Start Facial Recognition", command=self.start_facial_recognition)
        self.button_face.pack(pady=10)

        # Label and Entry for OTP
        self.label_otp = tk.Label(root, text="Enter OTP:")
        self.label_otp.pack(pady=10)

        self.entry_otp = tk.Entry(root, show="*")
        self.entry_otp.pack(pady=5)

        self.button_login = tk.Button(root, text="Login", command=self.verify_login)
        self.button_login.pack(pady=10)

    def start_facial_recognition(self):
        captured_face = capture_face()
        messagebox.showinfo("Facial Recognition", "Face captured successfully.")
        # Simulate face matching
        stored_face = None  # Replace with actual stored face data
        if match_face(stored_face, captured_face):
            messagebox.showinfo("Success", "Facial recognition successful!")
        else:
            messagebox.showerror("Error", "Facial recognition failed.")

    def verify_login(self):
        otp = self.entry_otp.get()
        if verify_otp(SECRET_KEY, otp):
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid OTP. Please try again.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()