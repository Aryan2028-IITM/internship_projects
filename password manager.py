import csv
import os
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"

def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key

key = Fernet(load_key())

def add_password(website, username, password):
    encrypted_password = key.encrypt(password.encode()).decode()
    with open("passwords.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([website, username, encrypted_password])
    print("Password for",website,"added successfully!")


def change_password(website):
    found = False
    with open("passwords.csv", "r") as file:
        reader = csv.reader(file)
        rows = list(reader)
    with open("passwords.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for row in rows:
            if row[0] == website:
                new_password = input("Enter the new password: ")
                row[2] = key.encrypt(new_password.encode()).decode()
                found = True
            writer.writerow(row)
    if found:
        print("Password for", website, "changed successfully!")
    else:
        print("Password not found!")


def get_password(website):
    found = False
    with open("passwords.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == website:
                decrypted_password = key.decrypt(row[2].encode()).decode()
                print("Password for", website, "is:",decrypted_password)
                found = True
                break
    if not found:
        print("Password not found!")

def main():
    while True:
        print("Password Manager")
        print("1. Add Password")
        print("2. Get Password")
        print("3. Change Password")
        print("4. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            website = input("Enter the website: ")
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            add_password(website, username, password)
        elif choice == 2:
            website = input("Enter the website: ")
            get_password(website)
        elif choice == 3:
            website = input("Enter the website: ")
            change_password(website)
        elif choice == 4:
            break
        else:
            print("Invalid choice!")
main()