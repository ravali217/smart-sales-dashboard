# services.py
from db import supabase
import pandas as pd

def list_products():
    """Fetch all products from Supabase"""
    res = supabase.table("products").select("*").execute()
    return res.data if res.data else []

def get_sales_report():
    """
    Generate sales report combining sales_orders, order_items, products, and salespersons
    """
    # Fetch all tables
    orders_res = supabase.table("sales_orders").select("*").execute()
    items_res = supabase.table("order_items").select("*").execute()
    products_res = supabase.table("products").select("*").execute()
    salespersons_res = supabase.table("salespersons").select("*").execute()

    # Check for empty tables
    if not orders_res.data or not items_res.data or not products_res.data or not salespersons_res.data:
        return []

    # Create lookup dictionaries for quick joins
    orders_lookup = {o["order_id"]: o for o in orders_res.data}
    products_lookup = {p["product_id"]: p for p in products_res.data}
    salespersons_lookup = {s["salesperson_id"]: s for s in salespersons_res.data}

    # Build the report
    report = []
    for item in items_res.data:
        order = orders_lookup.get(item["order_id"], {})
        product = products_lookup.get(item["product_id"], {})
        salesperson = salespersons_lookup.get(order.get("salesperson_id"), {})

        report.append({
            "Order ID": item["order_id"],
            "Product Name": product.get("name", "Unknown"),
            "Unit Price": item.get("price", 0),
            "Quantity": item.get("quantity", 0),
            "Total Amount": item.get("item_total", 0),
            "Salesperson": salesperson.get("name", "Unknown"),
            "Order Date": order.get("order_date")
        })

    return report
