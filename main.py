import tkinter as tk
from tkinter import messagebox
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
import base64

class ChaCha20CipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ChaCha20 Cipher GUI")
        self.root.geometry("500x400")
        
        self.key = get_random_bytes(32)  # Generate a random 256-bit key
        
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.root, text="Enter Text:").pack(pady=5)
        self.input_text = tk.Text(self.root, height=5, width=50)
        self.input_text.pack(pady=5)
        
        self.encrypt_button = tk.Button(self.root, text="Encrypt", command=self.encrypt_text)
        self.encrypt_button.pack(pady=5)
        
        self.decrypt_button = tk.Button(self.root, text="Decrypt", command=self.decrypt_text)
        self.decrypt_button.pack(pady=5)
        
        tk.Label(self.root, text="Output:").pack(pady=5)
        self.output_text = tk.Text(self.root, height=5, width=50)
        self.output_text.pack(pady=5)
    
    def encrypt_text(self):
        plaintext = self.input_text.get("1.0", tk.END).strip()
        if not plaintext:
            messagebox.showerror("Error", "Please enter text to encrypt.")
            return
        
        cipher = ChaCha20.new(key=self.key)
        ciphertext = cipher.encrypt(plaintext.encode())
        nonce = cipher.nonce
        
        encrypted_data = base64.b64encode(nonce + ciphertext).decode()
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, encrypted_data)
    
    def decrypt_text(self):
        encrypted_data = self.input_text.get("1.0", tk.END).strip()
        if not encrypted_data:
            messagebox.showerror("Error", "Please enter text to decrypt.")
            return
        
        try:
            encrypted_data = base64.b64decode(encrypted_data)
            nonce, ciphertext = encrypted_data[:8], encrypted_data[8:]
            cipher = ChaCha20.new(key=self.key, nonce=nonce)
            decrypted_text = cipher.decrypt(ciphertext).decode()
            
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, decrypted_text)
        except Exception as e:
            messagebox.showerror("Error", "Decryption failed: " + str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ChaCha20CipherApp(root)
    root.mainloop()
