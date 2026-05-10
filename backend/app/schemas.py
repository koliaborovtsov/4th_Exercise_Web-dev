from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


class ProductSpecifications(BaseModel):
    power: str
    colorTemp: str
    base: str
    luminousFlux: str

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    category: str
    price: float = Field(gt=0, description="Цена должна быть больше 0")
    image: str
    description: Optional[str] = None
    power: Optional[str] = None
    color_temp: Optional[str] = None
    base_type: Optional[str] = None
    luminous_flux: Optional[str] = None
    in_stock: int = Field(
        default=0, ge=0, description="Количество не может быть отрицательным"
    )


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    image: Optional[str] = None
    description: Optional[str] = None
    power: Optional[str] = None
    color_temp: Optional[str] = None
    base_type: Optional[str] = None
    luminous_flux: Optional[str] = None
    in_stock: Optional[int] = Field(None, ge=0)


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductDetailResponse(ProductResponse):
    specifications: Optional[ProductSpecifications] = None


class ProductsListResponse(BaseModel):
    success: bool = True
    data: List[ProductResponse]
    total: int


class ProductSingleResponse(BaseModel):
    success: bool = True
    data: ProductDetailResponse


class OrderItemBase(BaseModel):
    """Позиция заказа"""

    product_id: int
    product_name: str
    price: float
    quantity: int = Field(gt=0, description="Количество должно быть больше 0")


class OrderCustomer(BaseModel):
    """Данные клиента"""

    name: str
    email: str
    phone: str
    address: str


class OrderCreate(BaseModel):
    """Создание заказа"""

    customer: OrderCustomer
    items: List[OrderItemBase]
    total: float
    comment: Optional[str] = None


class OrderItemResponse(BaseModel):
    """Ответ с позицией заказа"""

    id: int
    product_id: int
    product_name: str
    price: float
    quantity: int

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """Ответ с данными заказа"""

    id: int
    customer_name: str
    customer_email: str
    customer_phone: str
    customer_address: str
    comment: Optional[str] = None
    total: float
    status: str
    items: List[OrderItemResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True


class OrderCreateResponse(BaseModel):
    """Ответ при создании заказа"""

    success: bool = True
    data: dict
    message: str = "Заказ успешно создан"


class ErrorResponse(BaseModel):
    """Ответ с ошибкой"""

    success: bool = False
    error: str
    message: str
