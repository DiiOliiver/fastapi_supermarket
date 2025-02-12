from typing import List, Optional

from pydantic import BaseModel

from fastapi_supermarket.schemas.product_sales_schema import (
    ProductSalesCreate,
)
from fastapi_supermarket.schemas.product_schema import ProductPublic


class SalesBase(BaseModel):
    id_user: int


class SalesCreate(SalesBase):
    products: List[ProductSalesCreate]


class SalesUpdate(BaseModel):
    id_user: Optional[int] = None
    products: Optional[List[ProductSalesCreate]] = None


class SalesResponse(SalesBase):
    id: int
    products: List[ProductPublic]

    class Config:
        from_attributes = True


class SalesListResponse(BaseModel):
    sales: List[SalesResponse]
