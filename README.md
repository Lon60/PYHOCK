# **PYHOCK**

<img src="Generally/LOGO_PYHOCK.jpg" alt="Logo" height="150">
PYHOCK is a file encryption and decryption program, written in Python, featuring a graphical user interface (GUI) that uses PyQt5.

## Features

- **File Encryption**: PYHOCK can encrypt any file on your system. You can provide a custom encryption key, or you can allow the program to automatically generate a strong, secure key for you.

- **File Decryption**: Once a file has been encrypted, PYHOCK can also decrypt it, provided the correct key is supplied. This feature can be used to access encrypted files or to reverse the encryption process if necessary.

- **Key Generation**: If you need a strong, secure key for encryption, PYHOCK can generate one for you with a single click. This key can then be used to encrypt or decrypt files.

- **User Interface Customization**: PYHOCK comes with both a light and a dark mode, so you can choose the one that is most comfortable for your eyes. Switching between modes is easy and instant.

- **Ease of Use**: With its simple and intuitive graphical user interface, PYHOCK is easy to use even for those who are not familiar with file encryption and decryption. Everything you need is just a few clicks away.


## Installation

Ensure you have Python 3 installed. If not, you can download and install it from [here](https://www.python.org/downloads/).

Download the ZIP file of this repository and extract it.

Install the required Python packages with the following command:

```bash
pip install pyqt5 qdarkstyle cryptography qtmodern
```
## Usage
Navigate to the directory containing the PYHOCK.py script and run the script with the following command:
```bash
python ./app/main.py
```
Choose the desired action from the "PYHOCK" dropdown menu: Encrypt, Decrypt, Generate Key, or Settings.

## Command Line Usage

For users who prefer operating from the terminal, PYHOCK also provides a command-line interface (CLI), which offers the same functionality as the GUI but in a scriptable format. This is particularly useful for automating tasks or integrating with other software solutions.

### Features

- **Automated Key Generation**: Generate encryption keys automatically with a command-line argument.
- **File Encryption**: Encrypt files quickly by specifying the file path and key directly in the command.
- **File Decryption**: Decrypt files easily using the command line by providing the file path and the correct decryption key.
- **Ease of Use**: Simplify repetitive tasks using scripts or integrate encryption and decryption into larger workflows.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT/).
