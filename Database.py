import sqlite3
import pandas as pd  #This module is used to import data from excel to directly sqlite database

def create_database():

    # Define the SQL statement
    create_table_customer = '''
    CREATE TABLE IF NOT EXISTS Customer (
        CustID INTEGER PRIMARY KEY,
        UserID TEXT,
        Fname TEXT,
        Lname TEXT,
        Contact TEXT,
        Password TEXT
    )
'''
    create_table_accounts = '''
    CREATE TABLE IF NOT EXISTS acc_details (
        CustID INTEGER,
        acc_savings INTEGER,
        acc_checking INTEGER,
        bal_savings REAL,
        bal_checking REAL,
        FOREIGN KEY (CustID) REFERENCES Customer(CustID)
)
'''
    create_table_transactions = '''
    CREATE TABLE IF NOT EXISTS transactions (
        TransID INTEGER PRIMARY KEY,
        Date TEXT,
        Time TEXT,
        SenderAccountNumber INTEGER,
        ReceiverAccountNumber INTEGER,
        Amount REAL,
        Remarks TEXT,
        SenderCustID INTEGER,
        ReceiverCustID INTEGER
)
'''
    create_table_CustomerDetails = '''
    CREATE TABLE IF NOT EXISTS CustomerDetails (
        CustID INTEGER PRIMARY KEY,
        EmailID TEXT,
        BirthDate TEXT,
        StreetAddress1 TEXT,
        StreetAddress2 TEXT,
        City TEXT,
        State TEXT,
        PostalCode TEXT
)
'''
    connection = sqlite3.connect("acme_database.db") # Establish a database connection
    cursor = connection.cursor() # Create a cursor

    cursor.execute(create_table_customer)
    print('Customer Table has been created')

    cursor.execute(create_table_accounts)
    print('Account Details Table has been created')

    cursor.execute(create_table_transactions)
    print('Transactions Table has been created')

    cursor.execute(create_table_CustomerDetails)
    print('Customer Details has been created')

    connection.commit()
    # Close the cursor and the connection
    cursor.close()
    connection.close()

create_database()

def insert_from_excel():

    #Inserting data into Customer Table from Excel
    excel_file = r'D:\Nirav\ALL Documents\America 2023\CMU\Study\BIS 628\Python Project\ProjectData.csv'  
    sheet_name = 'Sheet1'  
    data = pd.read_excel(excel_file, sheet_name=sheet_name)

    connection = sqlite3.connect("acme_database.db")
    cursor = connection.cursor()

    # Check if the table 'Customer' is empty
    cursor.execute("SELECT COUNT(*) FROM Customer")
    result = cursor.fetchone()

    if result[0] == 0:  # If the count is 0, indicating the table is empty
        # Insert data into the Customer table
        data.to_sql('Customer', connection, if_exists='append', index=False)
        print("Data inserted successfully.")
    else:
        print("Table 'Customer' is not empty. Data insertion skipped.")

    connection.commit()
    connection.close()

    #Inserting data into Account Table from Excel
    excel_file = r'D:\Nirav\ALL Documents\America 2023\CMU\Study\BIS 628\Python Project\ProjectData.csv'  
    sheet_name = 'Sheet2'  
    data = pd.read_excel(excel_file, sheet_name=sheet_name)

    connection = sqlite3.connect("acme_database.db")
    cursor = connection.cursor()

    # Check if the table 'acc_details' is empty
    cursor.execute("SELECT COUNT(*) FROM acc_details")
    result = cursor.fetchone()

    if result[0] == 0:  # If the count is 0, indicating the table is empty
        # Insert data into the table
        data.to_sql('acc_details', connection, if_exists='append', index=False)
        print("Data inserted successfully into acc_details.")
    else:
        print("Table 'acc_details' is not empty. Data insertion skipped.")

    connection.commit()
    connection.close()

    #Inserting data into Customer Details Table from Excel
    excel_file = r'D:\Nirav\ALL Documents\America 2023\CMU\Study\BIS 628\Python Project\ProjectData.csv'  
    sheet_name = 'Sheet3'  
    data = pd.read_excel(excel_file, sheet_name=sheet_name)

    connection = sqlite3.connect("acme_database.db")
    cursor = connection.cursor()

    # Check if the table 'CustomerDetails' is empty
    cursor.execute("SELECT COUNT(*) FROM CustomerDetails")
    result = cursor.fetchone()

    if result[0] == 0:  # If the count is 0, indicating the table is empty
        # Insert data into the CustomerDetails table
        data.to_sql('CustomerDetails', connection, if_exists='append', index=False)
        print("Data inserted successfully.")
    else:
        print("Table 'CustomerDetails' is not empty. Data insertion skipped.")

    connection.commit()
    connection.close()

insert_from_excel()

def drop_table():
    import sqlite3

    # Connect to the database
    connection = sqlite3.connect("acme_database.db")
    cursor = connection.cursor()

    # Execute the SQL command to drop the table
    cursor.execute("DROP TABLE IF EXISTS cust_filter_data")

    connection.commit()
    # Close the cursor and the connection
    cursor.close()
    connection.close()
