import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load scaler, daftar kolom kategorikal, dan model
# (Pastikan di rf_dropout.pkl sudah berisi: scaler, cat_columns, model)
scaler, cat_columns, model = joblib.load('model.pkl')

st.title("🎓 Prediksi Risiko Dropout Mahasiswa")
st.write("Masukkan data di bawah ini untuk memprediksi risiko dropout.")

# 1) INPUT FORM

# Numeric inputs
admission_grade = st.slider(
    "Admission Grade", min_value=0.0, max_value=200.0, value=140.0
)
age = st.number_input(
    "Age at Enrollment", min_value=15, max_value=100, value=19
)
curr_1st = st.slider(
    "1st Semester Grade", min_value=0.0, max_value=200.0, value=12.0
)
curr_2nd = st.slider(
    "2nd Semester Grade", min_value=0.0, max_value=200.0, value=12.0
)
prev_qual = st.slider(
    "Previous Qualification Grade", min_value=0.0, max_value=200.0, value=130.0
)

# Categorical / binary inputs
debtor = st.selectbox("Debtor (1 = Yes, 0 = No)", [0, 1])
tuition_paid = st.selectbox("Tuition Fees Up to Date (1 = Yes, 0 = No)", [0, 1])
scholarship = st.selectbox("Scholarship Holder (1 = Yes, 0 = No)", [0, 1])
attendance = st.selectbox("Daytime/Evening Attendance", ["Daytime", "Evening"])
gender = st.selectbox("Gender", ["Male", "Female"])
displaced = st.selectbox("Displaced (1 = Yes, 0 = No)", [0, 1])
special_needs = st.selectbox(
    "Educational Special Needs (1 = Yes, 0 = No)", [0, 1]
)

# 2) PREPROCESSING FUNCTION

def preprocess_input():
    # a) Buat DataFrame input
    df_input = pd.DataFrame([{
        'Admission_grade': admission_grade,
        'Age_at_enrollment': age,
        'Curricular_units_1st_sem_grade': curr_1st,
        'Curricular_units_2nd_sem_grade': curr_2nd,
        'Previous_qualification_grade': prev_qual,
        'Debtor': debtor,
        'Tuition_fees_up_to_date': tuition_paid,
        'Scholarship_holder': scholarship,
        'Daytime_evening_attendance': attendance,
        'Gender': gender,
        'Displaced': displaced,
        'Educational_special_needs': special_needs
    }])
    
    # b) Scaling numerik
    num_feats = [
        'Admission_grade',
        'Age_at_enrollment',
        'Curricular_units_1st_sem_grade',
        'Curricular_units_2nd_sem_grade',
        'Previous_qualification_grade'
    ]
    num_scaled = scaler.transform(df_input[num_feats])
    
    # c) One-hot encode kategorikal/biner
    cat_input = df_input.drop(columns=num_feats)
    cat_dummies = pd.get_dummies(cat_input, drop_first=True)
    
    # d) Align dummy cols dengan training
    cat_aligned = cat_dummies.reindex(columns=cat_columns, fill_value=0)
    
    # e) Gabungkan kembali
    X_proc = np.hstack([num_scaled, cat_aligned.values])
    return X_proc

# 3) PREDIKSI
if st.button("🔍 Prediksi Dropout"):
    X_new = preprocess_input()
    proba = model.predict_proba(X_new)[0]
    pred = model.predict(X_new)[0]

    st.subheader("📢 Hasil Prediksi:")
    st.write(f"**Status Prediksi:** `{pred}`")
    # Ambil probabilitas kelas 'Dropout'
    p_drop = proba[model.classes_ == 'Dropout'][0] * 100
    st.write(f"**Probabilitas Dropout:** `{p_drop:.2f}%`")

    if pred == 'Dropout':
        st.warning("⚠️ Mahasiswa ini berisiko tinggi untuk dropout.")
    else:
        st.success("✅ Mahasiswa diprediksi akan tetap aktif.")
