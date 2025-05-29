from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'resumes.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            education TEXT,
            skills TEXT,
            projects TEXT,
            achievements TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    resumes = conn.execute('SELECT * FROM resumes').fetchall()
    conn.close()
    return render_template('index.html', resumes=resumes)

@app.route('/add', methods=('GET', 'POST'))
def add_resume():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        education = request.form['education']
        skills = request.form['skills']
        projects = request.form['projects']
        achievements = request.form['achievements']

        conn = get_db_connection()
        conn.execute('INSERT INTO resumes (fullname, email, phone, education, skills, projects, achievements) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (fullname, email, phone, education, skills, projects, achievements))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_resume.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_resume(id):
    conn = get_db_connection()
    resume = conn.execute('SELECT * FROM resumes WHERE id = ?', (id,)).fetchone()

    if resume is None:
        return 'Resume Not Found!', 404

    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        education = request.form['education']
        skills = request.form['skills']
        projects = request.form['projects']
        achievements = request.form['achievements']

        conn.execute('''
            UPDATE resumes SET fullname = ?, email = ?, phone = ?, education = ?, skills = ?, projects = ?, achievements = ?
            WHERE id = ?
        ''', (fullname, email, phone, education, skills, projects, achievements, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_resume.html', resume=resume)

@app.route('/delete/<int:id>', methods=('POST',))
def delete_resume(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM resumes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
