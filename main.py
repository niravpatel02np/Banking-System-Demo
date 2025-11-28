import tkinter as tk
import ttkbootstrap as ttb
from ttkbootstrap import *
from PIL import ImageTk, Image
import datetime
from tkinter import messagebox
from Functions import insert_transaction, update_sender_acc, update_receiver_acc, get_current_datetime, fetch_transactions
from Functions import view_my_details, fetch_custid_details, display_contact_info

import sqlite3
from Database import create_database, drop_table #calling Databse.py file

# Global variables to store username and password
username = ""
password = ""
root = tk.Tk()

current_date, current_time = get_current_datetime()

# Function to handle the login button click
def login(entry_username, entry_password, result_label):
    global root,username, password  # Declare global to modify the global variables
    username = entry_username.get()
    password = entry_password.get()

    #after connecting with sqlite3, now connecting with created database acme_database
    connection = sqlite3.connect("acme_database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Customer WHERE UserID = ?", (username,))
    user_data = cursor.fetchone()

    # Check if the user exists and if the provided password matches the stored password
    if user_data is not None and user_data[5] == password:
        result_label.config(text="Login Successful", fg='green')
        navigate() 
    else:
        result_label.config(text="Login Failed: Invalid username or password", fg="red")

    cursor.close()
    connection.close()

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

    #Defining function to show panels in main window
    def show_panel(button_name, username):
        # Clear previous widgets in the main frame
        for widget in main_frame.winfo_children():
            widget.pack_forget()

        #General code to fetch customer ID for all panels for Screen 2
        connection = sqlite3.connect("acme_database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Customer WHERE UserID = ?", (username,))
        customer_data = cursor.fetchone()
        cust_id = customer_data[0]
        fname = customer_data[2]

        cursor.execute("SELECT * FROM acc_details WHERE CustID = ?", (cust_id,))
        account_data = cursor.fetchone()
        acc_savings = account_data[1]
        acc_checking = account_data[2]
        bal_savings =account_data[3]
        bal_checking = account_data[4]

        cursor.execute("SELECT acc_savings, acc_checking FROM acc_details")
        all_acc_data = cursor.fetchall()
        
        connection.close()

        if button_name == "View My Balance":

            # Create a frame for balance panel
            balance_frame = tk.Frame(main_frame)
            balance_frame.pack(fill=tk.BOTH, expand=True)
            balance_frame.configure(bg='#FFFAEB') 

            label_hello = tk.Label(balance_frame, text=f"Hello {fname}!", font=('Roboto', 13))
            label_hello.pack(padx=10, pady=10)
            label_hello.configure(bg='#FFFAEB')

            label_balance = tk.Label(balance_frame, text=f"Your Balance on", font=('Roboto', 13))
            label_balance.pack(padx=10, pady=10)
            label_balance.configure(bg='#FFFAEB')
            
            label_date = tk.Label(balance_frame, text=f"{current_date}", font=('Roboto', 13))
            label_date.pack(padx=10, pady=10)
            label_date.configure(bg='#FFFAEB')

            label_at = tk.Label(balance_frame, text=f"is", font=('Roboto', 13))
            label_at.pack(padx=10, pady=10)
            label_at.configure(bg='#FFFAEB')
            
            def show_balance():
                # Get the selected radio button value
                selected_value = var.get()

                if bal_checking <= 0:
                    color_checking = 'red'
                else:
                    color_checking = 'green'
                if bal_savings <= 0:
                    color_saving = 'red'
                else:
                    color_saving = 'green'

                # Retrieve and display the balance based on the selected radio button
                if selected_value == 1:
                    amount_label.config(text=f"Account number: {acc_checking}\n\nBalance:${bal_checking}", fg = color_checking)
                elif selected_value == 2:
                    amount_label.config(text=f"Account number: {acc_savings}\n\nBalance:${bal_savings}", fg = color_saving)

            var = tk.IntVar()
            # Radio buttons
            radio_button_1 = tk.Radiobutton(balance_frame, text="Checking", variable=var, value=1, command=show_balance, font=('Roboto', 13))
            radio_button_1.configure(bg='#FFFAEB')
            radio_button_1.pack()

            radio_button_2 = tk.Radiobutton(balance_frame, text="Savings", variable=var, value=2, command=show_balance, font=('Roboto', 13))
            radio_button_2.configure(bg='#FFFAEB')
            radio_button_2.pack()

            # Label to display balance
            amount_label = tk.Label(balance_frame, text="", font=("Roboto", 13))
            amount_label.pack(padx=10, pady=10)
            amount_label.configure(bg='#FFFAEB')

        elif button_name == "Transfer Fund":
            def on_select():
                selected_option = account_var.get()
                print(f"Selected option: {selected_option}")
                return selected_option

            def transfer_funds():
                # Get values from entry fields
                selected_option = on_select()
                your_account = selected_option # "checking:1234"
                your_acc_no = your_account.split(":") #['checking','1234']
                your_final_acc = your_acc_no[1] # '1234'

                account_number = entry_account.get()
                payee_name = entry_payee.get()
                amount = entry_amount.get()
                remarks = entry_remarks.get()

                if account_number == "":
                    messagebox.showwarning("Error", "Account Number field is mandatory!")
                elif account_number == your_final_acc:
                    messagebox.showwarning("Error", "Transferring funds to the same account is not permitted.")
                else: 
                    account_exists = any(int(account_number) == row[0] or int(account_number) == row[1] for row in all_acc_data)

                    if account_exists is True:
                        if amount == "":
                            messagebox.showinfo("Error", "Please enter amount")  
                        else:
                            #Checking if Sender has sufficient balance
                            connection = sqlite3.connect("acme_database.db")
                            cursor = connection.cursor()
                            cursor.execute("SELECT * FROM acc_details WHERE CustID = ? ", (cust_id,))
                            
                            sender_data = cursor.fetchone()
                            print(sender_data)
                            print(your_final_acc)
                            if your_final_acc == int(sender_data[1]):
                                sender_bal = sender_data[3]
                            else:
                                sender_bal = sender_data[4] 

                            if float(amount) <= sender_bal: #Sender can send money

                                cursor.execute("SELECT * FROM transactions ORDER BY TransID DESC LIMIT 1")
                                latest_transaction = cursor.fetchone()
                                latest_transid = latest_transaction[0]
                                connection.close()
                                if float(amount) > 0.0:
                                    #Fetching Receiver's Details

                                    connection = sqlite3.connect("acme_database.db")
                                    cursor = connection.cursor()
                                    cursor.execute("SELECT * FROM acc_details WHERE acc_savings = ? OR acc_checking = ?", (int(account_number),int(account_number)))
                                    receiver_data = cursor.fetchone()
                                    receiver_id = receiver_data[0]

                                    cursor.execute("SELECT * FROM transactions ORDER BY TransID DESC LIMIT 1")
                                    latest_transaction = cursor.fetchone()
                                    latest_transid = latest_transaction[0]
                                    connection.close()
                                    
                                    #Collecting values 
                                    TransID =  int(latest_transid) + 1
                                    #TransID = 1
                                    Date = current_date
                                    Time = current_time
                                    SenderAccountNumber = int(your_final_acc)
                                    ReceiverAccountNumber = int(account_number)
                                    Amount = float(amount)
                                    Remarks = remarks
                                    SenderCustID = cust_id
                                    ReceiverCustID = receiver_id

                                    # Create a tuple directly with all values
                                    transaction_data = (
                                        TransID,
                                        Date,
                                        Time,
                                        SenderAccountNumber,
                                        ReceiverAccountNumber,
                                        Amount,
                                        Remarks,
                                        SenderCustID,
                                        ReceiverCustID
                                    )

                                    insert_transaction(transaction_data)
                                    update_sender_acc(Amount, cust_id, SenderAccountNumber)
                                    update_receiver_acc(Amount,  ReceiverCustID, ReceiverAccountNumber)
                                    messagebox.showinfo("Success", "Fund Transfered successfully!")
                                 
                                else:
                                    messagebox.showinfo("Error", "Please enter amount more than 0$")   
                            else:
                                messagebox.showinfo("Error", f"You don't have sufficient balance!. Please enter amount less than {sender_bal}") 
                    else:
                        messagebox.showinfo("Error", "The account does not exist.")
                        
            # Create a frame for Home panel
            transfer_frame = tk.Frame(main_frame)
            transfer_frame.pack(fill=tk.BOTH, expand=True)
            transfer_frame.configure(bg='#FFFAEB') 

            label_your_account = tk.Label(transfer_frame, text=f"Choose your Account Number",font=('Roboto', 13))
            label_your_account.configure(bg='#FFFAEB') 
            label_your_account.grid(row=4, column=1,padx=20, pady=10)
            
            #Dropdown to choose your account
            account_options = [f"Savings:{acc_savings}", f"Checking:{acc_checking}"]    
            account_var = tk.StringVar( main_frame)
            account_var.set(account_options[0]) #Default value
          
            account_dropdown = tk.OptionMenu(transfer_frame, account_var,*account_options)
            account_dropdown.configure(font=('Roboto', 13), width=50) 
            account_dropdown.grid(row=4, column=3,padx=20, pady=10)
            account_var.trace('w', on_select)  # Track changes in the dropdown

            label_account = tk.Label(transfer_frame, text=f"Payee Account Number",font=('Roboto', 13))
            label_account.configure(bg='#FFFAEB') 
            label_account.grid(row=5, column=1,padx=20, pady=10)
            
            entry_account = tk.Entry(transfer_frame, font=('Roboto', 13), width=50)
            entry_account.grid(row=5, column=3,padx=20,  pady=10)

            label_payee = tk.Label(transfer_frame, text="Payee Name",font=('Roboto', 13))
            label_payee.configure(bg='#FFFAEB') 
            label_payee.grid(row=6, column=1,padx=20, pady=10)

            entry_payee = tk.Entry(transfer_frame, font=('Roboto', 13), width=50)
            entry_payee.grid(row=6, column=3,padx=20,  pady=10)

            label_amount = tk.Label(transfer_frame, text="Amount",font=('Roboto', 13))
            label_amount.configure(bg='#FFFAEB') 
            label_amount.grid(row=7, column=1,padx=20, pady=10)

            entry_amount = tk.Entry(transfer_frame, font=('Roboto', 13), width=50)
            entry_amount.grid(row=7, column=3,padx=20,  pady=10)

            label_remarks = tk.Label(transfer_frame, text="Remarks",font=('Roboto', 13))
            label_remarks.configure(bg='#FFFAEB') 
            label_remarks.grid(row=8, column=1,padx=20, pady=10)

            entry_remarks = tk.Entry(transfer_frame, font=('Roboto', 13), width=50)
            entry_remarks.grid(row=8, column=3,padx=20,  pady=10)

            send_button = tk.Button(transfer_frame, text="Send", width=50, height=2)
            send_button.config(command=lambda: transfer_funds()) 
            send_button.grid(row=10, column=3,padx=20, pady=10)
            
        elif button_name == "Transaction History":

            # Create a frame for Transaction History
            history_frame = tk.Frame(main_frame)
            history_frame.pack(fill=tk.BOTH, expand=True)
            history_frame.configure(bg='#FFFAEB') 

            transactions = fetch_transactions(cust_id)
            display_transactions = [(transaction[1], transaction[2], transaction[3], transaction[4],transaction[5],transaction[6]) for transaction in transactions]

            # Create a Treeview widget to display transaction history
            tree = ttk.Treeview(history_frame, columns=('Date', 'Time', 'SenderAccountNumber', 'ReceiverAccountNumber', 'Amount', 'Remarks'), show='headings')

            # Define column headings
            tree.heading('Date', text='Date')
            tree.heading('Time', text='Time')
            tree.heading('SenderAccountNumber', text='Sender Account')
            tree.heading('ReceiverAccountNumber', text='Receiver Account')
            tree.heading('Amount', text='Amount')
            tree.heading('Remarks', text='Remarks')

            # Insert transaction data into the treeview
            for transaction in display_transactions:
                tree.insert('', tk.END, values=transaction)

            # Pack the treeview into the frame
            tree.pack(fill=tk.BOTH, expand=True)

            # Create a ttk.Style and configure the font size for Treeview.Heading
            style = ttk.Style()
            style.configure("Treeview.Heading", font=('Roboto', 13))
            style.configure("Treeview", font=('Roboto', 12))
            
        elif button_name == "My Details":
            # Create a frame for My Details
            details_frame = tk.Frame(main_frame)
            details_frame.pack(fill=tk.BOTH, expand=True)
            details_frame.configure(bg='#FFFAEB') 

            view_my_details(details_frame,cust_id)
            fetch_custid_details(cust_id)
            drop_table()

        elif button_name == "Contact":
            contact_frame = tk.Frame(main_frame)
            contact_frame.pack(fill=tk.BOTH, expand=True)
            contact_frame.configure(bg='#FFFAEB') 
            display_contact_info(contact_frame)

        elif button_name == "Exit":
            drop_table()
            dashboard_window.destroy()

    # Simulate button click on Home button by default
    show_panel("View My Balance", username)
    dashboard_window.mainloop()

#Function to navigate from Screen 1 to Screen
def navigate():
    global root
    root.after(1000, open_dashboard)  # Open dashboard after 1000 milliseconds (1 seconds)

#Calling Screen 1
display_login_screen()
