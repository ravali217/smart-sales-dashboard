# services.py
from db import connect_db, create_tables
from models import Product, Salesperson, Order, OrderItem
from typing import List, Dict

create_tables()  # ensure tables exist

# ---- Products ----
def add_product(p: Product) -> int:
    conn = connect_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO products (name, sku, price, stock, category) VALUES (?, ?, ?, ?, ?)",
        (p.name, p.sku, p.price, p.stock, p.category),
    )
    product_id = c.lastrowid
    conn.commit()
    conn.close()
    return product_id

def list_products() -> List[Dict]:
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM products ORDER BY id")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_product(product_id: int):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def update_product_stock(product_id: int, new_stock: int):
    conn = connect_db()
    c = conn.cursor()
    c.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, product_id))
    conn.commit()
    conn.close()

# ---- Salespersons ----
def add_salesperson(s: Salesperson) -> int:
    conn = connect_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO salespersons (name, contact) VALUES (?, ?)",
        (s.name, s.contact),
    )
    sp_id = c.lastrowid
    conn.commit()
    conn.close()
    return sp_id

def list_salespersons() -> List[Dict]:
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM salespersons ORDER BY id")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_salesperson(sp_id: int):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM salespersons WHERE id = ?", (sp_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

# ---- Orders ----
def record_order(order: Order) -> int:
    # validate salesperson
    if not get_salesperson(order.salesperson_id):
        raise ValueError(f"Salesperson ID {order.salesperson_id} not found")

    # validate items
    for it in order.items:
        prod = get_product(it.product_id)
        if not prod:
            raise ValueError(f"Product ID {it.product_id} not found")
        if it.quantity <= 0:
            raise ValueError("Quantity must be > 0")
        if prod["stock"] < it.quantity:
            raise ValueError(f"Not enough stock for Product ID {it.product_id} (available {prod['stock']})")

    # calculate total
    total = sum(it.quantity * it.price for it in order.items)

    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO orders (salesperson_id, total_amount) VALUES (?, ?)",
              (order.salesperson_id, total))
    order_id = c.lastrowid

    for it in order.items:
        c.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
                  (order_id, it.product_id, it.quantity, it.price))
        # update stock
        prod = get_product(it.product_id)
        new_stock = prod["stock"] - it.quantity
        c.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, it.product_id))

    conn.commit()
    conn.close()
    return order_id

def get_sales_report() -> List[Dict]:
    conn = connect_db()
    c = conn.cursor()
    # join order_items, orders, products, salespersons
    c.execute("""
    SELECT oi.id as order_item_id, o.id as order_id, s.id as salesperson_id, s.name as salesperson,
           p.id as product_id, p.name as product_name, oi.quantity, oi.price,
           (oi.quantity * oi.price) as item_total, o.total_amount, o.created_at
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.id
    JOIN products p ON oi.product_id = p.id
    JOIN salespersons s ON o.salesperson_id = s.id
    ORDER BY o.created_at DESC, o.id DESC
    """)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows
