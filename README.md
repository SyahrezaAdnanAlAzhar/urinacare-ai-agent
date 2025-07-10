# UrinaCare - Agentic AI Service 🤖

Sebuah sistem backend Agentic AI yang dibangun dengan CrewAI dan FastAPI. Proyek ini berfungsi sebagai "otak" cerdas untuk aplikasi kesehatan UrinaCare, menggunakan tim agen AI khusus untuk mengotomatiskan alur kerja analisis gambar mikroskopis, pelaporan medis, dan penjadwalan janji temu.

## 📋 Daftar Isi
- [Gambaran Umum](#-gambaran-umum)
- [Arsitektur Sistem](#-arsitektur-sistem)
- [Instalasi](#-instalasi)
- [Mulai Cepat](#-mulai-cepat)
- [Kapabilitas Inti & Endpoint API](#-kapabilitas-inti--endpoint-api)
- [Contoh Respons API](#-contoh-respons-api)
- [Struktur File](#-struktur-file)
- [Catatan Penting](#-catatan-penting)
- [Untuk Penjurian Kompetisi](#-untuk-penjurian-kompetisi)

## 🔍 Gambaran Umum

Proyek ini mengimplementasikan sebuah layanan backend cerdas yang menggabungkan:
- **CrewAI** sebagai kerangka kerja untuk orkestrasi multi-agen.
- **Google Gemini 1.5 Pro** sebagai Large Language Model untuk penalaran.
- **FastAPI** untuk menyajikan fungsionalitas agen melalui REST API yang andal.
- **Arsitektur Berbasis Tool** di mana agen dapat memilih dan menggunakan fungsi spesifik untuk berinteraksi dengan layanan eksternal (misalnya, model CV atau API backend lain).

Tujuannya adalah untuk menyediakan analisis yang cepat, komprehensif, dan dapat ditindaklanjuti, yang ditenagai oleh kolaborasi antara agen-agen AI.

## 🏛️ Arsitektur Sistem

Sistem ini dirancang dengan pemisahan tugas yang jelas, di mana setiap agen memiliki peran, tujuan, dan perangkat (tools) yang spesifik. Mereka berkolaborasi dalam sebuah `Crew` untuk menyelesaikan `Task` yang kompleks dan dapat mengakses `Knowledge Base` untuk memperkaya konteks.

<p align="center">
  <!-- GANTI URL_TO_YOUR_DIAGRAM.png DENGAN LINK MENTAH KE GAMBAR DIAGRAM ANDA DI GITHUB/FIGMA -->
  <img src="URL_TO_YOUR_DIAGRAM.png" alt="Arsitektur Agen UrinaCare" width="800"/>
</p>

- **Agents**: Tim yang terdiri dari `Lab Analyst`, `Medical Advisor`, dan `Admin Assistant`.
- **Tasks**: Deskripsi pekerjaan yang didelegasikan ke agen (misal: analisis gambar, buat laporan).
- **Tools**: Kumpulan fungsi Python modular yang bisa dipanggil oleh agen.
- **Knowledge Base**: Sumber informasi eksternal (PDF, CSV) untuk memperdalam analisis agen.

## 🚀 Instalasi

### Persyaratan
```bash
python >= 3.10
```

### 1. Clone Repositori
```bash
git clone https://github.com/SyahrezaAdnanAlAzhar/urinacare-ai-agent.git
cd urina-care-agent
```

### 2. Setup Lingkungan Virtual
```bash
python -m venv venv
source venv/bin/activate  # Untuk macOS/Linux
# venv\Scripts\activate    # Untuk Windows
```

### 3. Install Dependensi
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment (Paling Penting)
Buat sebuah file bernama `.env` di direktori utama proyek dan isi dengan kredensial Anda. **JANGAN PERNAH** meng-commit file ini ke Git.
```env
# File: .env
GOOGLE_API_KEY="AIzaSy...your-google-api-key"
CV_MODEL_API_URL="https://your-cv-model.hf.space/analyze"
APPOINTMENT_BACKEND_API_URL="https://your-main-backend.com/api/v1/appointments"
```

## ⚡ Mulai Cepat

Setelah instalasi dan konfigurasi selesai, jalankan server API secara lokal:

```bash
uvicorn main_api:app --reload
```

Server akan berjalan dan API akan tersedia. Untuk menguji semua endpoint secara interaktif, buka browser Anda dan akses dokumentasi otomatisnya di:

**➡️ `http://127.0.0.1:8000/docs`**

## ✨ Kapabilitas Inti & Endpoint API

Layanan ini menyediakan beberapa endpoint untuk menangani seluruh alur kerja aplikasi:

- **`POST /analyze-sample`**: Endpoint utama. Menerima file gambar, menjalankan alur analisis lengkap (analisis gambar -> laporan terstruktur -> laporan naratif), dan mengembalikan kedua laporan tersebut.
- **`POST /overall-analysis`**: Menerima laporan terstruktur dan data kesehatan umum pasien (misal: berat badan, usia) untuk menghasilkan analisis komprehensif yang mengkorelasikan kedua data tersebut.
- **`POST /get-available-appointments`**: Menerima laporan terstruktur dan daftar lengkap jadwal dokter, lalu memfilter dan mengembalikan hanya slot yang tersedia jika konsultasi diperlukan.
- **`POST /book-appointment`**: Endpoint final. Menerima slot jadwal yang dipilih pengguna dan ID pasien untuk mengkonfirmasi janji temu dengan memanggil API backend lain.

## 📤 Contoh Respons API

Contoh output yang berhasil dari endpoint `/analyze-sample`:
```json
{
  "narrative_report": "Hasil analisis Anda menunjukkan adanya indikasi Hematuria karena jumlah sel darah merah yang terdeteksi cukup tinggi. Sangat disarankan untuk segera berkonsultasi dengan dokter untuk mendapatkan diagnosis yang lebih akurat dan penanganan lebih lanjut.",
  "structured_report": {
    "status": "Perlu Perhatian",
    "hematuria_finding": "Jumlah sel darah merah tinggi, mengindikasikan kemungkinan hematuria."
  }
}
```

## 📁 Struktur File

```
urinacare-ai-agent/
├── agents.py               # Definisi semua agen CrewAI
├── main_api.py             # Titik masuk aplikasi FastAPI dan definisi endpoint
├── tasks.py                # Definisi semua task yang akan dieksekusi agen
├── tools.py                # Implementasi semua tool yang bisa digunakan agen
├── .env.example            # Contoh file environment (tanpa nilai)
├── .gitignore
├── Dockerfile              # Konfigurasi untuk containerisasi aplikasi
└── requirements.txt        # Daftar dependensi Python
```

## 📝 Catatan Penting

- **Pengujian API**: Cara termudah untuk menguji fungsionalitas adalah melalui antarmuka Swagger UI di `/docs` saat server berjalan.
- **Keamanan**: Pastikan file `.env` sudah ada di dalam `.gitignore` dan tidak pernah ter-upload ke repositori publik. Gunakan *Secrets* saat melakukan deployment.
- **Deployment**: Proyek ini siap di-deploy menggunakan Docker. Untuk platform seperti Hugging Face Spaces, cukup upload semua file dan atur *Secrets* di menu *Settings*.

## 🏆 Untuk Penjurian Kompetisi

Untuk mereproduksi dan mengevaluasi proyek ini, panitia dapat mengikuti langkah-langkah berikut:

1.  **Ikuti Langkah Instalasi**: Clone repositori, buat lingkungan virtual, dan install dependensi dari `requirements.txt`.
2.  **Atur Kredensial**: Buat file `.env` dan isi `GOOGLE_API_KEY` dan URL API lainnya. Untuk deployment di HF Spaces, atur kredensial ini di bagian *Repository secrets*.
3.  **Jalankan Server**: Eksekusi perintah `uvicorn main_api:app --host 0.0.0.0 --port 8000`.
4.  **Verifikasi Endpoint**: Buka `http://<IP_SERVER>:8000/docs` dan uji setiap endpoint API secara berurutan, dimulai dari `/analyze-sample` untuk mendapatkan data yang bisa digunakan di endpoint lain.
