import os
import smtplib
import ssl
import base64
from cryptography.fernet import Fernet
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
from PIL import Image, ImageTk

class PyhockApp:
    def __init__(self):
        self.key = None
        self.cipher_suite = None
        self.key_generated = False
        self.encrypt_frame = None

        self.root = tk.Tk()
        self.root.title("PYHOCK")
        self.root.geometry("400x250")
        self.root.resizable(False, False)

        self.menu_pyhock = tk.Menu(self.root)
        self.root.config(menu=self.menu_pyhock)

        self.menu_dropdown = tk.Menu(self.menu_pyhock, tearoff=0)
        self.menu_dropdown.add_command(label="Encrypt", command=self.show_main_menu)
        self.menu_dropdown.add_command(label="Decrypt", command=self.show_decrypt)  # Hinzugefügt!
        self.menu_dropdown.add_command(label="Key Generator", command=self.show_key_generator)
        self.menu_dropdown.add_command(label="Settings", command=self.show_settings)

        self.menu_pyhock.add_cascade(label="PYHOCK", menu=self.menu_dropdown)

        self.main_menu_frame = tk.Frame(self.root)
        self.main_menu_frame.pack()

        self.key_generator_frame = tk.Frame(self.root)
        self.settings_frame = tk.Frame(self.root)
        self.decrypt_frame = tk.Frame(self.root)  


        self.label_email = tk.Label(self.main_menu_frame, text="Email Address for Key Delivery:")
        self.entry_email = tk.Entry(self.main_menu_frame, width=50)
        self.label_instructions = tk.Label(self.main_menu_frame, text="File Path for Encryption:")
        self.entry_path = tk.Entry(self.main_menu_frame, width=50)
        self.button_explore = tk.Button(self.main_menu_frame, text="...", command=self.select_file)

        self.key_auto_generate = tk.BooleanVar()
        self.key_auto_generate.set(True)

        self.label_settings = tk.Label(self.settings_frame, text="Settings")
        self.hide_settings()

        self.checkbox_auto_generate = tk.Checkbutton(self.main_menu_frame, text="Auto-generate Key",
                                                     variable=self.key_auto_generate, command=self.toggle_key_entry)
        self.label_key = tk.Label(self.main_menu_frame, text="Custom Key:")
        self.entry_key = tk.Entry(self.main_menu_frame, width=50, state="disabled")

        self.button_encrypt = tk.Button(self.main_menu_frame, text="Encrypt and Send Key",
                                        command=self.proceed_with_custom_key)

        self.x = self.y = 0

        self.label_email.pack(pady=5)
        self.entry_email.pack(pady=5)
        self.label_instructions.pack(pady=5)
        self.entry_path.pack(pady=5)
        self.button_explore.pack(side=tk.RIGHT, padx=10, pady=5)
        self.checkbox_auto_generate.pack(pady=5)
        self.label_key.pack(pady=5)
        self.entry_key.pack(pady=5)
        self.button_encrypt.pack(pady=10)

        self.label_instructions.bind("<ButtonPress-1>", self.on_left_click)
        self.label_instructions.bind("<B1-Motion>", self.move_window)

        self.label_key_generator = tk.Label(self.key_generator_frame, text="Generated Key:")
        self.label_generated_key = tk.Label(self.key_generator_frame, text="")
        self.button_generate_key = tk.Button(self.key_generator_frame, text="Generate Key", command=self.generate_key)

        self.copy_button = tk.Button(self.key_generator_frame, text="Copy", command=self.copy_key_to_clipboard)
        self.label_key_generator.pack(pady=5)
        self.label_generated_key.pack(pady=5)
        self.button_generate_key.pack(pady=10)

        self.copy_button.pack_forget()

        self.root.mainloop()


    def show_decrypt(self):
        self.decrypt_frame.pack_forget()
        self.main_menu_frame.pack_forget()
        self.key_generator_frame.pack_forget()
        self.settings_frame.pack_forget()

        self.decrypt_frame = tk.Frame(self.root)
        self.decrypt_frame.pack()

        self.label_decrypt_key = tk.Label(self.decrypt_frame, text="Decryption Key:")
        self.entry_decrypt_key = tk.Entry(self.decrypt_frame, width=50, show="*")
        self.label_decryption_instructions = tk.Label(self.decrypt_frame, text="File Path for Decryption:")
        self.entry_decryption_path = tk.Entry(self.decrypt_frame, width=50)
        self.button_explore_decryption = tk.Button(self.decrypt_frame, text="...", command=self.select_decryption_file)
        self.button_decrypt = tk.Button(self.decrypt_frame, text="Decrypt", command=self.proceed_with_decryption)

        self.label_decrypt_key.pack(pady=5)
        self.entry_decrypt_key.pack(pady=5)
        self.label_decryption_instructions.pack(pady=5)
        self.entry_decryption_path.pack(pady=5)
        self.button_explore_decryption.pack(side=tk.RIGHT, padx=10, pady=5)
        self.button_decrypt.pack(pady=10)

    def hide_decrypt(self):
        self.decrypt_frame.pack_forget()


    def select_decryption_file(self):
        file_path = filedialog.askopenfilename()
        self.entry_decryption_path.delete(0, tk.END)
        self.entry_decryption_path.insert(0, file_path)

    def proceed_with_decryption(self):
        decryption_key = self.entry_decrypt_key.get()
        if decryption_key:
            try:
                self.key = decryption_key.encode()
                self.cipher_suite = Fernet(self.key)
                self.decrypt_file(self.entry_decryption_path.get(), self.cipher_suite)
                messagebox.showinfo("Decryption Successful", "File decrypted successfully!")
            except Exception as e:
                messagebox.showerror("Decryption Error", f"Error while decrypting the file: {e}")
        else:
            messagebox.showerror("Invalid Key", "Please enter a valid decryption key.")

    def decrypt_file(self, file_path, cipher_suite):
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        
            with open(file_path, 'r+b') as file:
                decrypted_data = cipher_suite.decrypt(file.read())
                file.seek(0)
                file.write(decrypted_data)
        except Exception as e:
            raise e


    def show_settings(self):
        self.hide_main_menu()
        self.hide_key_generator()
        self.hide_decrypt()
        self.settings_frame.pack()

    def hide_settings(self):
        self.settings_frame.pack_forget()

    def show_dropdown_menu(self, event):
        if not self.dropdown_visible:
            self.menu_pyhock.post(event.x_root, event.y_root)
            self.dropdown_visible = True

    def hide_dropdown_menu(self, event):
        if self.dropdown_visible:
            self.menu_pyhock.unpost()
            self.dropdown_visible = False

    def copy_key_to_clipboard(self):
        if self.key:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.key.decode())
            self.root.update()

    def generate_key(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.label_generated_key.config(text=self.key.decode())

        self.copy_button.pack(side=tk.RIGHT)
        self.key_generated = True

    def hide_key_generator(self):
        self.key_generator_frame.pack_forget()

    def show_main_menu(self):
        self.main_menu_frame.pack()
        self.key_generator_frame.pack_forget()
        self.hide_decrypt()

    def show_key_generator(self):
        self.key_generator_frame.pack()
        self.main_menu_frame.pack_forget()
        self.hide_decrypt()

    def hide_main_menu(self):
        self.main_menu_frame.pack_forget()
        self.key_generator_frame.pack_forget()

    def toggle_key_entry(self):
        if self.key_auto_generate.get():
            self.entry_key.config(state="disabled")
        else:
            self.entry_key.config(state="normal")

    def select_file(self):
        file_path = filedialog.askopenfilename()
        self.entry_path.delete(0, tk.END)
        self.entry_path.insert(0, file_path)

    def show_warning(self):
        email = self.entry_email.get()
        if not email:
            return

        confirmation_window = tk.Toplevel(self.root)
        confirmation_window.title("Confirmation")
        confirmation_window.geometry("350x200")
        confirmation_window.resizable(False, False)

        warning_label = tk.Label(confirmation_window, text="Please confirm the email address.\n"
                                                           "If the email address is incorrect, the files will be lost.",
                                 wraplength=300, justify="center")
        warning_label.pack(pady=15)

        email_label = tk.Label(confirmation_window, text=f"E-mail Address: {email}", wraplength=300, justify="center")
        email_label.pack(pady=5)

        def proceed():
            confirmation_window.destroy()
            self.encrypt_file(self.entry_path.get(), self.cipher_suite)
            self.send_key(self.key, email)

        def cancel():
            confirmation_window.destroy()

        proceed_button = tk.Button(confirmation_window, text="Yes, continue", command=proceed)
        proceed_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(confirmation_window, text="Cancel", command=cancel)
        cancel_button.pack(side=tk.RIGHT, padx=10)

    def send_key(self, key, receiver_email):
        sender_email = "pyhock000@gmail.com"
        subject = "PYHOCK - Encryption Key"
        message = f"Here is the generated key: {key.decode()}"

        email = MIMEMultipart()
        email["From"] = sender_email
        email["To"] = receiver_email
        email["Subject"] = subject
        email.attach(MIMEText(message, "plain"))

        script_dir = os.path.dirname(os.path.abspath(__file__))
        credentials_file = os.path.join(script_dir, "pyhock-8efe0c1bdb0f.json")

        credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=["https://www.googleapis.com/auth/gmail.send"])
        credentials = credentials.with_subject(sender_email)
        if credentials.expired:
            credentials.refresh(Request())

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=ssl.create_default_context())
            password = "etzjacsrytqlsfmo"
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, email.as_string())

    def encrypt_file(self, file_path, cipher_suite):
        try:
            with open(file_path, 'r+b') as file:
                encrypted_data = cipher_suite.encrypt(file.read())
                file.seek(0)
                file.write(encrypted_data)
        except Exception as e:
            print(f"Error while encrypting the file: {file_path}: {e}")

    def proceed_with_custom_key(self):
        if not self.key_auto_generate.get():
            custom_key = self.entry_key.get()
            if custom_key:
                try:
                    self.key = custom_key.encode()
                    self.cipher_suite = Fernet(self.key)
                    self.show_warning()
                except ValueError:
                    messagebox.showerror("Invalid key", "Please enter a valid custom key.")
            else:
                messagebox.showerror("Invalid key", "Please enter a valid custom key.")
        else:
            if not self.key_generated:
                self.generate_key()
            self.cipher_suite = Fernet(self.key)
            self.show_warning()

    def move_window(self, event):
        self.root.geometry(f"+{self.root.winfo_pointerx() - self.x}+{self.root.winfo_pointery() - self.y}")

    def on_left_click(self, event):
        self.x, self.y = event.x, event.y

if __name__ == "__main__":
    app = PyhockApp()
