from flask import Flask, jsonify
import sqlite3
from Database import Get_Statistics


app = Flask(__name__)

DATABASE_NAME = "invoice_database.db"

def get_all_invoices():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    
    query = "SELECT * FROM Invoices;"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # Map rows to a list of dictionaries
    invoices = [
        {
            "InvoiceId": row[0],
            "Supplier": row[1],
            "InvoiceNum": row[2],
            "InvoiceDate": row[3],
            "TTC": row[4],
            "TVA": row[5],
            "TT": row[6]
        }
        for row in rows
    ]
    
    connection.close()
    return invoices


@app.route('/invoices', methods=['GET'])
def fetch_invoices():
    invoices = get_all_invoices()
    return jsonify(invoices), 200

@app.route('/statistics', methods=['GET'])
def fetch_statistics():
    statistics = Get_Statistics()
    return jsonify(statistics), 200

if __name__ == "__main__":
    app.run(debug=True,port=8000)






















