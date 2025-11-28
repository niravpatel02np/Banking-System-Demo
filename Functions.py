# Demo version of Banking Management System
# Full logic removed for safety; only GUI and partial code shown

import tkinter as tk
import datetime

# ---------------- Transaction Functions ----------------

def insert_transaction(transaction_data):
    # Original logic removed for demo
    print("Insert transaction called (demo)")

def update_sender_acc(Amount, cust_id, SenderAccountNumber):
    # Original logic removed for demo
    print(f"Update sender account called for {SenderAccountNumber} (demo)")

def update_receiver_acc(Amount, ReceiverCustID, ReceiverAccountNumber):
    # Original logic removed for demo
    print(f"Update receiver account called for {ReceiverAccountNumber} (demo)")

def get_current_datetime():
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime("%d %B, %Y")
    current_time = current_datetime.strftime("%I:%M %p")
    return current_date, current_time

def fetch_transactions(cust_id):
    # Original logic removed for demo
    print(f"Fetch transactions called for customer {cust_id} (demo)")
    return []

# ---------------- Customer Details Functions ----------------

def save_changes(entries, edit_buttons, feedback_label, cust_id):
    # Demo logic: show edited values only
    edited_data = [entry.get() for entry in entries]
    print("Edited data:", edited_data)
    # Original database save logic removed for demo
    feedback_label.config(text="Changes saved successfully! (demo)", fg="green")

def toggle_editability(entry, edit_button):
    entry.config(state=tk.NORMAL)  # Enable editing
    edit_button.config(state=tk.DISABLED)  # Disable edit button

def view_my_details(details_frame, cust_id):
    # Demo GUI structure
    labels = ['First Name','Last Name','User ID','Email ID','Birth Date']
    entries = []
    edit_buttons = []

    for i, label_text in enumerate(labels):
        label = tk.Label(details_frame, text=label_text, font=('Roboto', 13))
        label.grid(row=i, column=0, padx=10, pady=5)
        label.configure(bg='#FFFAEB') 

        entry = tk.Entry(details_frame, font=('Roboto', 13))
        entry.insert(0, f"Demo {label_text}")  # Placeholder demo data
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry.config(state='readonly')
        entries.append(entry)

        edit_button = tk.Button(details_frame, text='\u270E', font=('Segoe UI Symbol', 12))
        edit_button.grid(row=i, column=2, padx=5, pady=5)
        edit_buttons.append(edit_button)
        edit_button.config(command=lambda e=entry, eb=edit_button: toggle_editability(e, eb))

    feedback_label = tk.Label(details_frame, text="", fg="red", font=('Roboto', 13))
    feedback_label.grid(row=len(labels)+1, columnspan=3, padx=10, pady=5)
    feedback_label.configure(bg='#FFFAEB')

    save_button = tk.Button(details_frame, text="Save Changes", command=lambda: save_changes(entries, edit_buttons, feedback_label, cust_id), font=('Roboto', 13))
    save_button.grid(row=len(labels), columnspan=3, padx=10, pady=10)

def fetch_custid_details(cust_id):
    # Original database logic removed for demo
    print(f"Fetch customer details called for {cust_id} (demo)")
    return [f"Demo{i}" for i in range(13)]  # Placeholder demo data

def update_customer_details(cust_id, edited_data):
    # Original database logic removed for demo
    print(f"Update customer details called for {cust_id} with data {edited_data} (demo)")

# ---------------- Contact Info Function ----------------

def display_contact_info(contact_frame):
    # Demo GUI structure only
    labels = [
        "Customer Support Phone Number: 123-456-7890",
        "Email Address: support@acmebank.com",
        "Physical Address: 123 Main Street, Mount Pleasant, MI, USA",
        "Support Services",
        "24/7 Support: Available round the clock"
    ]

    for text in labels:
        lbl = tk.Label(contact_frame, text=text)
        lbl.pack()
        lbl.configure(bg='#FFFAEB')

    empty_label = tk.Label(contact_frame, text=" ")
    empty_label.pack()
    empty_label.configure(bg='#FFFAEB')

    # Original mainloop removed for demo
    # contact_frame.mainloop()
