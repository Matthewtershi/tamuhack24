from flask import Flask
import sqlite3

conn = sqlite3.connect("testerdb.db")

cursor = conn.cursor()

cursor.execute("""CREATE TABLE users (
                email text,
                first text,
                last text,
                user_ID integer
                )""")

cursor.execute("""CREATE TABLE transactions (
                email text,
                restaurant text,
                item text,
                purchase_amount integer,
                date text
               
                )""")

conn.commit()

conn.close()

app = Flask(__name__)


@app.route("/")
def home_page():


    return 

if __name__ == "__main__":
    app.run(debug=True)