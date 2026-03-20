import asyncio
from app.config.db import db


async def seed():
    await db.snapshots.insert_one({
        "patient_id": "p_test",
        "version": 1,
        "sources": [
            {
                "type": "clinic_emr",
                "medications": [
                    {
                        "name": "aspirin",
                        "dosage": "100mg",
                        "frequency": "daily",
                        "status": "active"
                    }
                ]
            }
        ]
    })

    print("Seed data inserted")


if __name__ == "__main__":
    asyncio.run(seed())