import sqlite3
import datetime
from flask import Flask, render_template, request, redirect, g, url_for
from database import Database

app = Flask(__name__, static_url_path="", static_folder="static")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()

@app.route('/', methods=['GET'])
def start():
    print("Hello")

@app.route('/submit', methods=['POST'])
def submit_form():
    user = request.form.get('user')
    name = request.form.get('name')
    date = datetime.date.today()
    totalPrice = request.form.get('totalPrice')
    isPaid = request.form.get('paymentStatus')
    clothes_detail = request.form.get('clothes_detail')
    color = request.form.get('color')
    price = request.form.get('price')
    details = request.form.get('details')

    request_data = request.get_json()
    clothes_data = request_data.get('clothesData', [])

    db = get_db()
    invoice_id = db.add_invoice(user, name, date, totalPrice, isPaid, clothes_detail, color, price, details)

    print("Success")
    print(user + " " + name)
    return redirect(url_for('invoice_page', id_invoice=invoice_id))

@app.route('/recu/<id_invoice>', methods=['GET'])
def invoice_page(id_invoice):
    invoice = get_db().get_invoice(id_invoice)
    if invoice:
        return render_template('details.html', invoice=invoice)
    else:
        return redirect(url_for('not_found'))  

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.route('/recherche')
def recherche():
    query = request.args.get('query').lower()
    db = get_db()
    invoices = db.get_invoices()
    
    filter = filter_invoice(invoices, query)

    if not filter:
        return render_template('notFound.html')
    else:  
        return render_template('results.html', invoices=filter)

def filter_invoice(invoices,query):
    filter = []
    for invoice in invoices:
        if invoice['name'].lower()in query or invoice['id'] in query:
            filter.append(invoice)
    return filter

if __name__ == "__main__":
    app.run(debug=True)
