# This project is a command-line Contact Book Manager developed in Python.
# It allows users to add, view, search, update, and delete contacts saved in a JSON file.
# Users can also import multiple contacts from a CSV file.

import json
import os
import csv

FILE_NAME = "Contacts.json"

def add_contact():
    while True:
        try:
            option = int(input("""
            1. Add contact manually
            2. Import contacts from CSV file
            3. Back to main menu

            Enter your choice: """))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        if option == 1:
            name = input("Enter name: ")
            phone = input("Enter phone number: ")
            email = input("Enter email: ")

            if not name or not phone:
                print("Email and name are required.")
                continue

            new_contact = {"Name": name, "Phone Number": phone, "Email": email if email else None}
            save_contact(new_contact)

        elif option == 2:
            csv_file = input("Enter path to CSV file: ")
            if not os.path.exists(csv_file):
                print("CSV file not found.")
                continue
            try:
                with open(csv_file, newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    contacts = [{"Name": row["Name"], "Phone Number": row["Phone Number"], "Email": row["Email"]} for row in reader]
                save_contacts_bulk(contacts)
            except Exception as e:
                print(f"Failed to read CSV file: {e}")

        elif option == 3:
            break
        else:
            print("Invalid option.")

def save_contact(contact):
    data = {"contacts": []}
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print("File was empty or corrupt. Starting fresh.")

    for existing in data["contacts"]:
        if existing["Phone Number"] == contact["Phone Number"]:
            print("Contact already exists.")
            return

    data["contacts"].append(contact)
    with open(FILE_NAME, 'w') as f:
        json.dump(data, f, indent=4)
    print("Contact saved successfully.")

def save_contacts_bulk(contacts):
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"contacts": []}
    else:
        data = {"contacts": []}

    data["contacts"].extend(contacts)
    with open(FILE_NAME, 'w') as f:
        json.dump(data, f, indent=4)
    print("Contacts added from CSV.")

def view_contacts():
    if not os.path.exists(FILE_NAME):
        print("No contacts available.")
        return

    with open(FILE_NAME, 'r') as f:
        print(f.read())

def search_contact():
    term = input("Enter name or phone number to search: ")
    try:
        with open(FILE_NAME, 'r') as f:
            data = json.load(f)

        found = False
        for contact in data.get("contacts", []):
            if term in contact["Name"] or term in contact["Phone Number"]:
                print(f"Name: {contact['Name']}, Phone: {contact['Phone Number']}, Email: {contact['Email']}")
                found = True

        if not found:
            print("Contact not found.")
    except Exception as e:
        print(f"Error: {e}")

def update_contact():
    term = input("Enter name or phone number to update: ")
    try:
        with open(FILE_NAME, 'r') as f:
            data = json.load(f)

        for contact in data["contacts"]:
            if term in contact["Name"] or term in contact["Phone Number"]:
                choice = input("Update name or number? ").strip().lower()
                if choice == "name":
                    contact["Name"] = input("Enter new name: ")
                elif choice == "number":
                    contact["Phone Number"] = input("Enter new phone number: ")
                else:
                    print("Invalid choice.")
                    return

                with open(FILE_NAME, 'w') as f:
                    json.dump(data, f, indent=4)
                print("Contact updated.")
                return
        print("Contact not found.")
    except Exception as e:
        print(f"Error: {e}")

def delete_contact():
    term = input("Enter name or phone number to delete: ")
    try:
        with open(FILE_NAME, 'r') as f:
            data = json.load(f)

        original_len = len(data["contacts"])
        data["contacts"] = [c for c in data["contacts"] if term not in c["Name"] and term not in c["Phone Number"]]

        if len(data["contacts"]) < original_len:
            with open(FILE_NAME, 'w') as f:
                json.dump(data, f, indent=4)
            print("Contact deleted.")
        else:
            print("Contact not found.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        try:
            choice = int(input("""
Contact Book Menu:
1. Add Contact
2. View Contacts
3. Search Contact
4. Update Contact
5. Delete Contact
6. Exit

Enter your choice: """))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            add_contact()
        elif choice == 2:
            view_contacts()
        elif choice == 3:
            search_contact()
        elif choice == 4:
            update_contact()
        elif choice == 5:
            delete_contact()
        elif choice == 6:
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
