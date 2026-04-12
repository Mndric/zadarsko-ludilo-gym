from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class EquipmentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    quantity: int = Field(..., gt=0)

class EquipmentCreate(EquipmentBase):
    name: str
    quantity: int

class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None

class EquipmentOut(EquipmentBase):
    id: int
    class Config:
        from_attributes = True

class ReservationOut(BaseModel):
    id: int
    user_id: int
    equipment_id: int
    reservation_date: datetime
    class Config: 
        from_attributes = True

class MembershipOut(BaseModel):
    id: int
    user_id: int
    start_date: datetime
    class Config:
        from_attributes = True