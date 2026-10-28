
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("customers.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()

        if name and email and phone:
            conn = get_db()
            conn.execute(
                "INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)",
                (name, email, phone)
            )
            conn.commit()
            conn.close()

        return redirect(url_for("index"))

    conn = get_db()
    customers = conn.execute(
        "SELECT * FROM customers ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("index.html", customers=customers)

@app.route("/update/<int:customer_id>", methods=["GET", "POST"])
def update_customer(customer_id):
    conn = get_db()

    customer = conn.execute(
        "SELECT * FROM customers WHERE id = ?",
        (customer_id,)
    ).fetchone()

    if customer is None:
        conn.close()
        return "Customer not found", 404

    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()

        if name and email and phone:
            conn.execute(
                """UPDATE customers
                   SET name = ?, email = ?, phone = ?
                   WHERE id = ?""",
                (name, email, phone, customer_id)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("index"))

    conn.close()
    return render_template("update.html", customer=customer)

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
