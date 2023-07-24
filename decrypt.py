import os
import smtplib
import ssl
from cryptography.fernet import Fernet
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import tkinter as tk
from tkinter import filedialog

icon_path = "decrypt_ico.ico"

def send_key(key, receiver_email):
    sender_email = "pyhock000@gmail.com"
    subject = "Verschlüsselungsschlüssel"
    message = f"Hier ist der generierte Schlüssel: {key.decode()}"

    # Erstelle eine E-Mail-Nachricht
    email = MIMEMultipart()
    email["From"] = sender_email
    email["To"] = receiver_email
    email["Subject"] = subject
    email.attach(MIMEText(message, "plain"))

    # Bestimme den Pfad zur JSON-Datei relativ zum Skript
    script_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_file = os.path.join(script_dir, "pyhock-8efe0c1bdb0f.json")

    # Verbinde dich mit dem SMTP-Server von Gmail mit OAuth 2.0-Authentifizierung
    credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=["https://www.googleapis.com/auth/gmail.send"])
    credentials = credentials.with_subject(sender_email)
    if credentials.expired:
        credentials.refresh(Request())

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls(context=ssl.create_default_context())
        password = "etzjacsrytqlsfmo"  # Hier das Gmail-Passwort des sendenden Kontos angeben
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, email.as_string())

def generate_key():
    key = Fernet.generate_key()
    return key

def encrypt_file(file_path, cipher_suite):
    try:
        with open(file_path, 'r+b') as file:
            encrypted_data = cipher_suite.encrypt(file.read())
            file.seek(0)
            file.write(encrypted_data)
    except:
        print(f"Fehler beim Verschlüsseln der Datei: {file_path}")

def encrypt_files(key):
    cipher_suite = Fernet(key)

    def select_file():
        root.filename = filedialog.askopenfilename()
        entry_path.delete(0, tk.END)
        entry_path.insert(0, root.filename)

    root = tk.Tk()
    root.title("Datei-Verschlüsselung")
    root.geometry("400x200")
    root.resizable(False, False)  # Fenstergröße nicht änderbar
    root.overrideredirect(False)  # Standard-Titelleiste des Fensters anzeigen

    label_email = tk.Label(root, text="E-Mail-Adresse für den Schlüsselversand:")
    label_email.pack(pady=5)

    entry_email = tk.Entry(root, width=50)
    entry_email.pack(pady=5)

    label_instructions = tk.Label(root, text="Dateipfad für Verschlüsselung:")
    label_instructions.pack(pady=5)

    entry_path = tk.Entry(root, width=50)
    entry_path.pack(pady=5)

    button_explore = tk.Button(root, text="...", command=select_file)
    button_explore.pack(side=tk.RIGHT, padx=10, pady=5)

    def encrypt_and_send():
        file_path = entry_path.get()
        email = entry_email.get()
        if file_path and email:
            encrypt_file(file_path, cipher_suite)
            send_key(key, email)
            root.quit()  # Schließe das Tkinter-Fenster, nachdem die Datei verschlüsselt und der Schlüssel versendet wurde

    button_encrypt = tk.Button(root, text="Verschlüsseln und Schlüssel senden", command=encrypt_and_send)
    button_encrypt.pack(pady=10)

    x = y = 0

    def move_window(event):
        root.geometry(f"+{event.x_root - x}+{event.y_root - y}")

    def on_left_click(event):
        nonlocal x, y
        x, y = event.x, event.y

    label_instructions.bind("<ButtonPress-1>", on_left_click)
    label_instructions.bind("<B1-Motion>", move_window)

    root.mainloop()

if __name__ == "__main__":
    # Erstelle ein Dummy-Fenster, um das Tkinter-Fenster zu verstecken
    hide_root = tk.Tk()
    hide_root.attributes("-alpha", 0.0)  # Fenster unsichtbar machen
    hide_root.withdraw()  # Fenster verstecken

    key = generate_key()
    encrypt_files(key)
    print(key)
