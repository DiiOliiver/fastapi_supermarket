from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    id_category: int
    description: str
    price: float


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    id_category: Optional[int] = None
    description: Optional[str] = None
    price: Optional[float] = None


class ProductPublic(BaseModel):
    category: str
    description: str
    price: float


class ProductResponse(ProductPublic):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ProductListResponse(BaseModel):
    products: list[ProductResponse]
