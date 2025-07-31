from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)

    password_input.insert(0, password)
    #copies password to clipboard
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
# Saves the data the user inputs to password.json and deletes information from the entry fields.
def save():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {website: {
        'email': email,
        'password': password,
        }
    }

# error if entries are empty
    if website == '' or password == '':
        messagebox.showerror(title="Oops", message="Please provide details and then continue.")
    else:
        try:
            with open('password.json', 'r') as data_file:
                # reading old data
                data = json.load(data_file)
                # updating old data with new data
        except FileNotFoundError:
            with open('password.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)

            with open('password.json', 'w') as data_file:
                # saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            # clears fields when saved
            website_input.delete(0, END)
            password_input.delete(0, END)

# ---------------------------- SEARCH ------------------------------- #

def find_password():
    website = website_input.get()
    try:
        with open('password.json') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error",
                            message="No data found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No data found for {website}")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50,pady=50)

# logo
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# website input
website_text = Label(text="Website:")
website_text.grid(column=0, row=1)
website_input = Entry(width=22)
website_input.grid(column=1, row=1)

# email/username input
email_text = Label(text="Email/Username:")
email_text.grid(column=0, row=2)
email_input = Entry(width=40)
email_input.grid(column=1, row=2, columnspan=2)
email_input.insert(0, "myemail@email.com")

# generate password field
password_text = Label(text="Password:")
password_text.grid(column=0, row=3)
password_input = Entry(width=22)
password_input.grid(column=1, row=3)

# generate button
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3)

# add button
add_button = Button(text="Add", width=34, command=save)
add_button.grid(column=1, row=4, columnspan=2)

# search button
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()