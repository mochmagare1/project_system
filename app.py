from flask import Flask, render_template, request, redirect, send_file, jsonify
import sqlite3
import pandas as pd
from io import BytesIO

app = Flask(__name__)

# إنشاء قاعدة البيانات والجداول

def init_db():
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    الفصل TEXT,
                    المادة TEXT,
                    النوع TEXT,
                    التسلسل INTEGER,
                    اسم_المشروع TEXT,
                    الكلفة_الكلية REAL,
                    الإجراءات TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'projects' in request.form:
            return redirect('/projects')
        elif 'reports' in request.form:
            return redirect('/reports')
    return render_template('home.html')

@app.route('/projects')
def projects():
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute('SELECT * FROM projects')
    projects = c.fetchall()
    conn.close()
    return render_template('projects.html', projects=projects)

@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        الفصل = request.form['الفصل']
        المادة = request.form['المادة']
        النوع = request.form['النوع']
        اسم_المشروع = request.form['اسم_المشروع']
        الكلفة_الكلية = request.form['الكلفة_الكلية']
        الإجراءات = request.form['الإجراءات']

        conn = sqlite3.connect('projects.db')
        c = conn.cursor()
        c.execute('''INSERT INTO projects (الفصل, المادة, النوع, اسم_المشروع, الكلفة_الكلية, الإجراءات) 
                     VALUES (?, ?, ?, ?, ?, ?)''',
                    (الفصل, المادة, النوع, اسم_المشروع, الكلفة_الكلية, الإجراءات))
        conn.commit()
        conn.close()

        return redirect('/projects')
    return render_template('add_project.html')

@app.route('/export_excel')
def export_excel():
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute('SELECT * FROM projects')
    projects = c.fetchall()
    conn.close()

    df = pd.DataFrame(projects, columns=['ID', 'الفصل', 'المادة', 'النوع', 'التسلسل', 'اسم المشروع', 'الكلفة الكلية', 'الإجراءات'])

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='مشاريع')
    output.seek(0)

    return send_file(output, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                     as_attachment=True, download_name="projects.xlsx")

@app.route('/reports', methods=['GET', 'POST'])
def reports():
    reports = []
    if request.method == 'POST':
        project_name = request.form.get('project_name')
        conn = sqlite3.connect('projects.db')
        c = conn.cursor()
        c.execute("SELECT * FROM projects WHERE اسم_المشروع LIKE ?", ('%' + project_name + '%',))
        reports = c.fetchall()
        conn.close()
    return render_template('reports.html', reports=reports)

@app.route('/search_reports', methods=['POST'])
def search_reports():
    data = request.get_json()
    project_name = data.get('project_name')

    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute("SELECT * FROM projects WHERE اسم_المشروع LIKE ?", ('%' + project_name + '%',))
    reports = c.fetchall()
    conn.close()
    return jsonify(reports)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
