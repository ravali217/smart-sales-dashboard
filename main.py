from services import list_products, list_salespersons

if __name__ == "__main__":
    print("=== Smart Sales Dashboard CLI ===")
    print("Products:", list_products())
    print("Salespersons:", list_salespersons())
