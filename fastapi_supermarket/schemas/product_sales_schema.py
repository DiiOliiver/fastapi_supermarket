from typing import List

from pydantic import BaseModel


class ProductSalesBase(BaseModel):
    id_product: int


class ProductSalesCreate(ProductSalesBase):
    pass


class ProductSalesResponse(ProductSalesBase):
    id: int
    id_sale: int

    class Config:
        from_attributes = True


class ProductSalesListResponse(BaseModel):
    products: List[ProductSalesResponse]
