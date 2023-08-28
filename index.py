import sqlite3
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

@app.route('/recu/<id_invoice>', methods=['GET'])
def invoice_page(id_invoice):
    invoice = get_db().get_invoice(id_invoice)
    if invoice:
        return render_template('details.html', invoice=invoice)
    else:
        return redirect(url_for('not_found'))  # Redirect to the not_found route

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.route('/recherche')
def recherche():
    Kword = request.args.get('Kword').lower()
    db = get_db()
    invoices = db.get_invoices()  # Use get_invoices from Database class

    filter_invoices = [invoice for invoice in invoices 
                     if Kword in str(invoice['id']).lower() or Kword in invoice['date']]

    if not filter_invoices:
        return render_template('notFound.html')
    else:  
        return render_template('results.html', invoices=filter_invoices)

if __name__ == "__main__":
    app.run(debug=True)
