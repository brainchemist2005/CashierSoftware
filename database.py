import sqlite3

connection = sqlite3.connect('invoices.db')
cursor = connection.cursor()

#Invoice table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Invoices (
    id INTEGER PRIMARY KEY,
    user TEXT NOT NULL,
    date DATE NOT NULL,
    totalPrice REAL
)
''')

#Clothes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Clothes (
    id INTEGER PRIMARY KEY,
    invoice_id INTEGER,
    clothes_detail TEXT NOT NULL,
    color TEXT,
    price INTEGER,    
    details TEXT,
    FOREIGN KEY(invoice_id) REFERENCES Invoices(id)
)
''')

connection.commit()
connection.close()