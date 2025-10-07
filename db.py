# db.py
from supabase import create_client
from dotenv import load_dotenv
import os

# ✅ Load .env variables
load_dotenv()

# ✅ Read and clean URL & KEY
url = os.getenv("SUPABASE_URL", "").strip().replace('"', '')
key = os.getenv("SUPABASE_KEY", "").strip().replace('"', '')

# ✅ Create Supabase client
supabase = create_client(url, key)

# ✅ Optional debug (can remove after first run)
print("URL (repr):", repr(url))
print("KEY (repr):", repr(key[:10] + "..."))

# ==============================
# Database Table Setup Functions
# ==============================

def create_tables():
    # Products table
    supabase.rpc("sql", {
        "q": """
        create table if not exists products (
            product_id bigint generated always as identity primary key,
            name text not null,
            sku text unique,
            price numeric,
            stock int,
            category text
        );
        """
    }).execute()

    # Salespersons table
    supabase.rpc("sql", {
        "q": """
        create table if not exists salespersons (
            salesperson_id bigint generated always as identity primary key,
            name text not null,
            contact text
        );
        """
    }).execute()

    # Orders table
    supabase.rpc("sql", {
        "q": """
        create table if not exists sales_orders (
            order_id bigint generated always as identity primary key,
            salesperson_id bigint references salespersons(salesperson_id),
            order_date timestamp default now()
        );
        """
    }).execute()

    # Order items
    supabase.rpc("sql", {
        "q": """
        create table if not exists order_items (
            order_item_id bigint generated always as identity primary key,
            order_id bigint references sales_orders(order_id),
            product_id bigint references products(product_id),
            quantity int,
            price numeric
        );
        """
    }).execute()

# ==============================
# Sample Data Insert Function
# ==============================

def insert_sample_data():
    # Insert products
    supabase.table("products").insert([
        {"name":"Mouse","sku":"M-001","price":599,"stock":50,"category":"Accessories"},
        {"name":"Keyboard","sku":"K-001","price":799,"stock":30,"category":"Accessories"},
        {"name":"Ice Cream","sku":"F-001","price":50,"stock":100,"category":"Food"}
    ]).execute()

    # Insert salesperson
    supabase.table("salespersons").insert([
        {"name":"Ravali","contact":"8121981396"},
        {"name":"Madhu","contact":"8121981234"}
    ]).execute()

    # Insert orders
    supabase.table("sales_orders").insert([
        {"salesperson_id": 1},
        {"salesperson_id": 2}
    ]).execute()

    # Insert order items
    supabase.table("order_items").insert([
        {"order_id": 1, "product_id":1, "quantity":3, "price":599},
        {"order_id": 1, "product_id":3, "quantity":5, "price":50},
        {"order_id": 2, "product_id":2, "quantity":2, "price":799}
    ]).execute()
