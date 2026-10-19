import pandas as pd
import random
from pathlib import Path
from datetime import datetime, timedelta

random.seed(42)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

products = {
    "Electronics": [
        ("Headphones", 1500),
        ("Keyboard", 900),
        ("Mouse", 500),
        ("Smart Watch", 2500)
    ],
    "Fashion": [
        ("T-Shirt", 600),
        ("Jeans", 1200),
        ("Shoes", 2000),
        ("Jacket", 1800)
    ],
    "Home": [
        ("Lamp", 800),
        ("Chair", 2500),
        ("Table", 4000),
        ("Bedsheet", 1000)
    ],
    "Books": [
        ("Python Book", 500),
        ("Data Science Book", 900),
        ("Novel", 350)
    ]
}

payment_methods = [
    "UPI", "Credit Card", "Debit Card", "Cash on Delivery"
]

start_date = datetime(2025, 1, 1)
rows = []

for order_id in range(1, 1001):
    category = random.choice(list(products.keys()))
    product, price = random.choice(products[category])

    quantity = random.randint(1, 4)
    discount = random.choice([0, 0, 5, 10, 15])

    revenue = quantity * price * (1 - discount / 100)

    order_date = start_date + timedelta(
        days=random.randint(0, 364)
    )

    rows.append({
        "order_id": order_id,
        "order_date": order_date.strftime("%Y-%m-%d"),
        "customer_id": random.randint(1001, 1250),
        "product": product,
        "category": category,
        "quantity": quantity,
        "unit_price": price,
        "discount_percent": discount,
        "revenue": round(revenue, 2),
        "payment_method": random.choice(payment_methods)
    })

df = pd.DataFrame(rows)

file_path = DATA_DIR / "shopping_data.csv"
df.to_csv(file_path, index=False)

print(f"Dataset created successfully: {file_path}")
print(f"Total orders generated: {len(df)}")
print(df.head())