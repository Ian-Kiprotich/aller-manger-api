from pydantic import BaseModel
from typing import Annotated
from uuid import uuid4

class Table(BaseModel):
    reservation_id: str = str(uuid4())
    guest_names: list
    guest_ids: list
    address: str
    phone: str
    table_no: int
    active: bool = True
    time: str #day, afternoon, night

class TableCancel(BaseModel):
    table_no: int