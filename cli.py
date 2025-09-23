# cli.py
from models import Product, Salesperson, OrderItem, Order
import services
import utils

def main():
    print("Smart Sales Dashboard - CLI")
    while True:
        print("\nMenu:")
        print("1. Add Product")
        print("2. Add Salesperson")
        print("3. Record Sale")
        print("4. Show Products")
        print("5. Show Salespersons")
        print("6. Sales Report")
        print("7. Exit")
        ch = input("Enter choice: ").strip()

        if ch == "1":
            name = input("Product Name: ").strip()
            sku = input("SKU (optional): ").strip()
            price = float(input("Price: ").strip())
            stock = int(input("Stock: ").strip())
            category = input("Category (optional): ").strip()
            pid = services.add_product(Product(name=name, sku=sku, price=price, stock=stock, category=category))
            print(f"Product added with ID {pid}")

        elif ch == "2":
            name = input("Salesperson Name: ").strip()
            contact = input("Contact (optional): ").strip()
            spid = services.add_salesperson(Salesperson(name=name, contact=contact))
            print(f"Salesperson added with ID {spid}")

        elif ch == "3":
            utils.print_products()
            utils.print_salespersons()
            sp_id = int(input("Salesperson ID: ").strip())
            n = int(input("How many different products in this sale? ").strip())
            items = []
            for _ in range(n):
                pid = int(input("Product ID: ").strip())
                qty = int(input("Quantity: ").strip())
                prod = services.get_product(pid)
                if not prod:
                    print("Invalid product ID - skipping")
                    continue
                if qty > prod["stock"]:
                    print(f"Not enough stock (available {prod['stock']}) - skipping")
                    continue
                items.append(OrderItem(product_id=pid, quantity=qty, price=float(prod["price"])))
            if not items:
                print("No valid items to record.")
                continue
            order = Order(salesperson_id=sp_id, items=items)
            try:
                oid = services.record_order(order)
                print(f"Order recorded with ID {oid}")
            except Exception as e:
                print("Error:", e)

        elif ch == "4":
            utils.print_products()

        elif ch == "5":
            utils.print_salespersons()

        elif ch == "6":
            utils.print_sales_report()

        elif ch == "7":
            print("Bye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
