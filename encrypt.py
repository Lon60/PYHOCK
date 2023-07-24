import os
import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog
from cryptography.fernet import Fernet

def decrypt_files(key):
    cipher_suite = Fernet(key)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(current_dir):
        file_path = os.path.join(current_dir, filename)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r+b') as file:
                    encrypted_data = file.read()
                    decrypted_data = cipher_suite.decrypt(encrypted_data)
                    file.seek(0)
                    file.write(decrypted_data)
                    file.truncate()
            except:
                print(f"Fehler beim Entschlüsseln der Datei: {filename}")
        else:
            print(f"Datei {filename} nicht gefunden.")

def get_decryption_key():
    root = tk.Tk()
    root.withdraw()
    key = simpledialog.askstring("Entschlüsselungsschlüssel", "Geben Sie den Entschlüsselungsschlüssel ein:")
    root.destroy()
    return key.encode()

if __name__ == "__main__":
    key = get_decryption_key()
    if key:
        decrypt_files(key)
        messagebox.showinfo("Entschlüsselung abgeschlossen", "Die Dateien wurden erfolgreich entschlüsselt.")
    else:
        messagebox.showinfo("Entschlüsselung abgebrochen", "Der Entschlüsselungsvorgang wurde abgebrochen.")
