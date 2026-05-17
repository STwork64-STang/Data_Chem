import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="ระบบจัดการข้อมูลสารเคมี", layout="wide")

st.title("🧪 ระบบบันทึกและจัดการข้อมูลสารเคมี")
st.write("กรอกข้อมูลสารเคมีด้านล่าง และสามารถทำการ Export เป็นไฟล์ Excel ได้ทันที")

# 1. สร้างระบบเก็บข้อมูลจำลอง (Session State) เพื่อไม่ให้ข้อมูลหายเมื่อกดปุ่ม
if "chemical_data" not in st.session_state:
    # สร้างข้อมูลเริ่มต้นตัวอย่าง
    st.session_state.chemical_data = pd.DataFrame([
        {"ชื่อสารเคมี": "Ethanol", "สูตรเคมี": "C2H5OH", "ปริมาณ (L)": 10.0, "ห้องเก็บ": "A1"},
        {"ชื่อสารเคมี": "Acetone", "สูตรเคมี": "CH3COCH3", "ปริมาณ (L)": 5.5, "ห้องเก็บ": "B2"}
    ])

# 2. ฟอร์มสำหรับกรอกข้อมูลเพิ่ม
st.subheader("📝 เพิ่มข้อมูลสารเคมีใหม่")
with st.form("chem_form", clear_on_submit=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        name = st.text_input("ชื่อสารเคมี")
    with col2:
        formula = st.text_input("สูตรเคมี")
    with col3:
        amount = st.number_input("ปริมาณ (L)", min_value=0.0, step=0.1)
    with col4:
        room = st.text_input("ห้องที่จัดเก็บ")
        
    submit_button = st.form_submit_button(label="บันทึกข้อมูล")

# เมื่อกดบันทึก นำข้อมูลไปต่อท้าย Dataframe หลัก
if submit_button:
    if name and formula:  # ตรวจสอบเบื้องต้นว่ากรอกชื่อและสูตรหรือยัง
        new_row = {"ชื่อสารเคมี": name, "สูตรเคมี": formula, "ปริมาณ (L)": amount, "ห้องเก็บ": room}
        st.session_state.chemical_data = pd.concat([st.session_state.chemical_data, pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"บันทึกข้อมูล {name} เรียบร้อยแล้ว!")
    else:
        st.error("กรุณากรอกชื่อสารเคมีและสูตรเคมีให้ครบถ้วน")

---

# 3. แสดงตารางข้อมูลปัจจุบัน
st.subheader("📊 รายการสารเคมีในระบบ")
st.dataframe(st.session_state.chemical_data, use_container_width=True)

---

# 4. ฟังก์ชันสำหรับการ Export เป็น Excel
def to_excel(df):
    output = io.BytesIO()
    # ใช้ ExcelWriter ร่วมกับ openpyxl
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Chemical_Inventory')
    processed_data = output.getvalue()
    return processed_data

# แปลงข้อมูลในตารางเป็น Excel Binary
excel_data = to_excel(st.session_state.chemical_data)

# 5. ปุ่มสำหรับ Download Excel
st.download_button(
    label="📥 Export เป็นไฟล์ Excel (.xlsx)",
    data=excel_data,
    file_name='chemical_inventory.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)
