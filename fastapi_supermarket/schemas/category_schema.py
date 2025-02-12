from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    description: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    description: str = None


class CategoryResponse(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CategoryListResponse(BaseModel):
    categories: list[CategoryResponse]
