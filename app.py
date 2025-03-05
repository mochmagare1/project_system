from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret123'  # مفتاح الجلسة لتأمين الكوكيز
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('يرجى إدخال اسم مستخدم وكلمة مرور.', 'danger')
            return redirect(url_for('register'))

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

# الصفحة الرئيسية
@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        flash('يجب تسجيل الدخول أولاً!', 'warning')
        return redirect(url_for('login'))

    return render_template('home.html')
# البحث عن مشروع معين
@app.route('/search_project', methods=['POST'])
def search_project():
    if 'username' not in session:
        return jsonify([])

    try:
        data = request.get_json()
        project_name = data.get('project_name', '').strip()

        conn = sqlite3.connect('projects.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM projects WHERE المشروع LIKE ?", ('%' + project_name + '%',))
        project = c.fetchone()
        conn.close()

        return jsonify(dict(project)) if project else jsonify([])
    except Exception as e:
        flash(f'حدث خطأ أثناء البحث: {str(e)}', 'danger')
        return jsonify([])
@app.route ( '/add_project', methods = ['GET', 'POST'] )
def add_project() :
    if 'username' not in session :
        flash ( 'يجب تسجيل الدخول أولاً!', 'warning' )
        return redirect ( url_for ( 'login' ) )

    if request.method == 'POST' :
        try :
            البيانات = {
                'التسلسل' : request.form.get ( 'التسلسل', '' ).strip ( ),
                'المحافظة' : request.form.get ( 'المحافظة', '' ).strip ( ),
                'المشروع' : request.form.get ( 'المشروع', '' ).strip ( ),
                'مدرج_في_وزارة_التخطيط' : request.form.get ( 'مدرج_في_وزارة_التخطيط', '' ).strip ( ),
                'مؤشر_لدى_وزارة_المالية' : request.form.get ( 'مؤشر_لدى_وزارة_المالية', '' ).strip ( ),
                'الكلفة_الكلية' : request.form.get ( 'الكلفة_الكلية', '' ).strip ( ),
                'الاستثناء_من_أساليب_التعاقد' : request.form.get ( 'الاستثناء_من_أساليب_التعاقد', '' ).strip ( ),
                'استثناء' : request.form.get ( 'استثناء', '' ).strip ( ),
                'الإعلان' : request.form.get ( 'الإعلان', '' ).strip ( ),
                'تاريخ_غلق_الدعوات' : request.form.get ( 'تاريخ_غلق_الدعوات', '' ).strip ( ),
                'لجنة_تحليل' : request.form.get ( 'لجنة_تحليل', '' ).strip ( ),
                'قرار_لجنة_التحليل_الى_دائرة_العقود' : request.form.get ( 'قرار_لجنة_التحليل_الى_دائرة_العقود',
                                                                          '' ).strip ( ),
                'لجنة_المراجعة_والمصادقة' : request.form.get ( 'لجنة_المراجعة_والمصادقة', '' ).strip ( ),
                'الإحالة' : request.form.get ( 'الإحالة', '' ).strip ( ),
                'مسودة_العقد' : request.form.get ( 'مسودة_العقد', '' ).strip ( ),
                'توقيع_العقد' : request.form.get ( 'توقيع_العقد', '' ).strip ( ),
                'ملاحظات' : request.form.get ( 'ملاحظات', '' ).strip ( ),
                'دراسة_سيرة_ذاتية' : 'صح' if request.form.get ( 'دراسة_سيرة_ذاتية' ) else '',
                'الدعوات' : 'صح' if request.form.get ( 'الدعوات' ) else '',
                'الوثيقة_القياسية' : 'صح' if request.form.get ( 'الوثيقة_القياسية' ) else '',
                'التخويل' : 'صح' if request.form.get ( 'التخويل' ) else '',
                'لجان_الفتح' : 'صح' if request.form.get ( 'لجان_الفتح' ) else ''
            }

            conn = sqlite3.connect ( 'projects.db' )
            c = conn.cursor ( )
            c.execute ( '''INSERT INTO projects (
                            التسلسل, المحافظة, المشروع, مدرج_في_وزارة_التخطيط, مؤشر_لدى_وزارة_المالية, 
                            الكلفة_الكلية, الاستثناء_من_أساليب_التعاقد, استثناء, الإعلان, 
                            تاريخ_غلق_الدعوات, لجنة_تحليل, قرار_لجنة_التحليل_الى_دائرة_العقود, 
                            لجنة_المراجعة_والمصادقة, الإحالة, مسودة_العقد, توقيع_العقد, ملاحظات, 
                            دراسة_سيرة_ذاتية, الدعوات, الوثيقة_القياسية, التخويل, لجان_الفتح
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        tuple ( البيانات.values ( ) ) )

            conn.commit ( )
            conn.close ( )

            flash ( 'تمت إضافة المشروع بنجاح!', 'success' )
            return redirect ( url_for ( 'add_project' ) )

        except Exception as e :
            flash ( f'حدث خطأ أثناء إضافة المشروع: {str ( e )}', 'danger' )

    return render_template ( 'add_project.html' )
@app.route('/edit_project', methods=['GET'])
def edit_project():
    if 'username' not in session:
        flash('يجب تسجيل الدخول أولاً!', 'warning')
        return redirect(url_for('login'))

    conn = sqlite3.connect('projects.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM projects")
    projects = [dict(row) for row in c.fetchall()]
    conn.close()

    return render_template('edit_project.html', projects=projects)

@app.route('/update_project', methods=['POST'])
def update_project():
    if 'username' not in session:
        flash('يجب تسجيل الدخول أولاً!', 'warning')
        return redirect(url_for('login'))

    project_name = request.form.get('المشروع', '').strip()
    if not project_name:
        flash('يجب تحديد المشروع لتعديله!', 'danger')
        return redirect(url_for('edit_project'))

    try:
        البيانات = {
            'التسلسل': request.form.get('التسلسل', ''),
            'المحافظة': request.form.get('المحافظة', ''),
            'مدرج_في_وزارة_التخطيط': request.form.get('مدرج_في_وزارة_التخطيط', ''),
            'مؤشر_لدى_وزارة_المالية': request.form.get('مؤشر_لدى_وزارة_المالية', ''),
            'الكلفة_الكلية': request.form.get('الكلفة_الكلية', ''),
            'الإعلان': request.form.get('الإعلان', ''),
            'تاريخ_غلق_الدعوات': request.form.get('تاريخ_غلق_الدعوات', ''),
            'لجنة_تحليل': request.form.get('لجنة_تحليل', ''),
            'قرار_لجنة_التحليل_الى_دائرة_العقود': request.form.get('قرار_لجنة_التحليل_الى_دائرة_العقود', ''),
            'لجنة_المراجعة_والمصادقة': request.form.get('لجنة_المراجعة_والمصادقة', ''),
            'الإحالة': request.form.get('الإحالة', ''),
            'مسودة_العقد': request.form.get('مسودة_العقد', ''),
            'توقيع_العقد': request.form.get('توقيع_العقد', ''),
            'ملاحظات': request.form.get('ملاحظات', ''),
            'دراسة_سيرة_ذاتية': 'صح' if request.form.get('دراسة_سيرة_ذاتية') else '',
            'الدعوات': 'صح' if request.form.get('الدعوات') else '',
            'الوثيقة_القياسية': 'صح' if request.form.get('الوثيقة_القياسية') else '',
            'التخويل': 'صح' if request.form.get('التخويل') else '',
            'لجان_الفتح': 'صح' if request.form.get('لجان_الفتح') else ''
        }

        conn = sqlite3.connect('projects.db')
        c = conn.cursor()
        c.execute('''
            UPDATE projects SET التسلسل=?, المحافظة=?, مدرج_في_وزارة_التخطيط=?, 
                             مؤشر_لدى_وزارة_المالية=?, الكلفة_الكلية=?, الإعلان=?, 
                             تاريخ_غلق_الدعوات=?, لجنة_تحليل=?, 
                             قرار_لجنة_التحليل_الى_دائرة_العقود=?, لجنة_المراجعة_والمصادقة=?, 
                             الإحالة=?, مسودة_العقد=?, توقيع_العقد=?, ملاحظات=?, 
                             دراسة_سيرة_ذاتية=?, الدعوات=?, الوثيقة_القياسية=?, 
                             التخويل=?, لجان_الفتح=? 
            WHERE المشروع=?''',
            (*بيانات.values(), project_name))

        conn.commit()
        conn.close()

        flash(f'تم تعديل بيانات المشروع "{project_name}" بنجاح!', 'success')
    except Exception as e:
        flash(f'حدث خطأ أثناء التعديل: {str(e)}', 'danger')

    return redirect(url_for('edit_project'))

@app.route('/search_reports', methods=['POST'])
def search_reports():
    if 'username' not in session:
        return jsonify([])

    try:
        data = request.get_json()
        project_name = data.get('project_name', '').replace('_', ' ').strip()

        conn = sqlite3.connect('projects.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM projects WHERE المشروع LIKE ?", ('%' + project_name + '%',))
        reports = [dict(row) for row in c.fetchall()]
        conn.close()

        return jsonify(reports)
    except Exception as e:
        return jsonify([])

@app.route('/reports', methods=['GET'])
def reports():
    if 'username' not in session:
        flash('يجب تسجيل الدخول أولاً!', 'warning')
        return redirect(url_for('login'))

    try:
        conn = sqlite3.connect('projects.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM projects")
        reports = [dict(row) for row in c.fetchall()]
        conn.close()
    except Exception as e:
        flash(f'حدث خطأ أثناء جلب التقارير: {str(e)}', 'danger')
        reports = []

    return render_template('reports.html', reports=reports)
@app.route('/delete_project', methods=['GET', 'POST'])
def delete_project():
    if 'username' not in session:
        flash('يجب تسجيل الدخول أولاً!', 'warning')
        return redirect(url_for('login'))

    project = None

    if request.method == 'POST':
        project_name = request.form.get('project_name', '').strip()

        if 'search' in request.form:
            if project_name:
                conn = sqlite3.connect('projects.db')
                c = conn.cursor()
                c.execute("SELECT * FROM projects WHERE المشروع = ?", (project_name,))
                project = c.fetchone()
                conn.close()

                if not project:
                    flash(f'المشروع "{project_name}" غير موجود!', 'danger')
            else:
                flash('يرجى إدخال اسم المشروع!', 'danger')

        elif 'delete' in request.form:
            if project_name:
                conn = sqlite3.connect('projects.db')
                c = conn.cursor()
                c.execute("DELETE FROM projects WHERE المشروع = ?", (project_name,))
                conn.commit()
                conn.close()
                flash(f'تم حذف المشروع "{project_name}" بنجاح!', 'success')
                return redirect(url_for('delete_project'))
            else:
                flash('يرجى إدخال اسم المشروع!', 'danger')

    return render_template('delete_project.html', project=project)
# تشغيل التطبيق
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
