from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret123'  # مفتاح الجلسة لتأمين الكوكيز

# إنشاء قاعدة البيانات والجداول
def init_db():
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()

    # جدول المشاريع
    c.execute('''CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    التسلسل INTEGER,
                    المحافظة TEXT,
                    المشروع TEXT UNIQUE,
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

    # جدول المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')

    # إضافة مستخدم افتراضي إذا لم يكن موجودًا
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  ('admin', generate_password_hash('admin123')))

    conn.commit()
    conn.close()

# صفحة تسجيل الدخول
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

        if user and check_password_hash(user[2], password):
            session['username'] = username
            flash('تم تسجيل الدخول بنجاح!', 'success')
            return redirect(url_for('home'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة.', 'danger')

    return render_template('login.html')

# تسجيل الخروج
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('تم تسجيل الخروج.', 'info')
    return redirect(url_for('login'))

# تسجيل مستخدم جديد
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('projects.db')
        c = conn.cursor()

        try:
            hashed_password = generate_password_hash(password)
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            flash('تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('اسم المستخدم موجود بالفعل. اختر اسمًا آخر.', 'warning')
        finally:
            conn.close()

    return render_template('register.html')

# الصفحة الرئيسية
@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        flash('يجب تسجيل الدخول أولاً!', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'manage_projects' in request.form:
            return redirect(url_for('add_project'))
        elif 'delete_project' in request.form:
            return redirect(url_for('delete_project'))

    return render_template('home.html')

# إضافة مشروع جديد
@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        form_data = {
            'التسلسل': request.form.get('التسلسل', ''),
            'المحافظة': request.form.get('المحافظة', ''),
            'المشروع': request.form.get('المشروع', ''),
            'مدرج_في_وزارة_التخطيط': request.form.get('مدرج_في_وزارة_التخطيط', ''),
            'مؤشر_لدى_وزارة_المالية': request.form.get('مؤشر_لدى_وزارة_المالية', ''),
            'الكلفة_الكلية': request.form.get('الكلفة_الكلية', '0'),
        }

        conn = sqlite3.connect('projects.db')
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO projects (التسلسل, المحافظة, المشروع, مدرج_في_وزارة_التخطيط, مؤشر_لدى_وزارة_المالية,
                         الكلفة_الكلية) VALUES (?, ?, ?, ?, ?, ?)''',
                      (form_data['التسلسل'], form_data['المحافظة'], form_data['المشروع'],
                       form_data['مدرج_في_وزارة_التخطيط'], form_data['مؤشر_لدى_وزارة_المالية'], form_data['الكلفة_الكلية']))
            conn.commit()
            flash('تمت إضافة المشروع بنجاح!', 'success')
        except Exception as e:
            flash(f'خطأ أثناء الحفظ: {str(e)}', 'danger')
        finally:
            conn.close()

        return redirect(url_for('home'))

    return render_template('add_project.html')

# حذف مشروع معين بعد عرض التفاصيل
@app.route('/delete_project', methods=['GET', 'POST'])
def delete_project():
    if 'username' not in session:
        flash('يجب تسجيل الدخول أولاً!', 'warning')
        return redirect(url_for('login'))

    project = None

    if request.method == 'POST':
        project_name = request.form.get('project_name', '').strip()

        if 'search' in request.form:
            conn = sqlite3.connect('projects.db')
            c = conn.cursor()
            c.execute("SELECT * FROM projects WHERE المشروع = ?", (project_name,))
            project = c.fetchone()
            conn.close()

            if not project:
                flash(f'المشروع "{project_name}" غير موجود!', 'danger')

        elif 'delete' in request.form:
            conn = sqlite3.connect('projects.db')
            c = conn.cursor()
            c.execute("DELETE FROM projects WHERE المشروع = ?", (project_name,))
            conn.commit()
            conn.close()
            flash(f'تم حذف المشروع "{project_name}" بنجاح!', 'success')
            return redirect(url_for('delete_project'))

    return render_template('delete_project.html', project=project)
@app.route('/edit_project', methods=['GET'])
def edit_project():
    if 'username' not in session:
        flash('يجب تسجيل الدخول أولاً!', 'warning')
        return redirect(url_for('login'))

    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute('SELECT * FROM projects')
    projects = c.fetchall()
    conn.close()

    return render_template('edit_project.html', projects=projects)
@app.route('/update_project/<project_name>', methods=['GET', 'POST'])
def update_project(project_name):
    if 'username' not in session:
        flash('يجب تسجيل الدخول أولاً!', 'warning')
        return redirect(url_for('login'))

    conn = sqlite3.connect('projects.db')
    c = conn.cursor()

    if request.method == 'POST':
        التسلسل = request.form.get('التسلسل', '')
        المحافظة = request.form.get('المحافظة', '')
        المشروع = request.form.get('المشروع', '')
        الكلفة_الكلية = request.form.get('الكلفة_الكلية', '')

        c.execute('''UPDATE projects SET التسلسل=?, المحافظة=?, المشروع=?, الكلفة_الكلية=? WHERE المشروع=?''',
                  (التسلسل, المحافظة, المشروع, الكلفة_الكلية, project_name))
        conn.commit()
        conn.close()

        flash('تم تعديل بيانات المشروع بنجاح!', 'success')
        return redirect(url_for('edit_project'))

    c.execute("SELECT * FROM projects WHERE المشروع = ?", (project_name,))
    project = c.fetchone()
    conn.close()

    if not project:
        flash('المشروع غير موجود!', 'danger')
        return redirect(url_for('edit_project'))

    return render_template('update_project.html', project=project)
@app.route('/reports', methods=['GET'])
def reports():
    if 'username' not in session:
        flash('يجب تسجيل الدخول أولاً!', 'warning')
        return redirect(url_for('login'))

    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute("SELECT * FROM projects")
    reports = c.fetchall()
    conn.close()

    return render_template('reports.html', reports=reports)

# تشغيل التطبيق
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
