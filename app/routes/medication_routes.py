from fastapi import APIRouter
from app.model.snapshot import Snapshot
from app.config.db import db
from app.utils.conflict_detector import detect_conflicts
from datetime import datetime

router = APIRouter()


# ------------------ INGEST API ------------------
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
    data["created_at"] = datetime.utcnow()

    # store snapshot
    await db.snapshots.insert_one(data)

    # detect conflicts
    conflicts = detect_conflicts(data["sources"])

    # store conflicts
    if len(conflicts) > 0:
        for conflict in conflicts:
            conflict["patient_id"] = patient_id
            conflict["version"] = new_version

        await db.conflicts.insert_many(conflicts)

    return {
        "message": "snapshot stored",
        "version": new_version
    }


# ------------------ GET CONFLICTS ------------------
@router.get("/conflicts/{patient_id}")
async def get_conflicts(patient_id: str):

    conflicts = await db.conflicts.find(
        {"patient_id": patient_id}
    ).to_list(100)

    for c in conflicts:
        c["_id"] = str(c["_id"])

    return {
        "patient_id": patient_id,
        "conflicts": conflicts
    }


# ------------------ REPORT API ------------------
@router.get("/reports/unresolved-conflicts")
async def unresolved_conflicts():

    conflicts = await db.conflicts.find(
        {"resolved": False}
    ).to_list(100)

    for c in conflicts:
        c["_id"] = str(c["_id"])

    return {
        "total_unresolved": len(conflicts),
        "data": conflicts
    }