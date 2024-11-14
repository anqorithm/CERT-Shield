from pydantic import BaseModel
from typing import Dict


class Alert(BaseModel):
    title: str
    severity: str
    logo: str
    alert_url: str
    details: Dict[str, str]
