from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL,
        title TEXT,
        description TEXT,
        favicon TEXT,
        keywords TEXT,
        clicks INTEGER DEFAULT 0,
        upvotes INTEGER DEFAULT 0,
        downvotes INTEGER DEFAULT 0
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    if request.method == 'POST':
        url = request.form['url']
        title = request.form['title']
        description = request.form['description']
        favicon = request.form['favicon']
        keywords = request.form['keywords']

        c.execute('INSERT INTO urls (url, title, description, favicon, keywords) VALUES (?, ?, ?, ?, ?)',
                  (url, title, description, favicon, keywords))
        conn.commit()

    c.execute('SELECT * FROM urls')
    urls = c.fetchall()
    conn.close()

    return render_template('admin.html', urls=urls)

@app.route('/results')
def results():
    query = request.args.get('q', '')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM urls WHERE keywords LIKE ? OR description LIKE ? ORDER BY clicks DESC, upvotes DESC', (f'%{query}%', f'%{query}%'))
    results = c.fetchall()
    conn.close()

    page = int(request.args.get('page', 1))
    per_page = 7
    total_pages = (len(results) + per_page - 1) // per_page

    start = (page - 1) * per_page
    end = start + per_page
    results = results[start:end]

    return render_template('results.html', query=query, results=results, page=page, total_pages=total_pages)

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    url_id = data['id']
    vote_type = data['type']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    if vote_type == 'up':
        c.execute('UPDATE urls SET upvotes = upvotes + 1 WHERE id = ?', (url_id,))
    elif vote_type == 'down':
        c.execute('UPDATE urls SET downvotes = downvotes + 1 WHERE id = ?', (url_id,))

    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

@app.route('/increment_click', methods=['POST'])
def increment_click():
    data = request.json
    url_id = data['id']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE urls SET clicks = clicks + 1 WHERE id = ?', (url_id,))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
