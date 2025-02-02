
# import online
import time
from pypresence import Presence, InvalidID
import os
import json
import pyperclip

# import files
import config as c

# var Default Settings
client_id = '1330216270477525053'
details = "In a conversation with someone"
state = "Working on something cool!"
party_size = [1, 4]
party_enabled = False
start_time = time.time()
rpc_enabled = True
by = "github.com/Tamino1230"
discord_server = "https://discord.gg/vpApZSjh3H"

# var Other Settings
config_file = c.config_file
rpc = None
first_time = True

#- Reconnecting
def reconnect():
    first_connect = True
    counti = 0
    while True:
        try:
            rpc = Presence(client_id)
            rpc.connect()
            set_rpc()
            print("Successfully connected!")
            break
        except Exception as e:
            counti += 1
            if first_connect:
                print(f"Try connecting: {counti}\nAn Error Accured: \"{e}\"")
            else:
                print(f"Tried reconnect: {counti}\nAn Error Accured: \"{e}\"")
            time.sleep(2)
            print("Trying to reconnect..")
            time.sleep(1)
            clear_console()
            continue

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


def print_files(filetype=".json", verzeichnis=os.getcwd()):
    #- finds all files in folder
    print("\nYour saves:")
    count = 0
    for datei in os.listdir(verzeichnis):
        if datei.endswith(filetype):
            count += 1
            print(f"Save {count}: {datei}")
    print("")


#- changes the config file while beeing in the program
def change_config():
    clear_console()
    print_files()
    global config_file
    old_config = config_file
    while True:
        new_conf = safe_input(str, "Which File do you want to load? (xxx.json): ", "Useless Errormessage")
        if new_conf == "main.py" or new_conf == "main.bat" or new_conf == "README.md" or new_conf == "LICENSE":
            print("You cant load a main File! only \".json\"!")
            continue
        elif not ".json" in new_conf:
            print("You can only load \".json\" files!")
            continue
        if os.path.exists(new_conf):
            print(f"Load File \"{new_conf}\" exist!")
            break
        else:
            print(f"File \"{new_conf}\" doesnt exist!")
            continue
    try:
        config_file = new_conf
        print("Trying to connect to new..")
        rpc.close()
        load_config()
        print("Sucessfully connected to new!")
    except Exception as e:
        print("Error accured", e)
        config_file = old_config
        try:
            print("Reconnecting old..")
            load_config()
        except Exception as e:
            print("An error Accured", e)

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

#- Clears the console
def clear_console():
    os.system('cls')

#- Gets a Safe Input from the User
def safe_input(datentype, prompt, error_message):
    while True:
        try:
            text = input(prompt)
            value = datentype(text)
            return value
        except ValueError:
            print(f"{error_message} \"{text}\"")
            continue


#- Checks if the Client ID inputed works!
def check_client_id(client_id):
    try:
        test_rpc = Presence(client_id)
        test_rpc.connect()
        print(f"Client ID {client_id} is available.")
        test_rpc.close()
        return True
    except InvalidID:
        print(f"Client ID {client_id} is not valid.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


#- Their getting the clientid, details, state, and etc
def get_client_id():
    return safe_input(str, "Input Client ID (numbers only): ", "You can only input numbers and not")

def get_details():
    return safe_input(str, "Input Details: ", "Invalid input")

def get_state():
    return safe_input(str, "Input State: ", "Invalid input")

def check_tuple_greater_than(tup, num):
    return all(element > num for element in tup)

def get_party_size():
    while True:
        current_party_size = safe_input(int, "Input current party size: ", "You can only input numbers and not")
        if current_party_size > 0:
            break
        else:
            print("You need to put at least 1 Party member!")

    while True:
        max_party_size = safe_input(int, "Input max party size: ", "You can only input numbers and not")
        if max_party_size >= current_party_size:
            break
        else:
            print(f"You need to input a number higher than or equal to \"{current_party_size}\"")

    return [
        current_party_size,
        max_party_size
    ]

#- Draws the Menu and lets the User pick an option
def draw_menu():
    global first_time
    av = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
    if first_time != False:
        print(f"\nCustom Discord RPC is running! 🎉\nJoin my Discord Server! Also if you got any problems:\n{discord_server}\nCurrent Save-/Active File: {config_file}")
        with open(config_file, 'r') as file:
                    summary = file.read()
        print(f"\nPreview Save File:\n\"{summary}\" (Save to Update)\n")
        first_time = False
    else:
        with open(config_file, 'r') as file:
                    summary = file.read()
        print(f"\nPreview Save File:\n\"{summary}\" (Save to Update)\n")
        print(f"\nCustom Discord RPC is running updated! 🎉\nCurrent: {config_file}")
    print("Menu:\n"
          "   1) Change Client ID (when doing that all your settings will reset to the last saved)\n"
          "   2) Change Details\n"
          "   3) Change State\n"
          "   4) Change Party\n"
          "   5) Toggle Party Visibility\n"
          "   6) Restart\n"
          "   7) Save Settings\n"
          "   8) Toggle RPC\n"
          "   9) Change current Save File\n"
          "  10) New Save File\n"
          "  11) Change Start-Up File (File which automaticly opens)\n"
          "  12) Copy Filedata to Clipboard\n\n"
          "You can Ignore Errors in the console if it didnt work change the Settings again.\nThe Program is rather slow.\n"
          f"by {sdaafasfasfgg}\n")
    while True:
        value = safe_input(int, f"Choose an Option ({av[0]}-{av[-1]}): ", f"You can only input numbers ({av[0]}-{av[-1]}) and not")
        if value in av:
            return value
        else:
            print(f"You can only input numbers ({av[0]}-{av[-1]}) and not \"{value}\"!")

#- Sets the RPC directly
def set_rpc():
    global sdaafasfasfgg
    global sdaafasfasfg1
    global rpc
    sdaafasfasfg1 = discord_server
    if not rpc_enabled:
        print("RPC is disabled.")
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
    sdaafasfasfgg = by
    if party_enabled:
        rpc_args.update({"party_id": "1234", "party_size": party_size})
    rpc.update(**rpc_args)

def create_file(filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('{"client_id": "1330216270477525053", "details": "In a conversation with someone", "state": "Working on something cool!", "party_size": [1, 4], "party_enabled": false, "rpc_enabled": true}')

    print(f"Savefile: \"{filename}\" was created with default settings!")

def newSave():
    clear_console()
    while True:
        file_name = safe_input(str, "What do you want to name the new safe file? (xxx.json) (write cancel to cancel): ", "useless error")
        file_name = file_name.lower()
        if " " in file_name:
            print("Spaces are getting deleted to avoid Errors!")
        file_name = file_name.replace(" ", "")
        if file_name == "cancel":
            break
        else:
            if ".json" not in file_name:
                print(f"You can only save in \".json\" Files and not \"{file_name}\"!")
                continue
            elif os.path.exists(file_name):
                print(f"You cant create two saves with the same name! \"{file_name}\"")
                continue
            else:
                create_file(file_name)
                break

def get_file_data():
    clear_console()
    print_files(".json")
    while True:
        file_name = safe_input(str, "Which File do you want to copy/share? (xxx.json): ", "Useless Error: Lara Gay1")
        if not ".json" in file_name:
            print("You can only read out .json Files!")
            continue
        elif not os.path.exists(file_name):
            print(f"File \"{file_name}\" doesnt exist!")
            continue
        elif os.path.exists(file_name):
            print("Reading Data..")
            time.sleep(1)
            print(f"Trying to get FileData of {file_name}")
            try:
                with open(file_name, 'r') as file:
                    summary = file.read()
            except Exception as e:
                print(f"An Error Accured while Opening File: \"{e}\"")
                continue
            try:
                print("Trying to copy on clipboard")
                pyperclip.copy(summary)
                time.sleep(1)
                print("Sucessfully copied to Clipboard!")
                print(f"\nPreview:\n{summary}")
                break

            except Exception as e:
                print(f"An Error Accured while Copying: \"{e}\"")

        else:
            print("An error Accured?")
    

def change_startup():
    clear_console()
    print_files(".json")
    while True:
        value = safe_input(str, "Choose the file you want to put as Start-up: (cancel to cancel): ", "useless :3 (jamie is a femboy!)")
        if value == "cancel":
            break
        elif not ".json" in value:
            print("You can only put \".json\" files!")
            continue
        elif os.path.exists(value):
            with open('config.py', 'w') as file:
                file.write(f"config_file = '{value}'\n")
                file.write("#- file where the settings will be saved / which saved config")
            print(f"Successfully set \"{value}\" as the Startup file!")
            break
        elif not os.path.exists(value):
            print(f"File \"{value}\" doesnt exist!")
        else:
            print("An error accured!")
            continue  


#- Uses the data from the Menu
def value_use():
    global client_id, details, state, party_size, party_enabled, rpc_enabled, rpc
    while True:
        menu_input = draw_menu()
        match menu_input:
            case 1:
                if rpc:
                    rpc.close()
                new_client_id = get_client_id()
                if check_client_id(new_client_id):
                    rpc = Presence(new_client_id)
                    clear_console()
                    print("Connecting new..")
                    try:
                        rpc.connect()
                        set_rpc()
                    except Exception as e:
                        print(f"\"{e}\"")
                        reconnect()
                    print("Successfully connected..\n")
                else:
                    clear_console()
                    print("Invalid Client ID")
                    print("Reconnection old Client ID..")
                    rpc = Presence(client_id)
                    try:
                        rpc.connect()
                        set_rpc()
                    except Exception as e:
                        print(f"\"{e}\"")
                        reconnect()
                    print("Reconnected to old..\n")
            case 2:
                clear_console()
                try:
                    details = get_details()
                    set_rpc()
                except Exception as e:
                    print(f"\"{e}\"")
                    reconnect()
                print("Changed details successfully..\n")
            case 3:
                clear_console()
                try:
                    state = get_state()
                    set_rpc()
                except Exception as e:
                    print(f"\"{e}\"")
                    reconnect()
                print("Changed state successfully..\n")
            case 4:
                clear_console()
                try:
                    party_size = get_party_size()
                    set_rpc()
                except Exception as e:
                    print(f"\"{e}\"")
                    reconnect()
                print("Changed party size successfully..\n")
            case 5:
                party_enabled = not party_enabled
                try:
                    set_rpc()
                except Exception as e:
                    print(f"\"{e}\"")
                    reconnect()
                clear_console()
                print(f"Party visibility {'enabled' if party_enabled else 'disabled'}.")
                time.sleep(1.5)
            case 6:
                clear_console()
                if rpc:
                    try:
                        rpc.close()
                    except Exception as e:
                        print(f"\"{e}\"")
                        exit()
                    print("Restarting..")
                time.sleep(1)
                rpc = Presence(client_id)
                print("Reconnecting..")
                try:
                    rpc.connect()
                    set_rpc()
                except Exception as e:
                    print(f"\"{e}\"")
                    reconnect()
                time.sleep(1.5)
            case 7:
                clear_console()
                save_config()
                print(f"Settings saved of File: \"{config_file}\".")
                time.sleep(1.5)
            case 8:
                rpc_enabled = not rpc_enabled
                if rpc_enabled:
                    try:
                        clear_console()
                        rpc.connect()
                        set_rpc()
                    except Exception as e:
                        print(f"\"{e}\"")
                        reconnect()
                    print("RPC enabled.")
                    time.sleep(1.5)
                else:
                    try:
                        clear_console()
                        rpc.close()
                        print("RPC disabled.")
                    except Exception as e:
                        print(f"\"{e}\"")
                        exit()
                    time.sleep(1.5)
            case 9:
                change_config()
                try:
                    rpc = Presence(client_id)
                    rpc.connect()
                    set_rpc()
                except Exception as e:
                    print(f"\"{e}\"")
                time.sleep(1.5)
            case 10:
                newSave()
                time.sleep(1.5)
            case 11:
                change_startup()
                time.sleep(1.5)
            case 12:
                get_file_data()
                time.sleep(1.5)


#- User to Start the Program
if __name__ == "__main__":
    counti = 0
    load_config()
    while True:
        try:
            rpc = Presence(client_id)
            rpc.connect()
            set_rpc()
            print("Successfully connected!")
            break
        except Exception as e:
            counti += 1
            print(f"Tried reconnect: {counti}\nAn Error Accured: \"{e}\"")
            time.sleep(2)
            print("Trying to reconnect..")
            time.sleep(1)
            clear_console()
            continue
    if sdaafasfasfgg != "github.com/Tamino1230":
        print("Wrong owner in file!") #- Yes i know you can just delete that
        exit()
    if sdaafasfasfg1 != "https://discord.gg/vpApZSjh3H":
        print("Wrong dcserver in file!") #- Yes i know you can just delete that
        exit()
    clear_console()
     
    value_use()
    print("Femboys are not gay")
