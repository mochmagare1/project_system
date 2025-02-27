from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret123'

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

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')

    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        hashed_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', hashed_password))

    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('projects.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            session['username'] = username
            flash('تم تسجيل الدخول بنجاح!', 'success')
            return redirect(url_for('home'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('تم تسجيل الخروج.', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('projects.db')
        c = conn.cursor()

        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            flash('تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('اسم المستخدم موجود بالفعل. اختر اسمًا آخر.', 'warning')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        flash('يجب تسجيل الدخول أولاً!', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'manage_projects' in request.form:
            return redirect(url_for('add_project'))
        elif 'contracts' in request.form:
            return redirect(url_for('projects'))
        elif 'reports' in request.form:
            return redirect(url_for('reports'))

    return render_template('home.html')

@app.route('/projects')
def projects():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute('SELECT * FROM projects')
    projects = c.fetchall()
    conn.close()

    return render_template('projects.html', projects=projects)

@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if 'username' not in session:
        return redirect(url_for('login'))

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

        flash('تمت إضافة المشروع بنجاح!', 'success')
        return redirect(url_for('projects'))

    return render_template('add_project.html')

@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if 'username' not in session:
        return redirect(url_for('login'))

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
    if 'username' not in session:
        return redirect(url_for('login'))

    data = request.get_json()
    project_name = data.get('project_name')

    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute("SELECT * FROM projects WHERE المشروع LIKE ?", ('%' + project_name + '%',))
    reports = c.fetchall()
    conn.close()

    return jsonify(reports)

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/service-worker.js')
def sw():
    return send_from_directory('static', 'service-worker.js')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
