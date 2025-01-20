import time
from pypresence import Presence, InvalidID
import os
import json
import atexit
import tkinter as tk
from tkinter import messagebox, simpledialog

# var Default Settings
client_id = '1330216270477525053'
details = "In a conversation with someone"
state = "Working on something cool!"
party_size = [1, 4]
party_enabled = False
start_time = time.time()
rpc_enabled = True
by = "github.com/Tamino1230"

# var Other Settings
config_file = 'rpc_config.json'
rpc = None
first_time = True

atexit.register(lambda: rpc.close() if rpc and rpc_enabled else None)

#- Loads the configuration
def load_config():
    global client_id, details, state, party_size, party_enabled, rpc_enabled
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
            client_id = config.get("client_id", client_id)
            details = config.get("details", details)
            state = config.get("state", state)
            party_size = config.get("party_size", party_size)
            party_enabled = config.get("party_enabled", party_enabled)
            rpc_enabled = config.get("rpc_enabled", rpc_enabled)
    except FileNotFoundError:
        pass

#- Saves the configuration
def save_config():
    config = {
        "client_id": client_id,
        "details": details,
        "state": state,
        "party_size": party_size,
        "party_enabled": party_enabled,
        "rpc_enabled": rpc_enabled
    }
    with open(config_file, 'w') as file:
        json.dump(config, file)

#- Checks if the Client ID inputed works!
def check_client_id(client_id):
    try:
        test_rpc = Presence(client_id)
        test_rpc.connect()
        messagebox.showinfo("Success", f"Client ID {client_id} is available.")
        test_rpc.close()
        return True
    except InvalidID:
        messagebox.showwarning("Error", f"Client ID {client_id} is not valid.")
        return False
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return False

#- Uses the data from the Menu
def update_rpc():
    global rpc, details, state, start_time, party_size, party_enabled, rpc_enabled
    if not rpc_enabled:
        messagebox.showinfo("Info", "RPC is disabled.")
        return
    
    rpc_args = {
        "details": details,
        "state": state,
        "start": start_time,
        "large_image": "large_image_key",
        "large_text": "Your large image tooltip text",
        "small_image": "small_image_key",
        "small_text": "Your small image tooltip text"
    }
    if party_enabled:
        rpc_args.update({"party_id": "1234", "party_size": party_size})
    
    rpc.update(**rpc_args)

def start_rpc():
    global rpc
    rpc = Presence(client_id)
    rpc.connect()
    update_rpc()
    update_preview()  # Das war der Fehler, da das Label noch nicht definiert war
    update_preview()  # Dies verschiebe ich nun auf später

#- GUI Functions
def update_client_id():
    global client_id
    new_client_id = simpledialog.askstring("Input", "Input Client ID (numbers only): ")
    if new_client_id and check_client_id(new_client_id):
        rpc.close()
        client_id = new_client_id
        start_rpc()

def update_details():
    global details
    details = simpledialog.askstring("Input", "Input Details: ")
    update_rpc()

def update_state():
    global state
    state = simpledialog.askstring("Input", "Input State: ")
    update_rpc()

def update_party_size():
    global party_size
    current_party_size = simpledialog.askinteger("Input", "Input current party size: ")
    max_party_size = simpledialog.askinteger("Input", "Input max party size: ")
    if current_party_size and max_party_size and max_party_size >= current_party_size:
        party_size = [current_party_size, max_party_size]
        update_rpc()

def toggle_party_visibility():
    global party_enabled
    party_enabled = not party_enabled
    update_rpc()
    messagebox.showinfo("Info", f"Party visibility {'enabled' if party_enabled else 'disabled'}.")

def restart_rpc():
    global rpc
    rpc.close()
    start_rpc()
    
def toggle_rpc_enabled():
    global rpc_enabled, rpc
    rpc_enabled = not rpc_enabled
    if rpc_enabled:
        start_rpc()
        messagebox.showinfo("Info", "RPC enabled.")
    else:
        rpc.close()
        messagebox.showinfo("Info", "RPC disabled.")

def save_settings():
    save_config()
    messagebox.showinfo("Info", "Settings saved.")

def update_preview():
    preview = f"Details: {details}\nState: {state}\nParty Size: {party_size}\nRPC Enabled: {rpc_enabled}"
    preview_label.config(text=preview)

#- User to Start the Program
if __name__ == "__main__":
    load_config()

    root = tk.Tk()
    root.title("Custom DRPC - @tamino1230")
    root.iconbitmap("icon/babToma.ico")

    tk.Button(root, text="Change Client ID", command=update_client_id).grid(row=0, column=0, padx=10, pady=5)
    tk.Button(root, text="Change Details", command=update_details).grid(row=1, column=0, padx=10, pady=5)
    tk.Button(root, text="Change State", command=update_state).grid(row=2, column=0, padx=10, pady=5)
    tk.Button(root, text="Change Party Size", command=update_party_size).grid(row=3, column=0, padx=10, pady=5)
    tk.Button(root, text="Toggle Party Visibility", command=toggle_party_visibility).grid(row=4, column=0, padx=10, pady=5)
    tk.Button(root, text="Restart RPC", command=restart_rpc).grid(row=5, column=0, padx=10, pady=5)
    tk.Button(root, text="Toggle RPC", command=toggle_rpc_enabled).grid(row=6, column=0, padx=10, pady=5)
    tk.Button(root, text="Save Settings", command=save_settings).grid(row=7, column=0, padx=10, pady=5)

    preview_label = tk.Label(root, text="", justify=tk.LEFT)
    preview_label.grid(row=0, column=1, rowspan=8, padx=10, pady=5, sticky=tk.N)

    start_rpc() # Der start_rpc-Aufruf kommt nun hierher, nachdem preview_label definiert ist
    
    root.mainloop()
