# 🏥 Patient Management API using FastAPI

A **fully functional REST API** for managing patient records built with **FastAPI** and **Pydantic**, featuring CRUD operations and computed fields (BMI and health verdict).

---

## 🚀 Features

- ✅ Create, Read, Update, Delete (CRUD) operations for patient records
- 🧮 Automatic BMI calculation and health verdict
- 📄 Data validation using **Pydantic models**
- 💾 Data persistence using a JSON file
- 🔹 Fast and asynchronous API responses using FastAPI and Uvicorn
- 🛡️ Proper error handling and HTTP status codes
- 📊 Optional query-based filtering (age, BMI)

---

## 🧱 Tech Stack

- **Backend Framework:** FastAPI  
- **Data Validation:** Pydantic  
- **Storage:** JSON file (can be replaced with DB in production)  
- **Server:** Uvicorn (ASGI)  
- **Python Version:** 3.10+  

---

## 📂 Project Structure

```text
fastapi_patient_api/
│
├── main.py           # FastAPI application
├── data.json         # Patient data storage
├── requirements.txt  # Python dependencies
└── README.md

## 🧠 How It Works

### API Endpoints

| Method | Endpoint               | Description                     |
|--------|------------------------|---------------------------------|
| GET    | `/`                    | API welcome message             |
| GET    | `/about`               | API info                        |
| GET    | `/view`                | View all patients               |
| GET    | `/view_patient/{id}`   | View patient by ID              |
| GET    | `/selective_patient`   | Filter patients by age or BMI   |
| POST   | `/create`              | Add a new patient               |
| PUT    | `/edit/{id}`           | Update an existing patient      |
| DELETE | `/delete/{id}`         | Delete a patient record         |

---

### Computed Fields

- **BMI:** Automatically calculated using height and weight  
- **Verdict:** Health verdict based on BMI:  
  - Underweight: BMI < 18.5  
  - Normal: 18.5 ≤ BMI < 30  
  - Overweight: BMI ≥ 30  

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/fastapi-patient-api.git
cd fastapi-patient-api

python -m venv venv

# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt

uvicorn basicapi:app --reload
