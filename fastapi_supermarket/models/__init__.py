from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    cpf: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    deleted_at: Mapped[datetime] = mapped_column(init=False, nullable=True)


@table_registry.mapped_as_dataclass
class Category:
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    deleted_at: Mapped[datetime] = mapped_column(init=False, nullable=True)

    # Relacionamento reverso com Product
    products: Mapped[list['Product']] = relationship(
        back_populates='category', init=False
    )


@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_category: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    description: Mapped[str]
    price: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    deleted_at: Mapped[datetime] = mapped_column(init=False, nullable=True)

    # Relacionamento com Category
    category: Mapped['Category'] = relationship(
        back_populates='products', init=False
    )


@table_registry.mapped_as_dataclass
class Sales:
    __tablename__ = 'sales'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    deleted_at: Mapped[datetime] = mapped_column(init=False, nullable=True)

    # Relacionamento com ProductSales
    products: Mapped[list['ProductSales']] = relationship(
        back_populates='sale', default_factory=list
    )


@table_registry.mapped_as_dataclass
class ProductSales:
    __tablename__ = 'product_sales'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_sale: Mapped[int] = mapped_column(ForeignKey('sales.id'))
    id_product: Mapped[int] = mapped_column(ForeignKey('products.id'))

    # Relacionamento com Sales e Product
    sale: Mapped['Sales'] = relationship(back_populates='products', init=False)
    product: Mapped['Product'] = relationship(init=False)
