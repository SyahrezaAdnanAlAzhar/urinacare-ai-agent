from crewai import Task
from agents import lab_analyst_agent, medical_advisor_agent, admin_assistant_agent

lab_analysis_task = Task(
    description=(
        "Jalankan alur kerja analisis laboratorium lengkap. "
        "1. Ambil path gambar dari input: '{image_path}'. "
        "2. Gunakan 'Image Analysis Tool' untuk mendapatkan data deteksi mentah (JSON). "
        "3. Gunakan 'Medical Report Generation Tool' pada data mentah tersebut untuk membuat "
        "laporan medis terstruktur (JSON) yang mengkategorikan semua temuan."
    ),
    expected_output=(
        "Sebuah dictionary Python yang merupakan laporan medis terstruktur. "
        "Harus berisi kunci 'status' ('Normal' atau 'Perlu Perhatian') dan "
        "detail temuan lainnya. Contoh: "
        "{'status': 'Perlu Perhatian', 'hematuria_finding': 'Indikasi Hematuria...'}"
    ),
    agent=lab_analyst_agent,
)

narrative_reporting_task = Task(
    description=(
        "Ambil laporan medis terstruktur (JSON) dari hasil 'lab_analysis_task'. "
        "Gunakan 'Simple Narrative Generator Tool' untuk mengubah JSON tersebut menjadi "
        "sebuah narasi penjelasan yang ringkas dan mudah dipahami oleh pasien. "
        "Gunakan bahasa '{language}' sesuai permintaan."
    ),
    expected_output=(
        "Sebuah string teks tunggal yang berisi penjelasan naratif dari hasil lab. "
        "Contoh: 'Hasil analisis Anda menunjukkan adanya indikasi...' "
    ),
    agent=medical_advisor_agent,
    context=[lab_analysis_task]
)

overall_review_task = Task(
    description=(
        "Berikan analisis kesehatan overall. "
        "1. Ambil laporan medis terstruktur: '{categorized_report}'. "
        "2. Ambil data kesehatan umum pasien: '{patient_health_data}'. "
        "3. Gunakan 'Overall Health Analysis Tool' untuk menganalisis korelasi "
        "antara kedua data tersebut dan hasilkan wawasan yang komprehensif. "
        "4. Gunakan bahasa '{language}'."
    ),
    expected_output=(
        "Sebuah string teks tunggal berisi analisis overall yang menggabungkan "
        "hasil lab dengan data kesehatan umum pasien."
    ),
    agent=medical_advisor_agent
)

appointment_search_task = Task(
    description=(
        "Cari jadwal dokter yang tersedia. "
        "1. Ambil laporan medis terstruktur: '{categorized_report}'. "
        "2. Ambil DAFTAR LENGKAP jadwal semua dokter: '{all_doctor_schedules}'. "
        "3. Gunakan 'Available Appointment Slots Finder Tool' untuk memfilter dan "
        "mengembalikan HANYA slot yang tersedia, JIKA laporan medis "
        "menyatakan 'Perlu Perhatian'."
    ),
    expected_output=(
        "Sebuah list berisi dictionary jadwal yang tersedia, atau sebuah string "
        "pesan yang menyatakan tidak ada jadwal tersedia atau tidak perlu konsultasi."
    ),
    agent=admin_assistant_agent
)

appointment_booking_task = Task(
    description=(
        "Finalisasi proses booking janji temu. "
        "1. Ambil detail slot yang dipilih oleh user: '{chosen_slot}'. "
        "2. Ambil ID pasien: '{patient_id}'. "
        "3. Gunakan 'Appointment Booking Tool' untuk mengkonfirmasi janji temu "
        "dengan memanggil API backend utama."
    ),
    expected_output=(
        "Sebuah string pesan konfirmasi dari sistem, contoh: 'Janji temu berhasil dikonfirmasi...'"
    ),
    agent=admin_assistant_agent
)