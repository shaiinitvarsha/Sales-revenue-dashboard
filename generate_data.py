"""
generate_data.py
Generates a 2-year sample sales dataset (sample_sales_data.csv) so the
dashboard has enough history for month-over-month trends and a real
year-over-year comparison.
"""
import random
import csv
from datetime import date, timedelta

random.seed(7)

regions = ["North", "South", "East", "West"]
categories = {
    "Electronics": ["Wireless Earbuds", "Bluetooth Speaker", "Smart Watch", "Laptop Stand", "USB-C Hub"],
    "Home & Kitchen": ["Air Fryer", "Coffee Maker", "Blender", "Non-Stick Pan Set", "Electric Kettle"],
    "Apparel": ["Running Shoes", "Denim Jacket", "Cotton T-Shirt", "Winter Jacket", "Sports Cap"],
    "Office Supplies": ["Notebook Pack", "Ergonomic Chair", "Desk Organizer", "Whiteboard", "LED Desk Lamp"],
}
unit_price = {
    "Wireless Earbuds": 1499, "Bluetooth Speaker": 1999, "Smart Watch": 3499, "Laptop Stand": 899, "USB-C Hub": 1299,
    "Air Fryer": 4499, "Coffee Maker": 2999, "Blender": 1799, "Non-Stick Pan Set": 2299, "Electric Kettle": 999,
    "Running Shoes": 2499, "Denim Jacket": 1999, "Cotton T-Shirt": 599, "Winter Jacket": 3299, "Sports Cap": 399,
    "Notebook Pack": 249, "Ergonomic Chair": 6999, "Desk Organizer": 799, "Whiteboard": 1499, "LED Desk Lamp": 1199,
}

start = date(2024, 9, 1)
end = date(2026, 8, 15)

# gentle upward growth trend + seasonal bump in Nov/Dec (festive/holiday sales)
def seasonal_factor(d: date) -> float:
    growth = 1 + 0.15 * ((d - start).days / (end - start).days)  # up to +15% over 2 yrs
    season = 1.35 if d.month in (11, 12) else (0.9 if d.month in (1, 2) else 1.0)
    return growth * season

rows = []
order_id = 5000
customer_pool = [f"CUST{1000+i}" for i in range(400)]
d = start
while d <= end:
    base_orders = random.randint(2, 5)
    n_orders = max(1, round(base_orders * seasonal_factor(d)))
    for _ in range(n_orders):
        category = random.choice(list(categories.keys()))
        product = random.choice(categories[category])
        region = random.choice(regions)
        customer = random.choice(customer_pool)
        units = random.randint(1, 8)
        price = unit_price[product]
        revenue = units * price
        rows.append([order_id, d.isoformat(), customer, product, category, region, units, price, revenue])
        order_id += 1
    d += timedelta(days=1)

with open("sample_sales_data.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Order ID", "Date", "Customer ID", "Product", "Category", "Region", "Quantity", "Unit Price", "Revenue"])
    w.writerows(rows)

print(f"Generated {len(rows)} rows from {start} to {end}")
