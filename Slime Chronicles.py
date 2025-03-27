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

def validateLog():
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
    user = reguser_entry.get()
    pass1 = regpass_entry1.get()
    pass2 = regpass_entry2.get()
    if user == "Enter Username..." or user.strip() == "" or \
    pass2 == "Confirm Password..." or pass2.strip() == "" or\
    pass1 == "Enter Password..." or pass1.strip() == "":
        feedback_lbl2.config(text="Please fill in all fields.", fg="firebrick1")
        return

    if pass1 != pass2:
        feedback_lbl2.config(text="Passwords don't match.", fg="firebrick1")
        return

    if len(pass2) < 8 or len(pass2) > 16:
        feedback_lbl2.config(text="Password must be between 8 and 16 characters.", fg="firebrick1")
        return

    pin = pin_entry.get()
    if len(str(pin)) != 4:
        feedback_lbl2.config(text="Invalid, Pin MUST be 4 digits", fg="firebrick1")
        return
    try:
        pin = int(pin)
    except ValueError:
        feedback_lbl2.config(text="Invalid Pin, must be 4 numerical values", fg="firebrick1")
        return

    pointer.execute("SELECT * FROM logins WHERE username=?", (user,))
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

def changePass():
    pass

def logOut():
    logged_account = None
    account_lbl.config(textvariable=logged_account)
    menupage.tkraise()

# Initialise Main Window
root = tk.Tk()
root.geometry("960x520")
root.title("Slime Chronicles")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Creating Frames for the Title/Login/Register Screen

menupage = Frame(root, background="khaki")
loginpage = Frame(root, background="khaki")
registerpage = Frame(root, background="khaki")
titlepage = Frame(root, background="khaki")

menupage.grid(row=0,column=0, sticky='nsew')
loginpage.grid(row=0,column=0, sticky='nsew')
registerpage.grid(row=0,column=0, sticky='nsew')
titlepage.grid(row=0,column=0, sticky='nsew')

# Background
image = PhotoImage(file= "Pics/background.png")
bg_lbl = Label(menupage, image=image)
bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)

bg_lbl = Label(loginpage, image=image)
bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)

bg_lbl = Label(registerpage, image=image)
bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)

bg_lbl = Label(titlepage, image=image)
bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)

buttonimg = PhotoImage(file= "Pics/Sprite/btn.png")

# Button Class + Functions
class menuButton(Button):
    def __init__(self, frame, **kwargs):
        super().__init__(frame, **kwargs)
        self.config(
            relief=tk.FLAT, bd=0, pady=0, font=("pokefont.ttf", 13), background="khaki")
        self.bind("<Enter>", self.hover)
        self.bind("<Leave>", self.default)
    def hover(self,event):
        self.config(
            background="khaki3")
    def default(self,event):
        self.config(
            background="khaki")

# Quit Button Subclass
class quitButton(menuButton):
    def __init__(self,frame, **kwargs):
        super().__init__(frame, **kwargs)
        self.config(
            command=root.destroy)

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

def regpasswordClick1(event):
    if regpass_entry1.get() == "Enter Password...":
        regpass_entry1.delete(0, tk.END)
        regpass_entry1.config(show="")

def regpasswordClick2(event):
    if regpass_entry2.get() == "Confirm Password...":
        regpass_entry2.delete(0, tk.END)
        regpass_entry2.config(show="")

def passwordDefault(event):
    if pass_entry.get() == "":
        pass_entry.insert(0, "Enter Password...")
        pass_entry.config(show="")

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

# Adding Text / Buttons For Menu Page
gname1 = Label(
    menupage, text="Slime Chronicles", font=("Cascadia Mono SemiBold",19), background="khaki2")
gname1.place(x=40,y=250)

mbtn1 = menuButton(
    menupage, text="Login", width=13, height=1, command=loginpage.tkraise)
mbtn1.place(x=95,y=350)

mbtn2 = menuButton(
    menupage, text="Register", width=13, height=1, command=registerpage.tkraise)
mbtn2.place(x=95,y=405)

mbtn3 = quitButton(
    menupage, text="Quit", width=13, height=1)
mbtn3.place(x=95,y=460)

logged_account = StringVar()
logged_account.set("")

logged_account = None
account_lbl = Label(
    menupage, textvariable=logged_account, font=("Arial",11), background="khaki")
account_lbl.place(x=95,y=300)

# Title/Play Screen
gname2 = Label(
    titlepage, text="Slime Chronicles", font=("Cascadia Mono SemiBold",19), background="khaki2")
gname2.place(x=40,y=220)

def start():
    root.destroy()
    g = Gameplay()
    g.intro()
    g.new()
    g.playmusic()
    while g.running:
        g.mainloop()
        g.game_over()
    pygame.quit()
    sys.exit()


playbtn = menuButton(
    titlepage, text="Play", width=13, height=1, command=start)
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
    loginpage, width=25, bg="dark khaki", relief=tk.FLAT)
username_entry.place(x=170,y=251)
username_entry.insert(0, "Enter Username...")
username_entry.bind("<FocusIn>", usernameClick)
username_entry.bind("<FocusOut>", usernameDefault)

pass_label = Label(
    loginpage, text="Password:", font=("Cascadia Mono SemiBold",12), background="khaki")
pass_label.place(x=60,y=310)

pass_entry = Entry(
    loginpage, width=25, bg="dark khaki", relief=tk.FLAT)
pass_entry.place(x=170,y=316)
pass_entry.insert(0, "Enter Password...")
pass_entry.bind("<FocusIn>", passwordClick)
pass_entry.bind("<FocusOut>", passwordDefault)

login = menuButton(
    loginpage, text="Log In", width=13, height=1, command=validateLog)
login.place(x=240,y=395)

back1 = menuButton(
    loginpage, text="Back", width=13, height=1, command=menupage.tkraise)
back1.place(x=65,y=395)

feedback_lbl1 = Label(
    loginpage, text="", font=("Cascadia Mono SemiBold",9), background="khaki")
feedback_lbl1.place(x=170,y=210)

forgot_lbl = menuButton

# Register Screen
registertitle = Label(
    registerpage, text="Registration", font=("Cascadia Mono SemiBold",19), background="khaki2")
registertitle.place(x=40,y=135)

reguser_lbl = Label(
    registerpage, text="Username:",  font=("Cascadia Mono SemiBold",12), background="khaki")
reguser_lbl.place(x=60,y=225)

reguser_entry = Entry(
    registerpage, width=25, bg="dark khaki", relief=tk.FLAT)
reguser_entry.place(x=170,y=231)
reguser_entry.insert(0, "Enter Username...")
reguser_entry.bind("<FocusIn>", usernameClick)
reguser_entry.bind("<FocusOut>", usernameDefault)

regpass_lbl1 = Label(
    registerpage, text="Password:", font=("Cascadia Mono SemiBold",12), background="khaki")
regpass_lbl1.place(x=60,y=280)

regpass_entry1 = Entry(
    registerpage, width=25, bg="dark khaki", relief=tk.FLAT)
regpass_entry1.place(x=170,y=286)
regpass_entry1.insert(0, "Enter Password...")
regpass_entry1.bind("<FocusIn>", regpasswordClick1)
regpass_entry1.bind("<FocusOut>", regpasswordDefault1)

regpass_lbl2 = Label(
    registerpage, text="Confirm Password:", font=("Cascadia Mono SemiBold",12), background="khaki")
regpass_lbl2.place(x=60,y=335)

regpass_entry2 = Entry(
    registerpage, width=25, bg="dark khaki", relief=tk.FLAT)
regpass_entry2.place(x=242,y=340)
regpass_entry2.insert(0, "Confirm Password...")
regpass_entry2.bind("<FocusIn>", regpasswordClick2)
regpass_entry2.bind("<FocusOut>", regpasswordDefault2)

pin_label = Label(
    registerpage, text="Pin:", font=("Cascadia Mono SemiBold", 12), background="khaki")
pin_label.place(x=60, y=390)

pin_entry = Entry(
    registerpage, width=25, bg="dark khaki", relief=tk.FLAT)
pin_entry.place(x=123, y=396)
pin_entry.insert(0,"Enter Pin...")
pin_entry.bind("<FocusIn>", pinClick)
pin_entry.bind("<FocusOut>", pinDefault)

back2 = menuButton(
    registerpage, text="Back", width=13, height=1, command=menupage.tkraise)
back2.place(x=65,y=445)

register = menuButton(
    registerpage, text="Register", width=13, height=1, command=registerUser)
register.place(x=240,y=445)

feedback_lbl2 = Label(
    registerpage, text="", font=("Cascadia Mono SemiBold",9), background="khaki")
feedback_lbl2.place(x=170,y=195)

# Displaying the screen
menupage.tkraise()

root.mainloop()
