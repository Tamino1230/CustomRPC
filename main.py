
# import online
import time
from pypresence import Presence, InvalidID
import os
import json
import atexit

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
    av = [1, 2, 3, 4, 5, 6, 7, 8]
    print("Menu:\n"
          "   1) Change Client ID (when doing that all your settings will reset to the last saved)\n"
          "   2) Change Details\n"
          "   3) Change State\n"
          "   4) Change Party\n"
          "   5) Toggle Party Visibility\n"
          "   6) Restart\n"
          "   7) Save Settings\n"
          "   8) Toggle RPC\n"
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
    global rpc
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
                    rpc.connect()
                    set_rpc()
                else:
                    print("Invalid Client ID")
                    print("Reconnection old Client ID..")
                    rpc = Presence(client_id)
                    rpc.connect()
                    set_rpc()
                    print("Reconnected to old..")
            case 2:
                details = get_details()
                set_rpc()
            case 3:
                state = get_state()
                set_rpc()
            case 4:
                party_size = get_party_size()
                set_rpc()
            case 5:
                party_enabled = not party_enabled
                set_rpc()
                print(f"Party visibility {'enabled' if party_enabled else 'disabled'}.")
            case 6:
                if rpc:
                    rpc.close()
                time.sleep(1)
                rpc = Presence(client_id)
                rpc.connect()
                set_rpc()
            case 7:
                save_config()
                print("Settings saved.")
            case 8:
                rpc_enabled = not rpc_enabled
                if rpc_enabled:
                    rpc.connect()
                    set_rpc()
                    print("RPC enabled.")
                else:
                    rpc.close()
                    print("RPC disabled.")
            case 9:
                return

#- User to Start the Program
if __name__ == "__main__":
    load_config()
    rpc = Presence(client_id)
    rpc.connect()
    set_rpc()
    if sdaafasfasfgg != "github.com/Tamino1230":
        print("Wrong owner in file!") #- Yes i know you can just delete that
        exit()
    clear_console()
    
    while True:
        if first_time != False:
            print("\nCustom Discord RPC is running! 🎉\nJoin my Discord Server! Also if you got any problems:\nhttps://discord.gg/vpApZSjh3H\n")
            first_time = False
        else:
            print("Custom Discord RPC is running updated! 🎉\n")
        value_use()
        clear_console()
        time.sleep(1)
