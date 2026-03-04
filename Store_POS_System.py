# 1. I learned how inheritance works using a base Discount class.
# 2. I understood how polymorphism works with different discount types.
# 3. I learned how to use @dataclass for Product and Receipt.
# 4. I learned how to manage stock properly.
# 5. I understood how to validate user input.
# 6. I learned how to calculate subtotal and total.
# 7. I learned how to build a sales history system.
# 8. I improved my OOP skills in Python.
# 9. I learned how to design a small POS (Point of Sale) system.





# Import dataclass decorator to automatically create constructor and other methods
from dataclasses import dataclass

# Import type hints for better code readability
from typing import Dict, List, Tuple, Optional


# Base Discount class (parent class)
class Discount:
    # This method applies discount to subtotal (default = no discount)
    def apply(self, subtotal: float) -> float:
        return subtotal


# Percentage Discount class (child of Discount)
class PercentDiscount(Discount):
    def __init__(self, percent: float):
        # Check if percent is between 0 and 100
        if not (0 <= percent <= 100):
            raise ValueError("Percent must be 0-100.")
        self.percent = percent  # Store discount percentage

    # Apply percentage discount
    def apply(self, subtotal: float) -> float:
        return subtotal * (1 - self.percent / 100)


# Fixed amount discount class
class FixedDiscount(Discount):
    def __init__(self, amount: float):
        # Check if amount is not negative
        if amount < 0:
            raise ValueError("Amount must be >= 0.")
        self.amount = amount  # Store discount amount

    # Subtract fixed amount from subtotal
    def apply(self, subtotal: float) -> float:
        return max(0.0, subtotal - self.amount)  # Total cannot go below 0


# Product class using dataclass
@dataclass
class Product:
    product_id: str   # Product ID
    name: str         # Product name
    price: float      # Product price
    stock: int        # Available stock quantity

    # Increase stock quantity
    def restock(self, qty: int) -> None:
        if qty <= 0:
            raise ValueError("Qty must be > 0.")
        self.stock += qty  # Add quantity to stock

    # Reduce stock after sale
    def reduce_stock(self, qty: int) -> None:
        if qty <= 0:
            raise ValueError("Qty must be > 0.")
        if qty > self.stock:
            raise ValueError("Not enough stock.")
        self.stock -= qty  # Decrease stock


# Receipt class to store sale details
@dataclass
class Receipt:
    receipt_id: int   # Receipt number
    items: List[Tuple[str, int, float, float]]  
    # Each item contains: (product_id, quantity, unit_price, line_total)

    # Calculate subtotal (sum of all line totals)
    def subtotal(self) -> float:
        return sum(line_total for *_rest, line_total in self.items)

    # Calculate total (after applying discount if any)
    def total(self, discount: Optional[Discount] = None) -> float:
        sub = self.subtotal()
        return discount.apply(sub) if discount else sub

    # Create receipt from cart
    @classmethod
    def from_cart(cls, receipt_id: int, cart: Dict[str, int], products: Dict[str, Product]) -> "Receipt":
        items: List[Tuple[str, int, float, float]] = []
        for pid, qty in cart.items():
            p = products[pid]      # Get product object
            unit = p.price         # Get unit price
            items.append((pid, qty, unit, unit * qty))  # Add item tuple
        return cls(receipt_id, items)  # Return new receipt object

    # Print receipt on screen
    def print_receipt(self, products: Dict[str, Product], discount: Optional[Discount] = None) -> None:
        print(f"\nReceipt #{self.receipt_id}")
        print("-" * 20)
        for pid, qty, unit, line_total in self.items:
            print(f"{products[pid].name} ({pid}) x{qty} @ {unit:.2f} = {line_total:.2f}")
        print("-" * 20)
        print(f"Subtotal: {self.subtotal():.2f}")
        if discount:
            print(f"Total after discount: {self.total(discount):.2f}")
        else:
            print(f"Total: {self.subtotal():.2f}")


# Store class to manage products and sales
class Store:
    def __init__(self):
        self.products: Dict[str, Product] = {}  # Dictionary of products
        self.sales: List[Receipt] = []          # List of receipts
        self._next_receipt_id = 1               # Auto increment receipt ID

    # Add new product to store
    def add_product(self, product_id: str, name: str, price: float, stock: int) -> None:
        product_id = product_id.strip()
        name = name.strip()

        if not product_id or not name:
            raise ValueError("Product_id and name are required.")
        if product_id in self.products:
            raise ValueError("Product ID already exists.")
        if price < 0:
            raise ValueError("Price must be >= 0.")
        if stock < 0:
            raise ValueError("Stock must be >= 0.")

        # Create Product object and store in dictionary
        self.products[product_id] = Product(product_id, name, price, stock)

    # Restock existing product
    def restock(self, product_id: str, qty: int) -> None:
        if product_id not in self.products:
            raise KeyError("Product not found.")
        self.products[product_id].restock(qty)

    # Return products with low stock
    def low_stock(self, threshold: int = 5) -> List[Product]:
        return [p for p in self.products.values() if p.stock <= threshold]

    # Create a sale
    def create_sale(self, cart: Dict[str, int], discount: Optional[Discount] = None) -> Receipt:
        if not cart:
            raise ValueError("Cart is empty.")

        # Check if all products exist and stock is enough
        for pid, qty in cart.items():
            if pid not in self.products:
                raise KeyError(f"Product not found: {pid}")
            if qty <= 0:
                raise ValueError("Qty must be > 0.")
            if qty > self.products[pid].stock:
                raise ValueError(f"Not enough stock for {pid}.")

        # Reduce stock after validation
        for pid, qty in cart.items():
            self.products[pid].reduce_stock(qty)

        # Generate receipt ID
        rid = self._next_receipt_id
        self._next_receipt_id += 1

        # Create receipt
        receipt = Receipt.from_cart(rid, cart, self.products)
        self.sales.append(receipt)

        return receipt

    # Read discount from user
    @staticmethod
    def read_discount() -> Optional[Discount]:
        ans = input("Discount? (none/percent/fixed): ").strip().lower()
        if ans in ("", "none"):
            return None
        if ans == "percent":
            return PercentDiscount(float(input("Percent (0-100): ")))
        if ans == "fixed":
            return FixedDiscount(float(input("Amount: ")))
        raise ValueError("Invalid discount type.")


# Main function (program starts here)
def main():
    store = Store()  # Create Store object

    while True:  # Infinite loop for menu
        print("\n--- Store Menu ---")
        print("1) Add product")
        print("2) Restock product")
        print("3) List products")
        print("4) Create sale")
        print("5) Low stock list")
        print("6) Exit")

        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                pid = input("Product ID: ")
                name = input("Name: ")
                price = float(input("Price: "))
                stock = int(input("Stock qty: "))
                store.add_product(pid, name, price, stock)
                print("Product added.")

            elif choice == "2":
                pid = input("Product ID: ")
                qty = int(input("Restock qty: "))
                store.restock(pid, qty)
                print("Restocked.")

            elif choice == "3":
                if not store.products:
                    print("No products.")
                else:
                    for p in store.products.values():
                        print(f"{p.product_id}: {p.name} price={p.price:.2f} stock={p.stock}")

            elif choice == "4":
                cart: Dict[str, int] = {}
                print("Enter items. type 'done' when finished.")
                while True:
                    pid = input("Product ID: ").strip()
                    if pid.lower() == "done":
                        break
                    qty = int(input("qty: "))
                    cart[pid] = cart.get(pid, 0) + qty

                discount = Store.read_discount()
                receipt = store.create_sale(cart, discount)
                receipt.print_receipt(store.products, discount)

            elif choice == "5":
                t = int(input("Threshold (default 5): ") or "5")
                low = store.low_stock(t)
                if not low:
                    print("No low-stock products.")
                else:
                    for p in low:
                        print(f"{p.product_id}: {p.name} stock={p.stock}")

            elif choice == "6":
                print("goodbye.")
                break

            else:
                print("invalid choice.")

        except Exception as e:
            print("Error:", e)


# Run program only if this file is executed directly
if __name__ == "__main__":
    main()
