"""
Synthetic Cafe POS Data Generator
----------------------------------
Generates realistic, randomized point-of-sale (POS) transaction data for a
cafe, including the channel the order was placed through (In Store,
Delivery, Mobile). Useful for building/testing dashboards when you don't
have a live POS data feed.

Usage:
    from generate_cafe_pos_data import generate_pos_data

    df = generate_pos_data(num_orders=5000, seed=42)
    df.to_csv("cafe_pos_data.csv", index=False)

Running this file directly will generate a sample CSV.
"""

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

MENU = [
    # (item_name, category, unit_price)
    ("Drip Coffee",        "Beverage", 2.75),
    ("Latte",               "Beverage", 4.50),
    ("Cappuccino",          "Beverage", 4.25),
    ("Americano",           "Beverage", 3.25),
    ("Espresso Shot",       "Beverage", 2.50),
    ("Cold Brew",           "Beverage", 4.75),
    ("Mocha",               "Beverage", 4.95),
    ("Chai Latte",          "Beverage", 4.50),
    ("Matcha Latte",        "Beverage", 5.00),
    ("Hot Chocolate",       "Beverage", 3.75),
    ("Iced Tea",            "Beverage", 3.00),
    ("Croissant",           "Pastry",   3.50),
    ("Blueberry Muffin",    "Pastry",   3.25),
    ("Chocolate Chip Cookie","Pastry",  2.50),
    ("Cinnamon Roll",       "Pastry",   4.00),
    ("Bagel w/ Cream Cheese","Pastry",  3.75),
    ("Scone",               "Pastry",   3.40),
    ("Turkey & Swiss Sandwich", "Food", 8.50),
    ("Avocado Toast",       "Food",     7.95),
    ("Breakfast Burrito",   "Food",     7.25),
    ("Veggie Wrap",         "Food",     7.75),
    ("Caesar Salad",        "Food",     8.25),
    ("Grilled Cheese",      "Food",     6.50),
    ("Granola & Yogurt Cup","Snack",    4.95),
    ("Fruit Cup",           "Snack",    3.95),
    ("Protein Box",         "Snack",    6.95),
    ("Bag of Chips",        "Snack",    2.00),
]

STORE_LOCATIONS = [
    "Downtown",
    "Uptown",
    "Riverside",
    "Campus",
]

# Payment methods differ slightly by channel (e.g. no cash for delivery/mobile)
PAYMENT_METHODS_BY_CHANNEL = {
    "In Store": ["Cash", "Credit Card", "Debit Card", "Mobile Wallet"],
    "Mobile":   ["Credit Card", "Debit Card", "Mobile Wallet"],
    "Delivery": ["Credit Card", "Debit Card", "Mobile Wallet"],
}

# Relative popularity of each channel (In Store most common for a cafe)
CHANNEL_WEIGHTS = {
    "In Store": 0.60,
    "Mobile":   0.28,
    "Delivery": 0.12,
}

# Delivery platforms (only populated when channel == Delivery)
DELIVERY_PLATFORMS = ["DoorDash", "Uber Eats", "Grubhub"]

# Busier during morning/lunch rush; define hourly weights for an open-at-6am,
# close-at-8pm cafe
HOUR_WEIGHTS = {
    6: 2, 7: 6, 8: 10, 9: 8, 10: 6, 11: 7, 12: 9, 13: 7,
    14: 5, 15: 5, 16: 4, 17: 4, 18: 3, 19: 2, 20: 1,
}


def _random_timestamp(day: datetime) -> datetime:
    """Pick a timestamp within a given day, weighted toward busier hours."""
    hours = list(HOUR_WEIGHTS.keys())
    weights = list(HOUR_WEIGHTS.values())
    hour = random.choices(hours, weights=weights, k=1)[0]
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return day.replace(hour=hour, minute=minute, second=second, microsecond=0)


def _pick_channel() -> str:
    return random.choices(
        population=list(CHANNEL_WEIGHTS.keys()),
        weights=list(CHANNEL_WEIGHTS.values()),
        k=1,
    )[0]


def generate_pos_data(
    num_orders: int = 2000,
    start_date: str = "2025-01-01",
    end_date: str = "2025-12-31",
    seed: int | None = 42,
) -> pd.DataFrame:
    """
    Generate synthetic, line-item-level cafe POS data.

    Each row represents one item within an order (an order can have multiple
    line items), which is the typical grain POS systems export at and is
    flexible for dashboarding (you can aggregate up to the order level).

    Parameters
    ----------
    num_orders : int
        Number of distinct orders (transactions) to generate.
    start_date, end_date : str ("YYYY-MM-DD")
        Date range orders can fall within.
    seed : int or None
        Random seed for reproducibility. Set to None for different
        results each run.

    Returns
    -------
    pd.DataFrame with one row per line item, columns:
        order_id, order_datetime, day_of_week, store_location,
        order_channel, delivery_platform, payment_method, customer_id,
        item_name, category, unit_price, quantity, line_total,
        order_total, order_item_count
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    date_span_days = (end - start).days
    if date_span_days <= 0:
        raise ValueError("end_date must be after start_date")

    rows = []

    for order_num in range(1, num_orders + 1):
        order_id = f"ORD-{order_num:06d}"

        # Random day in range, then weighted random time
        day_offset = random.randint(0, date_span_days)
        order_day = start + timedelta(days=day_offset)
        order_datetime = _random_timestamp(order_day)

        channel = _pick_channel()
        store_location = random.choice(STORE_LOCATIONS)
        payment_method = random.choice(PAYMENT_METHODS_BY_CHANNEL[channel])
        delivery_platform = (
            random.choice(DELIVERY_PLATFORMS) if channel == "Delivery" else None
        )

        # Loyalty/customer id: mobile orders almost always tied to an
        # account; in-store sometimes; delivery depends on the platform acct
        if channel == "Mobile" or random.random() < 0.35:
            customer_id = f"CUST-{random.randint(1000, 4999)}"
        else:
            customer_id = None

        # Number of distinct items in this order
        num_items = random.choices([1, 2, 3, 4, 5], weights=[35, 30, 20, 10, 5])[0]
        items_in_order = random.sample(MENU, k=min(num_items, len(MENU)))

        line_items = []
        for item_name, category, unit_price in items_in_order:
            quantity = random.choices([1, 2, 3], weights=[80, 15, 5])[0]
            # Small random price variance to mimic discounts/upsizes
            price_variance = round(random.uniform(-0.25, 0.50), 2)
            final_unit_price = max(0.5, round(unit_price + price_variance, 2))
            line_total = round(final_unit_price * quantity, 2)
            line_items.append(
                {
                    "order_id": order_id,
                    "order_datetime": order_datetime,
                    "day_of_week": order_datetime.strftime("%A"),
                    "store_location": store_location,
                    "order_channel": channel,
                    "delivery_platform": delivery_platform,
                    "payment_method": payment_method,
                    "customer_id": customer_id,
                    "item_name": item_name,
                    "category": category,
                    "unit_price": final_unit_price,
                    "quantity": quantity,
                    "line_total": line_total,
                }
            )

        order_total = round(sum(li["line_total"] for li in line_items), 2)
        for li in line_items:
            li["order_total"] = order_total
            li["order_item_count"] = len(line_items)

        rows.extend(line_items)

    df = pd.DataFrame(rows)
    df = df.sort_values("order_datetime").reset_index(drop=True)

    # Nice column order
    column_order = [
        "order_id", "order_datetime", "day_of_week", "store_location",
        "order_channel", "delivery_platform", "payment_method", "customer_id",
        "item_name", "category", "unit_price", "quantity", "line_total",
        "order_total", "order_item_count",
    ]
    return df[column_order]


if __name__ == "__main__":
    data = generate_pos_data(num_orders=3000, start_date="2025-01-01", end_date="2025-12-31", seed=42)
    output_path = "cafe_pos_data.csv"
    data.to_csv(output_path, index=False)

    print(f"Generated {len(data):,} line items across {data['order_id'].nunique():,} orders")
    print(f"Saved to {output_path}\n")
    print("Order channel breakdown (by unique order):")
    print(
        data.drop_duplicates("order_id")["order_channel"]
        .value_counts(normalize=True)
        .round(3)
        .mul(100)
    )
    print("\nSample rows:")
    print(data.head(10).to_string(index=False))
