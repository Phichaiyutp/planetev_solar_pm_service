from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class EnergyDataItem(BaseModel):
    timestamp: int 
    server_id: int
    data: str
    server_name: str
    name: str

class EnergyDataModel(BaseModel):
    data: list[EnergyDataItem]
