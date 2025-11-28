# Demo version of Banking Management System
# Full logic removed for safety; only GUI and partial code shown

import tkinter as tk
from ttkbootstrap import Style
from PIL import ImageTk, Image

username = ""
root = tk.Tk()

# -------------------------------
# Login function (partial demo)
# -------------------------------
def login(entry_username, entry_password, result_label):
    username = entry_username.get()
    
    # Original database and authentication logic removed for demo
    # Pretend login is successful
    result_label.config(text="Login Successful (demo)", fg='green')
    navigate()

# -------------------------------
# Display Login Screen
# -------------------------------
def display_login_screen():
    root.title("Acme Bank")
    style = Style("flatly")

    # Maximize window
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

    # Load background image (demo path)
    background_image = Image.open("demo_bank_image.png")
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Title label
    title_label = tk.Label(root, text="Welcome to Acme Bank!", font=("Helvetica", 30), bg="#ADD8E6", fg="#FFD700")
    title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    # Create login frame and widgets
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1)
    entry_username = tk.Entry(frame)
    entry_password = tk.Entry(frame, show="*")
    result_label = tk.Label(frame, text="", font=("Helvetica", 13))
    login_button = tk.Button(frame, text="Login", command=lambda: login(entry_username, entry_password, result_label))

    # Layout (simplified for demo)
    entry_username.grid(row=0, column=1)
    entry_password.grid(row=1, column=1)
    login_button.grid(row=2, column=1)
    result_label.grid(row=3, column=1)

    root.mainloop()

# -------------------------------
# Dashboard function (partial demo)
# -------------------------------
def open_dashboard():
    # Original logic removed for demo
    pass

# -------------------------------
# Navigate function
# -------------------------------
def navigate():
    # Original navigation logic removed for demo
    pass

# -------------------------------
# Start the demo
# -------------------------------
display_login_screen()
