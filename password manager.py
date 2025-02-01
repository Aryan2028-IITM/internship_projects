# ---------------------------importing necessary libraries---------------------------
import csv
import os
import random
from cryptography.fernet import Fernet
import psycopg2

# ---------------------------make a file to store key---------------------------
KEY_FILE = "secret.key"


# ---------------------------storing key in file created above if not stored earlier otherwise fetching it---------------------------
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
# ---------------------------database connection details---------------------------
conn={
    'dbname': 'password_manager',
    'user': 'postgres',
    'password': '134203',
    'host': 'localhost',
    'port': '5432'
}
# ---------------------------creating table in database---------------------------

con = psycopg2.connect(**conn)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS passwords (website TEXT, username TEXT, password TEXT)")
con.commit()
# ---------------------------creating function to add passwords---------------------------

def add_password(website, username, password):
    encrypted_password = key.encrypt(password.encode()).decode()
    insert_query="INSERT INTO passwords (website, username, password) VALUES (%s, %s, %s)"
    records=(website, username, encrypted_password)
    cur.execute(insert_query, records)
    con.commit()
    print("Password for", website, "added successfully!")


# ---------------------------creating function to change password---------------------------

def change_password(website):
    new_password=input("Enter the new password: ")
    encrypted_password = key.encrypt(new_password.encode()).decode()
    update_query="UPDATE passwords SET password=%s WHERE website=%s"
    cur.execute(update_query, (encrypted_password, website))
    con.commit()
    print("Password for", website, "changed successfully!")



# ---------------------------creating function to generate a random password---------------------------

def generate_password():
    password = ""
    for i in range(12):
        password += chr(random.randint(33, 126))
    return password


# ---------------------------creating a function to search a password for a particular website---------------------------

def get_password(website):
    query = "SELECT * FROM passwords WHERE website LIKE %s"
    cur.execute(query, (f"%{website}%",))
    records=cur.fetchall()
    if len(records)>0:
        for record in records:
            decrypted_password = key.decrypt(record[2].encode()).decode()
            print("Username for",website, "is:",record[1],"\nPassword for", record[1], "is:", decrypted_password)
    else:
        print("Details not found!")

# ---------------------------main program---------------------------

def main():
    while True:
        print("Password Manager")
        print("1. Add Password")
        print("2. Get Username and Password")
        print("3. Change Password")
        print("4. Import from CSV")
        print("5. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            print("1. Add your own Password")
            print("2. Generate Password")
            nested_choice = int(input("Enter your choice: "))
            if nested_choice == 1:
                website = input("Enter the website: ")
                username = input("Enter the username: ")
                password = input("Enter the password: ")
                add_password(website, username, password)
            elif nested_choice == 2:
                website = input("Enter the website: ")
                username = input("Enter the username: ")
                password = generate_password()
                add_password(website, username, password)
            else:
                print("Invalid choice!")
        elif choice == 2:
            website = input("Enter the website: ")
            get_password(website)
        elif choice == 3:
            website = input("Enter the website: ")
            change_password(website)
        elif choice == 4:
            path=input("Enter the path of the csv file: ")
            with open(path, "r") as file:
                reader=csv.reader(file)
                for row in reader:
                    website=row[0]
                    username=row[1]
                    password=row[2]
                    add_password(website, username, password)
                file.close()
        elif choice == 5:
            con.close()
            break
        else:
            print("Invalid choice!\nTry again!")


main()





