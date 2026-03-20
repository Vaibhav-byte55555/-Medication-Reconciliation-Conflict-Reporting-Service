from pydantic import BaseModel
from typing import List

class Medication(BaseModel):
    name: str
    dosage: str
    frequency: str
    status: str

class Source(BaseModel):
    type: str
    medications: List[Medication]

class Snapshot(BaseModel):
    sources: List[Source]