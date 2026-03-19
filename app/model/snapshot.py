from pydantic import BaseModel
from typing import List

class Medication(BaseModel):
    name: str
    dosage: str
    frequency: str
    status: str  # active / stopped

class Source(BaseModel):
    type: str
    medications: List[Medication]

class Snapshot(BaseModel):
    patient_id: str
    sources: List[Source]
    version: int