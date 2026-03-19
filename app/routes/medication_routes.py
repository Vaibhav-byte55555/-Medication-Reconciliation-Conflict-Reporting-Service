from fastapi import APIRouter
from app.model.snapshot import Snapshot
from app.config.db import db

router = APIRouter()

@router.post("/patients/{patient_id}/medications")
async def ingest_medications(patient_id: str, snapshot: Snapshot):
    
    # get latest version
    latest = await db.snapshots.find_one(
        {"patient_id": patient_id},
        sort=[("version", -1)]
    )

    new_version = 1
    if latest:
        new_version = latest["version"] + 1

    data = snapshot.dict()
    data["patient_id"] = patient_id
    data["version"] = new_version

    await db.snapshots.insert_one(data)

    return {
        "message": "snapshot stored",
        "version": new_version
    }