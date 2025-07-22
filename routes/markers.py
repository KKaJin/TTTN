from flask import Blueprint, request, jsonify
import sqlite3
from db import DB_FILE

bp = Blueprint('markers', __name__)

@bp.route('/api/markers', methods=['GET', 'POST'])
def markers():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if request.method == 'POST':
        data = request.get_json()
        c.execute('INSERT INTO markers (name, lat, lng) VALUES (?, ?, ?)', (data['name'], data['lat'], data['lng']))
        conn.commit()
        return jsonify({'success': True})
    else:
        c.execute('SELECT name, lat, lng FROM markers')
        rows = c.fetchall()
        return jsonify([{ 'name': r[0], 'lat': r[1], 'lng': r[2] } for r in rows])
