from pydantic import BaseModel
from typing import List, Dict, Optional

class PlanBase(BaseModel):
    name: str
    description: Optional[str] = None
    api_permissions: List[str]
    usage_limits: Dict[str, int]

class PlanCreate(PlanBase):
    pass

class PlanRead(PlanBase):
    id: int

    class Config:
        orm_mode = True
