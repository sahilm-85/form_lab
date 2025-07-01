import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import openpyxl
from openpyxl import Workbook

# === File Paths ===
OUTPUT_FOLDER = "Downloads/mpragati/filled_forms"
EXCEL_FILE = "Downloads/mpragati/form_data.xlsx"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# === Function to Create a PDF ===
def create_filled_pdf(data):
    safe_name = "".join(c for c in data['Name'] if c.isalnum() or c in (' ', '_')).strip().replace(" ", "_")
    output_path = os.path.join(OUTPUT_FOLDER, f"{safe_name}.pdf")

    c = canvas.Canvas(output_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "User Information Form")

    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"Name: {data['Name']}")
    c.drawString(100, 670, f"Age: {data['Age']}")
    c.drawString(100, 640, f"Gender: {data['Gender']}")
    c.drawString(100, 610, f"Phone Number: +91 {data['Phone Number']}")
    c.save()
    return output_path

# === Function to Save Data into Excel ===
def save_to_excel(data):
    if not os.path.exists(EXCEL_FILE):
        wb = Workbook()
        ws = wb.active
        ws.title = "User Data"
        ws.append(["Name", "Age", "Gender", "Phone Number"])
    else:
        wb = openpyxl.load_workbook(EXCEL_FILE)
        ws = wb.active

    ws.append([data['Name'], data['Age'], data['Gender'], f"+91 {data['Phone Number']}"])
    wb.save(EXCEL_FILE)

# === Streamlit UI ===
st.set_page_config(page_title="User Form PDF Generator", layout="centered")

st.title("📝 User Information Form")

with st.form("user_form"):
    name = st.text_input("Name")
    age = st.text_input("Age")
    gender = st.selectbox("Gender", ["", "Male", "Female", "Other"])
    phone = st.text_input("Phone Number (without +91)")

    submitted = st.form_submit_button("Submit")

if submitted:
    if not name or not age or not gender or not phone:
        st.warning("⚠️ Please fill in all fields.")
    elif not phone.isdigit():
        st.warning("📵 Phone number must contain only digits (without +91).")
    else:
        entry = {
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Phone Number": phone
        }

        create_filled_pdf(entry)
        save_to_excel(entry)

        # Temporary success message
        st.toast("✅ Entry saved successfully!", icon="✅")
