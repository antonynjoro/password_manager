import re
import string
from tkinter import *
import tkinter.messagebox as msgbox
import tkinter.simpledialog as sd
import random
# import the ability to copy to the clipboard
import pyperclip
import json

def is_valid_email(dict, key):
    """This function checks if the email address is valid"""
    try:
        # regex for validating an Email including the dot and the @
        email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        return bool(email_regex.match(dict[key]))
    except TypeError:
        return False
    except KeyError:
        return False


# ---------------------------- EMAIL PROMPT ------------------------------- #
# if the user has not added an email address in the email_addresses.txt, prompt them for the email
def request_email() -> dict:
    """This function prompts the user for their email address and saves it to a file."""
    try:
        with open("email_address.json", mode="r") as email_file:
            email_dict = json.load(email_file)


        if email_dict['Email'] == None or email_dict['Email'] == "":
            raise ValueError("No email address provided")
        elif not is_valid_email(email_dict, "Email"):
            raise ValueError(f"Invalid email address: {email_dict['Email']}")

    except json.decoder.JSONDecodeError:
        email = sd.askstring("Email Address", "Please enter your email address")
        email_dict = {"Email": email}
        with open("email_address.json", mode="w") as email_file:
            json.dump(email_dict, email_file)


    except FileNotFoundError:
        email = sd.askstring("Email Address", "Please enter your email address")
        email_dict = {"Email": email}
        with open("email_address.json", mode="w") as email_file:
            json.dump(email_dict, email_file)
    except ValueError as e:
        email = sd.askstring("Email Address", f"{e}\nPlease enter your email address.")
        email_dict = {"Email": email}
        with open("email_address.json", mode="w") as email_file:
            json.dump(email_dict, email_file)



    return email_dict
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# This function generates a random password of a given length
def generate_pw(length):
    # Create a list of all the characters that can be used in the password
    password_list = list(string.ascii_letters + string.digits + string.punctuation)
    password = ""
    # Loop through the list and add a random character to the password
    for _ in range(length):
        password += random.choice(password_list)

    # Insert the password into the password field
    password_field.delete(first=0, last=END)
    password_field.insert(string=password, index=0)


# ---------------------------- SAVE PASSWORD ------------------------------- #
# This function saves a password for a website, username and password to a file
def save_pw():
    # Get the user inputs for website, username, and password
    password = password_field.get()
    website = website_field.get()
    username = username_field.get()
    # Check if any of the fields are empty and raise an error
    try:
        if len(password) == 0:
            raise ValueError("Password field cannot be empty, Please generate a password and try again")
        elif len(website) == 0:
            raise ValueError("Website field cannot be empty. Please enter the name of the Website and try again")
        elif len(username) == 0:
            raise ValueError("Username cannot be empty. Please enter your username or email address and try again")
        else:
            # Copy the password to the clipboard
            pyperclip.copy(password)
            # Show a success message to the user
            msgbox.showinfo("Success", "Password copied to clipboard")
    except Exception as e:
        # Show an error message to the user if any of the fields are empty
        msgbox.showerror("Error", str(e))

    # try to open the file to save the password
    try:
        # Open the file to save the password
        with open("passwords.json", mode="r") as password_file:
            # Read the file
            data = json.load(password_file)
            # Add the new password to the file
            data[website] = {
                "email": username,
                "password": password
            }
        # Save the file
        with open("passwords.json", mode="w") as password_file:
            json.dump(data, password_file, indent=4)

    # If the file does not exist, create it and save the password
    except FileNotFoundError:
        with open("passwords.json", mode="w") as password_file:
            json.dump({website: {
                "email": username,
                "password": password
            }}, password_file, indent=4)


# ---------------------------- UI SETUP ------------------------------- #


EMAIL_ADDRESS = request_email()["Email"]


# Create a window
window = Tk()
window.title("Password Manager")
# Set the window size
window.config(pady=20, padx=20, )
# Set the window to be non-resizable
window.resizable(width=False, height=False)


# set the weight of the columns and rows
for i in range(3):
    window.columnconfigure(i, weight=1)
for i in range(6):
    window.rowconfigure(i, weight=1)

# Create a canvas to hold the logo
logo = Canvas(width=200, height=200, highlightthickness=0)
# Add the logo to the canvas
logo_image = PhotoImage(file="logo.png")
logo.create_image(100, 100, image=logo_image)
logo.grid(row=0, column=0, columnspan=3, )

#
website_label = Label(text="Website:", highlightthickness=0)
website_label.grid(row=1, column=0, sticky=E + W + N + S, pady=10)

website_field = Entry(highlightthickness=0, )
website_field.grid(column=1, row=1, columnspan=2, sticky=E + W + N + S, pady=10)
website_field.focus()

username_label = Label(text="Email", highlightthickness=0, )
username_label.grid(row=2, column=0, sticky=E + W + N + S, pady=10)

username_field = Entry(highlightthickness=0, )
username_field.grid(row=2, column=1, columnspan=2, sticky=E + W + N + S, pady=10, )
username_field.insert(0, EMAIL_ADDRESS)

# create label and entry for length of password
length_label = Label(text="Length", highlightthickness=0, )
length_label.grid(row=3, column=0, sticky=E + W + N + S, pady=10)


length_slider = Scale(from_=8, to=32, orient=HORIZONTAL, highlightthickness=0, )
length_slider.grid(row=3, column=1, sticky=E + W + N + S, pady=10, columnspan=2,)

password_label = Label(text="Password", highlightthickness=0, )
password_label.grid(row=4, column=0, sticky=E + W + N + S, pady=10)

password_field = Entry(highlightthickness=0, )
password_field.grid(row=4, column=1, sticky=E + W + N + S, pady=10)

# Create a button to generate a password of a given length obtained from the slider
generate_pw_btn = Button(text="Generate Password", highlightthickness=0, command=lambda: generate_pw(length_slider.get()))
generate_pw_btn.grid(row=4, column=2, sticky=E + W + N + S, pady=10, padx=10)

# Create a button to save the password
add_btn = Button(text="Add", highlightthickness=0, fg="black", command=save_pw)
add_btn.grid(row=5, column=1, columnspan=2, sticky=E + W + N + S, pady=10)

# Start the main loop
window.mainloop()
