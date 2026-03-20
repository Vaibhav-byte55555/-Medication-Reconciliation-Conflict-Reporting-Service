from fastapi import APIRouter
from app.model.snapshot import Snapshot
from app.config.db import db
from app.utils.conflict_detector import detect_conflicts
from datetime import datetime

router = APIRouter()


@router.post("/patients/{patient_id}/medications")
async def ingest_medications(patient_id: str, snapshot: Snapshot):

    # validation
    if not snapshot.sources:
        return {"error": "No sources provided"}

    # get latest version
    latest = await db.snapshots.find_one(
        {"patient_id": patient_id},
        sort=[("version", -1)]
    )

    new_version = 1
    if latest:
        new_version = latest["version"] + 1

    data = snapshot.dict()

    # NORMALIZATION ✅
    for source in data["sources"]:
        source["type"] = source["type"].lower().strip()

        for med in source["medications"]:
            med["name"] = med["name"].lower().strip()
            med["dosage"] = med["dosage"].lower().strip()
            med["status"] = med["status"].lower().strip()

    data["patient_id"] = patient_id
    data["version"] = new_version
    data["created_at"] = datetime.utcnow()

    try:
        # store snapshot
        await db.snapshots.insert_one(data)

        # detect conflicts
        conflicts = detect_conflicts(data["sources"])

        # store conflicts
        if conflicts:
            for conflict in conflicts:
                conflict["patient_id"] = patient_id
                conflict["version"] = new_version

            await db.conflicts.insert_many(conflicts)

        return {
            "message": "snapshot stored",
            "version": new_version
        }

    except Exception as e:
        return {"error": str(e)}


# GET conflicts for patient
@router.get("/conflicts/{patient_id}")
async def get_conflicts(patient_id: str):
    conflicts = await db.conflicts.find({"patient_id": patient_id}).to_list(100)

    for c in conflicts:
        c["_id"] = str(c["_id"])

    return {
        "patient_id": patient_id,
        "conflicts": conflicts
    }


# unresolved conflicts
@router.get("/reports/unresolved-conflicts")
async def unresolved_conflicts():
    conflicts = await db.conflicts.find({"resolved": False}).to_list(100)

    for c in conflicts:
        c["_id"] = str(c["_id"])

    return {
        "total_unresolved": len(conflicts),
        "data": conflicts
    }


# AGGREGATION ✅
@router.get("/reports/patients-with-conflicts")
async def patients_with_conflicts():
    patients = await db.conflicts.distinct("patient_id", {"resolved": False})

    return {
        "total_patients": len(patients),
        "patients": patients
    }