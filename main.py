#Function for Login Screen
def display_login_screen():
    #GUI SCREEN 1
    #Create the main window and set the ttkbootstrap style
    root.title("Acme Bank")
    style = Style("flatly")

    # Maximize the window
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

    # Calculate the screen width
    screen_width = root.winfo_screenwidth()

    # Load the image
    background_image = Image.open(r"C:\Users\HP\OneDrive\Desktop\Python\bank_1 conv.png")
    background_photo = ImageTk.PhotoImage(background_image)

    # Create and place widgets
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create a big-sized title text label
    title_label = tk.Label(root, text="Welcome to Acme Bank!", font=("Helvetica", 30), bg="#ADD8E6", fg="#FFD700")
    title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    # Create and place widgets
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1)

    # Custom font settings for labels
    label_font = ('Helvetica', 13)
    button_font = ('Helvetica', 13)  # Adjust the button size and style

    empty_label = tk.Label(frame, text="", font=("Helvetica", 13))
    label_username = tk.Label(frame, text="User ID:", font=label_font,  bg='#ADD8E6')
    label_password = tk.Label(frame, text="Password:", font=label_font)
    entry_username = tk.Entry(frame)
    entry_password = tk.Entry(frame, show="*")  # Mask the password
    result_label = tk.Label(frame, text="", font=("Helvetica", 13))
    login_button = tk.Button(frame, text="Login", command= lambda: login(entry_username, entry_password, result_label), width=6, height=1, font=button_font)  # Adjust the width and height
    login_button.configure(bg="light blue", fg="black")
    
    empty_label.grid(row=2, column=0, columnspan=2, pady=10, sticky='ew')
    label_username.grid(row=3, column=0, padx=(650, 10), pady=10, sticky='e')
    entry_username.grid(row=3, column=1, padx=(10, 650), pady=10, sticky='w')
    label_password.grid(row=4, column=0, padx=(650, 10), pady=10, sticky='e')
    entry_password.grid(row=4, column=1, padx=(10, 650), pady=10, sticky='w')
    login_button.grid(row=5, column=0, columnspan=2, padx=(425, 400), pady=20)
    result_label.grid(row=6, column=0, columnspan=2,  padx=(400, 400), pady=10 )

    # Start the main event loop
    root.mainloop()

# Function to construct GUI Screen 2 : Dashboard
def open_dashboard():
    global root, username # Access the main login window and the global username variable
    root.destroy()  # Close the login window
    dashboard_window = tk.Tk()
    dashboard_window.title("Dashboard")
    dashboard_window.geometry("{0}x{1}+0+0".format(
    dashboard_window.winfo_screenwidth(),
    dashboard_window.winfo_screenheight()
    ))

    #Defining sidebar and main frames
    # Sidebar Frame
    sidebar_frame = tk.Frame(dashboard_window, width=200)
    sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
    sidebar_frame.configure(bg='#D9E2F3')

    # Main Frame
    main_frame = tk.Frame(dashboard_window)
    main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    main_frame.configure( bg = "#E6BF8C")

    # To show all the Buttons in Sidebar
    button_labels = ["View My Balance","Transfer Fund", "Transaction History", "My Details", "Contact", "Exit"]
    for label_text in button_labels:
        btn = tk.Button(sidebar_frame, text=label_text, font=('Roboto', 14), relief=tk.FLAT,
                        command=lambda label_text=label_text: show_panel(label_text, username))
        btn.configure(fg='black',bg='#D9E2F3' )
        btn.pack(fill=tk.X, padx=10, pady=5)

  
#Function to navigate from Screen 1 to Screen
def navigate():
    global root
    root.after(1000, open_dashboard)  # Open dashboard after 1000 milliseconds (1 seconds)

#Calling Screen 1
display_login_screen()
