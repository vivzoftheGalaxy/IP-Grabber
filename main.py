import subprocess
import sys
import socket
import requests
import keyboard

# Function to install a library if not already installed
def install_library(library_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", library_name])

# Try to import requests and install if necessary
try:
    import requests
except ImportError:
    install_library('requests')
    import requests

# Try to import keyboard and install if necessary
try:
    import keyboard
except ImportError:
    install_library('keyboard')
    import keyboard

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        return data['ip']
    except requests.RequestException as e:
        return f"An error occurred: {e}"

def get_private_ip():
    try:
        hostname = socket.gethostname()
        private_ip = socket.gethostbyname(hostname)
        return private_ip
    except socket.error as e:
        return f"An error occurred: {e}"

def toggle_prompt():
    options = ['y', 'n']
    selected = 0
    green = "\033[32m"
    red = "\033[31m"
    reset = "\033[0m"
    print(f"{red}Use at your own risk!{reset}")
    print(f"{green}Use arrow keys to toggle. Press Enter to select.{reset}")
    print("-----------")
    print("")
    while True:
        prompt = f"\rShow IP Address(s)? ({options[selected]}) {options[1 - selected]} : "
        print(prompt, end='', flush=True)

        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'right' or event.name == 'left':
                selected = 1 - selected  # Toggle the selection
            elif event.name == 'enter':
                return options[selected] == 'y'

if __name__ == "__main__":
    blue = "\033[34m"
    reset = "\033[0m"
    logo = f"""
{blue}        ,-.----.                                                                                 
   ,---,\\    /  \\                                                                                
,`--.' ||   :    \\                                         ,---,     ,---,                       
|   :  :|   |  .\\ :                     __  ,-.          ,---.'|   ,---.'|               __   
:   |  '.   :  |: |          ,----._,.,' ,'/ /|          |   | :   |   | :             ,' ,'/ /| 
|   :  ||   |   \\ :         /   /  ' /'  | |' | ,--.--.  :   : :   :   : :      ,---.  '  | |' | 
'   '  ;|   : .   /        |   :     ||  |   ,'/       \\ :     |,-.:     |,-.  /     \\ |  |   ,' 
|   |  |;   | |`-'         |   | .\\  .'  :  / .--.  .-. ||   : '  ||   : '  | /    /  |'  :  /   
'   :  ;|   | ;            .   ; ';  ||  | '   \\__\\/: . .|   |  / :|   |  / :.    ' / ||  | '    
|   |  ':   ' |            '   .   . |;  : |   ," .--.; |'   : |: |'   : |: |'   ;   /|;  : |    
'   :  |:   : :             `---`-'| ||  , ;  /  /  ,.  ||   | '/ :|   | '/ :'   |  / ||  , ;    
;   |.' |   | :             .'__/\_: | ---'  ;  :   .'   \\   :    ||   :    ||   :    | ---'     
'---'   `---'.|             |   :    :       |  ,     .-./    \\  / /    \\  /  \\   \\  /           
          `---`              \\   \\  /         `--`---'   `-'----'  `-'----'    `----'            
                              `--`-'                                                             {reset}
    """
    print(logo)

    show_ip = toggle_prompt()

    if show_ip:
        public_ip = get_public_ip()
        private_ip = get_private_ip()
        bold = "\033[1m"
        reset = "\033[0m"
        print(f"\nYour Public IP address is: {bold}{public_ip}{reset}")
        print(f"\nYour Private IP address is: {bold}{private_ip}{reset}")

