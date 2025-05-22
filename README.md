# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding
Jaya Jaya Institut (berdiri 2000) menghadapi tingkat dropout yang tinggi yang sangat memengaruhi reputasi dan efisiensi biaya. Proyek ini bertujuan untuk mendeteksi dini siswa berisiko agar tim akademik dapat melakukan intervensi tepat waktu (bimbingan akademik, dukungan finansial, dsb.).

### Permasalahan Bisnis
1. Bagaimana mengidentifikasi siswa berisiko dropout sejak awal?
2. Faktor akademik, demografis, finansial apa saja yang memengaruhi keputusan dropout?
3. Bagaimana memonitor metrik kunci (dropout rate, admission grade) secara real time?

### Cakupan Proyek
1. Melakukan analisis data untuk menemukan faktor-faktor utama penyebab dropout.
2. Membangun dashboard interaktif menggunakan Metabase untuk monitoring performa mahasiswa.
3. Membuat prototype sistem machine learning untuk memprediksi kemungkinan dropout mahasiswa.

### Persiapan

Sumber data: **Predict Students' Dropout and Academic Success** (https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success)

Setup environment:
```bash
# Instalasi dependencies
pip install pipenv
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Business Dashboard
Dashboard dibuat menggunakan Metabase dan berisi beberapa visualisasi utama:
1. perbandingan jumlah status siswa
2. rata-rata nilai tes masuk per status
3. jumlah siswa debtor per status
4. rata-rata nilai semester 1 dan semester 2 per status
5. jumlah siswa pemegang beasiswa per status
6. rata-rata usia masuk siswa per status

```bash

docker run -d ^
  --name <nama_kontainer> ^
  -p 3000:3000 ^
  -v "<path_local_proyek>:/<direktori di kontainer>" ^
  -e "MB_DB_FILE=/<direktori di kontainer>/metabase.db" ^
  metabase/metabase

**Menambahkan Data Source SQLite**
** Setelah Metabase jalan: **
**1. Masuk ke Admin settings → Databases → Add database**
**2. Pilih SQLite**
**3. Masukkan Database file path:**
  /<direktori_di_kontainer>/data_mahasiswa.db
**4. Klik Save**

# Backup Dashboard Metabase
  docker cp metabase:/metabase.db ./metabase.db   
```

Akses Dashboard:
```bash

Email: datascience1@gmail.com
Password: 12345678@
URL: http://localhost:3000

```


## Menjalankan Sistem Machine Learning
Sistem machine learning dibangun menggunakan Random Forest Classifier dan telah di-deploy sebagai prototype menggunakan Streamlit.

Untuk mengakses prototype streamlit:

```
https://proyek-akhir-data-science.streamlit.app/
```
File model telah disimpan sebagai model.pkl.


## Conclusion
Proyek ini menunjukkan bahwa Admission_grade dan faktor finansial (Debtor, Tuition_fees_up_to_date) adalah prediktor paling kuat untuk risiko dropout. Model Random Forest yang dibangun mencapai recall 0.82 pada test set, memastikan sebagian besar calon dropout dapat terdeteksi. Dengan dashboard Metabase untuk monitoring real time dan aplikasi Streamlit untuk prediksi individual, Jaya Jaya Institut kini memiliki alat end-to-end untuk mendeteksi dini dan mengintervensi siswa berisiko—sebuah langkah strategis untuk menurunkan angka dropout dan meningkatkan keberhasilan akademik.

### Rekomendasi Action Items
1. Peringatan Otomatis
Kirim notifikasi (email/SMS) ke siswa dengan Admission_grade < 130 atau Debtor = 1.
2. Program Remedial & Mentoring
Terapkan kelas tambahan untuk siswa berisiko tinggi.
3. Skema Dukungan Finansial
Tawarkan beasiswa atau cicilan khusus bagi siswa bermasalah pembayaran.
4. Evaluasi Berkala
Rapat bulanan dengan tim akademik menggunakan dashboard Metabase untuk menyesuaikan strategi intervensi.
