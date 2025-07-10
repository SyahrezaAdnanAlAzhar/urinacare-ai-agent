from dotenv import load_dotenv
load_dotenv()

import os
import shutil
from typing import List, Dict, Any

from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from pydantic import BaseModel, Field

from crewai import Crew, Process

from agents import lab_analyst_agent, medical_advisor_agent, admin_assistant_agent
from tasks import (
    lab_analysis_task, 
    narrative_reporting_task,
    overall_review_task,
    appointment_search_task,
    appointment_booking_task
)

app = FastAPI(
    title="UrinaCare Agentic AI Service",
    version="1.0.0",
    description="Layanan AI untuk analisis sampel urin, pembuatan laporan, dan penjadwalan."
)

analysis_crew = Crew(
    agents=[lab_analyst_agent, medical_advisor_agent],
    tasks=[lab_analysis_task, narrative_reporting_task],
    process=Process.sequential,
    verbose=2 
)

class OverallAnalysisRequest(BaseModel):
    categorized_report: Dict[str, Any] = Field(..., description="JSON laporan medis terstruktur dari hasil analisis.")
    patient_health_data: Dict[str, Any] = Field(..., description="JSON data kesehatan umum pasien (berat, usia, dll).")
    language: str = Field("Indonesia", description="Bahasa yang diinginkan untuk output.")

class AppointmentSearchRequest(BaseModel):
    categorized_report: Dict[str, Any] = Field(..., description="JSON laporan medis terstruktur.")
    all_doctor_schedules: List[Dict[str, Any]] = Field(..., description="Daftar LENGKAP jadwal semua dokter.")

class AppointmentBookingRequest(BaseModel):
    chosen_slot: Dict[str, Any] = Field(..., description="Objek JSON dari slot jadwal yang dipilih user.")
    patient_id: str = Field(..., description="ID unik pasien yang melakukan booking.")
    

@app.get("/", summary="Health Check")
def read_root():
    return {"status": "UrinaCare AI Agent Service is running."}


@app.post("/analyze-sample", summary="1. Menganalisis Sampel Urin dari Gambar")
async def analyze_sample_endpoint(
    image: UploadFile = File(..., description="File gambar sampel urin."),
    language: str = "Indonesia"
):
    temp_dir = "temp_images"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, image.filename)

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        inputs = {
            "image_path": temp_file_path,
            "language": language
        }
        
        result = analysis_crew.kickoff(inputs=inputs)

        categorized_report_output = lab_analysis_task.output.raw if hasattr(lab_analysis_task.output, 'raw') else None
        
        return {
            "narrative_report": result,
            "structured_report": categorized_report_output
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi error saat proses analisis: {str(e)}")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@app.post("/overall-analysis", summary="2. Membuat Analisis Overall")
def overall_analysis_endpoint(request: OverallAnalysisRequest):
    overall_crew = Crew(agents=[medical_advisor_agent], tasks=[overall_review_task])
    result = overall_crew.kickoff(inputs=request.dict())
    return {"overall_analysis_report": result}

@app.post("/get-available-appointments", summary="3. Mencari Jadwal Dokter yang Tersedia")
def get_appointments_endpoint(request: AppointmentSearchRequest):
    appointment_crew = Crew(agents=[admin_assistant_agent], tasks=[appointment_search_task])
    result = appointment_crew.kickoff(inputs=request.dict())
    return {"available_slots": result}


@app.post("/book-appointment", summary="4. Memfinalisasi Janji Temu")
def book_appointment_endpoint(request: AppointmentBookingRequest):
    booking_crew = Crew(agents=[admin_assistant_agent], tasks=[appointment_booking_task])
    result = booking_crew.kickoff(inputs=request.dict())
    return {"booking_confirmation": result}