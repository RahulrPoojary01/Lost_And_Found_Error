from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras

app = Flask(__name__)
CORS(app)

# Database configuration for CampusFoundDB
DB_CONFIG = {
    "dbname": "CampusFoundDB",
    "user": "postgres",
    "password": "Guntar01",  # Replace with your actual PostgreSQL password
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# 1. Route to serve the frontend webpage
@app.route('/')
def home():
    return render_template('index.html')

# 2. GET API: Fetch all items from PostgreSQL
@app.route('/api/items', methods=['GET'])
def get_items():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM items ORDER BY created_at DESC;")
        items = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. POST API: Report a new lost/found item
@app.route('/api/items', methods=['POST'])
def add_item():
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            """
            INSERT INTO items (title, category, location, date, description, image_url, status) 
            VALUES (%s, %s, %s, %s, %s, %s, 'Available')
            """,
            (
                data['title'],
                data['category'],
                data['location'],
                data['date'],
                data['description'],
                data.get('image_url', 'https://images.unsplash.com/photo-1584438784894-089d6a62b8fa?w=600&auto=format&fit=crop&q=80')
            )
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"success": True, "message": "Item reported successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 4. POST API: Handle item claims
@app.route('/api/claim', methods=['POST'])
def claim_item():
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            """
            INSERT INTO claims (item_id, full_name, department, year, usn) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            (data['item_id'], data['full_name'], data['department'], data['year'], data['usn'])
        )
        
        cur.execute("UPDATE items SET status = 'Claimed' WHERE id = %s", (data['item_id'],))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"success": True, "message": "Claim submitted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)