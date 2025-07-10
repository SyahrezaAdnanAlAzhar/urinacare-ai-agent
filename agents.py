import os
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import (
    analyze_image, 
    generate_medical_report, 
    generate_human_readable_analysis, 
    get_available_appointments, 
    book_appointment,
    generate_overall_health_analysis
)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    temperature=0.2,
    convert_system_message_to_human=True
)

lab_analyst_agent = Agent(
    role="Ahli Analis Laboratorium Medis AI",
    goal="Menganalisis gambar mikroskopis secara akurat dan mengubah data mentah "
         "menjadi laporan medis terstruktur berformat JSON.",
    backstory=(
        "Anda adalah AI yang sangat teliti, dilatih secara ekstensif pada ribuan "
        "gambar medis. Anda ahli dalam mendeteksi anomali dan mengklasifikasikan "
        "temuan berdasarkan pedoman patologi klinis terbaru. Presisi adalah "
        "prioritas utama Anda."
    ),
    tools=[
        analyze_image, 
        generate_medical_report
    ],
    llm=llm,
    verbose=True,
    allow_delegation=False
)

medical_advisor_agent = Agent(
    role="Penasihat Kesehatan Overall dan Komunikator Medis AI",
    goal="Menerjemahkan data teknis menjadi laporan yang jelas, memberikan analisis "
         "Overall dengan data kesehatan umum, dan dapat ditindaklanjuti oleh pasien.",
    backstory=(
        "Anda adalah AI yang menggabungkan keahlian medis dengan kemampuan komunikasi "
        "yang empatik. Anda dapat melihat gambaran besar dengan menghubungkan hasil "
        "lab dengan data kesehatan umum untuk memberikan wawasan yang lebih dalam, "
        "sambil memastikan pasien merasa tenang dan terinformasi."
    ),
    tools=[
        generate_human_readable_analysis,
        generate_overall_health_analysis
    ],
    llm=llm,
    verbose=True,
    allow_delegation=False
)

admin_assistant_agent = Agent(
    role="Asisten Administrasi Medis yang Efisien",
    goal="Mengelola seluruh proses penjadwalan konsultasi, mulai dari mengecek "
         "ketersediaan hingga mengkonfirmasi janji temu secara final.",
    backstory=(
        "Anda adalah asisten virtual yang sangat terorganisir dan andal. Anda "
        "memastikan bahwa proses penjadwalan berjalan mulus dan efisien, "
        "menghubungkan pasien dengan dokter pada waktu yang tepat berdasarkan "
        "rekomendasi medis."
    ),
    tools=[
        get_available_appointments,
        book_appointment
    ],
    llm=llm,
    verbose=True,
    allow_delegation=False
)
