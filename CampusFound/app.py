from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import traceback

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "dbname": "CampusFoundDB",
    "user": "postgres",
    "password": "@Guntar01",  # Replace with your actual PostgreSQL password
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/')
def home():
    return render_template('index.html')

# GET Items (Supports filtering by reporter if requested)
@app.route('/api/items', methods=['GET'])
def get_items():
    try:
        reporter = request.args.get('reported_by')
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        if reporter:
            cur.execute("SELECT * FROM items WHERE reported_by = %s ORDER BY created_at DESC;", (reporter,))
        else:
            cur.execute("SELECT * FROM items ORDER BY created_at DESC;")
            
        items = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(items)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# POST: Report a new item
@app.route('/api/items', methods=['POST'])
def add_item():
    try:
        data = request.json
        print("Received item data:", data)
        
        title = data.get('title')
        category = data.get('category')
        location = data.get('location')
        date = data.get('date')
        description = data.get('description')
        image_url = data.get('image_url') or 'https://images.unsplash.com/photo-1584438784894-089d6a62b8fa?w=600&auto=format&fit=crop&q=80'
        reported_by = data.get('reported_by') or 'Guest'

        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            """
            INSERT INTO items (title, category, location, date, description, image_url, reported_by, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'Available')
            """,
            (title, category, location, date, description, image_url, reported_by)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"success": True, "message": "Item reported successfully!"})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

# DELETE: Cancel a report (Only by the person who reported it)
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        data = request.json or {}
        reporter = data.get('reported_by')
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verify ownership before deleting
        cur.execute("SELECT reported_by FROM items WHERE id = %s", (item_id,))
        item = cur.fetchone()
        
        if not item:
            return jsonify({"success": False, "error": "Item not found"}), 404
            
        if reporter and item[0].lower() != reporter.lower():
            return jsonify({"success": False, "error": "Unauthorized: Only the reporter can cancel this item."}), 403
            
        cur.execute("DELETE FROM items WHERE id = %s", (item_id,))
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"success": True, "message": "Report cancelled successfully."})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

# Claim Route
@app.route('/api/claim', methods=['POST'])
def claim_item():
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO claims (item_id, full_name, department, year, usn) VALUES (%s, %s, %s, %s, %s)",
            (data['item_id'], data['full_name'], data['department'], data['year'], data['usn'])
        )
        cur.execute("UPDATE items SET status = 'Claimed' WHERE id = %s", (data['item_id'],))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"success": True, "message": "Claim submitted successfully!"})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)