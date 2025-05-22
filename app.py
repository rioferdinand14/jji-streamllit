import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model dan label encoder
model, label_encoders = joblib.load('model.pkl')

st.title("🎓 Prediksi Risiko Dropout Mahasiswa")
st.write("Masukkan data di bawah ini untuk memprediksi risiko dropout.")

# Input user
admission_grade = st.slider("Admission Grade", 0.0, 200.0, 140.0)
age = st.number_input("Age at Enrollment", 15, 100, 19)
curr_1st = st.slider("1st Semester Grade", 0.0, 200.0, 12.0)
curr_2nd = st.slider("2nd Semester Grade", 0.0, 200.0, 12.0)
prev_qual = st.slider("Previous Qualification Grade", 0.0, 200.0, 130.0)

debtor = st.selectbox("Debtor (1 = Yes, 0 = No)", [0, 1])
tuition_paid = st.selectbox("Tuition Fees Up to Date (1 = Yes, 0 = No)", [0, 1])
scholarship = st.selectbox("Scholarship Holder (1 = Yes, 0 = No)", [0, 1])
# Jika Daytime_evening_attendance sudah numeric (0/1)
attendance = st.selectbox("Daytime/Evening Attendance (1 = evening, 0 = daytime)", [0, 1])
gender = st.selectbox("Gender (1 = Female, 0 = Male)", [0, 1])
displaced = st.selectbox("Displaced (1 = Yes, 0 = No)", [0, 1])
special_needs = st.selectbox("Educational Special Needs (1 = Yes, 0 = No)", [0, 1])

selected_features = [
    'Admission_grade',
    'Age_at_enrollment',
    'Curricular_units_1st_sem_grade',
    'Curricular_units_2nd_sem_grade',
    'Previous_qualification_grade',
    'Debtor',
    'Tuition_fees_up_to_date',
    'Scholarship_holder',
    'Daytime_evening_attendance',
    'Gender',
    'Displaced',
    'Educational_special_needs'
]

def preprocess_input():
    df_input = pd.DataFrame([{
        'Admission_grade': admission_grade,
        'Age_at_enrollment': age,
        'Curricular_units_1st_sem_grade': curr_1st,
        'Curricular_units_2nd_sem_grade': curr_2nd,
        'Previous_qualification_grade': prev_qual,
        'Debtor': debtor,
        'Tuition_fees_up_to_date': tuition_paid,
        'Scholarship_holder': scholarship,
        'Daytime_evening_attendance': attendance,  # sudah angka
        'Gender': gender,                           # masih string
        'Displaced': displaced,
        'Educational_special_needs': special_needs
    }], columns=selected_features)

    for col, le in label_encoders.items():
        val = df_input.loc[0, col]
        try:
            df_input[col] = le.transform([val])
        except Exception as e:
            st.error(f"Nilai '{val}' tidak dikenali untuk kolom {col}: {e}")
            return None

    return df_input.values


if st.button("🔍 Prediksi Dropout"):
    X_new = preprocess_input()
    if X_new is not None:
        proba = model.predict_proba(X_new)[0]
        pred = model.predict(X_new)[0]

        st.subheader("📢 Hasil Prediksi:")
        st.write(f"**Status Prediksi:** `{pred}`")
        p_drop = proba[1] * 100  # Karena label 1 adalah Dropout
        st.write(f"**Probabilitas Dropout:** `{p_drop:.2f}%`")

        if pred == 1:
            st.warning("⚠️ Mahasiswa ini berisiko tinggi untuk dropout.")
        else:
            st.success("✅ Mahasiswa diprediksi akan tetap aktif.")
