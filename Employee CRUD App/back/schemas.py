from pydantic import BaseModel, EmailStr
from decimal import Decimal

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    position: str
    salary: Decimal

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        from_attributes = True
