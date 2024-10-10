from colorama import Fore, Style
from os import system, name

def clear():
    """Clears the console screen."""
    # For Windows
    if name == 'nt':
        _ = system('cls')
    # For macOS and Linux (here, os.name is 'posix')
    else:
        _ = system('clear')

clear()

def filter_combos(combo_list):
    domains = {}
    for combo in combo_list:
        try:
            email, password = combo.strip().split(":")
            domain = email.split("@")[1]
            if domain not in domains:
                domains[domain] = []
            domains[domain].append(combo)
        except ValueError:
            print(f"Invalid combo format: {combo}")

    for domain, combos in domains.items():
        combos = remove_duplicates(combos, f"{domain}_nodupes.txt")  # Remove duplicates and save to a new file
        combos = convert_to_user_pass(combos, f"{domain}_userpass.txt")  # Convert to user:pass and save to a new file
        with open(f"{domain}.txt", "w") as f:
            f.write("\n".join(combos))
        print(f"Filtered combos saved to {domain}.txt")

def remove_duplicates(combos, output_file):
    result = list(set(combos))
    with open(output_file, "w") as f:
        f.write("\n".join(result))
    print(f"Duplicates removed and saved to {output_file}")
    return result  # Return the result for further processing

def convert_to_user_pass(combos, output_file):
    converted_combos = []
    for combo in combos:
        try:
            email, password = combo.split(":")
            user = email.split("@")[0]
            converted_combos.append(f"{user}:{password}")
        except ValueError:
            print(f"Invalid combo format: {combo}")
    with open(output_file, "w") as f:
        f.write("\n".join(converted_combos))
    print(f"Combos converted and saved to {output_file}")
    return converted_combos  # Return the result for further processing

def capture_remove(combo_list, output_file):
    captured_combos = []
    for combo in combo_list:
        try:
            email_password = combo.split("|")[2]
            captured_combos.append(email_password)
        except IndexError:
            print(f"Invalid combo format: {combo}")
    with open(output_file, "w") as f:
        f.write("\n".join(captured_combos))
    print(f"Email:password saved to {output_file}")

def convert_to_email(combo_list, output_file):
    """
    Extracts emails from a list of email:password combos and saves them to a file.

    Args:
      combo_list: A list of email:password combos.
      output_file: The name of the output file.
    """
    emails = []
    for combo in combo_list:
        try:
            email, password = combo.split(":")
            emails.append(email)
        except ValueError:
            print(f"Invalid combo format: {combo}")
    with open(output_file, "w") as f:
        f.write("\n".join(emails))
    print(f"Emails saved to {output_file}")

def banner():
    """Displays a red banner."""
    print(Fore.RED + "▄████▄   ▒█████   ███▄ ▄███▓ ▄▄▄▄   ▒█████     ▄▄▄█████▓ ▒█████   ▒█████   ██▓")
    print("▒██▀ ▀█  ▒██▒  ██▒▓██▒▀█▀ ██▒▓█████▄ ▒██▒  ██▒   ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒")
    print("▒▓█    ▄ ▒██░  ██▒▓██    ▓██░▒██▒ ▄██▒██░  ██▒   ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░")
    print("▒▓▓▄ ▄██▒▒██   ██░▒██    ▒██ ▒██░█▀  ▒██   ██░   ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░")
    print("▒ ▓███▀ ░░ ████▓▒░▒██▒   ░██▒░▓█  ▀█▓░ ████▓▒░     ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒")
    print("░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░   ░  ░░▒▓███▀▒░ ▒░▒░▒░     ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░")
    print("  ░  ▒     ░ ▒ ▒░ ░  ░      ░▒░▒   ░   ░ ▒ ▒░       ░     ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░")
    print("░    ░   ░ ░ ░ ▒  ░      ░    ░   ░ ░ ░ ░ ▒           ░ ░ ░ ▒  ░ ░ ░ ▒   ░ ░   ")
    print("░           ░ ░        ░    ░         ░ ░                 ░ ░        ░ ░   ")
    print("░                                                                              " + Style.RESET_ALL)

def main():
    """
    Displays the menu and executes the function chosen by the user.
    """
    banner()  # Display the banner when the program starts
    while True:
        print("\nChoose an operation:")
        print("1. Filter combos by domain")
        print("2. Remove duplicate combos")
        print("3. Convert email:password to user:password")
        print("4. Capture and save email:password")
        print("5. Convert email:password to email")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice in ["1", "2", "3", "4", "5"]:
            input_file = input("Enter the input file name: ")
            try:
                with open(input_file, "r") as f:
                    combo_list = [line.strip() for line in f]
            except FileNotFoundError:
                print(f"File not found: {input_file}")
                continue

            if choice == "1":
                filter_combos(combo_list)  # No need for output_file here
            elif choice in ["2", "3", "4", "5"]:
                output_file = input("Enter the output file name: ")
                if choice == "2":
                    remove_duplicates(combo_list, output_file)
                elif choice == "3":
                    convert_to_user_pass(combo_list, output_file)
                elif choice == "4":capture_remove(combo_list, output_file)
                elif choice == "5":
                    convert_to_email(combo_list, output_file)

            # Back and exit buttons
            while True:
                back = input("Back to main menu? (y/n): ")
                if back.lower() == "y":
                    break  # Go back to the main menu
                elif back.lower() == "n":
                    print("Exiting program.")
                    exit()  # Exit the program
                else:
                    print("Invalid choice.")
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()