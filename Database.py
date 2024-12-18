import sqlite3
import csv


DATABASE_NAME = "invoice_database.db"

def Create_database():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Invoices (
            InvoiceId INTEGER PRIMARY KEY AUTOINCREMENT,
            Supplier TEXT NOT NULL,
            InvoiceNum TEXT NOT NULL,
            InvoiceDate TEXT NOT NULL,
            TTC REAL NOT NULL,
            TVA REAL NOT NULL,
            TT REAL NOT NULL
        )
    ''')
    connection.commit()
    connection.close()
    print("Database and table created successfully.")


def Insert_invoice(data):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?' for _ in data.values()])
    query = f"INSERT INTO Invoices ({columns}) VALUES ({placeholders})"
    cursor.execute(query, tuple(data.values()))
    connection.commit()
    connection.close()
    print("New invoice inserted successfully.")

def delete_invoice_by_id(invoice_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    query = "DELETE FROM Invoices WHERE InvoiceId = ?"
    cursor.execute(query, (invoice_id,))
    connection.commit()
    connection.close()
    print(f"Invoice with ID {invoice_id} deleted successfully.")

def Insert_From_csv(csv_file_path):
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            data = {
                "Supplier": row[1],
                "InvoiceNum": row[3],
                "InvoiceDate": row[2],
                "TTC": float(row[4]),
                "TVA": float(row[6]),
                "TT": float(row[5])
            }
            Insert_invoice(data)
    print("All rows from CSV inserted successfully.")


def Get_Statistics():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    
    # Total invoices
    cursor.execute("SELECT COUNT(*) FROM Invoices")
    total_invoices = cursor.fetchone()[0]
    
    # Total unique suppliers
    cursor.execute("SELECT COUNT(DISTINCT Supplier) FROM Invoices")
    total_suppliers = cursor.fetchone()[0]
    
    # Cumulative TTC
    cursor.execute("SELECT SUM(TTC) FROM Invoices")
    cumulative_ttc = cursor.fetchone()[0] or 0.0  # Handle None case
    
    # Cumulative TVA
    cursor.execute("SELECT SUM(TVA) FROM Invoices")
    cumulative_tva = cursor.fetchone()[0] or 0.0  # Handle None case
    
    connection.close()
    
    # Return the statistics as a dictionary
    statistics = {
        "Total_Invoices": total_invoices,
        "Total_Suppliers": total_suppliers,
        "Cumulative_TTC": round(cumulative_ttc, 2),
        "Cumulative_TVA": round(cumulative_tva, 2),
    }
    
    return statistics


#Create_database()
#Insert_From_csv("grounding_truth.csv")



