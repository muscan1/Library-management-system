from flask import Flask, request, jsonify, send_from_directory, abort
from flask_cors import CORS
import mysql.connector
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# static files directory (project root)
STATIC_DIR = os.path.abspath(os.path.dirname(__file__))

# Debug: Print database config
print("="*50)
print("DATABASE CONFIGURATION:")
print(f"Host: {os.getenv('DB_HOST', 'localhost')}")
print(f"User: {os.getenv('DB_USER', 'root')}")
print(f"Password: {'*' * len(os.getenv('DB_PASSWORD', ''))}")
print(f"Database: {os.getenv('DB_NAME', 'library_db')}")
print("="*50)

# --- Connect to MySQL ---
def db():
    try:
        # Get the password and ensure it handles blank strings properly
        db_password = os.getenv("DB_PASSWORD", "")
        if db_password is None:
            db_password = ""

        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=db_password,
            database=os.getenv("DB_NAME", "library_db")
        )
        return connection
    except mysql.connector.Error as err:
        print(f"❌ Database Connection Error: {err}")
        raise

# --- SIGNUP ---
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()
    try:
        hashed = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())
        con = db()
        cur = con.cursor()
        cur.execute("INSERT INTO users (first_name, last_name, admission, email, password) VALUES (%s,%s,%s,%s,%s)",
                    (data["firstName"], data["lastName"], data["admission"], data["email"], hashed))
        con.commit()
        con.close()
        return jsonify({"message": "Account created!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# --- LOGIN ---
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    try:
        con = db()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE email = %s", (data["email"],))
        user = cur.fetchone()
        con.close()
        
        if user and bcrypt.checkpw(data["password"].encode(), user["password"].encode()):
            return jsonify({
                "message": f"Welcome {user['first_name']}!",
                "user": {
                    "id": user["id"],
                    "firstName": user['first_name'],
                    "lastName": user['last_name'],
                    "email": user['email'],
                    "admission": user['admission']
                }
            })
        return jsonify({"error": "Wrong email or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# --- ADD BOOK ---
@app.route("/api/books", methods=["POST"])
def add_book():
    data = request.get_json()
    try:
        con = db()
        cur = con.cursor()
        cur.execute("INSERT INTO books (title, author, isbn, category, copies) VALUES (%s,%s,%s,%s,%s)",
                    (data["title"], data["author"], data["isbn"], data["category"], data["copies"]))
        con.commit()
        con.close()
        return jsonify({"message": "Book added!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# --- GET ALL BOOKS ---
@app.route("/api/books", methods=["GET"])
def get_books():
    try:
        con = db()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM books")
        books = cur.fetchall()
        con.close()
        return jsonify(books)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# --- BORROW A BOOK ---
@app.route("/api/borrow", methods=["POST"])
def borrow():
    data = request.get_json()
    try:
        con = db()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT id, copies FROM books WHERE isbn = %s", (data["isbn"],))
        book = cur.fetchone()
        if not book:
            return jsonify({"error": "Book not found"}), 404
        if book["copies"] < 1:
            return jsonify({"error": "No copies available"}), 400
        cur.execute("UPDATE books SET copies = copies - 1 WHERE id = %s", (book["id"],))
        cur.execute("INSERT INTO borrow_logs (book_id, user_id, issue_date, status) VALUES (%s,%s,%s,%s)",
                    (book["id"], data["userId"], data["issueDate"], data["status"]))
        con.commit()
        con.close()
        return jsonify({"message": "Book borrowed!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# --- START SERVER ---
@app.route('/', defaults={'path': 'signup&login.html'})
@app.route('/signup')
@app.route('/signup&login')
@app.route('/dashboard')
@app.route('/home')
@app.route('/index')
@app.route('/<path:path>')
def serve(path=None):
    # keep API routes handled by their own view functions
    if not path:
        path = request.path.lstrip('/') or 'signup&login.html'
    if path.startswith('api/'):
        abort(404)

    route_aliases = {
        'signup': 'signup&login.html',
        'signup&login': 'signup&login.html',
        'dashboard': 'Dashboard.html',
        'home': 'index.html',
        'index': 'index.html'
    }

    path = route_aliases.get(path, path)
    full = os.path.join(STATIC_DIR, path)
    if not os.path.exists(full):
        return send_from_directory(STATIC_DIR, 'signup&login.html')
    return send_from_directory(STATIC_DIR, path)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
