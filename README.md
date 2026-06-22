# 🍎 Apple Developer Academy - Online Test Simulator

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.20+-FF4B4B?style=for-the-badge&logo=streamlit)

Repositori ini berisi aplikasi simulasi tes online untuk persiapan seleksi **Apple Developer Academy**. Aplikasi ini dikembangkan menggunakan **Python** dan **Streamlit** dengan fitur pengacakan soal (randomization) dan sistem penilaian otomatis.

## 🚀 Fitur Utama
- **Bank Soal Dinamis**: Mengambil soal secara acak dari database `questions.py`.
- **Sesuai Kurikulum Academy**: Terdiri dari 4 section utama:
    - **Section 1: Logic** (25 Soal)
    - **Section 2: Programming - Swift Focus** (15 Soal)
    - **Section 3: OOP** (10 Soal)
    - **Section 4: Bonus (Design/UX)** (2 Soal)
- **Real-time Timer**: Simulasi durasi pengerjaan selama 45 menit.
- **Scoring System**: Nilai muncul otomatis setelah submit beserta pembahasan jawaban yang salah.
- **Session State Management**: Jawaban tidak hilang saat halaman di-refresh.

## 🛠️ Teknologi yang Digunakan
- **Python**: Bahasa pemrograman utama.
- **Streamlit**: Framework untuk antarmuka web (UI).
- **Random Module**: Untuk mengacak soal dari bank soal.

## 📦 Cara Instalasi & Menjalankan
1. **Clone Repositori ini:**
   ```bash
   git clone [https://github.com/RayanHakim/Latihan-Apple-Developer-Academy.git](https://github.com/RayanHakim/Latihan-Apple-Developer-Academy.git)
   cd Latihan-Apple-Developer-Academy
2. **Install Dependensi:**
   Install Dependensi:
Pastikan Anda sudah menginstal Python, kemudian jalankan:
pip install streamlit

3. **Jalankan Aplikasi:**
   streamlit run app.py

4. **Struktur Folder**
├── app.py           # Logika utama aplikasi, timer, dan UI Streamlit
├── questions.py     # Database/Bank soal dalam bentuk dictionary Python
└── README.md        # Dokumentasi proyek
