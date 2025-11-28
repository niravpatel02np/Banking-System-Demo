import tkinter as tk
import sqlite3
import datetime

def insert_transaction(transaction_data):
    connection = sqlite3.connect("acme_database.db") # Establish a database connection
    cursor = connection.cursor() # Create a cursor

    insert_query = '''INSERT INTO transactions (TransID, Date, Time, SenderAccountNumber, ReceiverAccountNumber, Amount, Remarks, SenderCustID, ReceiverCustID  ) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    cursor.execute(insert_query, transaction_data)

    connection.commit()
    # Close the cursor and the connection
    cursor.close()
    connection.close()

def update_sender_acc(Amount, cust_id, SenderAccountNumber):
    connection = sqlite3.connect("acme_database.db") # Establish a database connection
    cursor = connection.cursor() # Create a cursor

    # Update balance for sender account if checking account
    cursor.execute('''
    UPDATE acc_details
    SET bal_checking = bal_checking - ?
    WHERE CustID = ? AND acc_checking = ? ;
''', (Amount, cust_id, SenderAccountNumber))
    
    # Update balance for sender account if saving account
    cursor.execute('''
    UPDATE acc_details
    SET bal_savings = bal_savings - ?
    WHERE CustID = ? AND acc_savings = ? ;
''', (Amount, cust_id, SenderAccountNumber))
    
    connection.commit()
    # Close the cursor and the connection
    cursor.close()
    connection.close()

def update_receiver_acc(Amount,  ReceiverCustID, ReceiverAccountNumber):
    connection = sqlite3.connect("acme_database.db") # Establish a database connection
    cursor = connection.cursor() # Create a cursor

    # Update balance for receiver account if checking account
    cursor.execute('''
    UPDATE acc_details
    SET bal_checking = bal_checking + ?
    WHERE CustID = ? AND acc_checking = ? ;
''', (Amount,  ReceiverCustID, ReceiverAccountNumber))
    
    #Update balance for receiver account if savings account
    cursor.execute('''
    UPDATE acc_details
    SET bal_savings = bal_savings + ?
    WHERE CustID = ? AND acc_savings = ? ;
''', (Amount,  ReceiverCustID, ReceiverAccountNumber))
    
    connection.commit()
    # Close the cursor and the connection
    cursor.close()
    connection.close()

def get_current_datetime():
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime("%d %B, %Y")
    current_time = current_datetime.strftime("%I:%M %p")
    return current_date, current_time

def fetch_transactions(cust_id):
    connection = sqlite3.connect("acme_database.db") # Establish a database connection
    cursor = connection.cursor() # Create a cursor

    fetch_query = "SELECT * FROM transactions WHERE SenderCustID = ? OR ReceiverCustID = ?"
    cursor.execute(fetch_query,(cust_id, cust_id))
    transactions = cursor.fetchall()

    connection.commit()
    # Close the cursor and the connection
    cursor.close()
    connection.close()

    return transactions

# Function to save changes
def save_changes(entries, edit_buttons, feedback_label,cust_id):
    edited_data = [entry.get() for entry in entries]
    print(edited_data)
    update_customer_details(cust_id, edited_data) #Calling function to save edited changes
    feedback_label.config(text="Changes saved successfully!", fg="green")

# Function to toggle editability of entry fields
def toggle_editability(entry, edit_button):
        entry.config(state=tk.NORMAL)  # Enable editing
        edit_button.config(state=tk.DISABLED)  # Disable edit button

def view_my_details(details_frame,cust_id):

    # Create labels and entry fields for each detail
    labels = ['First Name','Last Name','User ID', 'Email ID', 'Birth Date','Savings Account Number', 'Checking Account Number',
                'Contact Number', 'Street Address 1', 'Street Address 2', 'City', 'State', 'Postal Code']
    entries = []
    edit_buttons = []
    readonly_fields = [0,1,2,4,5,6]  # Indices of fields to be read-only
    cust_data = fetch_custid_details(cust_id)
    entry_edit_map = {}

    for i, label_text in enumerate(labels):
        label = tk.Label(details_frame, text=label_text, font=('Roboto', 13))
        label.grid(row=i, column=0, padx=10, pady=5)
        label.configure(bg='#FFFAEB') 
        
        entry = tk.Entry(details_frame, font=('Roboto', 13))
        entry.insert(0, cust_data[i])  
        entry.grid(row=i, column=1, padx=10, pady=5)

        if i in readonly_fields:
            entry.config(state='readonly')  # Set read-only state for specified fields
        else:
            entry.config(state='readonly') #initialy uneditable

            edit_button = tk.Button(details_frame, text='\u270E', font=('Segoe UI Symbol', 12))        
            edit_buttons.append(edit_button)
            entry_edit_map[entry] = edit_button
            entries.append(entry)
            edit_button.config(command=lambda e=entry, eb=edit_button: toggle_editability(e, eb))
            edit_button.grid(row=i, column=2, padx=5, pady=5)

     # Create Save button
    save_button = tk.Button(details_frame, text="Save Changes", command=lambda: save_changes(entries, edit_buttons, feedback_label,cust_id),font=('Roboto', 13))
    save_button.grid(row=len(labels), columnspan=3, padx=10, pady=10)

    feedback_label = tk.Label(details_frame, text="", fg="red", font=('Roboto', 13))
    feedback_label.grid(row=len(labels) + 1, columnspan=3, padx=10, pady=5)
    feedback_label.configure(bg='#FFFAEB')

def fetch_custid_details(cust_id):
    connection = sqlite3.connect("acme_database.db") # Establish a database connection
    cursor = connection.cursor() # Create a cursor

    join_query = '''CREATE TABLE IF NOT EXISTS cust_filter_data AS 
    SELECT Customer.FName, Customer.LName, Customer.UserID, CustomerDetails.EmailID, CustomerDetails.BirthDate, acc_details.acc_savings, acc_details.acc_checking,
    Customer.Contact, CustomerDetails.StreetAddress1, CustomerDetails.StreetAddress2, CustomerDetails.City, CustomerDetails.State, CustomerDetails.PostalCode
    FROM Customer
    INNER JOIN CustomerDetails ON Customer.CustID = CustomerDetails.CustID 
    INNER JOIN acc_details ON CustomerDetails.CustID = acc_details.CustID WHERE Customer.CustID = ? '''
    cursor.execute(join_query,(cust_id,))

    fetch_query = "SELECT * FROM cust_filter_data"
    cursor.execute(fetch_query)
    cust_data = cursor.fetchone()
    
    connection.commit()
    # Close the cursor and the connection
    cursor.close()
    connection.close()

    return cust_data

def update_customer_details(cust_id, edited_data):
    connection = sqlite3.connect("acme_database.db") # Establish a database connection
    cursor = connection.cursor() # Create a cursor

    cursor.execute('''
    UPDATE CustomerDetails
    SET EmailID = ?,
        StreetAddress1 = ?,
        StreetAddress2 = ?,
        City = ?,
        State = ?,
        PostalCode = ?
    WHERE CustID = ?
                   ''',(edited_data[0], edited_data[2],edited_data[3],edited_data[4],edited_data[5],edited_data[6],cust_id))
    
    cursor.execute('''
    UPDATE Customer
    SET Contact = ?
    WHERE CustID = ?
                   ''',(edited_data[1],cust_id))

    connection.commit()
    # Close the cursor and the connection
    cursor.close()
    connection.close()

def display_contact_info(contact_frame):

    # Contact Information
    phone_label = tk.Label(contact_frame, text="Customer Support Phone Number: 123-456-7890")
    phone_label.pack()
    phone_label.configure(bg='#FFFAEB')

    email_label = tk.Label(contact_frame, text="Email Address: support@acmebank.com")
    email_label.pack()
    email_label.configure(bg='#FFFAEB')

    address_label = tk.Label(contact_frame, text="Physical Address: 123 Main Street, Mount Pleasant, MI, USA")
    address_label.pack()
    address_label.configure(bg='#FFFAEB')

    empty_label = tk.Label(contact_frame, text=" ")
    empty_label.pack()
    empty_label.configure(bg='#FFFAEB')

    # Support Services
    support_label = tk.Label(contact_frame, text="Support Services")
    support_label.pack()
    support_label.configure(bg='#FFFAEB')

    twenty_four_seven_label = tk.Label(contact_frame, text="24/7 Support: Available round the clock")
    twenty_four_seven_label.pack()
    twenty_four_seven_label.configure(bg='#FFFAEB')

    contact_frame.mainloop()    
