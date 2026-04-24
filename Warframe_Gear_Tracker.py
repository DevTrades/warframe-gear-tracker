import os
import difflib
import requests
import json

gear_list = {}

file_name = "gear_public.txt"

if os.path.exists(file_name):
    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            parts = line.split(",")
            name = parts[0]
            category = parts[1]
            owned = parts[2] == "True"
            mastered = parts[3] == "True"
            note = parts[4]
            gear_list[name] = {"category": category, "owned": owned, "mastered": mastered,
                               "note": note}

def display_menu():
    print("\n---Warframe Gear Menu---\n")
    print("1: Add gear to list")
    print("2: View item")
    print("3: View all gear")
    print("4: Remove item from list")
    print("5: Change item stats")
    print("6: Change item stats in bulk")
    print("7: See total stats")
    print("8: Save changes and exit")
    print("9: Help")

def sync_gear():
    url = "https://api.warframestat.us/items"
    response = requests.get(url)
    type_map = {"Warframe": "warframe", "Archwing": "vehicle",
                "Necramech": "warframe", "Rifle": "primary",
                "Bow": "primary", "Shotgun": "primary",
                "Sniper": "primary", "Launcher": "primary",
                "Kitgun Component": "primary", "Pistol": "secondary",
                "Dual Pistols": "secondary", "Melee": "melee",
                "Arch-Gun": "archgun", "Arch-Melee": "archmelee",
                "Amp": "amp", "Companion Weapon": "robotic",
                "Pets": "companion", "K-Drive Component": "vehicle",
                "Zaw Component": "primary", "Sentinel": "robotic",
                "Throwing": "secondary"}
    excluded = {"excalibur prime", "skana prime", "lato prime"}
    force_include = {
        "cantic prism": "amp",
        "granmu prism": "amp",
        "klamora prism": "amp",
        "lega prism": "amp",
        "mote prism": "amp",
        "rahn prism": "amp",
        "raplak prism": "amp",
        "shwaak prism": "amp",
        "mote amp": "amp",
        "sporelacer": "primary",
        "vermisplicer": "primary",
        "plexus": "vehicle",
        "amp": "amp",
    }
    if response.status_code == 200:
        data = response.json()
        for item in data:
            if item["name"].lower() in excluded:
                continue
            if item["type"] in type_map and item.get("masterable") == True:
                if item["name"].lower() not in gear_list.keys():
                    category = type_map[item["type"]]
                    mastered = False
                    owned = False
                    note = ""
                    gear_list[item["name"].lower()] = {"category": category, "owned": owned,
                                   "mastered": mastered, "note": note}
        for name, category in force_include.items():
            if name not in gear_list.keys():
                gear_list[name] = {"category": category, "owned": False, "mastered": False, "note": ""}
        save_sync()
        print("Warframe gear has been updated\n")
    else:
        print(f"API upload failed -- {response.status_code}\n")

def add_gear():
    print("\n Add gear --press enter to during naming process to exit")
    is_naming = True
    while is_naming:
        name = input("Please enter name of gear: ")
        if name == "":
            is_naming = False
            print("Exiting")
            return
        else:
            if name in gear_list.keys():
                print(f"{name} already exists. Returning to main menu")
                return
            else:
                print(f"\n{'1: Warframe':<8} {'2: Primary':<8} {'3: Secondary'}")
                print(f"{'4: Melee':<8} {'5: Robotic':<8} {'6: Companion'}")
                print(f"{'7: Vehicle':<8} {'8: Arch gun':<8} {'9: Arch melee'}")
                print(f"{'10: Amp':<8}\n")
                category = input("Please enter category of gear - (use number): ")
                if category == "1":
                    category = "warframe"
                elif category == "2":
                    category = "primary"
                elif category == "3":
                    category = "secondary"
                elif category == "4":
                    category = "melee"
                elif category == "5":
                    category = "robotic"
                elif category == "6":
                    category = "companion"
                elif category == "7":
                    category = "vehicle"
                elif category == "8":
                    category = "archgun"
                elif category == "9":
                    category = "archmelee"
                elif category == "10":
                    category = "amp"
                else:
                    print("invalid input, please select 1-10")
                    return
                owned = input("Item acquired? (yes/no): ") == "yes"
                if owned:
                    mastered = input("Item mastered? (yes/no): ") == "yes"
                    note = input("Enter note or press enter to skip ")
                else:
                    mastered = False
                    note = ""
                gear_list[name] = {"category": category, "owned": owned,
                                   "mastered": mastered, "note": note}
                print(f"{name} added to list")

def view_gear():
    name = input("Please enter name of gear you wish to check: ")
    if name in gear_list.keys():
        details = gear_list[name]
        owned_box = "[X]" if details['owned'] else "[]"
        mastered_box = "[X]" if details['mastered'] else "[]"
        print(f"\n--- {name} ---")
        print(f"  Category: {details['category'].title()}")
        print(f"  Owned: {owned_box}")
        print(f"  Mastered: {mastered_box}")
        if details['note'] != "":
            print(f"  Note: {details['note']}")
    else:
        close_matches = difflib.get_close_matches(name, gear_list.keys(), n=3, cutoff=0.6)
        if len(close_matches) == 0:
            print(f"No item found with matching {name}")
        else:
            print(f"\nNo items found, did you mean?")
            for i, match in enumerate(close_matches):
                print(f"  {i + 1}: {match}")
            print(f"  {len(close_matches) + 1}: None of these - return")
            suggestion_choice = input("\nEnter your choice ")
            try:
                suggestion_choice = int(suggestion_choice)
            except ValueError:
                print("Not a valid choice, returning to menu")
                return
            if 1<= suggestion_choice <= len(close_matches):
                chosen = close_matches[suggestion_choice - 1]
                details = gear_list[chosen]
                owned_box = "[X]" if details['owned'] else "[ ]"
                mastered_box = "[X]" if details['mastered'] else "[ ]"
                print(f"\n--- {chosen} ---")
                print(f"  Category: {details['category'].title()}")
                print(f"  Owned   : {owned_box}")
                print(f"  Mastered: {mastered_box}")
                if details['note'] != "":
                    print(f"  Note    : {details['note']}")
            else:
                return

def view_all_gear():
    if len(gear_list) == 0:
        print("No gears available. Returning to main menu")
        return
    else:
        while True:
            categories = set(details['category'] for name, details in gear_list.items())
            print("\n--- Gear Summary ---")
            for category in categories:
                total = len([name for name, details in gear_list.items()
                            if details['category'] == category])
                owned = len([name for name, details in gear_list.items()
                            if details['category'] == category and details['owned']])
                mastered = len([name for name, details in gear_list.items()
                                if details['category'] == category and details['mastered']])
                print(f"  {category.title():<12} : {owned}/{total} acquired | {mastered}/{total} mastered")
            print("...\n")
            category_choice = input("Please select a category you wish to view (press enter to go back) ")
            if category_choice == "":
                return
            elif category_choice.lower() not in categories:
                print(f"{category_choice.title()} does not exist.")
            else:
                while True:
                    print(f"\n--- {category_choice.title()} ---")
                    print("1: Not acquired")
                    print("2: Acquired but not mastered")
                    print("3: Fully mastered")
                    print("4: Show all")
                    filter_choice = input("Enter your choice (press enter to go back) ")
                    if filter_choice == "":
                        break
                    elif filter_choice == "1":
                        result = [(name, details) for name, details in gear_list.items()
                                  if details['category'] == category_choice.lower() and not details['owned']]
                    elif filter_choice == "2":
                        result = [(name, details) for name, details in gear_list.items()
                                  if details['category'] == category_choice.lower() and details['owned'] and not details['mastered']]
                    elif filter_choice == "3":
                        result = [(name, details) for name, details in gear_list.items()
                                  if details['category'] == category_choice.lower() and details['owned'] and details['mastered']]
                    elif filter_choice == "4":
                        result = [(name, details) for name, details in gear_list.items()
                                  if details['category'] == category_choice.lower()]
                    else:
                        print("Invalid choice")
                        continue
                    if len(result) == 0:
                        print("No items found for that filter")
                    else:
                        for name, details in result:
                                owned_box = "[X]" if details['owned'] else "[]"
                                mastered_box = "[X]" if details['mastered'] else "[]"
                                print(f"\n--- {name} ---")
                                print(f"  Owned: {owned_box}")
                                print(f"  Mastered: {mastered_box}")
                                if details['note'] != "":
                                    print(f"  Note: {details['note']}")

def remove_gear():
    name = input("Please enter name of gear you wish to remove: ")
    if name in gear_list.keys():
        start_choice = input("1: yes\n  2: no")
        if start_choice == "1":
            del gear_list[name]
            print(f"{name} removed from list")
            return
        else:
            print("Cancelled, returning to main menu")
            return
    else:
        close_matches = difflib.get_close_matches(name, gear_list.keys())
        if len(close_matches) == 0:
            print(f"No item found matching {name}")
            return
        else:
            print(f"\nNo item found... did you mean?")
            for i, match in enumerate(close_matches):
                print(f"  {i + 1}: {match}")
            print(f"  {len(close_matches) + 1}: None of these - return")
            suggestion_choice = input("Enter your choice ")
            try:
                suggestion_choice = int(suggestion_choice)
            except ValueError:
                print("Invalid choice, returning to menu")
                return
            if 1 <= suggestion_choice <= len(close_matches):
                chosen = close_matches[suggestion_choice - 1]
                print(f"Are you sure you want to delete {chosen}?")
                user_choice = input(  "1: yes\n  2: no")
                if user_choice == "1":
                    del gear_list[chosen]
                    print(f"{chosen} removed from list")
                else:
                    print(f"\n{chosen} was not deleted, returning to menu")
                    return
            else:
                return

def check_stats():
    if len(gear_list) == 0:
        print("No gears available. Returning to main menu")
        return
    else:
        total = len(gear_list)
        owned = len([name for name, details in gear_list.items() if details['owned']])
        mastered = len([name for name, details in gear_list.items() if details['mastered']])
        percentage_owned = (owned/total)*100
        percentage_mastered = (mastered/total)*100
        items_left = (total - owned)
        mastered_left = (total - mastered)
        print("\n--- Warframe gear Tracker ---")
        print(f"{'Total items':<14} : {total}")
        print(f"{'Acquired':<14} : {owned}/{total} ({percentage_owned:.1f}%)")
        print(f"{'Mastered':<14} : {mastered}/{total} ({percentage_mastered:.1f}%)")
        print(f"{'Not acquired':<14} : {items_left}")
        print(f"{'Needs mastered':<14} : {mastered_left}")

        print("\n--- Progress by Category ---")
        categories = set(details['category'] for name, details in gear_list.items())
        for category in categories:
            category_total = len([name for name, details in gear_list.items()
                         if details['category'] == category])
            category_owned = len([name for name, details in gear_list.items()
                         if details['category'] == category and details['owned']])
            category_mastered = len([name for name, details in gear_list.items()
                            if details['category'] == category and details['mastered']])
            category_percentage_owned = (category_owned/category_total)*100
            category_percentage_mastered = (category_mastered/category_total)*100
            print(f"{category.title():<14} : {category_owned}/{category_total} acquired - {category_percentage_owned:.1f}% | {category_mastered}/{category_total} mastered - {category_percentage_mastered:.1f}%")
        input("\nPress enter to go back")

def change_status():
    name = input("Enter item name ")
    if name not in gear_list.keys():
        close_matches = difflib.get_close_matches(name, gear_list.keys())
        if len(close_matches) == 0:
            print(f"\nNo item found matching {name}, returning to menu")
            return
        else:
            print(f"\nNo item found.. did you mean?")
            for i, match in enumerate(close_matches):
                print(f"  {i + 1}: {match}")
            print(f"  {len(close_matches) + 1}: None of these - return")
            suggestion_choice = input("\nEnter your choice ")
            try:
                suggestion_choice = int(suggestion_choice)
            except ValueError:
                print("Invalid choice, returning to menu")
                return
            if 1 <= suggestion_choice <= len(close_matches):
                chosen = close_matches[suggestion_choice - 1]
                details = gear_list[chosen]
                owned_box = "[X]" if details['owned'] else "[]"
                mastered_box = "[X]" if details['mastered'] else "[]"
                print(f"\n--- {chosen} ---")
                print(f"  Owned: {owned_box}")
                print(f"  Mastered: {mastered_box}")
                if details['note'] != "":
                    print(f"  Note: {details['note']}")
                print("\n")
                print("1: Toggle Owned")
                print("2: Toggle Mastered")
                print("3: Edit note")
                print("4: Cancel")
                choice = input("Please select an option ")
                if choice == "1":
                    gear_list[chosen]['owned'] = not gear_list[chosen]['owned']
                    owned_box = "[X]" if gear_list[chosen]['owned'] else "[]"
                    print(f"\n status has been changed to | {owned_box}")
                elif choice == "2":
                    gear_list[chosen]['mastered'] = not gear_list[chosen]['mastered']
                    mastered_box = "[X]" if gear_list[chosen]['mastered'] else "[]"
                    print(f"\n status has been changed to | {mastered_box}")
                elif choice == "3":
                    note = input("Add your note here...")
                    gear_list[chosen]['note'] = note
                elif choice == "4":
                    return
                else:
                    print("Invalid input, returning to main menu")
                    return

    else:
        details = gear_list[name]
        owned_box = "[X]" if details['owned'] else "[]"
        mastered_box = "[X]" if details['mastered'] else "[]"
        print(f"\n--- {name} ---")
        print(f"  Owned: {owned_box}")
        print(f"  Mastered: {mastered_box}")
        if details['note'] != "":
            print(f"  Note: {details['note']}")
        print("\n")
        print("1: Toggle Owned")
        print("2: Toggle Mastered")
        print("3: Edit note")
        print("4: Cancel")
        choice = input("Please select an option ")
        if choice == "1":
            gear_list[name]['owned'] = not gear_list[name]['owned']
            owned_box = "[X]" if gear_list[name]['owned'] else "[]"
            print(f"\n status has been changed to | {owned_box}")
        elif choice == "2":
            gear_list[name]['mastered'] = not gear_list[name]['mastered']
            mastered_box = "[X]" if gear_list[name]['mastered'] else "[]"
            print(f"\n status has been changed to | {mastered_box}")
        elif choice == "3":
            note = input("Add your note here...")
            gear_list[name]['note'] = note
        elif choice == "4":
            return
        else:
            print("Invalid input, returning to main menu")

def bulk_update():
    raw = input("Enter item names separated by commas ")
    items = [item.strip() for item in raw.split(",")]

    found = []
    not_found = []

    for item in items:
        if item in gear_list.keys():
            found.append(item)
        else:
            suggestions = difflib.get_close_matches(item, gear_list.keys(), n=3, cutoff=0.6)
            if len(suggestions) == 0:
                print(f"{item} not found and no suggestions available -- skipping")
            else:
                not_found.append((item, suggestions))

    for original, suggestion in not_found:
        print(f"\n{original} not found.. did you mean? ")
        for i, match in enumerate(suggestion):
            print(f"  {i+1}. {match}")
        print(f"  {len(suggestion) + 1}: skip this item")
        try:
            suggestion_choice = int(input("\n Enter your choice: "))
        except ValueError:
            print("Invalid input -- skipping")
            continue
        if 1 <= suggestion_choice <= len(suggestion):
            found.append(suggestion[suggestion_choice - 1])
        else:
            print(f"Skipping {original}")
    if len(found) == 0:
        print("No valid items to update")
        return
    print(f"\n---Items to update---")
    for item in found:
        print(f"  {item}")
    print("\n1: Mark all as acquired")
    print("2: Mark all as mastered")
    print("3: Mark all as acquired and mastered")
    print("4: Cancel")
    choice = input("\nSelect option: ")

    if choice == "4" or choice == "":
        return
    elif choice not in ["1", "2", "3"]:
        print("Invalid input, returning to main menu")
        return

    confirm = input(f"Update {len(found)} items ? (yes/no) ")
    if confirm != "yes":
        print("Canceled")
        return

    for item in found:
        if choice == "1":
            gear_list[item]['owned'] = True
        elif choice == "2":
            gear_list[item]['mastered'] = True
        elif choice == "3":
            gear_list[item]['owned'] = True
            gear_list[item]['mastered'] = True

    print(f"\n--- Updated ---")
    for item in found:
        owned_box = "[X]" if gear_list[item]['owned'] else "[ ]"
        mastered_box = "[X]" if gear_list[item]['mastered'] else "[ ]"
        print(f"  {item:<30} Acquired: {owned_box}  Mastered: {mastered_box}")


def save_gear():
    if len(gear_list) == 0:
        print("No gears available. Returning to main menu")
    else:
        with open(file_name, "w") as f:
            for name, details in gear_list.items():
                f.write(f"{name},{details['category']},{details['owned']},{details['mastered']},{details['note']}\n")
        print("Gear saved to file..")

def save_sync():
    if len(gear_list) == 0:
        print("No gears available. Returning to main menu")
    else:
        with open(file_name, "w") as f:
            for name, details in gear_list.items():
                f.write(f"{name},{details['category']},{details['owned']},{details['mastered']},{details['note']}\n")

def help_menu():
    print("""1. Add Gear \n
    Manually add an item to your tracker. You will be prompted for the item 
    name, category, ownership status, mastery status, and an optional note. 
    Note that modular weapon components such as Zaw blades, Kitgun parts, and Amp prisms 
    cannot always be retrieved by the API and may need to be added through this option.\n""")

    print("""2. View Item \n
    Search for a specific item by name and display its current tracking details. If no exact 
    match is found, the tracker will suggest close matches automatically.\n""")

    print("""3. View All Gear \n
    Browse your entire collection organized by category. From here you can filter items 
    by acquisition and mastery status within each category.\n""")

    print("""4. Remove Item \n
    Permanently remove an item from your tracker. You will be asked to confirm before deletion. 
    If no exact match is found, close matches will be suggested.\n""")

    print("""5. Change Item Stats \n
    Update the owned status, mastered status, or note for a single item. Supports fuzzy matching 
    if the exact name is not found.\n""")

    print("""6. Bulk Update \n
    Update multiple items at once by entering their names separated by commas. Useful for marking 
    several items as acquired or mastered in one operation.\n""")

    print("""7. Total Stats \n
    Display a full breakdown of your collection progress including overall acquisition and mastery 
    percentages, items remaining, and a per-category summary.\n""")

    print("""8. Save and Exit \n
    Save all changes to your gear file and exit the program. You will be given the option to save 
    or exit without saving.\n""")

    print("""9. Help \n
    Display this menu.\n""")

    input("Please press enter to go back.")

sync_gear()
is_running = True
while is_running:
    display_menu()
    choice = input("Please enter your choice: ")
    if choice == "1":
        add_gear()
    elif choice == "2":
        view_gear()
    elif choice == "3":
        view_all_gear()
    elif choice == "4":
        remove_gear()
    elif choice == "5":
        change_status()
    elif choice == "6":
        bulk_update()
    elif choice == "7":
        check_stats()
    elif choice == "8":
        warning_message = input("Enter 1 to save before exiting, press enter to exit the program. ")
        if warning_message == "1":
            save_gear()
        print("Goodbye!")
        is_running = False
    elif choice == "9":
        help_menu()
    else:
        print("Please enter a valid input")