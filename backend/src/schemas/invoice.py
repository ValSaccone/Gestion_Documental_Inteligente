from pydantic import BaseModel
from typing import List
from datetime import date

class ItemSchema(BaseModel):
    description: str
    quantity: float
    unitPrice: float


class InvoiceCreate(BaseModel):
    invoiceNumber: str
    date: date
    total: float
    provider: str
    providerCuit: str
    providerAddress: str
    items: List[ItemSchema]


class InvoiceResponse(BaseModel):
    id: int
    invoiceNumber: str
    date: date
    total: float
    provider: str
    user: str

"""from pydantic import BaseModel
from typing import List
from datetime import date

class ItemSchema(BaseModel):
    description: str
    quantity: str
    unitPrice: str

class InvoiceCreate(BaseModel):
    invoiceNumber: str
    date: date
    total: str
    provider: str
    providerCuit: str
    providerAddress: str
    items: List[ItemSchema]"""

