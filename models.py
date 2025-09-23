# models.py
from dataclasses import dataclass
from typing import List

@dataclass
class Product:
    name: str
    sku: str
    price: float
    stock: int
    category: str = None

@dataclass
class Salesperson:
    name: str
    contact: str = None

@dataclass
class OrderItem:
    product_id: int
    quantity: int
    price: float

@dataclass
class Order:
    salesperson_id: int
    items: List[OrderItem]
