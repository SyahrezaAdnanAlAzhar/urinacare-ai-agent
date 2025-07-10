import os
import json
import requests
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI


llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.2, convert_system_message_to_human=True)

CV_MODEL_API_URL = os.getenv("CV_MODEL_API_URL")
MAIN_BACKEND_API_URL = os.getenv("MAIN_BACKEND_API_URL")
APPOINTMENT_BACKEND_API_URL = os.getenv("APPOINTMENT_BACKEND_API_URL")


# Image Analysis Tool

@tool("Image Analysis Tool")
def analyze_image(image_path: str) -> dict:
    if not CV_MODEL_API_URL:
        return {"error": "URL API Model CV tidak terdapat di environment variables."}
    
    try:
        with open(image_path, 'rb') as f:
            files = {'image_file': f}
            response = requests.post(CV_MODEL_API_URL, files=files, timeout=60)
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Gagal memanggil API model CV: {str(e)}"}
    except FileNotFoundError:
        return {"error": f"File gambar tidak ditemukan di path: {image_path}"}
    


# Medical Report Generation Tool

medical_report_prompt = ChatPromptTemplate.from_template(
    """
    Anda adalah seorang ahli patologi klinis AI. Tugas Anda adalah menganalisis data lab mentah dari analisis urin dan membuat laporan medis terstruktur dalam format JSON.
    
    Konteks Medis Penting (Penyakit yang Mungkin Terdeteksi):
    - Hematuria (darah dalam urin): Curigai jika 'sel_darah_merah' > 10.
    - Bakteriuria (infeksi saluran kemih): Curigai jika 'bakteri' adalah 'sedang' atau 'tinggi'.
    - Urolithiasis (risiko batu ginjal): Curigai jika 'kristal_asam_urat' > 20.
    - Proteinuria (protein dalam urin): Curigai jika 'protein' adalah 'sedikit' atau lebih.

    Data Lab Mentah dari Model CV:
    {analysis_data}

    Instruksi:
    1. Analisis data lab berdasarkan konteks medis di atas.
    2. Buat output HANYA dalam format JSON yang valid.
    3. JSON harus memiliki kunci "status", yang bisa bernilai "Normal" atau "Perlu Perhatian".
    4. Untuk setiap kondisi yang terdeteksi, tambahkan kunci baru dengan penjelasan singkat.
    Contoh: {{"status": "Perlu Perhatian", "hematuria_finding": "Jumlah sel darah merah tinggi, mengindikasikan kemungkinan hematuria."}}
    5. Jika tidak ada yang terdeteksi, JSON hanya berisi: {{"status": "Normal", "summary": "Tidak ada anomali signifikan yang terdeteksi."}}

    JSON Output Anda:
    """
)
medical_report_chain = medical_report_prompt | llm | StrOutputParser()

@tool("Medical Report Generation Tool")
def generate_medical_report(analysis_data: dict) -> dict:
    json_string_output = medical_report_chain.invoke({"analysis_data": str(analysis_data)})
    try:
        return json.loads(json_string_output)
    except json.JSONDecodeError:
        return {"error": "AI gagal membuat laporan JSON yang valid.", "raw_output": json_string_output}
    
  
    
# Simple Narrative Generator Tool

human_readable_prompt = ChatPromptTemplate.from_template(
    """
    Anda adalah seorang komunikator medis AI. Tugas Anda adalah mengubah laporan medis terstruktur menjadi narasi sederhana.

    Laporan Medis Terstruktur (JSON):
    {categorized_report}

    Instruksi:
    1. Berdasarkan laporan di atas, tulis ringkasan naratif yang menjelaskan temuannya saja.
    2. JANGAN memberikan saran kesehatan atau korelasi dengan data lain.
    3. Tulis SELURUH output Anda dalam Bahasa {language}.

    Penjelasan Anda untuk Pasien:
    """
)
human_readable_chain = human_readable_prompt | llm | StrOutputParser()

@tool("Simple Narrative Generator Tool")
def generate_human_readable_analysis(categorized_report: dict, language: str = "Indonesia") -> str:
    return human_readable_chain.invoke({
        "categorized_report": str(categorized_report),
        "language": language
    })
    


# Available Appointment Slots Finder Tool

@tool("Available Appointment Slots Finder Tool")
def get_available_appointments(medical_report: dict, all_doctor_schedules: list) -> list | str:
    if medical_report.get("status") != "Perlu Perhatian":
        return "Hasil analisis tidak menunjukkan kebutuhan untuk konsultasi segera."
    
    available_slots = [slot for slot in all_doctor_schedules if slot.get("is_available", False)]
    
    if not available_slots:
        return "Mohon maaf, saat ini tidak ada jadwal dokter yang tersedia."
        
    return available_slots



# Appointment Booking Tool

@tool("Appointment Booking Tool")
def book_appointment(chosen_slot: dict, patient_id: str) -> str:
    if not APPOINTMENT_BACKEND_API_URL:
        return {"error": "URL Backend Appointment belum di-setting di environment variables."}

    booking_endpoint = APPOINTMENT_BACKEND_API_URL
    payload = {
        "patient_id": patient_id,
        "doctor_id": chosen_slot.get("doctor_id"),
        "appointment_datetime": f"{chosen_slot.get('date')}T{chosen_slot.get('time')}",
    }
    
    try:
        response = requests.post(booking_endpoint, json=payload, timeout=30)
        response.raise_for_status()
        return response.json().get("message", "Janji temu berhasil dikonfirmasi oleh sistem.")
    except requests.exceptions.RequestException as e:
        error_detail = e.response.text if e.response else "Tidak ada respons dari server."
        return f"Gagal membuat janji temu. Error: {str(e)}. Detail: {error_detail}"
    


# Overall Health Analysis Tool

overall_analysis_prompt = ChatPromptTemplate.from_template(
    """
    Anda adalah seorang penasihat kesehatan overall AI. Tugas Anda adalah memberikan analisis komprehensif dengan mengkorelasikan hasil lab dengan data kesehatan umum pasien.

    Laporan Medis Lab (JSON):
    {categorized_report}

    Data Kesehatan Umum Pasien (JSON):
    {patient_health_data}

    Instruksi:
    1. Analisis kedua sumber data tersebut.
    2. Cari korelasi yang mungkin ada. Contoh: jika laporan lab menunjukkan risiko batu ginjal dan data pasien menunjukkan berat badan berlebih, sebutkan hubungannya.
    3. Buat ringkasan naratif yang menggabungkan semua informasi ini menjadi wawasan yang berguna.
    4. Selalu sarankan untuk berkonsultasi dengan dokter untuk diagnosis akhir.
    5. Tulis SELURUH output Anda dalam Bahasa {language}.

    Analisis overall Anda:
    """
)
overall_analysis_chain = overall_analysis_prompt | llm | StrOutputParser()

@tool("Overall Health Analysis Tool")
def generate_overall_health_analysis(categorized_report: dict, patient_health_data: dict, language: str = "Indonesia") -> str:
    return overall_analysis_chain.invoke({
        "categorized_report": str(categorized_report),
        "patient_health_data": str(patient_health_data),
        "language": language
    })