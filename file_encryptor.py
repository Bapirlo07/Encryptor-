import os
from tkinter import Tk, Label, Button, filedialog, messagebox
from cryptography.fernet import Fernet

# Step 1: Generate and Save Key
# This function generates a new encryption key and saves it to a file.
def generate_key():
    key = Fernet.generate_key()
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)
    messagebox.showinfo("Key Generated", "A new key has been generated and saved as 'encryption_key.key'.")

# Step 2: Load the Key
# This function loads the encryption key from a file.
def load_key():
    try:
        with open("encryption_key.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        messagebox.showerror("Error", "Key file not found. Please generate a key first.")
        return None

# Step 3: Encrypt File
# This function encrypts a selected file using the loaded key.
def encrypt_file():
    key = load_key()
    if not key:
        return

    file_path = filedialog.askopenfilename(title="Select a File to Encrypt")
    if file_path:
        try:
            with open(file_path, "rb") as file:
                data = file.read()
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(data)

            encrypted_file_path = file_path + ".encrypted"
            with open(encrypted_file_path, "wb") as encrypted_file:
                encrypted_file.write(encrypted_data)

            messagebox.showinfo("Success", f"File encrypted successfully!\nSaved as: {encrypted_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Step 4: Decrypt File
# This function decrypts a selected file using the loaded key.
def decrypt_file():
    key = load_key()
    if not key:
        return

    file_path = filedialog.askopenfilename(title="Select a File to Decrypt")
    if file_path:
        try:
            with open(file_path, "rb") as file:
                encrypted_data = file.read()
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)

            decrypted_file_path = os.path.splitext(file_path)[0]
            with open(decrypted_file_path, "wb") as decrypted_file:
                decrypted_file.write(decrypted_data)

            messagebox.showinfo("Success", f"File decrypted successfully!\nSaved as: {decrypted_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Step 5: Create GUI
# This function creates the GUI for the application.
def create_app():
    root = Tk()
    root.title("File Encryptor & Decryptor")
    root.geometry("400x300")

    Label(root, text="File Encryptor & Decryptor", font=("Arial", 16)).pack(pady=10)

    Button(root, text="Generate Key", command=generate_key, width=20, bg="lightblue").pack(pady=10)
    Button(root, text="Encrypt File", command=encrypt_file, width=20, bg="lightgreen").pack(pady=10)
    Button(root, text="Decrypt File", command=decrypt_file, width=20, bg="lightcoral").pack(pady=10)

    Label(root, text="Ensure the key file is secure.", fg="red").pack(pady=20)

    root.mainloop()

# Entry point of the application
if __name__ == "__main__":
    create_app()
