# models.py
from pydantic import BaseModel
from typing import List, Optional

# Blueprint for each clinical trial record
class ClinicalTrial(BaseModel):
    id: str
    title: str
    status: str
    conditions: List[str]
    interventions: List[str]
    locations: List[str]
    url: str

# Blueprint for each drug label record
class DrugLabel(BaseModel):
    id: str
    brand_name: str
    generic_name: Optional[str]
    purpose: Optional[str]
    warnings: Optional[str]
    indications: Optional[str]
