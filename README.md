Advanced Keylogger with Google Sheets Integration & Remote Control

📌 Project Overview

This is a Python-based keylogger designed for ethical hacking, penetration testing, and security research. The tool records keystrokes, clipboard data, and mouse activity, storing the logs in Google Sheets in real-time for remote monitoring. It also features stealth execution, automatic startup, and a remote stop command for controlled testing.

🚀 Features

✅ Real-time Keystroke Logging – Captures all keyboard inputs.
✅ Google Sheets Integration – Stores logs in the cloud for remote monitoring.
✅ Clipboard Monitoring – Tracks copied text.
✅ Mouse Click Logging – Records mouse interactions.
✅ Stealth Execution – Runs in the background without detection.
✅ Windows Persistence – Automatically starts on system boot.
✅ Remote Stop Command – Typing "STOPLOG" terminates the keylogger.
✅ Multi-threaded Architecture – Ensures smooth execution without blocking the system.

🔧 Technologies Used

Programming Language: Python 🐍

Libraries: pynput, gspread, oauth2client, pyperclip, logging, threading

Cloud Integration: Google Sheets API ☁️

System Utilities: os, ctypes, shutil

🛠️ Installation & Setup

1️⃣ Clone the Repository

git clone https://github.com/HHHARDIK/keylogger.git
cd keylogger-project

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Set Up Google Sheets API

Enable Google Sheets API in the Google Cloud Console.

Create a Service Account and download credentials.json.

Share your Google Sheet with the service account email.

4️⃣ Run the Keylogger

python keylogger.py

📜 Ethical Disclaimer

🚨 This tool is for educational and security research purposes only. Unauthorized use is illegal.

🔐 Use responsibly for penetration testing and ethical hacking. This project aims to help cybersecurity professionals understand attack vectors and improve defensive measures.

📌 Future Enhancements

🔒 AES Encryption for Logs

🌍 Remote Control via Web Interface

🎭 Enhanced Stealth Mode



