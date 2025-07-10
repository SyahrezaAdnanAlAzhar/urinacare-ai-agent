# UrinaCare - Agentic AI Service 🤖

An Agentic AI backend system built with CrewAI and FastAPI. This project serves as the intelligent "brain" for the UrinaCare health application, leveraging a team of specialized AI agents to automate the workflow of microscopic image analysis, medical reporting, and appointment scheduling.

## 📋 Table of Contents
- [Overview](#-overview)
- [System Architecture](#️-system-architecture)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Core Capabilities & API Endpoints](#-core-capabilities--api-endpoints)
- [Example API Response](#-example-api-response)
- [File Structure](#-file-structure)
- [Important Notes](#-important-notes)
- [For Competition Judging](#-for-competition-judging)

## 🔍 Overview

This project implements an intelligent backend service that combines:
- **CrewAI** as a framework for multi-agent orchestration.
- **Google Gemini 1.5 Pro** as the Large Language Model for reasoning.
- **FastAPI** to serve the agent's functionalities through a robust REST API.
- **A Tool-Based Architecture** where agents can select and use specific functions to interact with external services (e.g., a CV model or other backend APIs).

The goal is to provide fast, comprehensive, and actionable analysis, powered by the collaboration of AI agents.

## 🏛️ System Architecture

The system is designed with a clear separation of concerns, where each agent has a specific role, goal, and set of tools. They collaborate within a `Crew` to solve complex `Tasks` and can access a `Knowledge Base` to enrich their context.

<p align="center">
  <img src="https://raw.githubusercontent.com/SyahrezaAdnanAlAzhar/urinacare-ai-agent/main/Arsitektur_AI_Agent.png" alt="UrinaCare Agent Architecture" width="800"/>
</p>

- **Agents**: A team consisting of a `Lab Analyst`, a `Medical Advisor`, and an `Admin Assistant`.
- **Tasks**: Job descriptions delegated to the agents (e.g., analyze an image, create a report).
- **Tools**: A modular set of Python functions that can be invoked by the agents.
- **Knowledge Base**: An external source of information (PDFs, CSVs) to deepen the agents' analysis.

## 🚀 Installation

### Prerequisites
```bash
python >= 3.10
```

### 1. Clone the Repository
```bash
git clone https://github.com/SyahrezaAdnanAlAzhar/urinacare-ai-agent.git
cd urinacare-ai-agent
```

### 2. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
# venv\Scripts\activate    # For Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment (Crucial Step)
Create a file named `.env` in the project's root directory and fill it with your credentials. **NEVER** commit this file to Git.
```env
# File: .env
GOOGLE_API_KEY="AIzaSy...your-google-api-key"
CV_MODEL_API_URL="https://your-cv-model.hf.space/analyze"
APPOINTMENT_BACKEND_API_URL="https://your-main-backend.com/api/v1/appointments"
```

## ⚡ Quick Start

After completing the installation and configuration, run the API server locally:

```bash
uvicorn main_api:app --reload
```

The server will start, and the API will be available. To test all endpoints interactively, open your browser and access the auto-generated documentation at:

**➡️ `http://127.0.0.1:8000/docs`**

## ✨ Core Capabilities & API Endpoints

This service provides several endpoints to handle the application's entire workflow:

- **`POST /analyze-sample`**: The main endpoint. It accepts an image file, runs the complete analysis pipeline (image analysis -> structured report -> narrative report), and returns both reports.
- **`POST /overall-analysis`**: Accepts a structured report and general patient health data (e.g., weight, age) to generate a comprehensive analysis that correlates both datasets.
- **`POST /get-available-appointments`**: Accepts a structured report and a full list of doctor schedules, then filters and returns only the available slots if a consultation is required.
- **`POST /book-appointment`**: The final endpoint. It accepts a user-selected appointment slot and a patient ID to confirm the appointment by calling another backend API.

## 📤 Example API Response

A successful output example from the `/analyze-sample` endpoint:
```json
{
  "narrative_report": "Your analysis results indicate a potential for Hematuria due to a high count of red blood cells. It is highly recommended to consult with a doctor promptly to get an accurate diagnosis and further treatment.",
  "structured_report": {
    "status": "Attention Required",
    "hematuria_finding": "High red blood cell count, indicating possible hematuria."
  }
}
```

## 📁 File Structure

```
urinacare-ai-agent/
├── agents.py               # Defines all CrewAI agents
├── main_api.py             # FastAPI application entrypoint and endpoint definitions
├── tasks.py                # Defines all tasks to be executed by the agents
├── tools.py                # Implements all tools usable by the agents
├── .env.example            # Example environment file (without values)
├── .gitignore
├── Dockerfile              # Configuration for application containerization
└── requirements.txt        # List of Python dependencies
```

## 📝 Important Notes

- **API Testing**: The easiest way to test functionality is through the Swagger UI interface at `/docs` while the server is running.
- **Security**: Ensure the `.env` file is included in `.gitignore` and is never uploaded to a public repository. Use *Secrets* for deployment.
- **Deployment**: This project is ready for deployment using Docker. For platforms like Hugging Face Spaces, simply upload all files and configure the *Secrets* in the *Settings* menu.

## 🏆 For Competition Judging

To reproduce and evaluate this project, the committee can follow these steps:

1.  **Follow Installation Steps**: Clone the repository, create a virtual environment, and install dependencies from `requirements.txt`.
2.  **Set Credentials**: Create a `.env` file and populate the `GOOGLE_API_KEY` and other API URLs. For deployment on HF Spaces, set these credentials in the *Repository secrets* section.
3.  **Run the Server**: Execute the command `uvicorn main_api:app --host 0.0.0.0 --port 8000`.
4.  **Verify Endpoints**: Open `http://<SERVER_IP>:8000/docs` and test each API endpoint sequentially, starting with `/analyze-sample` to obtain data that can be used in other endpoints.
