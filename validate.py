# Import tkinter library and database

import tkinter as tk
from tkinter import *
import sqlite3

from sprites import Spritesheet

# Sqlite Database and the pointer
connect = sqlite3.connect("Logins.DB")
pointer = connect.cursor()

# Creating the Table
create_db = """
    CREATE TABLE IF NOT EXISTS
    logins(username TEXT, password TEXT, pin TEXT)
"""
pointer.execute(create_db)

pointer.execute("SELECT * FROM logins")
all_accounts = pointer.fetchall()

def verifyLog():
    pointer.execute("SELECT * FROM logins")
    all_accounts = pointer.fetchall()
    global logged_account
    for all_accounts in all_accounts:
        if username_entry.get() == all_accounts[0] and pass_entry.get() == all_accounts[1]:
            logged_account = all_accounts[0]
            feedback_lbl1.config(text="Valid", fg="green")
            account_lbl.config(text=f"Welcome, {logged_account} !")
            titlepage.tkraise()
            return
    else:
        feedback_lbl1.config(text="Invalid login", fg="firebrick1")
        return

def registerUser():
    user = username_entry = reguser_entry.get()
    pass1 = regpass_entry1.get()
    pass2 = pass_entry = regpass_entry2.get()
    pin = pin_entry.get()
    # Check for default or no input
    if user == "Enter Username..." or user.strip() == "" or \
    pass2 == "Confirm Password..." or pass2.strip() == "" or\
    pass1 == "Enter Password..." or pass1.strip() == "" or\
    pin == "Enter Pin..." or pin.strip() == "":
        feedback_lbl2.config(text="Please fill in all fields.", fg="firebrick1") # Shows an error on their screen
        return

    if pass1 != pass2:
        feedback_lbl2.config(text="Passwords don't match.", fg="firebrick1")
        return

    if len(pass2) < 8 or len(pass2) > 16:
        feedback_lbl2.config(text="Password must be between 8 and 16 characters.", fg="firebrick1")
        return

    if len(user) > 15:
        feedback_lbl2.config(text="Username too long; 15 characters limit", fg="firebrick1")

    if len(str(pin)) < 4 or len(str(pin)) >6:
        feedback_lbl2.config(text="Invalid, Pin MUST be 4-6 digits", fg="firebrick1")
        return
    try:
        pin = int(pin)
    except ValueError:
        feedback_lbl2.config(text="Invalid Pin, must be 4-6 numerical values", fg="firebrick1")
        return

    pointer.execute("SELECT * FROM logins WHERE username=?", user)
    if pointer.fetchone():
        feedback_lbl2.config(text="Username already exists.", fg="firebrick1")
        return

    pointer.execute("INSERT INTO logins (username, password, pin) VALUES (?, ?, ?)", (user, pass2, pin))
    connect.commit()
    reguser_entry.bind("<FocusIn>", usernameClick)
    reguser_entry.bind("<FocusOut>", usernameDefault)
    regpass_entry1.bind("<FocusIn>", regpasswordClick1)
    regpass_entry1.bind("<FocusOut>", regpasswordDefault1)
    regpass_entry2.bind("<FocusIn>", regpasswordClick2)
    regpass_entry2.bind("<FocusOut>", regpasswordDefault2)
    loginpage.tkraise()

def authenticate():
    user = username_entry.get()
    pin = pin_entry1.get()
    pointer.execute("SELECT * FROM logins WHERE username=?", (user,))
    if pointer.fetchone():
        pointer.execute(f"SELECT * FROM logins WHERE username=? AND pin=?", (user,pin))
        match = pointer.fetchone()
        if match:
            pass_lbl1.place(x=60, y=335)
            pass_entry1.place(x=170,y=341)
            changePass(user)

def changePass(username):
    new_pass = pass_entry1.get()
    user = username
    pointer.execute("UPDATE logins SET password=? WHERE username=?", (new_pass, user))
    connect.commit()
    loginpage.tkraise()

def logOut():
    logged_account = None
    account_lbl.config(textvariable=logged_account)
    menupage.tkraise()

# Initialise Main Window
root = tk.Tk()
root.geometry("960x520")
root.resizable = False
root.title("Slime Chronicles")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Creating Frames for the Title/Login/Register Screen

menupage = Frame(root, background="khaki")
loginpage = Frame(root, background="khaki")
registerpage = Frame(root, background="khaki")
titlepage = Frame(root, background="khaki")
verifypage = Frame(root, background="khaki")
frames = [menupage, loginpage, registerpage, titlepage, verifypage] # For easy grid plotting

# Background + Setting the frames
image = PhotoImage(file= "Pics/background.png") # Image
for frame in frames:
    frame.grid(row=0, column=0, sticky='nsew')
    bg_lbl = Label(frame, image=image)  # Placing Image in specific frame
    bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)

# Button Class + Functions
class menuButton(Button):
    def __init__(self, frame, **kwargs):
        super().__init__(frame, **kwargs)
        buttonimg = PhotoImage(file="Pics/btn.png")
        self.config(
            relief=tk.FLAT, bd=0, pady=0, font=("pokefont.ttf", 13), background="khaki") # Purely customisation
        self.bind("<Enter>", self.hover) # Creates an effect when hovering over object
        self.bind("<Leave>", self.default)
    def hover(self,event):
        self.config(
            background="khaki3")
    def default(self,event):
        self.config(
            background="khaki")

# Quit Button Subclass
class quitButton(menuButton): # Inherit all atributes and methods from menuButton
    def __init__(self,frame, **kwargs):
        super().__init__(frame, **kwargs)
        self.config(
            command=root.destroy) # Set self.config for object to close window when pressed

# Login Page Events
def usernameClick(event):
    if username_entry.get() == "Enter Username...":
        username_entry.delete(0, tk.END)
    if reguser_entry.get() == "Enter Username...":
        reguser_entry.delete(0, tk.END)


def usernameDefault(event):
    if username_entry.get() == "":
        username_entry.insert(0, "Enter Username...")
    if reguser_entry.get() == "":
        reguser_entry.insert(0, "Enter Username...")

def passwordClick(event):
    if pass_entry.get() == "Enter Password...":
        pass_entry.delete(0, tk.END)
        pass_entry.config(show="*")

def passwordDefault(event):
    if pass_entry.get() == "":
        pass_entry.insert(0, "Enter Password...")
        pass_entry.config(show="")

def regpasswordClick1(event):
    if regpass_entry1.get() == "Enter Password...":
        regpass_entry1.delete(0, tk.END)
        regpass_entry1.config(show="")

def regpasswordClick2(event):
    if regpass_entry2.get() == "Confirm Password...":
        regpass_entry2.delete(0, tk.END)
        regpass_entry2.config(show="*")

def regpasswordDefault1(event):
    if regpass_entry1.get() == "":
        regpass_entry1.insert(0, "Enter Password...")
        regpass_entry1.config(show="")

def regpasswordDefault2(event):
    if regpass_entry2.get() == "":
        regpass_entry2.insert(0, "Confirm Password...")
        regpass_entry2.config(show="")

def pinDefault(event):
    if pin_entry.get() == "":
        pin_entry.insert(0, "Enter Pin...")
        pin_entry.config(show="")

def pinClick(event):
    if pin_entry.get() == "Enter Pin...":
        pin_entry.delete(0, tk.END)
        pin_entry.config(show="")

def pinDefault1(event):
    if pin_entry1.get() == "":
        pin_entry1.insert(0, "Enter Pin...")
        pin_entry1.config(show="")

def pinClick1(event):
    if pin_entry1.get() == "Enter Pin...":
        pin_entry1.delete(0, tk.END)
        pin_entry1.config(show="*")

def usernameClick1(event):
    if username_entry1.get() == "Enter Username...":
        username_entry1.delete(0, tk.END)

def usernameDefault1(event):
    if username_entry1.get() == "":
        username_entry1.insert(0, "Enter Username...")

# Adding Text / Buttons For Menu Page
gname1 = Label(
    menupage, text="Slime Chronicles", font=("Cascadia Mono SemiBold",19), background="khaki2")
gname1.place(x=40,y=250)

menuimage = PhotoImage(file="Pics/btnbg.png")
menubg = Label(
    menupage, image= menuimage)
menuimage.zoom((200/352), 400)
menubg.place(x=50,y=300)

mbtn1 = menuButton(
    menupage, text="Login", width=13, height=1, command=loginpage.tkraise)
mbtn1.place(x=95,y=350)

mbtn2 = menuButton(
    menupage, text="Register", width=13, height=1, command=registerpage.tkraise)
mbtn2.place(x=95,y=405)

mbtn3 = quitButton(
    menupage, text="Quit", width=13, height=1)
mbtn3.place(x=95,y=460)

# Title/Play Screen
gname2 = Label(
    titlepage, text="Slime Chronicles", font=("Cascadia Mono SemiBold",19), background="khaki2")
gname2.place(x=40,y=220)

playbtn = menuButton(
    titlepage, text="Play", width=13, height=1)
playbtn.place(x=95,y=310)

settingbtn = menuButton(
    titlepage, text="Settings", width=13, height=1)
settingbtn.place(x=95,y=365)

logoutbtn = menuButton(
    titlepage, text="Log Out", width=13, height=1, command=logOut)
logoutbtn.place(x=95,y=420)

qbtn = quitButton(
    titlepage, text="Quit", width=13, height=1)
qbtn.place(x=95,y=475)

logged_account = StringVar()
logged_account.set("")
logged_account = None

account_lbl = Label(
    titlepage, textvariable=logged_account, font=("Arial",11), background="khaki")
account_lbl.place(x=95,y=270)

# Adding Text / Entry Boxes For Login Page
logtitle = Label(
    loginpage, text="Login", font=("Cascadia Mono SemiBold",19), background="khaki2")
logtitle.place(x=40,y=150)

user_label = Label(
    loginpage, text="Username: ",  font=("Cascadia Mono SemiBold",12), background="khaki")
user_label.place(x=60,y=245)

username_entry = Entry(
    loginpage, width=25, bg="dark khaki", relief=tk.FLAT) # User Entry
username_entry.place(x=170,y=251)
username_entry.insert(0, "Enter Username...")
username_entry.bind("<FocusIn>", usernameClick)
username_entry.bind("<FocusOut>", usernameDefault)

pass_label = Label(
    loginpage, text="Password:", font=("Cascadia Mono SemiBold",12), background="khaki")
pass_label.place(x=60,y=310)

pass_entry = Entry(
    loginpage, width=25, bg="dark khaki", relief=tk.FLAT) # Pass Entry
pass_entry.place(x=170,y=316)
pass_entry.insert(0, "Enter Password...")
pass_entry.bind("<FocusIn>", passwordClick)
pass_entry.bind("<FocusOut>", passwordDefault)

login = menuButton(
    loginpage, text="Log In", width=13, height=1, command=verifyLog) # Confirm Inputs
login.place(x=240,y=395)

back1 = menuButton(
    loginpage, text="Back", width=13, height=1, command=menupage.tkraise)
back1.place(x=65,y=395)

forgot = menuButton(
    loginpage, text="Forgot Password", width=14, height=1, command=verifypage.tkraise)
forgot.place(x=170, y=350)

feedback_lbl1 = Label(
    loginpage, text="", font=("Cascadia Mono SemiBold",9), background="khaki") # To show errors for Inputs
feedback_lbl1.place(x=170,y=210)

# Verify Page
verifytitle = Label(
    verifypage, text="Verification", font=("Cascadia Mono SemiBold",19), background="khaki2")
verifytitle.place(x=40,y=135)

user_label = Label(
    verifypage, text="Username: ",  font=("Cascadia Mono SemiBold",12), background="khaki")
user_label.place(x=60,y=245)

username_entry1 = Entry(
    verifypage, width=25, bg="dark khaki", relief=tk.FLAT) # User Entry
username_entry1.place(x=170,y=251)
username_entry1.insert(0, "Enter Username...")
username_entry1.bind("<FocusIn>", usernameClick1)
username_entry1.bind("<FocusOut>", usernameDefault1)

pin_label = Label(
    verifypage, text="Pin:", font=("Cascadia Mono SemiBold", 12), background="khaki")
pin_label.place(x=60, y=280)

pin_entry1 = Entry(
    verifypage, width=25, bg="dark khaki", relief=tk.FLAT) # Pin Entry
pin_entry1.place(x=170, y=286)
pin_entry1.insert(0,"Enter Pin...")
pin_entry1.bind("<FocusIn>", pinClick1)
pin_entry1.bind("<FocusOut>", pinDefault1)

back3 = menuButton(
    verifypage, text="Back", width=13, height=1, command=loginpage.tkraise)
back3.place(x=65,y=390)

confirm = menuButton(
    verifypage, text="Confirm", width=13, height=1, command=authenticate) # Confirm Inputs
confirm.place(x=240,y=390)

pass_lbl1 = Label(
    verifypage, text="NewPassword:", font=("Cascadia Mono SemiBold", 12), background="khaki")

pass_entry1 = Entry(
    verifypage, width=25, bg="dark khaki", relief=tk.FLAT)  # Confirm Password



# Register Screen
registertitle = Label(
    registerpage, text="Registration", font=("Cascadia Mono SemiBold",19), background="khaki2")
registertitle.place(x=40,y=135)

reguser_lbl = Label(
    registerpage, text="Username:",  font=("Cascadia Mono SemiBold",12), background="khaki")
reguser_lbl.place(x=60,y=225)

reguser_entry = Entry(
    registerpage, width=25, bg="dark khaki", relief=tk.FLAT) # User Entry
reguser_entry.place(x=170,y=231)
reguser_entry.insert(0, "Enter Username...")
reguser_entry.bind("<FocusIn>", usernameClick)
reguser_entry.bind("<FocusOut>", usernameDefault)

regpass_lbl1 = Label(
    registerpage, text="Password:", font=("Cascadia Mono SemiBold",12), background="khaki")
regpass_lbl1.place(x=60,y=280)

regpass_entry1 = Entry(
    registerpage, width=25, bg="dark khaki", relief=tk.FLAT) # Password Entry
regpass_entry1.place(x=170,y=286)
regpass_entry1.insert(0, "Enter Password...")
regpass_entry1.bind("<FocusIn>", regpasswordClick1)
regpass_entry1.bind("<FocusOut>", regpasswordDefault1)

regpass_lbl2 = Label(
    registerpage, text="Confirm Password:", font=("Cascadia Mono SemiBold",12), background="khaki")
regpass_lbl2.place(x=60,y=335)

regpass_entry2 = Entry(
    registerpage, width=25, bg="dark khaki", relief=tk.FLAT) # Confirm Password
regpass_entry2.place(x=242,y=340)
regpass_entry2.insert(0, "Confirm Password...")
regpass_entry2.bind("<FocusIn>", regpasswordClick2)
regpass_entry2.bind("<FocusOut>", regpasswordDefault2)

pin_label = Label(
    registerpage, text="Pin:", font=("Cascadia Mono SemiBold", 12), background="khaki")
pin_label.place(x=60, y=390)

pin_entry = Entry(
    registerpage, width=25, bg="dark khaki", relief=tk.FLAT) # Pin Entry
pin_entry.place(x=123, y=396)
pin_entry.insert(0,"Enter Pin...")
pin_entry.bind("<FocusIn>", pinClick)
pin_entry.bind("<FocusOut>", pinDefault)

back2 = menuButton(
    registerpage, text="Back", width=13, height=1, command=menupage.tkraise)
back2.place(x=65,y=445)

register = menuButton(
    registerpage, text="Register", width=13, height=1, command=registerUser) # Confirm Inputs
register.place(x=240,y=445)

feedback_lbl2 = Label(
    registerpage, text="", font=("Cascadia Mono SemiBold",9), background="khaki") # To show errors for Inputs
feedback_lbl2.place(x=170,y=195)

# Displaying the screen
menupage.tkraise()

root.mainloop()
