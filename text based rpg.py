import json
import os
import random
import copy
import time
import sys
from termcolor import colored

playing = True

# Game text colors
red = "\033[31m"
orange = "\033[38;2;255;165;0m"
green = "\033[32m"
dark_brown = "\033[38;5;94m"
light_brown = "\033[38;5;137m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"
gray = "\033[90m"
silver = "\033[38;5;7m"
light_red = "\033[91m"
light_green = "\033[92m"
light_yellow = "\033[93m"
light_blue = "\033[94m"
light_magenta = "\033[95m"
light_cyan = "\033[96m"
reset = "\033[0m"

# Text styles
underline = "\033[4m"
bold = "\033[1m"

# Rainbow text
def print_rainbow(text):

    # Standard terminal colors for a rainbow effect
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    
    for index, char in enumerate(text):
        # Pick color using the modulo operator so it loops cleanly
        color = colors[index % len(colors)]
        
        # Print a single character without a newline and force flush
        print(colored(char, color), end='', flush=True)

# Animated text
def typewriter(text, speed=0.02):

    # Scans every character in the text
    for char in text:

        # Prevents a new line from being created after each character
        sys.stdout.write(char)

        # Forces the computer to immediately display the next character as soon as it is processed
        sys.stdout.flush()

        # Delay of each character displayed on text
        time.sleep(speed)

# Base player stats and inventory
player_stats = {
    "name": "Unknown Player",
    "hp": 100, 
    "max_hp": 100, 
    "damage": 1
}

player_inventory = {
    "gold": 0, 
    "potions": 0, 
    "super_potions": 0, 
    "hyper_potions": 0, 
    "rainbow_potions": 0, 
    "gear": "None", 
    "weapon": "None"
}

# Save data
save_file = "savegame.json"

# Enemy database (HP, Max HP, Damage, Gold Earnings, Spawn Chances)
enemy_database = {
    "Ooze": {
        "hp": 5, 
        "max_hp": 5, 
        "damage": 1, 
        "gold_earnings": 5,
        "spawn_weight": 30      # Highest chance to spawn
        },
    "Slime": {
        "hp": 10, 
        "max_hp": 10, 
        "damage": 2, 
        "gold_earnings": 10,
        "spawn_weight": 20
        },
    "Bat": {
        "hp": 20,
        "max_hp": 20,
        "damage": 5,
        "gold_earnings": 15,
        "spawn_weight": 15
        },
    "Zombie": {
        "hp": 25,
        "max_hp": 25,
        "damage": 10,
        "gold_earnings": 20,
        "spawn_weight": 12
        },
    "Skeleton": {
        "hp": 50,
        "max_hp": 50,
        "damage": 15,
        "gold_earnings": 35,
        "spawn_weight": 10
        },
    "Spider": {
        "hp": 100,
        "max_hp": 100,
        "damage": 25,
        "gold_earnings": 50,
        "spawn_weight": 7
        },
    "Goblin": {
        "hp": 250,
        "max_hp": 250,
        "damage": 30,
        "gold_earnings": 100,
        "spawn_weight": 3
        },
    "Orc": {
        "hp": 500,
        "max_hp": 500,
        "damage": 50,
        "gold_earnings": 250,
        "spawn_weight": 2
        },
    "Brute": {
        "hp": 1000,
        "max_hp": 1000,
        "damage": 100,
        "gold_earnings": 500,
        "spawn_weight": 1        # Lowest chance to spawn
        },

    "Boss": {
        "name": "Dragon",
        "hp": 10000,
        "max_hp": 10000,
        "damage": 500,
        "spawn_weight": 0
        }
}

# Shop items
shop_gear = {
    "Leather": {"max_hp": 125, "cost": 10},
    "Wooden": {"max_hp": 150, "cost": 25},
    "Copper": {"max_hp": 200, "cost": 50},
    "Silver": {"max_hp": 300, "cost": 125},
    "Iron": {"max_hp": 500, "cost": 200},
    "Diamond": {"max_hp": 1250, "cost": 500},
    "Emerald": {"max_hp": 2500, "cost": 1000},
    "Rainbow": {"max_hp": 5000, "cost": 2000}
}

shop_weapons = {
    "Stick": {"damage": 2, "cost": 10},
    "Sword": {"damage": 5, "cost": 25},
    "Axe": {"damage": 10, "cost": 50},
    "Knife": {"damage": 20, "cost": 125},
    "Dagger": {"damage": 50, "cost": 250},
    "Katana": {"damage": 100, "cost": 500},
    "Mace": {"damage": 250, "cost": 1000},
    "Chromasaber": {"damage": 500, "cost": 2000}
}

shop_potions = {
    "Potion": {"cost": 50},
    "Super Potion": {"cost": 125},
    "Hyper Potion": {"cost": 300},
    "Rainbow Potion": {"cost": 750}
}

# Function to save game data
def save_game():

    current_player = {
    "stats": player_stats,
    "inventory": player_inventory
    }

    # Saves player data dictionary to a JSON file.
    try:
        with open(save_file, "w") as file: # Writes the save file and automatically closes the file when the code indented under this block finishes running.
            json.dump(current_player, file, indent=4) # Saving game
        typewriter(f"\n{bold}[System]{reset} Game saved {green}successfully{reset}!\n")
    except IOError:
        typewriter(f"{bold}{light_red}ERROR:{reset} Could not save game data.")

# Function to load game data
def load_game():

    # Tells Python to modify the global dictionaries (player stats and inventory)
    global player_stats, player_inventory

    # Loads player data from a JSON file. Returns "None" if file doesn't exist.
    if not os.path.exists(save_file):
        typewriter(f"\n{red}{bold}Save file does not exist.\n{reset}")
        time.sleep(0.5)
        bootup()
        return False # No save file exists yet

    try:
        with open(save_file, "r") as file: # Reads the save file if it exists
            loaded_data = json.load(file) # Loads saved file
            typewriter(f"\nGame loaded {green}successfully{reset}!\n")

        # Extracts and updates global dictionaries with the saved data
        player_stats.clear()
        player_stats.update(loaded_data["stats"])

        player_inventory.clear()
        player_inventory.update(loaded_data["inventory"])

        time.sleep(0.5)
        typewriter(f"{bold}Welcome back, {player_stats['name']}!{reset}\n")
        time.sleep(1)

        return True

    except FileNotFoundError:
        typewriter(f"\n{bold}[System] {light_red}No save file found or file corrupted.{reset}\n")
        return False

# Function to load a new game
def start_new_game():
    # Tells this function to update these global dictionaries (player stats and player inventory)
    global player_stats, player_inventory

    # Deletes the physical save file and returns a fresh copy of the stats.

    # Delete the old text file from the computer's hard drive
    if os.path.exists(save_file):
        os.remove(save_file)
        typewriter(f"\n{bold}[System]{reset} Old save file deleted.")

    time.sleep(0.5)

    # Start a brand new game
    typewriter("\nStarting a new game!")
    time.sleep(0.5)

    # Base player stats and inventory
    player_stats = {
        "name": "Unknown Player",
        "hp": 100, 
        "max_hp": 100, 
        "damage": 1
    }

    player_inventory = {
        "gold": 0, 
        "potions": 0, 
        "super_potions": 0, 
        "hyper_potions": 0, 
        "rainbow_potions": 0, 
        "gear": "None", 
        "weapon": "None"
    }

    player_stats["name"] = input(f"\n{bold}Enter your character's name:{reset} ")
    print(f"{light_cyan}{bold}\nGame Creator:{reset} ", end=""); typewriter(f"Welcome, {bold}{player_stats["name"]}!{reset}\n")
    time.sleep(1)

    # Immediately saves game
    save_game()
    time.sleep(0.5)
    main()


# Welcomes the player
print(f"{bold}{light_cyan}Game Creator:{reset} ", end=""); typewriter(f"Hello there, {bold}player{reset}. Welcome to my {bold}text-based {orange}RPG{reset}! :D\n")
time.sleep(1)

# Initialization function
def bootup():
    in_welcome_screen = True

    while in_welcome_screen:

        # Gives the player options to either load or start a new game
        print(f"\n{bold}{underline}What would you like to do?{reset}")
        print(f"{light_cyan}Start a new game{reset}")
        print(f"{blue}Load game{reset}\n")

        choice = input(f"{bold}Type any of the options above here:{reset} ")

        # If the player chooses to load their game, then load their save data. Else, start a new game.
        if "load" in choice:
            success = load_game()

            if success:
                break
            
            if not success:
                start_new_game()
                break

        elif "new" in choice:
            action = input(f"{bold}\nAre you sure you want to start a {light_magenta}new game{white}?{reset}\nThis will erase your current progress and start a fresh instance.{reset} ({light_green}Yes{white}/{light_red}No{reset}): ")

            if "yes" in action:
                start_new_game()
                break
            elif "no" in action:
                bootup()
            else:
                print(f"\nPlease type an option in the menu. ({light_green}Perhaps you made a typo?{reset})")
                time.sleep(2)
        else:
            print(f"\nPlease type any of the options above. ({green}Perhaps you made a typo?{reset})")
            time.sleep(2)



# Function to show stats
def show_stats():
    print(f"\n{bold}{cyan}--- Your stats ---{reset}")
    print(f"{green}HP:{reset} {player_stats["hp"]}/{player_stats["max_hp"]}")
    print(f"{red}Damage:{reset} {player_stats["damage"]}")
    time.sleep(2)

def inventory():
    print(f"\n{bold}{light_cyan}--- Your inventory ---{reset}")
    print(f"{yellow}{player_inventory["gold"]} Gold{reset}")
    print(f"{green}Potions:{reset} {player_inventory["potions"]}")
    print(f"{orange}Super Potions:{reset} {player_inventory["super_potions"]}")
    print(f"{light_magenta}Hyper Potions:{reset} {player_inventory["hyper_potions"]}")
    print_rainbow("Rainbow Potions:"); print(f" {player_inventory["rainbow_potions"]}")
    print(f"{bold}{blue}Gear:{reset} {player_inventory["gear"]}")
    print(f"{bold}{light_red}Weapon:{reset} {player_inventory["weapon"]}")
    time.sleep(2.5)


# Function to spawn random enemies
def spawn_random_enemy():

    # Gets a list of names and their spawn chances from the dictionary
    enemy_names = list(enemy_database.keys())
    enemy_weights = [enemy_database[name]["spawn_weight"] for name in enemy_names]

    # Chooses a random enemy name from the list of dictionaries based on spawn chances
    chosen_name = random.choices(enemy_names, weights=enemy_weights, k=1)[0]

    # Copies the stats defined from the chosen enemy's dictionary from the enemy pool
    enemy_stats = copy.deepcopy(enemy_database[chosen_name])

    # The function then returns the values of the chosen enemy's stats to be used later in the program
    return {
        "name": chosen_name,
        "hp": enemy_stats["hp"],
        "max_hp": enemy_stats["max_hp"],
        "damage": enemy_stats["damage"],
        "gold": enemy_stats["gold_earnings"]
    }

def spawn_boss():

    # Gets the boss's name from the enemy database
    boss_name = enemy_database["Boss"]["name"]

    # Copies stats of the boss from the enemy database
    boss_stats = copy.deepcopy(enemy_database["Boss"])

    # Returns the values of the boss stats to be used later in the program
    return {
        "name": boss_name,
        "hp": boss_stats["hp"],
        "max_hp": boss_stats["max_hp"],
        "damage": boss_stats["damage"],
    }

    
    
# Function to open shop
def shop():
    
    # The cutscene
    typewriter(f"\nYou leave your home and take your {bold}bag{reset} with you.\n")
    time.sleep(0.5)
    typewriter(f"You make your way to the {bold}{underline}shop{reset}!\n")
    time.sleep(0.5)
    typewriter("You walk inside the shop...\n\n")
    time.sleep(0.5)
    typewriter(f"A {bold}{light_yellow}merchant{reset} walks up to you.\n\n")
    time.sleep(0.5)
    print(f"{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Hello there! Welcome to my shop!\n")
    time.sleep(0.5)
    typewriter(f"Here, you can buy some wonderful goods in exchange for some precious {yellow}gold{reset}, from {blue}gear{reset}, to {light_red}weapons{reset}, to {green}potions{reset}, you name it!\n")
    time.sleep(0.5)
    typewriter(f"They would really help you out on your adventures!\n")
    time.sleep(0.5)
    typewriter(f"Why don't you take a look around?\n")
    time.sleep(1)

    in_shop = True

    while in_shop:
        # Prompts the user on what they want to spend gold on
        print(f"\n{bold}{light_yellow}---- Merchant's Shop -----{reset}")
        action = input(f"{underline}{bold}What would you like to do?{reset}\nBuy {blue}gear{reset}\nBuy {light_red}weapon{reset}\nBuy {green}potions{reset}\n{red}Exit shop{reset}\n\n{bold}You have {yellow}{player_inventory["gold"]} Gold{reset}\n\n{bold}Type any of the options above here:{reset} ").lower().strip()

        # If the user chooses gear, then give them a variety of gear options, showing the benefits of each of them.
        # If the user already has that gear on, then say that they have that gear on already
        # If the user decides to buy gear that is worse than the current gear that they have, then warn them before doing so
        # The same logic applies to all other options.

        if "gear" in action:
            in_gear_aisle = True

            while in_gear_aisle:

                # Shows the user the list of items in the aisle, along with their gold balance and current gear
                print(f"\n{bold}{blue}~~~ Gear Aisle ~~~{reset}")
                print(f"{dark_brown}Leather Gear{reset} - {green}+{shop_gear["Leather"]["max_hp"] - 100} Max HP{reset} - Cost: {yellow}{shop_gear["Leather"]["cost"]} Gold")
                print(f"{light_brown}Wooden Gear{reset} - {green}+{shop_gear["Wooden"]["max_hp"] - 100} Max HP{reset} - Cost: {yellow}{shop_gear["Wooden"]["cost"]} Gold")
                print(f"{gray}Silver Gear{reset} - {green}+{shop_gear["Silver"]["max_hp"] - 100} Max HP{reset} - Cost: {yellow}{shop_gear["Silver"]["cost"]} Gold")
                print(f"{silver}Iron Gear{reset} - {green}+{shop_gear["Iron"]["max_hp"] - 100} Max HP{reset} - Cost: {yellow}{shop_gear["Iron"]["cost"]} Gold")
                print(f"{light_cyan}Diamond Gear{reset} - {green}+{shop_gear["Diamond"]["max_hp"] - 100} Max HP{reset} - Cost: {yellow}{shop_gear["Diamond"]["cost"]} Gold")
                print(f"{light_green}Emerald Gear{reset} - {green}+{shop_gear["Emerald"]["max_hp"] - 100} Max HP{reset} - Cost: {yellow}{shop_gear["Emerald"]["cost"]} Gold")
                print_rainbow("Rainbow Gear "); print(f"- {green}+{shop_gear["Rainbow"]["max_hp"] - 100} Max HP{reset} - Cost: {yellow}{shop_gear["Rainbow"]["cost"]} Gold{reset}\n")
                print(f"{blue}{underline}Your current gear:{reset} {bold}{player_inventory["gear"]}{reset}")
                print(f"{bold}You have {yellow}{player_inventory["gold"]} Gold{reset}\n")

                # Prompts the user on either exiting the aisle or purchasing an item of their choice from the provided list
                user_choice = input(f"{bold}Type any item in the aisle to purchase it or type {red}exit{white} to exit this aisle and return to the shop menu:{reset} ").lower().strip()

                # If the user chooses to purchase leather, then do two things: if they don't have enough gold to purchase the leather, then say that they don't have enough gold, otherwise, proceed with the purchase and modify the player stats to mimic the stats of the gear.
                # The same logic applies to all of the other options
                if "leather" in user_choice:
                    if player_inventory["gold"] < shop_gear["Leather"]["cost"]:
                        print(f"\n{red}Oops! You don't have enough {yellow}gold{red} to purchase this item!")
                        time.sleep(2)
                        continue

                    elif player_stats["max_hp"] > shop_gear["Leather"]["max_hp"]:
                        print(f"\nThis item is {red}inferior{reset} to the current gear you have equipped. Please choose a different item.")
                        time.sleep(2)
                        continue

                    elif player_stats["max_hp"] == shop_gear["Leather"]["max_hp"]:
                        print(f"\nYou already have this gear equipped!")
                        time.sleep(2) 
                        continue
                
                    
                    else:
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Fantastic choice! That will be {yellow}{shop_gear["Leather"]["cost"]} Gold{reset}.\n")
                        time.sleep(1)
                        user_confirmation = input(f"{bold}Are you sure you want to make this purchase?{reset} ({green}Yes{reset}/{red}No{reset}): ").lower().strip()

                        if "yes" in user_confirmation:
                            player_inventory["gold"] -= shop_gear["Leather"]["cost"]
                            typewriter(f"\nYou purchased {bold}{dark_brown}Leather Gear{reset} for {yellow}{shop_gear["Leather"]["cost"]} Gold{reset}!\n")
                            time.sleep(1)
                            typewriter(f"You {bold}equip{reset} your new gear!")
                            time.sleep(1)

                            # Modifies player stats to match gear stats
                            player_stats["max_hp"] = int(shop_gear["Leather"]["max_hp"])
                            player_stats["hp"] = player_stats["max_hp"]
    
                            # Changes the player_inventory's "gear" key value to the gear purchased
                            player_inventory["gear"] = f"{dark_brown}Leather{reset}"

                            typewriter(f"\nYour {green}Max HP{reset} is now {bold}{light_green}{shop_gear["Leather"]["max_hp"]}{reset}!\n")
                            time.sleep(1)
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Thank you very much for your purchase! Feel free to continue exploring my shop.\n")
                            time.sleep(1)
                            typewriter(f"\n{bold}Your balance is now {yellow}{player_inventory["gold"]} Gold{reset}.\n")
                            time.sleep(1)
                            break
                    
                        elif "no" in user_confirmation:
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Very well then. Would you like to purchase something else?\n")
                            time.sleep(1)
                            continue
                        else:
                            print(f"\nPlease type {green}yes{reset} or {red}no{reset}.")
                            time.sleep(2)
                            continue

                elif "wooden" in user_choice:
                    if player_inventory["gold"] < shop_gear["Wooden"]["cost"]:
                        print(f"\n{red}Oops! You don't have enough {yellow}gold{red} to purchase this item!")
                        time.sleep(2)
                        continue
                    
                    elif player_stats["max_hp"] > shop_gear["Wooden"]["max_hp"]:
                        print(f"\nThis item is {red}inferior{reset} to the current gear you have equipped. Please choose a different item.")
                        time.sleep(2)
                        continue

                    elif player_stats["max_hp"] == shop_gear["Wooden"]["max_hp"]:
                        print(f"\nYou already have this gear equipped!")
                        time.sleep(2)
                        continue

                    else:
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Fantastic choice! That will be {yellow}{shop_gear["Wooden"]["cost"]} Gold{reset}.\n")
                        time.sleep(1)
                        user_confirmation = input(f"{bold}Are you sure you want to make this purchase?{reset} ({green}Yes{reset}/{red}No{reset}): ").lower().strip()

                        if "yes" in user_confirmation:
                            player_inventory["gold"] -= shop_gear["Wooden"]["cost"]
                            typewriter(f"\nYou purchased {bold}{light_brown}Wooden Gear{reset} for {yellow}{shop_gear["Wooden"]["cost"]} Gold{reset}!\n")
                            time.sleep(1)
                            typewriter(f"You {bold}equip{reset} your new gear!")
                            time.sleep(1)

                            # Modifies player stats to match gear stats
                            player_stats["max_hp"] = int(shop_gear["Wooden"]["max_hp"])
                            player_stats["hp"] = player_stats["max_hp"]

                            # Changes the player_inventory's "gear" key value to the gear purchased
                            player_inventory["gear"] = f"{light_brown}Wooden{reset}"

                            typewriter(f"\nYour {green}Max HP{reset} is now {bold}{light_green}{shop_gear["Wooden"]["max_hp"]}{reset}!\n")
                            time.sleep(1)
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Thank you very much for your purchase! Feel free to continue exploring my shop.\n")
                            time.sleep(1)
                            typewriter(f"\n{bold}Your balance is now {yellow}{player_inventory["gold"]} Gold{reset}.\n")
                            time.sleep(1)
                            break
                    
                        elif "no" in user_confirmation:
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Very well then. Would you like to purchase something else?\n")
                            time.sleep(1)
                            continue
                        else:
                            print(f"\nPlease type {green}yes{reset} or {red}no{reset}.")
                            time.sleep(2)
                            continue

                if "silver" in user_choice:
                    if player_inventory["gold"] < shop_gear["Silver"]["cost"]:
                        print(f"\n{red}Oops! You don't have enough {yellow}gold{red} to purchase this item!")
                        time.sleep(2)
                        continue

                    elif player_stats["max_hp"] > shop_gear["Silver"]["max_hp"]:
                        print(f"\nThis item is {red}inferior{reset} to the current gear you have equipped. Please choose a different item.")
                        time.sleep(2)
                        continue

                    elif player_stats["max_hp"] == shop_gear["Silver"]["max_hp"]:
                        print(f"\nYou already have this gear equipped!")
                        time.sleep(2) 
                        continue
                
                    
                    else:
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Fantastic choice! That will be {yellow}{shop_gear["Silver"]["cost"]} Gold{reset}.\n")
                        time.sleep(1)
                        user_confirmation = input(f"{bold}Are you sure you want to make this purchase?{reset} ({green}Yes{reset}/{red}No{reset}): ").lower().strip()

                        if "yes" in user_confirmation:
                            player_inventory["gold"] -= shop_gear["Silver"]["cost"]
                            typewriter(f"\nYou purchased {bold}{gray}Silver Gear{reset} for {yellow}{shop_gear["Silver"]["cost"]} Gold{reset}!\n")
                            time.sleep(1)
                            typewriter(f"You {bold}equip{reset} your new gear!")
                            time.sleep(1)

                            # Modifies player stats to match gear stats
                            player_stats["max_hp"] = int(shop_gear["Silver"]["max_hp"])
                            player_stats["hp"] = player_stats["max_hp"]


                            # Changes the player_inventory's "gear" key value to the gear purchased
                            player_inventory["gear"] = f"{gray}Silver{reset}"

                            typewriter(f"\nYour {green}Max HP{reset} is now {bold}{light_green}{shop_gear["Silver"]["max_hp"]}{reset}!\n")
                            time.sleep(1)
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Thank you very much for your purchase! Feel free to continue exploring my shop.\n")
                            time.sleep(1)
                            typewriter(f"\n{bold}Your balance is now {yellow}{player_inventory["gold"]} Gold{reset}.\n")
                            time.sleep(1)
                            break
                    
                        elif "no" in user_confirmation:
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Very well then. Would you like to purchase something else?\n")
                            time.sleep(1)
                            continue
                        else:
                            print(f"\nPlease type {green}yes{reset} or {red}no{reset}.")
                            time.sleep(2)
                            continue

                if "iron" in user_choice:
                    if player_inventory["gold"] < shop_gear["Iron"]["cost"]:
                        print(f"\n{red}Oops! You don't have enough {yellow}gold{red} to purchase this item!")
                        time.sleep(2)
                        continue

                    elif player_stats["max_hp"] > shop_gear["Iron"]["max_hp"]:
                        print(f"\nThis item is {red}inferior{reset} to the current gear you have equipped. Please choose a different item.")
                        time.sleep(2)
                        continue

                    elif player_stats["max_hp"] == shop_gear["Iron"]["max_hp"]:
                        print(f"\nYou already have this gear equipped!")
                        time.sleep(2) 
                        continue
                
                    
                    else:
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Fantastic choice! That will be {yellow}{shop_gear["Iron"]["cost"]} Gold{reset}.\n")
                        time.sleep(1)
                        user_confirmation = input(f"{bold}Are you sure you want to make this purchase?{reset} ({green}Yes{reset}/{red}No{reset}): ").lower().strip()

                        if "yes" in user_confirmation:
                            player_inventory["gold"] -= shop_gear["Iron"]["cost"]
                            typewriter(f"\nYou purchased {bold}{silver}Iron Gear{reset} for {yellow}{shop_gear["Iron"]["cost"]} Gold{reset}!\n")
                            time.sleep(1)
                            typewriter(f"You {bold}equip{reset} your new gear!")
                            time.sleep(1)

                            # Modifies player stats to match gear stats
                            player_stats["max_hp"] = int(shop_gear["Iron"]["max_hp"])
                            player_stats["hp"] = player_stats["max_hp"]

                            # Changes the player_inventory's "gear" key value to the gear purchased
                            player_inventory["gear"] = f"{silver}Iron{reset}"

                            typewriter(f"\nYour {green}Max HP{reset} is now {bold}{light_green}{shop_gear["Iron"]["max_hp"]}{reset}!\n")
                            time.sleep(1)
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Thank you very much for your purchase! Feel free to continue exploring my shop.\n")
                            time.sleep(1)
                            typewriter(f"\n{bold}Your balance is now {yellow}{player_inventory["gold"]} Gold{reset}.\n")
                            time.sleep(1)
                            break
                    
                        elif "no" in user_confirmation:
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Very well then. Would you like to purchase something else?\n")
                            time.sleep(1)
                            continue
                        else:
                            print(f"\nPlease type {green}yes{reset} or {red}no{reset}.")
                            time.sleep(2)
                            continue

                if "diamond" in user_choice:
                    if player_inventory["gold"] < shop_gear["Diamond"]["cost"]:
                        print(f"\n{red}Oops! You don't have enough {yellow}gold{red} to purchase this item!")
                        time.sleep(2)
                        continue

                    elif player_stats["max_hp"] > shop_gear["Diamond"]["max_hp"]:
                        print(f"\nThis item is {red}inferior{reset} to the current gear you have equipped. Please choose a different item.")
                        time.sleep(2)
                        continue

                    elif player_stats["max_hp"] == shop_gear["Diamond"]["max_hp"]:
                        print(f"\nYou already have this gear equipped!")
                        time.sleep(2) 
                        continue
                
                    
                    else:
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Fantastic choice! That will be {yellow}{shop_gear["Diamond"]["cost"]} Gold{reset}.\n")
                        time.sleep(1)
                        user_confirmation = input(f"{bold}Are you sure you want to make this purchase?{reset} ({green}Yes{reset}/{red}No{reset}): ").lower().strip()

                        if "yes" in user_confirmation:
                            player_inventory["gold"] -= shop_gear["Diamond"]["cost"]
                            typewriter(f"\nYou purchased {bold}{light_cyan}Diamond Gear{reset} for {yellow}{shop_gear["Diamond"]["cost"]} Gold{reset}!\n")
                            time.sleep(1)
                            typewriter(f"You {bold}equip{reset} your new gear!")
                            time.sleep(1)

                            # Modifies player stats to match gear stats
                            player_stats["max_hp"] = int(shop_gear["Diamond"]["max_hp"])
                            player_stats["hp"] = player_stats["max_hp"]

                            # Changes the player_inventory's "gear" key value to the gear purchased
                            player_inventory["gear"] = f"{light_cyan}Diamond{reset}"

                            typewriter(f"\nYour {green}Max HP{reset} is now {bold}{light_green}{shop_gear["Diamond"]["max_hp"]}{reset}!\n")
                            time.sleep(1)
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Thank you very much for your purchase! Feel free to continue exploring my shop.\n")
                            time.sleep(1)
                            typewriter(f"\n{bold}Your balance is now {yellow}{player_inventory["gold"]} Gold{reset}.\n")
                            time.sleep(1)
                            break
                    
                        elif "no" in user_confirmation:
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Very well then. Would you like to purchase something else?\n")
                            time.sleep(1)
                            continue
                        else:
                            print(f"\nPlease type {green}yes{reset} or {red}no{reset}.")
                            time.sleep(2)
                            continue

                if "emerald" in user_choice:
                    if player_inventory["gold"] < shop_gear["Emerald"]["cost"]:
                        print(f"\n{red}Oops! You don't have enough {yellow}gold{red} to purchase this item!")
                        time.sleep(2)
                        continue

                    elif player_stats["max_hp"] > shop_gear["Emerald"]["max_hp"]:
                        print(f"\nThis item is {red}inferior{reset} to the current gear you have equipped. Please choose a different item.")
                        time.sleep(2)
                        continue

                    elif player_stats["max_hp"] == shop_gear["Emerald"]["max_hp"]:
                        print(f"\nYou already have this gear equipped!")
                        time.sleep(2) 
                        continue
                
                    
                    else:
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Fantastic choice! That will be {yellow}{shop_gear["Emerald"]["cost"]} Gold{reset}.\n")
                        time.sleep(1)
                        user_confirmation = input(f"{bold}Are you sure you want to make this purchase?{reset} ({green}Yes{reset}/{red}No{reset}): ").lower().strip()

                        if "yes" in user_confirmation:
                            player_inventory["gold"] -= shop_gear["Emerald"]["cost"]
                            typewriter(f"\nYou purchased {bold}{light_green}Emerald Gear{reset} for {yellow}{shop_gear["Emerald"]["cost"]} Gold{reset}!\n")
                            time.sleep(1)
                            typewriter(f"You {bold}equip{reset} your new gear!")
                            time.sleep(1)

                            # Modifies player stats to match gear stats
                            player_stats["max_hp"] = int(shop_gear["Emerald"]["max_hp"])
                            player_stats["hp"] = player_stats["max_hp"]


                            # Changes the player_inventory's "gear" key value to the gear purchased
                            player_inventory["gear"] = f"{light_green}Emerald{reset}"

                            typewriter(f"\nYour {green}Max HP{reset} is now {bold}{light_green}{shop_gear["Emerald"]["max_hp"]}{reset}!\n")
                            time.sleep(1)
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Thank you very much for your purchase! Feel free to continue exploring my shop.\n")
                            time.sleep(1)
                            typewriter(f"\n{bold}Your balance is now {yellow}{player_inventory["gold"]} Gold{reset}.\n")
                            time.sleep(1)
                            break
                    
                        elif "no" in user_confirmation:
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Very well then. Would you like to purchase something else?\n")
                            time.sleep(1)
                            continue
                        else:
                            print(f"\nPlease type {green}yes{reset} or {red}no{reset}.")
                            time.sleep(2)
                            continue

                if "rainbow" in user_choice:
                    if player_inventory["gold"] < shop_gear["Rainbow"]["cost"]:
                        print(f"\n{red}Oops! You don't have enough {yellow}gold{red} to purchase this item!")
                        time.sleep(2)
                        continue

                    elif player_stats["max_hp"] > shop_gear["Rainbow"]["max_hp"]:
                        print(f"\nThis item is {red}inferior{reset} to the current gear you have equipped. Please choose a different item.")
                        time.sleep(2)
                        continue

                    elif player_stats["max_hp"] == shop_gear["Rainbow"]["max_hp"]:
                        print(f"\nYou already have this gear equipped!")
                        time.sleep(2) 
                        continue
                
                    
                    else:
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Fantastic choice! That will be {yellow}{shop_gear["Rainbow"]["cost"]} Gold{reset}.\n")
                        time.sleep(1)
                        user_confirmation = input(f"{bold}Are you sure you want to make this purchase?{reset} ({green}Yes{reset}/{red}No{reset}): ").lower().strip()

                        if "yes" in user_confirmation:
                            player_inventory["gold"] -= shop_gear["Rainbow"]["cost"]
                            typewriter(f"\nYou purchased {bold}"); print_rainbow("Rainbow Gear"); typewriter(f"{reset} for {yellow}{shop_gear["Rainbow"]["cost"]} Gold{reset}!\n")
                            time.sleep(1)
                            typewriter(f"You {bold}equip{reset} your new gear!")
                            time.sleep(1)

                            # Modifies player stats to match gear stats
                            player_stats["max_hp"] = int(shop_gear["Rainbow"]["max_hp"])
                            player_stats["hp"] = player_stats["max_hp"]


                            # Changes the player_inventory's "gear" key value to the gear purchased
                            player_inventory["gear"] = f"{red}R{yellow}a{green}i{cyan}n{blue}b{magenta}o{red}w{reset}"

                            typewriter(f"\nYour {green}Max HP{reset} is now {bold}{light_green}{shop_gear["Rainbow"]["max_hp"]}{reset}!\n")
                            time.sleep(1)
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Thank you very much for your purchase! Feel free to continue exploring my shop.\n")
                            time.sleep(1)
                            typewriter(f"\n{bold}Your balance is now {yellow}{player_inventory["gold"]} Gold{reset}.\n")
                            time.sleep(1)
                            break
                    
                        elif "no" in user_confirmation:
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Very well then. Would you like to purchase something else?\n")
                            time.sleep(1)
                            continue
                        else:
                            print(f"\nPlease type {green}yes{reset} or {red}no{reset}.")
                            time.sleep(2)
                            continue

                elif "exit" in user_choice:
                    break
            
                else:
                    print(f"\nThis choice is {red}invalid{reset}.")
                    time.sleep(2)
                    continue

        elif "weapon" in action:
            in_weapon_aisle = True

            while in_weapon_aisle:

                # Shows the player all the items in the aisle, along with their current gold balance and weapon
                print(f"\n{bold}{light_red}~~~ Weapon Aisle ~~~{reset}")
                print(f"{dark_brown}Stick{reset} - {red}{shop_weapons["Stick"]["damage"]} Damage{reset} - Cost: {yellow}{shop_weapons["Stick"]["cost"]} Gold")
                print(f"{light_brown}Sword{reset} - {red}{shop_weapons["Sword"]["damage"]} Damage{reset} - Cost: {yellow}{shop_weapons["Sword"]["cost"]} Gold")
                print(f"{green}Axe{reset} - {red}{shop_weapons["Axe"]["damage"]} Damage{reset} - Cost: {yellow}{shop_weapons["Axe"]["cost"]} Gold")
                print(f"{gray}Knife{reset} - {red}{shop_weapons["Knife"]["damage"]} Damage{reset} - Cost: {yellow}{shop_weapons["Knife"]["cost"]} Gold")
                print(f"{cyan}Dagger{reset} - {red}{shop_weapons["Dagger"]["damage"]} Damage{reset} - Cost: {yellow}{shop_weapons["Dagger"]["cost"]} Gold")
                print(f"{magenta}Katana{reset} - {red}{shop_weapons["Katana"]["damage"]} Damage{reset} - Cost: {yellow}{shop_weapons["Katana"]["cost"]} Gold")
                print(f"{silver}Mace{reset} - {red}{shop_weapons["Mace"]["damage"]} Damage{reset} - Cost: {yellow}{shop_weapons["Mace"]["cost"]} Gold")
                print_rainbow("Chromasaber"); print(f" - {red}{shop_weapons["Chromasaber"]["damage"]} Damage{reset} - Cost: {yellow}{shop_weapons["Chromasaber"]["cost"]} Gold\n")
                print(f"{light_red}{underline}Your current weapon:{reset} {bold}{player_inventory["weapon"]}{reset}")
                print(f"{bold}You have {yellow}{player_inventory["gold"]} Gold{reset}\n")

                # Prompts the user on either exiting the aisle or purchasing an item of their choice from the provided list
                user_choice = input(f"{bold}Type any item in the aisle to purchase it or type {red}exit{white} to exit this aisle and return to the shop menu:{reset} ").lower().strip()

                # The same logic with the gear aisle applies to the weapon aisle
                if "stick" in user_choice:
                    if player_inventory["gold"] < shop_weapons["Stick"]["cost"]:
                        print(f"\n{red}Oops! You don't have enough {yellow}gold{red} to purchase this item!")
                        time.sleep(2)
                        continue

                    elif player_stats["damage"] > shop_weapons["Stick"]["damage"]:
                        print(f"\nThis item is {red}inferior{reset} to the current weapon you have equipped. Please choose a different item.")
                        time.sleep(2)
                        continue

                    elif player_stats["damage"] == shop_weapons["Stick"]["damage"]:
                        print(f"\nYou already have this weapon equipped!")
                        time.sleep(2) 
                        continue
                
                    
                    else:
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Fantastic choice! That will be {yellow}{shop_weapons["Stick"]["cost"]} Gold{reset}.\n")
                        time.sleep(1)
                        user_confirmation = input(f"{bold}Are you sure you want to make this purchase?{reset} ({green}Yes{reset}/{red}No{reset}): ").lower().strip()

                        if "yes" in user_confirmation:
                            player_inventory["gold"] -= shop_weapons["Stick"]["cost"]
                            typewriter(f"\nYou purchased {bold}{dark_brown}Stick{reset} for {yellow}{shop_weapons["Stick"]["cost"]} Gold{reset}!\n")
                            time.sleep(1)
                            typewriter(f"You {bold}equip{reset} your new weapon!")
                            time.sleep(1)

                            # Modifies player stats to match weapon stats
                            player_stats["damage"] = shop_weapons["Stick"]["damage"]

                            # Changes the player_inventory's "weapon" key value to the weapon purchased
                            player_inventory["weapon"] = f"{dark_brown}Stick{reset}"

                            typewriter(f"\nYour {red}damage{reset} is now {bold}{light_red}{shop_weapons["Stick"]["damage"]}{reset}!\n")
                            time.sleep(1)
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Thank you very much for your purchase! Feel free to continue exploring my shop.\n")
                            time.sleep(1)
                            typewriter(f"\n{bold}Your balance is now {yellow}{player_inventory["gold"]} Gold{reset}.\n")
                            time.sleep(1)
                            break
                    
                        elif "no" in user_confirmation:
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Very well then. Would you like to purchase something else?\n")
                            time.sleep(1)
                            continue
                        else:
                            print(f"\nPlease type {green}yes{reset} or {red}no{reset}.")
                            time.sleep(2)
                            continue

                if "sword" in user_choice:
                    if player_inventory["gold"] < shop_weapons["Sword"]["cost"]:
                        print(f"\n{red}Oops! You don't have enough {yellow}gold{red} to purchase this item!")
                        time.sleep(2)
                        continue

                    elif player_stats["damage"] > shop_weapons["Sword"]["damage"]:
                        print(f"\nThis item is {red}inferior{reset} to the current weapon you have equipped. Please choose a different item.")
                        time.sleep(2)
                        continue

                    elif player_stats["damage"] == shop_weapons["Sword"]["damage"]:
                        print(f"\nYou already have this weapon equipped!")
                        time.sleep(2) 
                        continue
                
                    
                    else:
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Fantastic choice! That will be {yellow}{shop_weapons["Sword"]["cost"]} Gold{reset}.\n")
                        time.sleep(1)
                        user_confirmation = input(f"{bold}Are you sure you want to make this purchase?{reset} ({green}Yes{reset}/{red}No{reset}): ").lower().strip()

                        if "yes" in user_confirmation:
                            player_inventory["gold"] -= shop_weapons["Sword"]["cost"]
                            typewriter(f"\nYou purchased {bold}{light_brown}Sword{reset} for {yellow}{shop_weapons["Sword"]["cost"]} Gold{reset}!\n")
                            time.sleep(1)
                            typewriter(f"You {bold}equip{reset} your new weapon!")
                            time.sleep(1)

                            # Modifies player stats to match weapon stats
                            player_stats["damage"] = shop_weapons["Sword"]["damage"]

                            # Changes the player_inventory's "weapon" key value to the weapon purchased
                            player_inventory["weapon"] = f"{light_brown}Sword{reset}"

                            typewriter(f"\nYour {red}damage{reset} is now {bold}{light_red}{shop_weapons["Sword"]["damage"]}{reset}!\n")
                            time.sleep(1)
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Thank you very much for your purchase! Feel free to continue exploring my shop.\n")
                            time.sleep(1)
                            typewriter(f"\n{bold}Your balance is now {yellow}{player_inventory["gold"]} Gold{reset}.\n")
                            time.sleep(1)
                            break
                    
                        elif "no" in user_confirmation:
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Very well then. Would you like to purchase something else?\n")
                            time.sleep(1)
                            continue
                        else:
                            print(f"\nPlease type {green}yes{reset} or {red}no{reset}.")
                            time.sleep(2)
                            continue

                if "axe" in user_choice:
                    if player_inventory["gold"] < shop_weapons["Axe"]["cost"]:
                        print(f"\n{red}Oops! You don't have enough {yellow}gold{red} to purchase this item!")
                        time.sleep(2)
                        continue

                    elif player_stats["damage"] > shop_weapons["Axe"]["damage"]:
                        print(f"\nThis item is {red}inferior{reset} to the current weapon you have equipped. Please choose a different item.")
                        time.sleep(2)
                        continue

                    elif player_stats["damage"] == shop_weapons["Axe"]["damage"]:
                        print(f"\nYou already have this weapon equipped!")
                        time.sleep(2) 
                        continue
                
                    
                    else:
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Fantastic choice! That will be {yellow}{shop_weapons["Axe"]["cost"]} Gold{reset}.\n")
                        time.sleep(1)
                        user_confirmation = input(f"{bold}Are you sure you want to make this purchase?{reset} ({green}Yes{reset}/{red}No{reset}): ").lower().strip()

                        if "yes" in user_confirmation:
                            player_inventory["gold"] -= shop_weapons["Axe"]["cost"]
                            typewriter(f"\nYou purchased {bold}{green}Axe{reset} for {yellow}{shop_weapons["Axe"]["cost"]} Gold{reset}!\n")
                            time.sleep(1)
                            typewriter(f"You {bold}equip{reset} your new weapon!")
                            time.sleep(1)

                            # Modifies player stats to match weapon stats
                            player_stats["damage"] = shop_weapons["Axe"]["damage"]

                            # Changes the player_inventory's "weapon" key value to the weapon purchased
                            player_inventory["weapon"] = f"{green}Axe{reset}"

                            typewriter(f"\nYour {red}damage{reset} is now {bold}{light_red}{shop_weapons["Axe"]["damage"]}{reset}!\n")
                            time.sleep(1)
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Thank you very much for your purchase! Feel free to continue exploring my shop.\n")
                            time.sleep(1)
                            typewriter(f"\n{bold}Your balance is now {yellow}{player_inventory["gold"]} Gold{reset}.\n")
                            time.sleep(1)
                            break
                    
                        elif "no" in user_confirmation:
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Very well then. Would you like to purchase something else?\n")
                            time.sleep(1)
                            continue
                        else:
                            print(f"\nPlease type {green}yes{reset} or {red}no{reset}.")
                            time.sleep(2)
                            continue
                
                if "knife" in user_choice:
                    if player_inventory["gold"] < shop_weapons["Knife"]["cost"]:
                        print(f"\n{red}Oops! You don't have enough {yellow}gold{red} to purchase this item!")
                        time.sleep(2)
                        continue

                    elif player_stats["damage"] > shop_weapons["Knife"]["damage"]:
                        print(f"\nThis item is {red}inferior{reset} to the current weapon you have equipped. Please choose a different item.")
                        time.sleep(2)
                        continue

                    elif player_stats["damage"] == shop_weapons["Knife"]["damage"]:
                        print(f"\nYou already have this weapon equipped!")
                        time.sleep(2) 
                        continue
                
                    
                    else:
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Fantastic choice! That will be {yellow}{shop_weapons["Knife"]["cost"]} Gold{reset}.\n")
                        time.sleep(1)
                        user_confirmation = input(f"{bold}Are you sure you want to make this purchase?{reset} ({green}Yes{reset}/{red}No{reset}): ").lower().strip()

                        if "yes" in user_confirmation:
                            player_inventory["gold"] -= shop_weapons["Knife"]["cost"]
                            typewriter(f"\nYou purchased {bold}{gray}Knife{reset} for {yellow}{shop_weapons["Knife"]["cost"]} Gold{reset}!\n")
                            time.sleep(1)
                            typewriter(f"You {bold}equip{reset} your new weapon!")
                            time.sleep(1)

                            # Modifies player stats to match weapon stats
                            player_stats["damage"] = shop_weapons["Knife"]["damage"]

                            # Changes the player_inventory's "weapon" key value to the weapon purchased
                            player_inventory["weapon"] = f"{gray}Knife{reset}"

                            typewriter(f"\nYour {red}damage{reset} is now {bold}{light_red}{shop_weapons["Knife"]["damage"]}{reset}!\n")
                            time.sleep(1)
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Thank you very much for your purchase! Feel free to continue exploring my shop.\n")
                            time.sleep(1)
                            typewriter(f"\n{bold}Your balance is now {yellow}{player_inventory["gold"]} Gold{reset}.\n")
                            time.sleep(1)
                            break
                    
                        elif "no" in user_confirmation:
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Very well then. Would you like to purchase something else?\n")
                            time.sleep(1)
                            continue
                        else:
                            print(f"\nPlease type {green}yes{reset} or {red}no{reset}.")
                            time.sleep(2)
                            continue

                if "dagger" in user_choice:
                    if player_inventory["gold"] < shop_weapons["Dagger"]["cost"]:
                        print(f"\n{red}Oops! You don't have enough {yellow}gold{red} to purchase this item!")
                        time.sleep(2)
                        continue

                    elif player_stats["damage"] > shop_weapons["Dagger"]["damage"]:
                        print(f"\nThis item is {red}inferior{reset} to the current weapon you have equipped. Please choose a different item.")
                        time.sleep(2)
                        continue

                    elif player_stats["damage"] == shop_weapons["Dagger"]["damage"]:
                        print(f"\nYou already have this weapon equipped!")
                        time.sleep(2) 
                        continue
                
                    
                    else:
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Fantastic choice! That will be {yellow}{shop_weapons["Dagger"]["cost"]} Gold{reset}.\n")
                        time.sleep(1)
                        user_confirmation = input(f"{bold}Are you sure you want to make this purchase?{reset} ({green}Yes{reset}/{red}No{reset}): ").lower().strip()

                        if "yes" in user_confirmation:
                            player_inventory["gold"] -= shop_weapons["Dagger"]["cost"]
                            typewriter(f"\nYou purchased {bold}{cyan}Dagger{reset} for {yellow}{shop_weapons["Dagger"]["cost"]} Gold{reset}!\n")
                            time.sleep(1)
                            typewriter(f"You {bold}equip{reset} your new weapon!")
                            time.sleep(1)

                            # Modifies player stats to match weapon stats
                            player_stats["damage"] = shop_weapons["Dagger"]["damage"]

                            # Changes the player_inventory's "weapon" key value to the weapon purchased
                            player_inventory["weapon"] = f"{cyan}Dagger{reset}"

                            typewriter(f"\nYour {red}damage{reset} is now {bold}{light_red}{shop_weapons["Dagger"]["damage"]}{reset}!\n")
                            time.sleep(1)
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Thank you very much for your purchase! Feel free to continue exploring my shop.\n")
                            time.sleep(1)
                            typewriter(f"\n{bold}Your balance is now {yellow}{player_inventory["gold"]} Gold{reset}.\n")
                            time.sleep(1)
                            break
                    
                        elif "no" in user_confirmation:
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Very well then. Would you like to purchase something else?\n")
                            time.sleep(1)
                            continue
                        else:
                            print(f"\nPlease type {green}yes{reset} or {red}no{reset}.")
                            time.sleep(2)
                            continue

                if "katana" in user_choice:
                    if player_inventory["gold"] < shop_weapons["Katana"]["cost"]:
                        print(f"\n{red}Oops! You don't have enough {yellow}gold{red} to purchase this item!")
                        time.sleep(2)
                        continue

                    elif player_stats["damage"] > shop_weapons["Katana"]["damage"]:
                        print(f"\nThis item is {red}inferior{reset} to the current weapon you have equipped. Please choose a different item.")
                        time.sleep(2)
                        continue

                    elif player_stats["damage"] == shop_weapons["Katana"]["damage"]:
                        print(f"\nYou already have this weapon equipped!")
                        time.sleep(2) 
                        continue
                
                    
                    else:
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Fantastic choice! That will be {yellow}{shop_weapons["Katana"]["cost"]} Gold{reset}.\n")
                        time.sleep(1)
                        user_confirmation = input(f"{bold}Are you sure you want to make this purchase?{reset} ({green}Yes{reset}/{red}No{reset}): ").lower().strip()

                        if "yes" in user_confirmation:
                            player_inventory["gold"] -= shop_weapons["Katana"]["cost"]
                            typewriter(f"\nYou purchased {bold}{magenta}Katana{reset} for {yellow}{shop_weapons["Katana"]["cost"]} Gold{reset}!\n")
                            time.sleep(1)
                            typewriter(f"You {bold}equip{reset} your new weapon!")
                            time.sleep(1)

                            # Modifies player stats to match weapon stats
                            player_stats["damage"] = shop_weapons["Katana"]["damage"]

                            # Changes the player_inventory's "weapon" key value to the weapon purchased
                            player_inventory["weapon"] = f"{magenta}Katana{reset}"

                            typewriter(f"\nYour {red}damage{reset} is now {bold}{light_red}{shop_weapons["Katana"]["damage"]}{reset}!\n")
                            time.sleep(1)
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Thank you very much for your purchase! Feel free to continue exploring my shop.\n")
                            time.sleep(1)
                            typewriter(f"\n{bold}Your balance is now {yellow}{player_inventory["gold"]} Gold{reset}.\n")
                            time.sleep(1)
                            break
                    
                        elif "no" in user_confirmation:
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Very well then. Would you like to purchase something else?\n")
                            time.sleep(1)
                            continue
                        else:
                            print(f"\nPlease type {green}yes{reset} or {red}no{reset}.")
                            time.sleep(2)
                            continue

                if "mace" in user_choice:
                    if player_inventory["gold"] < shop_weapons["Mace"]["cost"]:
                        print(f"\n{red}Oops! You don't have enough {yellow}gold{red} to purchase this item!")
                        time.sleep(2)
                        continue

                    elif player_stats["damage"] > shop_weapons["Mace"]["damage"]:
                        print(f"\nThis item is {red}inferior{reset} to the current weapon you have equipped. Please choose a different item.")
                        time.sleep(2)
                        continue

                    elif player_stats["damage"] == shop_weapons["Mace"]["damage"]:
                        print(f"\nYou already have this weapon equipped!")
                        time.sleep(2) 
                        continue
                
                    
                    else:
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Fantastic choice! That will be {yellow}{shop_weapons["Mace"]["cost"]} Gold{reset}.\n")
                        time.sleep(1)
                        user_confirmation = input(f"{bold}Are you sure you want to make this purchase?{reset} ({green}Yes{reset}/{red}No{reset}): ").lower().strip()

                        if "yes" in user_confirmation:
                            player_inventory["gold"] -= shop_weapons["Mace"]["cost"]
                            typewriter(f"\nYou purchased {bold}{silver}Mace{reset} for {yellow}{shop_weapons["Mace"]["cost"]} Gold{reset}!\n")
                            time.sleep(1)
                            typewriter(f"You {bold}equip{reset} your new weapon!")
                            time.sleep(1)

                            # Modifies player stats to match weapon stats
                            player_stats["damage"] = shop_weapons["Mace"]["damage"]

                            # Changes the player_inventory's "weapon" key value to the weapon purchased
                            player_inventory["weapon"] = f"{silver}Mace{reset}"

                            typewriter(f"\nYour {red}damage{reset} is now {bold}{light_red}{shop_weapons["Mace"]["damage"]}{reset}!\n")
                            time.sleep(1)
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Thank you very much for your purchase! Feel free to continue exploring my shop.\n")
                            time.sleep(1)
                            typewriter(f"\n{bold}Your balance is now {yellow}{player_inventory["gold"]} Gold{reset}.\n")
                            time.sleep(1)
                            break
                    
                        elif "no" in user_confirmation:
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Very well then. Would you like to purchase something else?\n")
                            time.sleep(1)
                            continue
                        else:
                            print(f"\nPlease type {green}yes{reset} or {red}no{reset}.")
                            time.sleep(2)
                            continue

                elif "chromasaber" in user_choice:
                    if player_inventory["gold"] < shop_weapons["Chromasaber"]["cost"]:
                        print(f"\n{red}Oops! You don't have enough {yellow}gold{red} to purchase this item!")
                        time.sleep(2)
                        continue

                    elif player_stats["damage"] > shop_weapons["Chromasaber"]["damage"]:
                        print(f"\nThis item is {red}inferior{reset} to the current weapon you have equipped. Please choose a different item.")
                        time.sleep(2)
                        continue

                    elif player_stats["damage"] == shop_weapons["Chromasaber"]["damage"]:
                        print(f"\nYou already have this weapon equipped!")
                        time.sleep(2) 
                        continue
                    
                        
                    else:
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Fantastic choice! That will be {yellow}{shop_weapons["Chromasaber"]["cost"]} Gold{reset}.\n")
                        time.sleep(1)
                        user_confirmation = input(f"{bold}Are you sure you want to make this purchase?{reset} ({green}Yes{reset}/{red}No{reset}): ").lower().strip()

                        if "yes" in user_confirmation:
                            player_inventory["gold"] -= shop_weapons["Chromasaber"]["cost"]
                            typewriter(f"\nYou purchased "); print_rainbow("Chromasaber"); typewriter(f" for {yellow}{shop_weapons["Chromasaber"]["cost"]} Gold{reset}!\n")
                            time.sleep(2)
                            typewriter(f"You {bold}equip{reset} your new weapon!\n")
                            time.sleep(1)

                            # Modifies player stats to match weapon stats
                            player_stats["damage"] = shop_weapons["Chromasaber"]["damage"]

                            # Changes the player_inventory's "weapon" key value to the weapon purchased
                            player_inventory["weapon"] = f"{red}C{yellow}h{green}r{cyan}o{blue}m{magenta}a{red}s{yellow}a{green}b{cyan}e{blue}r{reset}"

                            typewriter(f"Your {red}damage{reset} is now {bold}{light_red}{shop_weapons["Chromasaber"]["damage"]}{reset}!\n")
                            time.sleep(1)
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Thank you very much for your purchase! Feel free to continue exploring my shop.\n")
                            time.sleep(1)
                            typewriter(f"\n{bold}Your balance is now {yellow}{player_inventory["gold"]} Gold{reset}.\n")
                            time.sleep(1)
                            break
                    
                        elif "no" in user_confirmation:
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Very well then. Would you like to purchase something else?")
                            time.sleep(1)
                            continue
                        else:
                            print(f"\nPlease type {green}yes{reset} or {red}no{reset}.")
                            time.sleep(2)
                            continue

                elif "exit" in user_choice:
                    break
            
                else:
                    print(f"\nThis choice is {red}invalid{reset}.")
                    time.sleep(2)
                    continue



        elif "potion" in action:
            in_potion_aisle = True
            
            while in_potion_aisle:

                # Shows the items in the aisle for the player to choose, including their current potion counts
                print(f"\n{bold}{green}~~~ Potion Aisle ~~~{reset}")
                print(f"{green}Potion{reset} - {light_green}Heals 10% of Max HP{reset} - Cost: {yellow}{shop_potions["Potion"]["cost"]} Gold{cyan} each")
                print(f"{orange}Super Potion{reset} - {light_green}Heals 25% of Max HP{reset} - Cost: {yellow}{shop_potions["Super Potion"]["cost"]} Gold{cyan} each")
                print(f"{light_magenta}Hyper Potion{reset} - {light_green}Heals 50% of Max HP{reset} - Cost: {yellow}{shop_potions["Hyper Potion"]["cost"]} Gold{cyan} each")
                print_rainbow("Rainbow Potion"); print(f" - {light_green}Heals 100% of Max HP{reset} - Cost: {yellow}{shop_potions["Rainbow Potion"]["cost"]} Gold{cyan} each{reset}\n")
                print(f"Your {green}Potions:{reset} {bold}{player_inventory["potions"]}{reset}")
                print(f"Your {orange}Super Potions:{reset} {bold}{player_inventory["super_potions"]}{reset}")
                print(f"Your {light_magenta}Hyper Potions:{reset} {bold}{player_inventory["hyper_potions"]}{reset}")
                print(f"Your ", end=""); print_rainbow("Rainbow Potions:"); print(f" {bold}{player_inventory["rainbow_potions"]}{reset}")
                print(f"\n{bold}You have {yellow}{player_inventory["gold"]} Gold{reset}\n")

                # Prompts the user on either exiting the aisle or purchasing an item of their choice from the provided list
                user_choice = input(f"{bold}Type any item in the aisle to purchase it or type {red}exit{white} to exit this aisle and return to the shop menu:{reset} ").lower().strip()

                if user_choice == "potion":

                    # Asks the user for the amount of the item they want to buy.
                    try:    
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Fantastic choice! How many {bold}{green}potions{reset} would you like?\n")
                        time.sleep(1)
                        amount = int(input(f"{bold}Type any number:{reset} ").lower().strip())
                    
                    # If the user types anything other than a number, then bring them back to the aisle
                    except ValueError:
                        print(f"\nPlease type a {bold}number{reset}.")
                        time.sleep(2)
                        continue

                    # Calculates total cost based on the amount of items the user wants
                    total_cost = shop_potions["Potion"]["cost"] * amount

                    # If the player's gold count in their inventory is less than the total cost of the items, then tell them they don't have enough gold.
                    if player_inventory["gold"] < total_cost:
                        print(f"\n{red}Oops! You don't have enough {yellow}gold{red} to purchase this!")
                        time.sleep(2)

                    # If they do have enough gold, proceed with the purchasing process, with the same logic in mind for the gears and weapons
                    else:
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Great! That will be {yellow}{shop_potions["Potion"]["cost"] * amount} Gold{reset} for {bold}{amount}{reset}.\n")
                        time.sleep(1)
                        user_confirmation = input(f"{bold}Are you sure you want to make this purchase?{reset} ({green}Yes{reset}/{red}No{reset}): ").lower().strip()
                        
                        if "yes" in user_confirmation:
                            player_inventory["gold"] -= total_cost
                            typewriter(f"\nYou purchased {bold}x{amount} {bold}{green}potion(s){reset} for {yellow}{shop_potions["Potion"]["cost"] * amount} Gold{reset}!\n")
                            time.sleep(1)
                            typewriter(f"You put the {green}potion(s){reset} in your {bold}bag{reset}!\n")
                            time.sleep(1)

                            # Modifies the player inventory (in this case, the potion count) with the amount of items purchased
                            player_inventory["potions"] += amount

                            typewriter(f"Your {green}Potion{reset} count is now {bold}{player_inventory["potions"]}{reset}!\n")
                            time.sleep(1)
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Thank you very much for your purchase! Feel free to continue exploring my shop.\n")
                            time.sleep(1)
                            typewriter(f"\n{bold}Your balance is now {yellow}{player_inventory["gold"]} Gold{reset}.\n")
                            time.sleep(1)
                            break
                        elif "no" in user_confirmation:
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Very well then. Would you like to purchase something else?")
                            time.sleep(1)
                            continue
                        else:
                            print(f"\nPlease type {green}yes{reset} or {red}no{reset}.")
                            time.sleep(2)
                            continue



                if user_choice == "super potion":

                    # Asks the user for the amount of the item they want to buy.
                    try:    
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Fantastic choice! How many {bold}{orange}super potions{reset} would you like?\n")
                        time.sleep(1)
                        amount = int(input(f"{bold}Type any number:{reset} ").lower().strip())
                    
                    # If the user types anything other than a number, then bring them back to the aisle
                    except ValueError:
                        print(f"\nPlease type a {bold}number{reset}.")
                        time.sleep(2)
                        continue

                    # Calculates total cost based on the amount of items the user wants
                    total_cost = shop_potions["Super Potion"]["cost"] * amount

                    # If the player's gold count in their inventory is less than the total cost of the items, then tell them they don't have enough gold.
                    if player_inventory["gold"] < total_cost:
                        print(f"\n{red}Oops! You don't have enough {yellow}gold{red} to purchase this!")
                        time.sleep(2)

                    # If they do have enough gold, proceed with the purchasing process, with the same logic in mind for the gears and weapons
                    else:
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Great! That will be {yellow}{shop_potions["Super Potion"]["cost"] * amount} Gold{reset} for {bold}{amount}{reset}.\n")
                        time.sleep(1)
                        user_confirmation = input(f"{bold}Are you sure you want to make this purchase?{reset} ({green}Yes{reset}/{red}No{reset}): ").lower().strip()
                        
                        if "yes" in user_confirmation:
                            player_inventory["gold"] -= total_cost
                            typewriter(f"\nYou purchased {bold}x{amount} {bold}{orange}super potion(s){reset} for {yellow}{shop_potions["Super Potion"]["cost"] * amount} Gold{reset}!\n")
                            time.sleep(1)
                            typewriter(f"You put the {orange}super potion(s){reset} in your {bold}bag{reset}!\n")
                            time.sleep(1)

                            # Modifies the player inventory (in this case, the potion count) with the amount of items purchased
                            player_inventory["super_potions"] += amount

                            typewriter(f"Your {orange}Super Potion{reset} count is now {bold}{player_inventory["super_potions"]}{reset}!\n")
                            time.sleep(1)
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Thank you very much for your purchase! Feel free to continue exploring my shop.\n")
                            time.sleep(1)
                            typewriter(f"{bold}Your balance is now {yellow}{player_inventory["gold"]} Gold{reset}.\n")
                            time.sleep(1)
                            break
                        elif "no" in user_confirmation:
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Very well then. Would you like to purchase something else?")
                            time.sleep(1)
                            continue
                        else:
                            print(f"\nPlease type {green}yes{reset} or {red}no{reset}.")
                            time.sleep(2)
                            continue

                if user_choice == "hyper potion":

                    # Asks the user for the amount of the item they want to buy.
                    try:    
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Fantastic choice! How many {bold}{light_magenta}hyper potions{reset} would you like?\n")
                        time.sleep(1)
                        amount = int(input(f"{bold}Type any number:{reset} ").lower().strip())
                    
                    # If the user types anything other than a number, then bring them back to the aisle
                    except ValueError:
                        print(f"\nPlease type a {bold}number{reset}.")
                        time.sleep(2)
                        continue

                    # Calculates total cost based on the amount of items the user wants
                    total_cost = shop_potions["Hyper Potion"]["cost"] * amount

                    # If the player's gold count in their inventory is less than the total cost of the items, then tell them they don't have enough gold.
                    if player_inventory["gold"] < total_cost:
                        print(f"\n{red}Oops! You don't have enough {yellow}gold{red} to purchase this!")
                        time.sleep(2)

                    # If they do have enough gold, proceed with the purchasing process, with the same logic in mind for the gears and weapons
                    else:
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Great! That will be {yellow}{shop_potions["Hyper Potion"]["cost"] * amount} Gold{reset} for {bold}{amount}{reset}.\n")
                        time.sleep(1)
                        user_confirmation = input(f"{bold}Are you sure you want to make this purchase?{reset} ({green}Yes{reset}/{red}No{reset}): ").lower().strip()
                        
                        if "yes" in user_confirmation:
                            player_inventory["gold"] -= total_cost
                            typewriter(f"\nYou purchased {bold}x{amount} {bold}{light_magenta}hyper potion(s){reset} for {yellow}{shop_potions["Hyper Potion"]["cost"] * amount} Gold{reset}!\n")
                            time.sleep(1)
                            typewriter(f"You put the {light_magenta}hyper potion(s){reset} in your {bold}bag{reset}!\n")
                            time.sleep(1)

                            # Modifies the player inventory (in this case, the potion count) with the amount of items purchased
                            player_inventory["hyper_potions"] += amount

                            typewriter(f"Your {light_magenta}Hyper Potion{reset} count is now {bold}{player_inventory["hyper_potions"]}{reset}!\n")
                            time.sleep(1)
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Thank you very much for your purchase! Feel free to continue exploring my shop.\n")
                            time.sleep(1)
                            typewriter(f"\n{bold}Your balance is now {yellow}{player_inventory["gold"]} Gold{reset}.\n")
                            time.sleep(1)
                            break
                        elif "no" in user_confirmation:
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Very well then. Would you like to purchase something else?")
                            time.sleep(1)
                            continue
                        else:
                            print(f"\nPlease type {green}yes{reset} or {red}no{reset}.")
                            time.sleep(2)
                            continue

                elif user_choice == "rainbow potion":

                    # Asks the user for the amount of the item they want to buy.
                    try:    
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Fantastic choice! How many "); print_rainbow("Rainbow Potions"); typewriter(" would you like?\n")
                        time.sleep(1)
                        amount = int(input(f"{bold}Type any number:{reset} ").lower().strip())
                    
                    # If the user types anything other than a number, then bring them back to the aisle
                    except ValueError:
                        print(f"\nPlease type a {bold}number{reset}.")
                        time.sleep(2)
                        continue

                    # Calculates total cost based on the amount of items the user wants
                    total_cost = shop_potions["Rainbow Potion"]["cost"] * amount

                    # If the player's gold count in their inventory is less than the total cost of the items, then tell them they don't have enough gold.
                    if player_inventory["gold"] < total_cost:
                        print(f"\n{red}Oops! You don't have enough {yellow}gold{red} to purchase this!")
                        time.sleep(2)

                    # If they do have enough gold, proceed with the purchasing process, with the same logic in mind for the gears and weapons
                    else:
                        print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter(f"Great! That will be {yellow}{shop_potions["Rainbow Potion"]["cost"] * amount} Gold{reset} for {bold}{amount}{reset}.\n")
                        time.sleep(1)
                        user_confirmation = input(f"{bold}Are you sure you want to make this purchase?{reset} ({green}Yes{reset}/{red}No{reset}): ").lower().strip()
                        
                        if "yes" in user_confirmation:
                            player_inventory["gold"] -= total_cost
                            typewriter(f"\nYou purchased {bold}x{amount} "); print_rainbow("Rainbow Potion(s)"); typewriter(f" for {yellow}{shop_potions["Rainbow Potion"]["cost"] * amount} Gold{reset}!\n")
                            time.sleep(1)
                            typewriter(f"You put the "); print_rainbow("rainbow potion(s)"); typewriter(f" in your {bold}bag{reset}!\n")
                            time.sleep(1)

                            # Modifies the player inventory (in this case, the potion count) with the amount of items purchased
                            player_inventory["rainbow_potions"] += amount

                            typewriter(f"Your "); print_rainbow("Rainbow Potion"); typewriter(f" count is now {bold}{player_inventory["rainbow_potions"]}{reset}!\n")
                            time.sleep(1)
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Thank you very much for your purchase! Feel free to continue exploring my shop.\n")
                            time.sleep(1)
                            typewriter(f"{bold}\nYour balance is now {yellow}{player_inventory["gold"]} Gold{reset}.\n")
                            time.sleep(1)
                            break
                        elif "no" in user_confirmation:
                            print(f"\n{bold}{light_yellow}Merchant:{reset} ", end=""); typewriter("Very well then. Would you like to purchase something else?\n")
                            time.sleep(2)
                            continue
                        else:
                            print(f"\nPlease type {green}yes{reset} or {red}no{reset}.")
                            time.sleep(2)
                            continue

                elif "exit" in user_choice:
                    break
            
                else:
                    print(f"\nThis choice is {red}invalid{reset}. Please type {bold}ONLY{reset} and {bold}EXACTLY{reset} an item displayed in the aisle. ({light_green}Perhaps you made a typo?{reset})")
                    time.sleep(2)
                    continue

        elif "exit" in action:
            print(f"\n{light_yellow}{bold}Merchant:{reset} ", end=""); typewriter("Thanks for visiting my shop! Come back at anytime! :)\n")
            time.sleep(1)
            typewriter("\nYou exit the shop and return to your home.\n")
            time.sleep(1)
            main()
            break
        else:
            print(f"\nThis action is {red}invalid{reset}. Please type any of the options prompted in the menu. ({light_green}Perhaps you made a typo?{reset})\n")
            time.sleep(3)
            continue


# Function to initiate a fight
def fight():

    # Asks the user who they want to battle
    print(f"\n{bold}{underline}Who would you like to fight?{reset}")
    print(f"{green}Random enemy{reset}")
    print(f"{red}{bold}BOSS{reset}")
    print(f"{light_brown}Return to main menu{reset}\n")

    user_choice = input(f"{bold}Type any of the options above here:{reset} ").lower().strip()

    # If they choose to battle a random enemy, pick a random enemy from the pool
    if "random" in user_choice:
        spawn_random_enemy()
        battle()
        return

        # If they choose to fight the boss, then make the player encounter the boss
    elif "boss" in user_choice:
        spawn_boss()
        battle_boss()
        return

        # If they chosse to return to the main menu, then make them return to the main menu
    elif "main menu" in user_choice:
        main()
    else:
        # Otherwise, say that the action is not valid and prompt the user to type an option in the menu.
        print(f"\nThis action is {red}invalid{reset}. Please type an option in the menu. ({light_green}Perhaps you made a typo?{reset})\n")
        fight()
    

# Function to battle
def battle():
    # Tells this function to update these global dictionaries
    global player_stats, player_inventory

    typewriter("\nYou set out for an adventure!")
    time.sleep(1)
    typewriter(f"\nYou grab your {bold}bag{reset} and bring it with you on your way out of your home.")
    time.sleep(1)
    typewriter(f"\nYou notice something {underline}peculiar{reset} and decide to check it out.\n")
    time.sleep(1)
    typewriter(f"\nYou walk into a {gray}dark cave{reset}...\n")
    time.sleep(1.5)

    # The chosen enemy's values returned from the "spawn random enemy" function is now assigned to a local variable that can be used in the function
    current_enemy = spawn_random_enemy()

    # Tell the player the enemy they ran into and their stats
    typewriter(f"\nA wild {bold}{underline}{current_enemy["name"]}{reset} has appeared!\n")
    time.sleep(1)
    print(f"{bold}{green}HP:{reset} {current_enemy["hp"]}/{current_enemy["max_hp"]}")
    print(f"{red}{bold}Damage:{reset} {current_enemy["damage"]}\n")
    time.sleep(2.5)

    while player_stats["hp"] > 0 and current_enemy["hp"] > 0:

        # Gives the player a choice of actions
        print(f"{bold}{underline}What will you do?{reset}")
        print(f"{light_red}Attack{reset}")
        print(f"{light_green}Heal")
        print(f"{blue}Run away{reset}\n")

        action = input(f"{bold}Type any of the options above here:{reset} ").lower().strip()

        # If they choose to attack, player deals damage to enemy and enemy deals damage to player, with each of them taking turns until one is defeated.
        if "attack" in action:

            # Function to make player inflict a critical hit on enemy
            def critical_hit_player():
                # Selects a random integer from 1 to 10.
                # If the following condition is true, then player damage is doubled, and the enemy loses that much health from the critical hit.
                if random.randint(1, 10) == 1:
                    damage = player_stats["damage"] * 2
                    player_stats["damage"] = damage
                    current_enemy["hp"] -= player_stats["damage"]
                    return True
                else:
                    return False
                    
            
            # Enemy takes damage from player
            damage = player_stats["damage"]
            
            if critical_hit_player() == True:
                typewriter(f"\nYou landed a {orange}{bold}critical hit{reset}!\n")
                time.sleep(0.5)
                typewriter(f"You dealt {orange}{player_stats["damage"]}{reset} damage to {bold}{current_enemy["name"]}{reset}!\n")
                player_stats["damage"] = int(player_stats["damage"] / 2)
                time.sleep(0.5)
            else:
                # If a critical hit didn't occur, deal regular damage.
                current_enemy["hp"] -= damage
                typewriter(f"\nYou dealt {red}{damage}{reset} damage to {bold}{current_enemy["name"]}{reset}!\n")
                time.sleep(0.5)

            # Prevents enemy HP from going under zero.
            if current_enemy["hp"] < 0:
                current_enemy["hp"] = 0

            
            # Player takes damage from enemy
            enemy_damage = current_enemy["damage"]

            # Function to make enemy inflict a critical hit on player
            def critical_hit_enemy():
                # Selects a random integer from 1 to 20. 
                # If the following condition is true, then enemy damage is doubled, and the player loses that much health from the critical hit.
                if random.randint(1, 20) == 1:
                    enemy_damage = current_enemy["damage"] * 2
                    current_enemy["damage"] = enemy_damage
                    player_stats["hp"] -= current_enemy["damage"]
                    return True
                else:
                    return False
                
            if critical_hit_enemy() == True:
                typewriter(f"\nOh no! {bold}{current_enemy["name"]}{reset} landed a {orange}{bold}critical hit{reset}!\n")
                time.sleep(0.5)
                typewriter(f"{bold}{current_enemy["name"]}{reset} dealt {orange}{current_enemy["damage"]}{reset} damage to you!\n")
                current_enemy["damage"] = int(current_enemy["damage"] / 2)
                time.sleep(0.5)
            else:
                # If a critical hit didn't occur, deal regular damage.
                player_stats["hp"] -= enemy_damage
                typewriter(f"\n{bold}{current_enemy["name"]}{reset} dealt {red}{current_enemy["damage"]}{reset} damage to you!\n")
                time.sleep(0.5)

            # Prevents player HP from going under zero.
            if player_stats["hp"] < 0:
                player_stats["hp"] = 0
            

            # Displays current health stats of both the player and enemy
            print("\n---------------------")
            print(f"{bold}{current_enemy["name"]}{reset} HP: {green}{current_enemy["hp"]}/{current_enemy["max_hp"]}{reset}")
            print(f"{bold}Your{reset} HP: {green}{player_stats["hp"]}/{player_stats["max_hp"]}{reset}")
            print("---------------------\n")
            time.sleep(2)

            # If both the player HP and the enemy HP hit zero at the same time, then player is healed by wizard and teleported home, despite enemy being defeated.
            if player_stats["hp"] <= 0 and current_enemy["hp"] <= 0:
                typewriter(f"You defeated {bold}{current_enemy["name"]}{reset}, but {bold}{current_enemy["name"]}{reset} also {red}defeated{reset} you...\n")
                time.sleep(1)
                typewriter(f"\nA {bold}{light_magenta}wizard{reset} spots you...\n")
                time.sleep(1)
                typewriter(f"The {bold}{light_magenta}wizard{reset} uses its magic wand to {light_green}heal{reset} you and teleports you back home.\n")
                player_stats["hp"] = player_stats["max_hp"]
                time.sleep(1)
                main()

            # If enemy HP hits zero, then tell the player that the enemy ran out of health. Gold is awarded to player and then player returns home
            elif current_enemy["hp"] <= 0:
                typewriter(f"{bold}{current_enemy["name"]}{reset} ran out of health!\n")
                time.sleep(0.5)
                typewriter(f"You have defeated {bold}{current_enemy["name"]}{reset}!\n")
                time.sleep(1)
                typewriter(f"\nYou earned {yellow}{bold}{current_enemy["gold"]} Gold {reset}from defeating {bold}{current_enemy["name"]}{reset}!\n")
                player_inventory["gold"] += current_enemy["gold"]
                time.sleep(0.5)
                typewriter(f"You collect the {yellow}gold{reset} dropped from {bold}{current_enemy["name"]}{reset}, exit the cave, and return home safely.\n")
                time.sleep(2)
                main()

            # If player HP hits zero, then tell the player that they have been defeated. Wizard notices player and heals them. Player is then teleported home.
            elif player_stats["hp"] <= 0:
                typewriter(f"\nOh no! You {red}ran out{reset} of health!\n")
                time.sleep(0.5)
                typewriter(f"\nYou have been {red}defeated{reset} by {bold}{current_enemy["name"]}{reset}!\n")
                time.sleep(1)
                typewriter(f"\nA {bold}{light_magenta}wizard{reset} spots you...\n")
                time.sleep(1)
                typewriter(f"The {bold}{light_magenta}wizard{reset} uses its magic wand to {light_green}heal{reset} you and teleports you back home.\n")
                player_stats["hp"] = player_stats["max_hp"]
                time.sleep(3)
                main()


        # If they choose to heal, then make the player choose which potion to use. 
        elif "heal" in action:

            search_keys = ["potions", "super_potions", "hyper_potions", "rainbow_potions"]

            # Menu will only be displayed if player has at least one potion in their inventory.
            if any(player_inventory.get(key, 0) > 0 for key in search_keys):

                in_heal_menu = True

                while in_heal_menu:

                    # Asks the player about which potion they want to use to heal themselves. Also shows the amounts of each potion currently in their inventory
                    print(f"\n{bold}{underline}What would you like to {light_green}heal{white} with?{reset}")
                    print(f"{green}Potion{reset} (You have {bold}{player_inventory["potions"]}{reset})")
                    print(f"{orange}Super Potion{reset} (You have {bold}{player_inventory["super_potions"]}{reset})")
                    print(f"{light_magenta}Hyper Potion{reset} (You have {bold}{player_inventory["hyper_potions"]}{reset})")
                    print_rainbow("Rainbow Potion"); print(f" (You have {bold}{player_inventory["rainbow_potions"]}{reset})\n")

                    user_choice = input(f"{bold}Type any of the options above or type {red}exit{white} to exit this menu:{reset} ").lower().strip()

                    # If the player chooses to use the potion, then go through the healing process. The same logic applies to all other options.
                    if user_choice == "potion":
                        if player_inventory["potions"] > 0:

                            # If the player is at full HP, then the potion is not used.
                            if player_stats["hp"] == player_stats["max_hp"] and player_inventory["potions"] > 0:
                                print(f"\nYou are already at {green}full health{reset}!")
                                time.sleep(2)

                            # Otherwise, heal the user with respect to the potion's heal value, along with decreasing the amount of the potion in their inventory by 1.
                            else:
                                typewriter(f"\nYou go into your {bold}bag{reset}, take out the {green}potion{reset}, and consume it.\n")
                                time.sleep(1)

                                heal_percentage = 0.1

                                # "int" is used to prevent decimals from showing on the screen
                                heal_value = int(player_stats["max_hp"] * heal_percentage)

                                # Ensures it heals at least 1 HP
                                if heal_value < 1:
                                    heal_value = 1

                                player_stats["hp"] += heal_value

                                # The potion is removed from the player's inventory
                                player_inventory["potions"] -= 1

                                # Prevents player from going over max HP after healing
                                if player_stats["hp"] > player_stats["max_hp"]:
                                        player_stats["hp"] = player_stats["max_hp"]

                                typewriter(f"You have {green}healed {bold}{light_green}{heal_value} HP{reset} from drinking the {green}potion{reset}!\n")
                                time.sleep(0.5)
                                print("\n---------------------")
                                print(f"{bold}{current_enemy["name"]}{reset} HP: {green}{current_enemy["hp"]}/{current_enemy["max_hp"]}{reset}")
                                print(f"{bold}Your{reset} HP: {green}{player_stats["hp"]}/{player_stats["max_hp"]}{reset}")
                                print("---------------------\n")
                                time.sleep(2)
                                break
                        else:
                            print(f"\nYou don't have any {green}potions{reset} to heal with!\n")
                            time.sleep(2)

                    if user_choice == "super potion":
                        if player_inventory["super_potions"] > 0:

                            # If the player is at full HP, then the potion is not used.
                            if player_stats["hp"] == player_stats["max_hp"] and player_inventory["super_potions"] > 0:
                                print(f"\nYou are already at {green}full health{reset}!")
                                time.sleep(2)

                            # Otherwise, heal the user with respect to the potion's heal value, along with decreasing the amount of the potion in their inventory by 1.
                            else:
                                typewriter(f"\nYou go into your {bold}bag{reset}, take out the {orange}super potion{reset}, and consume it.\n")
                                time.sleep(1)

                                heal_percentage = 0.25

                                # "int" is used to prevent decimals from showing on the screen
                                heal_value = int(player_stats["max_hp"] * heal_percentage)

                                # Ensures it heals at least 1 HP
                                if heal_value < 1:
                                    heal_value = 1

                                player_stats["hp"] += heal_value

                                # The potion is removed from the player's inventory
                                player_inventory["super_potions"] -= 1

                                # Prevents player from going over max HP after healing
                                if player_stats["hp"] > player_stats["max_hp"]:
                                        player_stats["hp"] = player_stats["max_hp"]

                                typewriter(f"You have {green}healed {bold}{light_green}{heal_value} HP{reset} from drinking the {orange}super potion{reset}!\n")
                                time.sleep(0.5)
                                print("\n---------------------")
                                print(f"{bold}{current_enemy["name"]}{reset} HP: {green}{current_enemy["hp"]}/{current_enemy["max_hp"]}{reset}")
                                print(f"{bold}Your{reset} HP: {green}{player_stats["hp"]}/{player_stats["max_hp"]}{reset}")
                                print("---------------------\n")
                                time.sleep(2)
                                break
                        else:
                            print(f"\nYou don't have any {orange}super potions{reset} to heal with!\n")
                            time.sleep(2)

                    if user_choice == "hyper potion":
                        if player_inventory["hyper_potions"] > 0:

                            # If the player is at full HP, then the potion is not used.
                            if player_stats["hp"] == player_stats["max_hp"] and player_inventory["hyper_potions"] > 0:
                                print(f"\nYou are already at {green}full health{reset}!")
                                time.sleep(2)

                            # Otherwise, heal the user with respect to the potion's heal value, along with decreasing the amount of the potion in their inventory by 1.
                            else:
                                typewriter(f"\nYou go into your {bold}bag{reset}, take out the {light_magenta}hyper potion{reset}, and consume it.\n")
                                time.sleep(1)

                                heal_percentage = 0.5

                                # "int" is used to prevent decimals from showing on the screen
                                heal_value = int(player_stats["max_hp"] * heal_percentage)

                                # Ensures it heals at least 1 HP
                                if heal_value < 1:
                                    heal_value = 1

                                player_stats["hp"] += heal_value

                                # The potion is removed from the player's inventory
                                player_inventory["hyper_potions"] -= 1

                                # Prevents player from going over max HP after healing
                                if player_stats["hp"] > player_stats["max_hp"]:
                                        player_stats["hp"] = player_stats["max_hp"]

                                typewriter(f"You have {green}healed {bold}{light_green}{heal_value} HP{reset} from drinking the {light_magenta}hyper potion{reset}!\n")
                                time.sleep(0.5)
                                print("\n---------------------")
                                print(f"{bold}{current_enemy["name"]}{reset} HP: {green}{current_enemy["hp"]}/{current_enemy["max_hp"]}{reset}")
                                print(f"{bold}Your{reset} HP: {green}{player_stats["hp"]}/{player_stats["max_hp"]}{reset}")
                                print("---------------------\n")
                                time.sleep(2)
                                break
                        else:
                            print(f"\nYou don't have any {light_magenta}hyper potions{reset} to heal with!\n")
                            time.sleep(2)

                    elif user_choice == "rainbow potion":
                        if player_inventory["rainbow_potions"] > 0:

                            # If the player is at full HP, then the potion is not used.
                            if player_stats["hp"] == player_stats["max_hp"] and player_inventory["rainbow_potions"] > 0:
                                print(f"\nYou are already at {green}full health{reset}!")
                                time.sleep(2)

                            # Otherwise, heal the user with respect to the potion's heal value, along with decreasing the amount of the potion in their inventory by 1.
                            else:
                                typewriter(f"\nYou go into your {bold}bag{reset}, take out the "); print_rainbow("Rainbow Potion"); typewriter(", and consume it.\n")
                                time.sleep(1)

                                heal_percentage = 1

                                # "int" is used to prevent decimals from showing on the screen
                                heal_value = int(player_stats["max_hp"] * heal_percentage)

                                # Ensures it heals at least 1 HP
                                if heal_value < 1:
                                    heal_value = 1

                                player_stats["hp"] += heal_value

                                # The potion is removed from the player's inventory
                                player_inventory["rainbow_potions"] -= 1

                                # Prevents player from going over max HP after healing
                                if player_stats["hp"] > player_stats["max_hp"]:
                                        player_stats["hp"] = player_stats["max_hp"]

                                typewriter(f"You have {light_green}{bold}fully healed{reset} from drinking the "); print_rainbow("Rainbow Potion"); typewriter("!\n")
                                time.sleep(0.5)
                                print("\n---------------------")
                                print(f"{bold}{current_enemy["name"]}{reset} HP: {green}{current_enemy["hp"]}/{current_enemy["max_hp"]}{reset}")
                                print(f"{bold}Your{reset} HP: {green}{player_stats["hp"]}/{player_stats["max_hp"]}{reset}")
                                print("---------------------\n")
                                time.sleep(2)
                                break
                        else:
                            print(f"\nYou don't have any ", end=""); print_rainbow("Rainbow Potions"); print(" to heal with!\n")
                            time.sleep(2)

                    elif user_choice == "exit":
                        print("")
                        break

                    else:
                        print(f"\nPlease type {bold}ONLY{reset} and {bold}EXACTLY{reset} the item you want to heal with. ({light_green}Perhaps you made a typo?{reset})")
                        time.sleep(3)


            else:
                print(f"\nOops! You don't have anything to {light_green}heal{reset} with!\n")
                time.sleep(2)
        

        # If they chosse to run, there is a 50% chance for them to escape, exit the cave, and return to the main menu.
        elif "run" in action:
            if random.randint(1, 2) == 1:

                # Player successfully escapes the cave and returns home
                typewriter("\nYou attempt an escape...\n")

                # Delay of 1 second
                time.sleep(1)

                typewriter(f"You escaped {light_green}successfully{reset}! You exit the cave and return to your home safely.\n")
                time.sleep(1)

                # Returns to the main menu
                main()
                break
            
            else:

                # Player fails to escape and takes damage from enemy as a result.
                typewriter("\nYou attempt an escape...\n")

                # Delay of 1 second
                time.sleep(1)

                typewriter(f"Oh no! You tripped and {light_red}failed to escape{reset}!\n")
                time.sleep(1)

                # Player takes damage from enemy
                enemy_damage = current_enemy["damage"]

                def critical_hit_enemy():
                    if random.randint(1, 20) == 1:
                        enemy_damage = current_enemy["damage"] * 2
                        current_enemy["damage"] = enemy_damage
                        player_stats["hp"] -= current_enemy["damage"]
                        return True
                    else:
                        return False
                    
                if critical_hit_enemy() == True:
                    typewriter(f"\nOh no! {bold}{current_enemy["name"]}{reset} landed a {orange}{bold}critical hit{reset}!\n")
                    time.sleep(0.5)
                    typewriter(f"{bold}{current_enemy["name"]}{reset} dealt {orange}{current_enemy["damage"]}{reset} damage to you!\n")
                    current_enemy["damage"] = int(current_enemy["damage"] / 2)
                    time.sleep(0.5)
                else:
                    # If no critical hit occurs, deal only regular damage.
                    player_stats["hp"] -= enemy_damage
                    typewriter(f"\n{bold}{current_enemy["name"]}{reset} dealt {red}{current_enemy["damage"]}{reset} damage to you!\n")
                    time.sleep(0.5)
            
                critical_hit_enemy()
            
                print("\n---------------------")
                print(f"{bold}{current_enemy["name"]}{reset} HP: {green}{current_enemy["hp"]}/{current_enemy["max_hp"]}{reset}")
                print(f"{bold}Your{reset} HP: {green}{player_stats["hp"]}/{player_stats["max_hp"]}{reset}")
                print("---------------------\n")
                time.sleep(2)

                if player_stats["hp"] <= 0:
                    typewriter(f"\nOh no! You {red}ran out{reset} of health!\n")
                    time.sleep(0.5)
                    typewriter(f"\nYou have been {red}defeated{reset} by {bold}{current_enemy["name"]}{reset}!\n")
                    time.sleep(1)
                    typewriter(f"\nA {bold}{light_magenta}wizard{reset} spots you...\n")
                    time.sleep(1)
                    typewriter(f"The {bold}{light_magenta}wizard{reset} uses its magic wand to {light_green}heal{reset} you and teleports you back home.\n")
                    player_stats["hp"] = player_stats["max_hp"]
                    time.sleep(3)
                    main()
        else:
            # Tells the player that their action is invalid; nothing will be done.
            print(f"\nOops! This action is {red}invalid{reset}! You stand frozen.\n")
            time.sleep(2)

def battle_boss():
    # Tells this function to update these global dictionaries
    global player_stats, player_inventory

    boss = spawn_boss()

    # The cutscene
    typewriter(f"\nYou decide to go on a {bold}{underline}VERY LONG{reset} adventure!\n")
    time.sleep(1)
    typewriter(f"You take your {bold}bag{reset} with you on your way out.\n")
    time.sleep(1)
    typewriter(f"You found a {gray}{bold}very ominous cave{reset}...\n")
    time.sleep(0.5)
    typewriter(f"You feel very {underline}ambitious{reset}, so you decide to walk inside!\n")
    time.sleep(1.5)
    typewriter(f"\n{bold}[ROARRRRRR!]{reset}")
    time.sleep(1)
    print(f"\n{bold}You:{reset} ", end=""); typewriter("What was that noise?!!!\n")
    time.sleep(1.5)
    typewriter(f"\nA very {underline}mysterious{reset} creature emerges from the dark...\n")
    time.sleep(1)
    typewriter(f"\nA ferocious {bold}{red}{underline}{boss["name"]}{reset} appeared!")
    time.sleep(0.5)
    print(f"\n{bold}{light_green}HP:{reset} {boss["hp"]}")
    print(f"{light_red}{bold}Damage:{reset} {boss["damage"]}\n")
    time.sleep(2)

    while boss["hp"] > 0 and player_stats["hp"] > 0:
    
        # Gives the player a choice of actions
        print(f"{bold}{underline}What will you do?{reset}")
        print(f"{light_red}Attack{reset}")
        print(f"{light_green}Heal")
        print(f"{blue}Run away{reset}\n")

        action = input(f"{bold}Type any of the options above here:{reset} ").lower().strip()

        # If they choose to attack, player deals damage to boss and boss deals damage to player, with each of them taking turns until one is defeated.
        if "attack" in action:

            # Function to make player inflict a critical hit on boss
            def critical_hit_player():
                # Selects a random integer from 1 to 10.
                # If the following condition is true, then player damage is doubled, and the boss loses that much health from the critical hit.
                if random.randint(1, 10) == 1:
                    damage = player_stats["damage"] * 2
                    player_stats["damage"] = damage
                    boss["hp"] -= player_stats["damage"]
                    return True
                else:
                    return False
                    
            
            # Boss takes damage from player
            damage = player_stats["damage"]
            
            if critical_hit_player() == True:
                typewriter(f"\nYou landed a {orange}{bold}critical hit{reset}!\n")
                time.sleep(0.5)
                typewriter(f"You dealt {orange}{player_stats["damage"]}{reset} damage to {light_red}{bold}{boss["name"]}{reset}!\n")
                player_stats["damage"] = int(player_stats["damage"] / 2)
                time.sleep(0.5)
            else:
                # If a critical hit didn't occur, deal regular damage.
                boss["hp"] -= damage
                typewriter(f"\nYou dealt {red}{damage}{reset} damage to {light_red}{bold}{boss["name"]}{reset}!\n")
                time.sleep(0.5)

            # Prevents boss HP from going under zero
            if boss["hp"] < 0:
                boss["hp"] = 0

            
            # Player takes damage from boss
            boss_damage = boss["damage"]

            # Function to make boss inflict a critical hit on player
            def critical_hit_enemy():
                # Selects a random integer from 1 to 20. 
                # If the following condition is true, then boss damage is doubled, and the player loses that much health from the critical hit.
                if random.randint(1, 20) == 1:
                    boss_damage = boss["damage"] * 2
                    boss["damage"] = boss_damage
                    player_stats["hp"] -= boss["damage"]
                    return True
                else:
                    return False
                
            if critical_hit_enemy() == True:
                typewriter(f"\nOh no! {bold}{boss["name"]}{reset} landed a {orange}{bold}critical hit{reset}!\n")
                time.sleep(0.5)
                typewriter(f"{light_red}{bold}{boss["name"]}{reset} dealt {orange}{boss["damage"]}{reset} damage to you!\n")
                boss["damage"] = int(boss["damage"] / 2)
                time.sleep(0.5)
            else:
                # If a critical hit didn't occur, deal regular damage.
                player_stats["hp"] -= boss_damage
                typewriter(f"\n{light_red}{bold}{boss["name"]}{reset} dealt {red}{boss["damage"]}{reset} damage to you!\n")
                time.sleep(0.5)

            # Prevents player HP from going under zero
            if player_stats["hp"] < 0:
                player_stats["hp"] = 0
            

            # Displays current health stats of both the player and the boss
            print("\n--------------------------")
            print(f"{light_red}{bold}{boss["name"]}{reset} HP: {green}{boss["hp"]}/{boss["max_hp"]}{reset}")
            print(f"{bold}Your{reset} HP: {green}{player_stats["hp"]}/{player_stats["max_hp"]}{reset}")
            print("--------------------------\n")
            time.sleep(2)

            # If both the player HP and the boss HP hit zero at the same time, then player is healed by wizard and teleported home, despite enemy being defeated.
            if player_stats["hp"] <= 0 and boss["hp"] <= 0:
                typewriter(f"You defeated {light_red}{bold}{boss["name"]}{reset}, but {light_red}{bold}{boss["name"]}{reset} also {red}defeated{reset} you...\n")
                time.sleep(1)
                typewriter(f"\nA {bold}{light_magenta}wizard{reset} spots you...\n")
                time.sleep(1)
                typewriter(f"The {bold}{light_magenta}wizard{reset} uses its magic wand to {light_green}heal{reset} you and teleports you back home.\n")
                player_stats["hp"] = player_stats["max_hp"]
                time.sleep(1)
                main()

            # If boss HP hits zero, then tell the player that the boss ran out of health. Congratulates player for beating the RPG game, awards them gold, and returns to the main menu.
            elif boss["hp"] <= 0:
                typewriter(f"{light_red}{bold}{reset}{boss["name"]}{reset} ran out of health!\n")
                time.sleep(0.5)
                typewriter(f"{light_yellow}{bold}Congratulations!{reset} You have defeated the {light_red}{bold}{boss["name"]}{reset}!\n")
                time.sleep(1)
                print(f"\n{bold}You:{reset} ", end=""); typewriter(f"Yes! I have defeated the {bold}{red}{boss["name"]}{reset}!\n")
                time.sleep(2)
                print(f"\n{bold}{light_cyan}Game Creator:{reset} ", end=""); typewriter(f"Hello there! Game creator here! Congratulations on beating my very own {bold}text-based {orange}RPG{reset} game!\n")
                time.sleep(1.5)
                typewriter(f"You have went on numerous adventures....\n")
                time.sleep(1.5)
                typewriter("fought many foes...\n")
                time.sleep(1.5)
                typewriter("and met great people...\n")
                time.sleep(1)
                print(f"\n{light_yellow}{bold}Merchant:{reset} ", end=""); typewriter("Like me!\n")
                time.sleep(1.5)
                print(f"\n{bold}{light_cyan}Game Creator:{reset} ", end=""); typewriter("...that helped you make this achievement become a reality.\n")
                time.sleep(1)
                typewriter(f"You shall rest now, my friend, and thank you so much for playing this game, it really means {underline}a lot{reset} to me. :D\n")
                time.sleep(2)
                typewriter(f"\nYou return home {light_green}happily ever after{reset}. :)\n\n")
                time.sleep(2)
                typewriter(f"{bold}{light_green}THE END{reset}")
                time.sleep(1)
                sys.exit()

            # If player HP hits zero, then tell the player that they have been defeated. Wizard notices player and heals them. Player is then teleported home.
            elif player_stats["hp"] <= 0:
                typewriter(f"Oh no! You {red}ran out{reset} of health!")
                time.sleep(0.5)
                typewriter(f"\nThe {bold}{light_red}{boss["name"]}{reset} has {red}defeated{reset} you!\n")
                time.sleep(1)
                print(f"\n{light_red}{bold}{boss["name"]}:{reset} ", end=""); typewriter(f"{bold}[MWHAHAHAHAHAHAHA!]{reset}\n")
                time.sleep(1)
                typewriter(f"\nA {bold}{light_magenta}wizard{reset} spots you...\n")
                time.sleep(1)
                typewriter(f"The {bold}{light_magenta}wizard{reset} uses its magic wand to {light_green}heal{reset} you and teleports you back home.\n")
                player_stats["hp"] = player_stats["max_hp"]
                time.sleep(3)
                main()


        # If they choose to heal, then make the player choose which potion to use. 
        elif "heal" in action:

            search_keys = ["potions", "super_potions", "hyper_potions", "rainbow_potions"]

            # Menu will only be displayed if player has at least one potion in their inventory.
            if any(player_inventory.get(key, 0) > 0 for key in search_keys):

                in_heal_menu = True

                while in_heal_menu:

                    # Asks the player about which potion they want to use to heal themselves. Also shows the amounts of each potion currently in their inventory
                    print(f"\n{bold}{underline}What would you like to {light_green}heal{white} with?{reset}")
                    print(f"{green}Potion{reset} (You have {bold}{player_inventory["potions"]}{reset})")
                    print(f"{orange}Super Potion{reset} (You have {bold}{player_inventory["super_potions"]}{reset})")
                    print(f"{light_magenta}Hyper Potion{reset} (You have {bold}{player_inventory["hyper_potions"]}{reset})")
                    print_rainbow("Rainbow Potion"); print(f" (You have {bold}{player_inventory["rainbow_potions"]}{reset})\n")

                    user_choice = input(f"{bold}Type any of the options above or type {red}exit{white} to exit this menu:{reset} ").lower().strip()

                    # If the player chooses to use the potion, then go through the healing process. The same logic applies to all other options.
                    if user_choice == "potion":
                        if player_inventory["potions"] > 0:

                            # If the player is at full HP, then the potion is not used.
                            if player_stats["hp"] == player_stats["max_hp"] and player_inventory["potions"] > 0:
                                print(f"\nYou are already at {green}full health{reset}!")
                                time.sleep(2)

                            # Otherwise, heal the user with respect to the potion's heal value, along with decreasing the amount of the potion in their inventory by 1.
                            else:
                                typewriter(f"\nYou go into your {bold}bag{reset}, take out the {green}potion{reset}, and consume it.\n")
                                time.sleep(1)

                                heal_percentage = 0.1

                                # "int" is used to prevent decimals from showing on the screen
                                heal_value = int(player_stats["max_hp"] * heal_percentage)

                                # Ensures it heals at least 1 HP
                                if heal_value < 1:
                                    heal_value = 1

                                player_stats["hp"] += heal_value

                                # The potion is removed from the player's inventory
                                player_inventory["potions"] -= 1

                                # Prevents player from going over max HP after healing
                                if player_stats["hp"] > player_stats["max_hp"]:
                                        player_stats["hp"] = player_stats["max_hp"]

                                typewriter(f"You have {green}healed {bold}{light_green}{heal_value} HP{reset} from drinking the {green}potion{reset}!\n")
                                time.sleep(0.5)
                                print("\n--------------------------")
                                print(f"{light_red}{bold}{boss["name"]}{reset} HP: {green}{boss["hp"]}/{boss["max_hp"]}{reset}")
                                print(f"{bold}Your{reset} HP: {green}{player_stats["hp"]}/{player_stats["max_hp"]}{reset}")
                                print("--------------------------\n")
                                time.sleep(2)
                                break
                        else:
                            print(f"\nYou don't have any {green}potions{reset} to heal with!\n")
                            time.sleep(2)

                    if user_choice == "super potion":
                        if player_inventory["super_potions"] > 0:

                            # If the player is at full HP, then the potion is not used.
                            if player_stats["hp"] == player_stats["max_hp"] and player_inventory["super_potions"] > 0:
                                print(f"\nYou are already at {green}full health{reset}!")
                                time.sleep(2)

                            # Otherwise, heal the user with respect to the potion's heal value, along with decreasing the amount of the potion in their inventory by 1.
                            else:
                                typewriter(f"\nYou go into your {bold}bag{reset}, take out the {orange}super potion{reset}, and consume it.\n")
                                time.sleep(1)

                                heal_percentage = 0.25

                                # "int" is used to prevent decimals from showing on the screen
                                heal_value = int(player_stats["max_hp"] * heal_percentage)

                                # Ensures it heals at least 1 HP
                                if heal_value < 1:
                                    heal_value = 1

                                player_stats["hp"] += heal_value

                                # The potion is removed from the player's inventory
                                player_inventory["super_potions"] -= 1

                                # Prevents player from going over max HP after healing
                                if player_stats["hp"] > player_stats["max_hp"]:
                                        player_stats["hp"] = player_stats["max_hp"]

                                typewriter(f"You have {green}healed {bold}{light_green}{heal_value} HP{reset} from drinking the {orange}super potion{reset}!\n")
                                time.sleep(0.5)
                                print("\n--------------------------")
                                print(f"{light_red}{bold}{boss["name"]}{reset} HP: {green}{boss["hp"]}/{boss["max_hp"]}{reset}")
                                print(f"{bold}Your{reset} HP: {green}{player_stats["hp"]}/{player_stats["max_hp"]}{reset}")
                                print("--------------------------\n")
                                time.sleep(2)
                                break
                        else:
                            print(f"\nYou don't have any {orange}super potions{reset} to heal with!\n")
                            time.sleep(2)

                    if user_choice == "hyper potion":
                        if player_inventory["hyper_potions"] > 0:

                            # If the player is at full HP, then the potion is not used.
                            if player_stats["hp"] == player_stats["max_hp"] and player_inventory["hyper_potions"] > 0:
                                print(f"\nYou are already at {green}full health{reset}!")
                                time.sleep(2)

                            # Otherwise, heal the user with respect to the potion's heal value, along with decreasing the amount of the potion in their inventory by 1.
                            else:
                                typewriter(f"\nYou go into your {bold}bag{reset}, take out the {light_magenta}hyper potion{reset}, and consume it.\n")
                                time.sleep(1)

                                heal_percentage = 0.5

                                # "int" is used to prevent decimals from showing on the screen
                                heal_value = int(player_stats["max_hp"] * heal_percentage)

                                # Ensures it heals at least 1 HP
                                if heal_value < 1:
                                    heal_value = 1

                                player_stats["hp"] += heal_value

                                # The potion is removed from the player's inventory
                                player_inventory["hyper_potions"] -= 1

                                # Prevents player from going over max HP after healing
                                if player_stats["hp"] > player_stats["max_hp"]:
                                        player_stats["hp"] = player_stats["max_hp"]

                                typewriter(f"You have {green}healed {bold}{light_green}{heal_value} HP{reset} from drinking the {light_magenta}hyper potion{reset}!\n")
                                time.sleep(0.5)
                                print("\n--------------------------")
                                print(f"{light_red}{bold}{boss["name"]}{reset} HP: {green}{boss["hp"]}/{boss["max_hp"]}{reset}")
                                print(f"{bold}Your{reset} HP: {green}{player_stats["hp"]}/{player_stats["max_hp"]}{reset}")
                                print("--------------------------\n")
                                time.sleep(2)
                                break
                        else:
                            print(f"\nYou don't have any {light_magenta}hyper potions{reset} to heal with!\n")
                            time.sleep(2)

                    elif user_choice == "rainbow potion":
                        if player_inventory["rainbow_potions"] > 0:

                            # If the player is at full HP, then the potion is not used.
                            if player_stats["hp"] == player_stats["max_hp"] and player_inventory["rainbow_potions"] > 0:
                                print(f"\nYou are already at {green}full health{reset}!")
                                time.sleep(2)

                            # Otherwise, heal the user with respect to the potion's heal value, along with decreasing the amount of the potion in their inventory by 1.
                            else:
                                typewriter(f"\nYou go into your {bold}bag{reset}, take out the "); print_rainbow("Rainbow Potion"); typewriter(", and consume it.\n")
                                time.sleep(1)

                                heal_percentage = 1

                                # "int" is used to prevent decimals from showing on the screen
                                heal_value = int(player_stats["max_hp"] * heal_percentage)

                                # Ensures it heals at least 1 HP
                                if heal_value < 1:
                                    heal_value = 1

                                player_stats["hp"] += heal_value

                                # The potion is removed from the player's inventory
                                player_inventory["rainbow_potions"] -= 1

                                # Prevents player from going over max HP after healing
                                if player_stats["hp"] > player_stats["max_hp"]:
                                        player_stats["hp"] = player_stats["max_hp"]

                                typewriter(f"You have {light_green}{bold}fully healed{reset} from drinking the "); print_rainbow("Rainbow Potion"); typewriter("!\n")
                                time.sleep(0.5)
                                print("\n--------------------------")
                                print(f"{light_red}{bold}{boss["name"]}{reset} HP: {green}{boss["hp"]}/{boss["max_hp"]}{reset}")
                                print(f"{bold}Your{reset} HP: {green}{player_stats["hp"]}/{player_stats["max_hp"]}{reset}")
                                print("--------------------------\n")
                                time.sleep(2)
                                break
                        else:
                            print(f"\nYou don't have any ", end=""); print_rainbow("Rainbow Potions"); print(" to heal with!\n")
                            time.sleep(2)

                    elif user_choice == "exit":
                        print("")
                        break

                    else:
                        print(f"\nPlease type {bold}ONLY{reset} and {bold}EXACTLY{reset} the item you want to heal with. ({light_green}Perhaps you made a typo?{reset})")
                        time.sleep(3)


            else:
                print(f"\nOops! You don't have anything to {light_green}heal{reset} with!\n")
                time.sleep(2)
        

        # If they chosse to run, there is a 50% chance for them to escape, exit the cave, and return to the main menu.
        elif "run" in action:
            if random.randint(1, 2) == 1:

                # Player successfully escapes the cave and returns home
                typewriter("\nYou attempt an escape...\n")

                # Delay of 1 second
                time.sleep(1)

                typewriter(f"You escaped {light_green}successfully{reset}! You exit the cave and return to your home safely.\n")
                time.sleep(1)

                # Returns to the main menu
                main()
                break
            
            else:

                # Player fails to escape and takes damage from enemy as a result.
                typewriter("\nYou attempt an escape...\n")

                # Delay of 1 second
                time.sleep(1)

                typewriter(f"Oh no! You tripped and {light_red}failed to escape{reset}!\n")
                time.sleep(1)

                # Player takes damage from enemy
                boss_damage = boss["damage"]

                def critical_hit_enemy():
                    if random.randint(1, 20) == 1:
                        boss_damage = boss["damage"] * 2
                        boss["damage"] = boss_damage
                        player_stats["hp"] -= boss["damage"]
                        return True
                    else:
                        return False
                    
                if critical_hit_enemy() == True:
                    typewriter(f"\nOh no! {light_red}{bold}{boss["name"]}{reset} landed a {orange}{bold}critical hit{reset}!\n")
                    time.sleep(0.5)
                    typewriter(f"{light_red}{bold}{boss["name"]}{reset} dealt {orange}{boss["damage"]}{reset} damage to you!\n")
                    boss["damage"] = int(boss["damage"] / 2)
                    time.sleep(0.5)
                else:
                    player_stats["hp"] -= boss_damage
                    typewriter(f"\n{light_red}{bold}{boss["name"]}{reset} dealt {red}{boss["damage"]}{reset} damage to you!\n")
                    time.sleep(0.5)
            
                critical_hit_enemy()
            
                print("\n--------------------------")
                print(f"{light_red}{bold}{boss["name"]}{reset} HP: {green}{boss["hp"]}/{boss["max_hp"]}{reset}")
                print(f"{bold}Your{reset} HP: {green}{player_stats["hp"]}/{player_stats["max_hp"]}{reset}")
                print("--------------------------\n")
                time.sleep(2)
        else:
            # Tells the player that their action is invalid; nothing will be done.
            print(f"\nOops! This action is {red}invalid{reset}! You stand frozen.\n")
            time.sleep(2)
            


def main():
    while playing:
        # Asks the player what they want to do
        print(f"\n{bold}{light_brown}--- Main Menu ---{reset}")
        print(f"{bold}{underline}What would you like to do?{reset}")
        print(f"{light_yellow}Show me how to play this game{reset}")
        print(f"{cyan}Show stats{reset}")
        print(f"{light_cyan}View inventory")
        print(f"{light_red}Fight{reset}")
        print(f"{yellow}Go to the shop{reset}")
        print(f"{light_green}Rest{reset}")
        print(f"{green}Show game version{reset}")
        print(f"{light_magenta}Start a new game{reset}")
        print(f"{blue}Save game{reset}")
        print(f"{red}Quit{reset}\n")

        action = input(f"{bold}Type any of the options above here:{reset} ").lower().strip()

        # If they say "show stats", then show player stats and go back to the main menu
        if "how to play" in action:
            print(f"{bold}{light_cyan}\nGame Creator:{reset} ", end=""); typewriter(f"Playing this game is {light_green}very simple{reset}!\n")
            time.sleep(1)
            typewriter(f"Fight enemies to earn {yellow}gold{reset}!\n")
            time.sleep(1)
            typewriter(f"You can do that by choosing the {bold}{light_red}Fight{reset} option in the {bold}{light_brown}Main menu{reset}.\n")
            time.sleep(1)
            typewriter(f"If you want to fight a {green}random enemy{reset} or the {light_red}BOSS{reset}, you can do that in the {bold}{light_red}Fight{reset} menu.\n")
            time.sleep(1)
            typewriter(f"If you are ever on {red}{underline}low health{reset} after a battle, be sure to heal up by using the {bold}{light_green}Rest{reset} option in the {bold}{light_brown}Main menu{reset}!\n")
            time.sleep(1)
            typewriter(f"Once you earn {yellow}gold{reset} from defeating enemies, you can then spend the {yellow}gold{reset} on some very {underline}useful items{reset} by heading to the {bold}{light_yellow}shop{reset}!\n")
            time.sleep(1)
            typewriter(f"These items from the {bold}{light_yellow}shop{reset} help you to defeat enemies {underline}faster{reset} and {underline}aid{reset} you in battle!\n")
            time.sleep(1)
            typewriter(f"Finally, there's the {light_red}{bold}BOSS{reset}, the strongest enemy in the game.\n")
            time.sleep(1)
            typewriter(f"If you defeat the {light_red}{bold}BOSS{reset}, then you beat the game!\n")
            time.sleep(1)
            typewriter(f"Now, off you go, {bold}{player_stats['name']}{reset}, and {underline}have fun{reset}! :D\n")
            time.sleep(1)

        
        elif "stats" in action:
            show_stats()

        # If they say "view inventory", open the inventory
        elif "inventory" in action:
            inventory()

        # If they choose to save and quit, save the game and thank the player for playing.
        elif "quit" in action:
            
            action = input(f"{bold}\nDo you want to {green}save{white} your game before quitting?{reset} ({light_green}Yes{white}/{light_red}No{reset}): ")

            if "yes" in action:
                save_game()
                time.sleep(0.5)
                typewriter("\nThanks for playing my text-based RPG game! Hope to see you again soon!\n")
                time.sleep(0.5)
                break
            elif "no" in action:
                typewriter("\nThanks for playing my text-based RPG game! Hope to see you again soon!")
                time.sleep(1)
                break
            else:
                print(f"\nPlease type an option in the menu. ({light_green}Perhaps you made a typo?{reset})")
                time.sleep(2)


        elif "save" in action:
            typewriter(f"\n{green}Saving{reset} your game...")
            time.sleep(1)
            save_game()
            time.sleep(0.5)

        # If they choose to start a new game, then wipe out current save data and start a new game.
        elif "new" in action:

            action = input(f"{bold}\nAre you sure you want to start a {light_magenta}new game{white}?{reset}\nThis will erase your current progress and start a fresh instance.{reset} ({light_green}Yes{white}/{light_red}No{reset}): ")

            if "yes" in action:
                start_new_game()
            elif "no" in action:
                main()
            else:
                print(f"\nPlease type an option in the menu. ({light_green}Perhaps you made a typo?{reset})")
                time.sleep(2)



        # If they type "version": display game version
        elif "version" in action:
            print(f"\n{bold}Game Version: {green}1.1{reset}")
            time.sleep(1.5)
            
            # If they choose to fight, prompt the player on which monster they want to fight
        elif "fight" in action:
            fight()
            break

            # If they choose to enter the treasure room, then check to see if the player has the key to enter the room
        elif "shop" in action:
            shop()
            break
            
            # If they choose to rest, then make them enter a bedroom and tell that that they have fully healed.
        elif "rest" in action:
            if player_stats["hp"] < player_stats["max_hp"]:
                typewriter(f"\nYou enter your {blue}bedroom{reset}...\n")
                time.sleep(1)
                typewriter(f"You get a good rest and feel fully {green}refreshed{reset}.\n")
                time.sleep(2)
                player_stats["hp"] = player_stats["max_hp"]
                typewriter(f"\nYou fully {light_green}healed{reset} to {bold}{green}{player_stats["max_hp"]} HP{reset}!\n")
                time.sleep(1)
            else:
                print(f"\nYou are already {light_green}well rested!{reset}")
                time.sleep(2)
                continue
             
        # Otherwise, say that the action is not valid.
        else:
            print(f"\nThis action is {red}invalid{reset}. Please type an option in the menu. ({light_green}Perhaps you made a typo?{reset})")
            time.sleep(2)

bootup()
main()