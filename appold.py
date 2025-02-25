{% extends "layout.html" %}

{% block content %}
<h2 class="text-center my-4">إضافة مشروع جديد</h2>
<div class="container">
    <form action="/add_project" method="POST" class="row g-3">
        <div class="col-md-6">
            <label class="form-label">التسلسل:</label>
            <input type="number" name="التسلسل" class="form-control" required>
        </div>
        <div class="col-md-6">
            <label class="form-label">المحافظة:</label>
            <input type="text" name="المحافظة" class="form-control" required>
        </div>
        <div class="col-md-6">
            <label class="form-label">المشروع:</label>
            <input type="text" name="المشروع" class="form-control" required>
        </div>
        <div class="col-md-6">
            <label class="form-label">مدرج في وزارة التخطيط:</label>
            <select name="مدرج_في_وزارة_التخطيط" class="form-select" required>
                <option value="مدرج">مدرج</option>
                <option value="قيد الإدراج">قيد الإدراج</option>
            </select>
        </div>
        <div class="col-md-6">
            <label class="form-label">مؤشر لدى وزارة المالية:</label>
            <select name="مؤشر_لدى_وزارة_المالية" class="form-select" required>
                <option value="مؤشر">مؤشر</option>
                <option value="غير مؤشر">غير مؤشر</option>
            </select>
        </div>
        <div class="col-md-6">
            <label class="form-label">الكلفة الكلية (دينار):</label>
            <input type="number" name="الكلفة_الكلية" class="form-control" required>
        </div>
        <div class="col-md-6">
            <label class="form-label">الاستثناء من أساليب التعاقد:</label>
            <select name="الاستثناء_من_أساليب_التعاقد" class="form-select" required>
                <option value="دعوة">دعوة</option>
                <option value="إعلان">إعلان</option>
            </select>
        </div>
        <div class="col-md-6">
            <label class="form-label">استثناء (تصميم وتنفيذ / جداول كميات):</label>
            <select name="استثناء" class="form-select" required>
                <option value="تصميم وتنفيذ">تصميم وتنفيذ</option>
                <option value="جداول كميات">جداول كميات</option>
            </select>
        </div>
        <div class="col-md-6">
            <label class="form-label">الإعلان:</label>
            <input type="date" name="الإعلان" class="form-control" required>
        </div>
        <div class="col-md-6">
            <div class="form-check">
                <input class="form-check-input" type="checkbox" name="دراسة_سيرة_ذاتية" value="صح">
                <label class="form-check-label">دراسة سيرة ذاتية</label>
            </div>
        </div>
        <div class="col-md-6">
            <div class="form-check">
                <input class="form-check-input" type="checkbox" name="الدعوات" value="صح">
                <label class="form-check-label">الدعوات</label>
            </div>
        </div>
        <div class="col-md-6">
            <div class="form-check">
                <input class="form-check-input" type="checkbox" name="الوثيقة_القياسية" value="صح">
                <label class="form-check-label">الوثيقة القياسية</label>
            </div>
        </div>
        <div class="col-md-6">
            <div class="form-check">
                <input class="form-check-input" type="checkbox" name="التخويل" value="صح">
                <label class="form-check-label">التخويل</label>
            </div>
        </div>
        <div class="col-md-6">
            <label class="form-label">تاريخ غلق الدعوات:</label>
            <input type="date" name="تاريخ_غلق_الدعوات" class="form-control" required>
        </div>
        <div class="col-md-6">
            <div class="form-check">
                <input class="form-check-input" type="checkbox" name="لجان_الفتح" value="صح">
                <label class="form-check-label">لجان الفتح</label>
            </div>
        </div>
        <div class="col-md-6">
            <label class="form-label">لجنة تحليل:</label>
            <input type="text" name="لجنة_تحليل" class="form-control" required>
        </div>
        <div class="col-md-6">
            <label class="form-label">قرار لجنة التحليل إلى دائرة العقود:</label>
            <input type="date" name="قرار_لجنة_التحليل" class="form-control" required>
        </div>
        <div class="col-md-6">
            <label class="form-label">لجنة المراجعة والمصادقة:</label>
            <input type="text" name="لجنة_المراجعة_والمصادقة" class="form-control" required>
        </div>
        <div class="col-md-6">
            <label class="form-label">الإحالة:</label>
            <input type="text" name="الإحالة" class="form-control" required>
        </div>
        <div class="col-md-6">
            <label class="form-label">مسودة العقد:</label>
            <input type="text" name="مسودة_العقد" class="form-control" required>
        </div>
        <div class="col-md-6">
            <label class="form-label">توقيع العقد:</label>
            <input type="date" name="توقيع_العقد" class="form-control" required>
        </div>
        <div class="col-md-12">
            <label class="form-label">ملاحظات:</label>
            <textarea name="ملاحظات" class="form-control" rows="3"></textarea>
        </div>
        <div class="col-12 text-center">
            <button type="submit" class="btn btn-primary">إضافة المشروع</button>
        </div>
    </form>
</div>
{% endblock %}
