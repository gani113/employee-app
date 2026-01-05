import os
import mysql.connector
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        role = request.form.get("role")
        experience = request.form.get("experience")

        conn = None
        cursor = None

        try:
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                database=os.getenv("DB_NAME"),
                port=3306,
                charset="utf8mb4",
                connection_timeout=5   # ⭐ VERY IMPORTANT
            )

            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO employees (name, role, experience) VALUES (%s, %s, %s)",
                (name, role, experience)
            )
            conn.commit()

        except mysql.connector.Error as err:
            return f"<h3>Database error: {err}</h3>", 500

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    return """
    <!DOCTYPE html>
    <html>
    <head>
      <title>Employee App</title>
    </head>
    <body>
      <h2>Add Employee</h2>
      <form method="POST">
        <label>Name:</label><br>
        <input type="text" name="name" required><br><br>

        <label>Role:</label><br>
        <input type="text" name="role" required><br><br>

        <label>Experience (Years):</label><br>
        <input type="number" name="experience" required><br><br>

        <button type="submit">Save</button>
      </form>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
