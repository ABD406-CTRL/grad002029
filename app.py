from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__) # تصحيح بسيط لـ name

EXCEL_FILE = '2029دفعة.xlsx'

def get_student_data(query):
    try:
        # قراءة الملف
        df = pd.read_excel(EXCEL_FILE, header=None)
        
        # تحويل الاستعلام لنص عشان نقارنه بالأسماء
        query_str = str(query).strip()
        
        # هلق بنحدد الأعمدة اللي بدنا نبحث فيها:
        # العمود 0: الرقم الجامعي | العمود 3: الرقم الامتحاني | العمود 5: الاسم الكامل
        # بنستخدم .astype(str) عشان نضمن إن المقارنة نصية وما يضرب الكود
        mask = (df[0].astype(str) == query_str) | \
               (df[1].astype(str) == query_str) | \
               (df[5].astype(str) == query_str)  | \
                              (df[4].astype(str) == query_str)


        
        student_row = df[mask]
        
        if not student_row.empty:
            # تحويل السطر لقائمة (List)
            return student_row.iloc[0].tolist()
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sort', methods=['POST'])
def sort_students():
    try:
        # استلام رقم العمود من القائمة المنسدلة
        col_index = int(request.form.get('column_index'))
        df = pd.read_excel(EXCEL_FILE, header=None)
        
        # تحويل العمود لأرقام لضمان ترتيب (99 قبل 9)
        df[col_index] = pd.to_numeric(df[col_index], errors='coerce')
        
        # ترتيب تنازلي
        df_sorted = df.dropna(subset=[col_index]).sort_values(by=col_index, ascending=False)
        
        results = df_sorted.values.tolist()
        # نرسل رقم العمود المختار لكي نعرف أي درجة نعرض في الجدول
        return render_template('index.html', results=results, sorted_col=col_index)
    except Exception as e:
        return f"خطأ تقني: {e}"
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)