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

# 2. API Route to fetch items from PostgreSQL
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

# 3. API Route to handle item claims
@app.route('/api/claim', methods=['POST'])
def claim_item():
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert claim record into database
        cur.execute(
            """
            INSERT INTO claims (item_id, full_name, department, year, usn) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            (data['item_id'], data['full_name'], data['department'], data['year'], data['usn'])
        )
        
        # Update item status to 'Claimed'
        cur.execute("UPDATE items SET status = 'Claimed' WHERE id = %s", (data['item_id'],))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"success": True, "message": "Claim submitted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)