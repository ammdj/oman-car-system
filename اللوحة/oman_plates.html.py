import streamlit as st
import json
import os

# إعدادات الصفحة لتناسب الهاتف الذكي
st.set_page_config(page_title="نظام المركبات العماني", page_icon="🇴🇲", layout="centered")

# تعديل المسار ليعمل بشكل دائم وصحيح على السيرفر السحابي
DB_FILE = "/tmp/oman_secure_db.json"
OMAN_LETTERS = ["أ", "ب", "ج", "د", "ر", "س", "ش", "ص", "ط", "ظ", "ع", "غ", "ف", "ق", "ك", "ل", "م", "ن", "هـ", "و", "ي"]

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# عنوان التطبيق علوياً
st.markdown("<h2 style='text-align: center; color: #00FF00;'>[ نظام تسجيل المركبات العماني ]</h2>", unsafe_allow_html=True)

# شريط للتنقل بين التسجيل والبحث متوافق مع شاشات الهاتف
page = st.radio("اختر العملية:", ["تسجيل مركبة جديدة", "البحث والمطابقة الميدانية"], horizontal=True)

db = load_db()

if page == "تسجيل مركبة جديدة":
    st.write("---")
    name = st.text_input("أدخل اسم القريب:")
    mode = st.radio("نوع اللوحة:", ["لوحة برمز واحد", "لوحة برمزين"], horizontal=True)
    
    st.write("شكل اللوحة التقريبي:")
    
    col_num, col_c1, col_c2 = st.columns([2, 1, 1])
    with col_num:
        number = st.text_input("رقم اللوحة:", max_chars=5, key="reg_num")
    with col_c1:
        c1 = st.selectbox("الرمز الأول:", OMAN_LETTERS, key="reg_c1")
    with col_c2:
        if mode == "لوحة برمزين":
            c2 = st.selectbox("الرمز الثاني:", OMAN_LETTERS, key="reg_c2")
        else:
            c2 = ""

    if st.button("💾 تسجيل المركبة", use_container_width=True):
        if not name.strip():
            st.error("⚠️ الرجاء إدخال اسم القريب أولاً!")
        elif not number.isdigit() or not (1 <= len(number) <= 5):
            st.error("⚠️ خطأ: اللوحة العمانية تتكون من 1 إلى 5 أرقام فقط!")
        else:
            final_symbol = c1 if mode == "لوحة برمز واحد" else f"{c1} {c2}"
            plate_id = f"{number.strip()}-{final_symbol}"
            
            db[plate_id] = name.strip()
            save_db(db)
            st.success(f"✔️ تم حفظ اللوحة ({plate_id}) بنجاح تحت اسم: {name}")

elif page == "البحث والمطابقة الميدانية":
    st.write("---")
    st.write("أدخل بيانات اللوحة المرصودة للبحث عنها:")
    
    search_mode = st.radio("نوع اللوحة المرصودة:", ["لوحة برمز واحد", "لوحة برمزين"], horizontal=True, key="search_mode")
    
    col_snum, col_sc1, col_sc2 = st.columns([2, 1, 1])
    with col_snum:
        s_number = st.text_input("رقم اللوحة:", max_chars=5, key="search_num")
    with col_sc1:
        s_c1 = st.selectbox("الرمز الأول:", OMAN_LETTERS, key="search_c1")
    with col_sc2:
        if search_mode == "لوحة برمزين":
            s_c2 = st.selectbox("الرمز الثاني:", OMAN_LETTERS, key="search_c2")
        else:
            s_c2 = ""
            
    if st.button("🔍 بدء المطابقة الرادارية", use_container_width=True):
        if not s_number.isdigit():
            st.error("⚠️ يرجى إدخال رقم لوحة صحيح")
        else:
            final_search_symbol = s_c1 if search_mode == "لوحة برمز واحد" else f"{s_c1} {s_c2}"
            target_plate = f"{s_number.strip()}-{final_search_symbol}"
            
            if target_plate in db:
                st.markdown(f"<div style='background-color: #005500; padding: 15px; border-radius: 5px; text-align: center;'>🎯 تم العثور على تطابق!<br><b>المركبة تعود لقريبك: {db[target_plate]}</b></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='background-color: #550000; padding: 15px; border-radius: 5px; text-align: center;'>❌ لم يتم العثور على أي تطابق في قاعدة البيانات المحلية.</div>", unsafe_allow_html=True)
