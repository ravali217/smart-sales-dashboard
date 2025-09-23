# utils.py
from services import list_products, list_salespersons, get_sales_report

def print_products():
    products = list_products()
    if not products:
        print("No products yet.")
        return
    print("\nProducts:")
    print(f"{'ID':<4} {'Name':<20} {'Price':<8} {'Stock':<6} {'SKU':<10} {'Category'}")
    for p in products:
        print(f"{p['id']:<4} {p['name'][:20]:<20} {p['price']:<8} {p['stock']:<6} {p.get('sku',''):<10} {p.get('category','')}")

def print_salespersons():
    sps = list_salespersons()
    if not sps:
        print("No salespersons yet.")
        return
    print("\nSalespersons:")
    print(f"{'ID':<4} {'Name':<20} {'Contact'}")
    for s in sps:
        print(f"{s['id']:<4} {s['name'][:20]:<20} {s.get('contact','')}")

def print_sales_report():
    rows = get_sales_report()
    if not rows:
        print("No sales recorded yet.")
        return
    print("\nSales Report (recent):")
    for r in rows:
        print(f"Order {r['order_id']} | {r['salesperson']} sold {r['quantity']} x {r['product_name']} @ {r['price']} = {r['item_total']} (Order total: {r['total_amount']})")
