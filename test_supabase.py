import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch products
try:
    res = supabase.table("products").select("*").execute()
    print("Products:", res.data)
except Exception as e:
    print("Error:", e)
