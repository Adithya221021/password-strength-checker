from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# ==============================
# DATABASE CONNECTION
# ==============================
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="adithya2104",
        database="password-checker",
        port=3307
    )

# ==============================
# HOME ROUTE
# ==============================
@app.route("/")
def home():
    return "Backend running!"

# ==============================
# CHECK PASSWORD API
# ==============================
@app.route("/check", methods=["POST"])
def check_password():
    data = request.json
    password = data.get("password")

    score = 0

    if len(password) >= 8:
        score += 25
    if any(c.isupper() for c in password):
        score += 25
    if any(c.isdigit() for c in password):
        score += 25
    if any(c in "!@#$%^&*()_+" for c in password):
        score += 25

    strength = "WEAK"

    if score >= 75:
        strength = "STRONG"
    elif score >= 50:
        strength = "MEDIUM"

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "INSERT INTO history (password, strength) VALUES (%s, %s)",
        (password, strength)
    )

    db.commit()
    cur.close()
    db.close()

    return jsonify({
        "score": score,
        "strength": strength
    })

# ==============================
# GET HISTORY API
# ==============================
@app.route("/history", methods=["GET"])
def history():
    db = get_db()
    cur = db.cursor()

    cur.execute(
        "SELECT id, password, strength FROM history ORDER BY id DESC"
    )

    rows = cur.fetchall()

    cur.close()
    db.close()

    return jsonify([
        {
            "id": row[0],
            "password": row[1],
            "strength": row[2]
        }
        for row in rows
    ])

# ==============================
# DELETE HISTORY API
# ==============================
@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_history(id):

    db = get_db()
    cur = db.cursor()

    # check if exists
    cur.execute("SELECT id FROM history WHERE id = %s", (id,))
    record = cur.fetchone()

    if not record:
        cur.close()
        db.close()

        return jsonify({
            "status": "error",
            "message": "Record not found"
        }), 404

    # delete record
    cur.execute("DELETE FROM history WHERE id = %s", (id,))
    db.commit()

    cur.close()
    db.close()

    return jsonify({
        "status": "success",
        "message": "History deleted successfully"
    })

# ==============================
# RUN SERVER
# ==============================
if __name__ == "__main__":
    print("Running on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)