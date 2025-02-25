from flask import Flask, render_template, request, redirect, send_file, jsonify, url_for
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
                    التسلسل INTEGER,
                    المحافظة TEXT,
                    المشروع TEXT,
                    مدرج_في_وزارة_التخطيط TEXT,
                    مؤشر_لدى_وزارة_المالية TEXT,
                    الكلفة_الكلية REAL,
                    الاستثناء_من_أساليب_التعاقد TEXT,
                    استثناء TEXT,
                    الإعلان DATE,
                    دراسة_سيرة_ذاتية BOOLEAN,
                    الدعوات BOOLEAN,
                    الوثيقة_القياسية BOOLEAN,
                    التخويل BOOLEAN,
                    تاريخ_غلق_الدعوات DATE,
                    لجان_الفتح BOOLEAN,
                    لجنة_تحليل TEXT,
                    قرار_لجنة_التحليل_الى_دائرة_العقود DATE,
                    لجنة_المراجعة_والمصادقة TEXT,
                    الإحالة TEXT,
                    مسودة_العقد TEXT,
                    توقيع_العقد DATE,
                    ملاحظات TEXT
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'manage_projects' in request.form:
            return redirect(url_for('add_project'))
        elif 'contracts' in request.form:
            return redirect('/contracts')
        elif 'reports' in request.form:
            return redirect('/reports')
        elif 'other_reports' in request.form:
            return redirect('/other_reports')
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
        form_data = {key: request.form.get(key, '') for key in request.form}
        checkboxes = ['دراسة سيرة ذاتية', 'الدعوات', 'الوثيقة القياسية', 'التخويل', 'لجان الفتح']
        for box in checkboxes:
            form_data[box] = 'صح' if request.form.get(box) else 'خطأ'

        conn = sqlite3.connect('projects.db')
        c = conn.cursor()
        c.execute('''INSERT INTO projects (التسلسل, المحافظة, المشروع, مدرج_في_وزارة_التخطيط, مؤشر_لدى_وزارة_المالية,
                     الكلفة_الكلية, الاستثناء_من_أساليب_التعاقد, استثناء, الإعلان, دراسة_سيرة_ذاتية, الدعوات, الوثيقة_القياسية,
                     التخويل, تاريخ_غلق_الدعوات, لجان_الفتح, لجنة_تحليل, قرار_لجنة_التحليل_الى_دائرة_العقود,
                     لجنة_المراجعة_والمصادقة, الإحالة, مسودة_العقد, توقيع_العقد, ملاحظات)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (
                      form_data['التسلسل'], form_data['المحافظة'], form_data['المشروع'],
                      form_data['مدرج_في_وزارة_التخطيط'], form_data['مؤشر_لدى_وزارة_المالية'],
                      form_data['الكلفة الكلية (دينار عراقي)'], form_data['الاستثناء من أساليب التعاقد'],
                      form_data['استثناء'], form_data['الإعلان'], form_data['دراسة سيرة ذاتية'],
                      form_data['الدعوات'], form_data['الوثيقة القياسية'], form_data['التخويل'],
                      form_data['تاريخ غلق الدعوات'], form_data['لجان الفتح'], form_data['لجنة تحليل'],
                      form_data['قرار لجنة التحليل الى دائرة العقود'], form_data['لجنة المراجعة والمصادقة'],
                      form_data['الإحالة'], form_data['مسودة العقد'], form_data['توقيع العقد'],
                      form_data['ملاحظات']
                  ))
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

    columns = [
        'ID', 'التسلسل', 'المحافظة', 'المشروع', 'مدرج في وزارة التخطيط', 'مؤشر لدى وزارة المالية',
        'الكلفة الكلية', 'الاستثناء من أساليب التعاقد', 'استثناء', 'الإعلان', 'دراسة سيرة ذاتية',
        'الدعوات', 'الوثيقة القياسية', 'التخويل', 'تاريخ غلق الدعوات', 'لجان الفتح',
        'لجنة تحليل', 'قرار لجنة التحليل الى دائرة العقود', 'لجنة المراجعة والمصادقة',
        'الإحالة', 'مسودة العقد', 'توقيع العقد', 'ملاحظات'
    ]

    df = pd.DataFrame(projects, columns=columns)

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
        c.execute("SELECT * FROM projects WHERE المشروع LIKE ?", ('%' + project_name + '%',))
        reports = c.fetchall()
        conn.close()
    return render_template('reports.html', reports=reports)

@app.route('/search_reports', methods=['POST'])
def search_reports():
    data = request.get_json()
    project_name = data.get('project_name')

    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute("SELECT * FROM projects WHERE المشروع LIKE ?", ('%' + project_name + '%',))
    reports = c.fetchall()
    conn.close()
    return jsonify(reports)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
