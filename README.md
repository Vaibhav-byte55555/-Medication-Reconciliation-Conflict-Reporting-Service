# Medication Reconciliation Conflict Reporting Service

##  Overview

This project is a FastAPI-based backend service designed to:

* Collect medication data from multiple healthcare sources
* Detect conflicts in medications (dosage mismatch, status conflict)
* Maintain version history of patient records
* Provide APIs to retrieve and analyze conflicts

---

##  Tech Stack

* **Backend:** FastAPI (Python)
* **Database:** MongoDB
* **Tools:** Uvicorn, Pydantic

---

##  How to Run the Project

### 1. Start MongoDB

Make sure MongoDB is installed and running locally.

---

### 2. Run FastAPI Server

```bash
uvicorn app.main:app --reload
```

---

### 3. Open API Docs

Go to:

```
http://127.0.0.1:8000/docs
```

---

## 📡 API Endpoints

### 🔹 1. Add Medications

**POST** `/patients/{patient_id}/medications`

Stores medication data and detects conflicts.

---

### 🔹 2. Get Conflicts

**GET** `/conflicts/{patient_id}`

Returns all detected conflicts for a patient.

---

### 🔹 3. Get Unresolved Conflicts

**GET** `/reports/unresolved-conflicts`

Returns all unresolved conflicts across patients.

---

### 🔹 4. Root Endpoint

**GET** `/`

Basic health check.

---

##  Example Request

```json
{
  "sources": [
    {
      "type": "clinic_emr",
      "medications": [
        {
          "name": "Aspirin",
          "dosage": "100mg",
          "frequency": "daily",
          "status": "active"
        }
      ]
    },
    {
      "type": "hospital_discharge",
      "medications": [
        {
          "name": "Aspirin",
          "dosage": "150mg",
          "frequency": "daily",
          "status": "active"
        }
      ]
    }
  ]
}
```

---

## Example Response

```json
{
  "message": "snapshot stored",
  "version": 1
}
```

---

##  Features

* ✔ Medication data ingestion from multiple sources
* ✔ Version tracking of patient records
* ✔ Conflict detection (dosage & status)
* ✔ MongoDB storage
* ✔ REST API using FastAPI

---

##  Project Structure

```
app/
 ├── config/        # Database connection
 ├── model/         # Pydantic models
 ├── routes/        # API routes
 ├── utils/         # Conflict detection logic
 ├── main.py        # Entry point
```

---
##  Author

Vaibhav Kadam

---

##  Note

Ensure MongoDB is running before starting the FastAPI server.

## Assumptions
- Medication names are treated as plain strings
- Conflict detection is rule-based

## Trade-offs
- Used MongoDB for flexible schema
- Simpler rules instead of complex medical logic

## Limitations
- No real drug interaction database
- Limited validation

## AI Usage
- Used AI for structure and debugging
- Manually verified logic and added improvements