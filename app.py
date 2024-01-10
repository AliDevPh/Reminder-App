from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)
app.static_folder = 'static' 

# Database initialization
conn = sqlite3.connect('schedules.db')
conn.execute('''
    CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        category TEXT NOT NULL,
        datetime TEXT NOT NULL
    )
''')
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_schedule', methods=['POST'])
def add_schedule():
    data = request.json
    text = data['text']
    category = data['category']
    datetime_str = data['datetime']

    try:
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
    except ValueError:
        return jsonify({'message': 'Invalid datetime format'}), 400

    conn = sqlite3.connect('schedules.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO schedules (text, category, datetime) VALUES (?, ?, ?)',
                   (text, category, datetime_obj))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Schedule added successfully'}), 200

@app.route('/get_schedules')
def get_schedules():
    conn = sqlite3.connect('schedules.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, text, category, datetime FROM schedules')
    schedules = [{'id': row[0], 'text': row[1], 'category': row[2], 'datetime': row[3]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(schedules)

@app.route('/delete_schedule/<int:schedule_id>')
def delete_schedule(schedule_id):
    conn = sqlite3.connect('schedules.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM schedules WHERE id = ?', (schedule_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Schedule deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
