import sqlite3

def get_connection_and_cursor():
    connection = sqlite3.connect('db/invoices.db')
    cursor = connection.cursor()
    return connection, cursor

# Invoice table
connection, cursor = get_connection_and_cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    name TEXT NOT NULL,
    date DATE NOT NULL,
    totalPrice REAL,
    isPaid INTEGER
)
''')

# Clothes table
connection, cursor = get_connection_and_cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Clothes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER,
    clothes_detail TEXT NOT NULL,
    color TEXT
)
''')
connection.commit()
connection.close()


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/invoices.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def get_invoices(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = ("SELECT id, name, date, totalPrice, isPaid, clothes_detail, color, details FROM Invoices, Clothes WHERE Invoices.id = Clothes.invoice_id")
        cursor.execute(query)
        all_data = cursor.fetchall()
        return [_build_invoice(item) for item in all_data]

    def get_invoice(self, invoice_id):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = ("SELECT id, name, date, totalPrice, isPaid, details, color FROM Invoices, Clothes WHERE Invoices.id = ? AND Invoices.id = Clothes.invoice_id")
        cursor.execute(query, (invoice_id,))
        item = cursor.fetchone()
        if item is None:
            return item
        else:
            return _build_invoice(item)

    def add_invoice(self, user, name, date, totalPrice, isPaid, clothes_detail, color, price, details):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO Invoices (user, name, date, totalPrice, isPaid) VALUES (?, ?, ?, ?, ?)",
                    (user, name, date, totalPrice, isPaid))

        invoice_id = cursor.lastrowid

        cursor.execute("INSERT INTO Clothes (invoice_id, clothes_detail, color, price, details) VALUES (?, ?, ?, ?, ?)",
                    (invoice_id, clothes_detail, color, price, details))

        connection.commit()
        connection.close()

        return invoice_id
