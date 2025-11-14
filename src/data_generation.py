from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Sequence


@dataclass(frozen=True)
class DataConfig:
    """Configuration that controls how many records to generate."""

    num_users: int = 50
    num_products: int = 30
    num_orders: int = 80
    max_items_per_order: int = 5
    num_reviews: int = 60


def _random_date(within_days: int = 120) -> str:
    """Return an ISO formatted date within the last N days."""
    end = datetime.now()
    start = end - timedelta(days=within_days)
    random_ts = start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))
    return random_ts.strftime("%Y-%m-%d")


def _weighted_choice(options: Sequence[str]) -> str:
    return random.choice(tuple(options))


def generate_users(cfg: DataConfig) -> List[Dict[str, str]]:
    first_names = ["Avery", "Jordan", "Parker", "Emerson", "Riley", "Quinn", "Dakota", "Harper"]
    last_names = ["Lee", "Garcia", "Patel", "Nguyen", "Walker", "Bennett", "Chen", "Lopez"]
    countries = ["USA", "Canada", "Germany", "India", "Brazil", "Australia", "UK"]

    users = []
    for idx in range(1, cfg.num_users + 1):
        first = random.choice(first_names)
        last = random.choice(last_names)
        email = f"{first.lower()}.{last.lower()}{idx}@example.com"
        users.append(
            {
                "user_id": idx,
                "first_name": first,
                "last_name": last,
                "email": email,
                "signup_date": _random_date(365),
                "country": random.choice(countries),
            }
        )
    return users


def generate_products(cfg: DataConfig) -> List[Dict[str, object]]:
    categories = ["Electronics", "Home", "Outdoors", "Beauty", "Fitness", "Toys"]
    adjectives = ["Eco", "Smart", "Compact", "Premium", "Lite", "Pro"]
    nouns = ["Speaker", "Blender", "Tent", "Watch", "Mat", "Drone", "Bottle", "Camera"]

    products = []
    for idx in range(1, cfg.num_products + 1):
        name = f"{random.choice(adjectives)} {random.choice(nouns)}"
        price = round(random.uniform(15.0, 500.0), 2)
        products.append(
            {
                "product_id": idx,
                "name": name,
                "category": random.choice(categories),
                "price": price,
                "inventory": random.randint(10, 400),
            }
        )
    return products


def generate_orders(cfg: DataConfig, users: List[Dict[str, object]]) -> List[Dict[str, object]]:
    statuses = ["PENDING", "SHIPPED", "DELIVERED", "CANCELLED"]
    orders = []
    for idx in range(1, cfg.num_orders + 1):
        user = random.choice(users)
        orders.append(
            {
                "order_id": idx,
                "user_id": user["user_id"],
                "order_date": _random_date(120),
                "status": random.choices(statuses, weights=[0.2, 0.4, 0.35, 0.05])[0],
                "total_amount": 0.0,  # updated after order items are generated
            }
        )
    return orders


def generate_order_items(
    cfg: DataConfig,
    orders: List[Dict[str, object]],
    products: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    items = []
    item_id = 1
    for order in orders:
        num_items = random.randint(1, cfg.max_items_per_order)
        order_total = 0.0
        for _ in range(num_items):
            product = random.choice(products)
            quantity = random.randint(1, 4)
            unit_price = product["price"]
            line_total = round(unit_price * quantity, 2)
            order_total += line_total
            items.append(
                {
                    "order_item_id": item_id,
                    "order_id": order["order_id"],
                    "product_id": product["product_id"],
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "line_total": line_total,
                }
            )
            item_id += 1
        order["total_amount"] = round(order_total, 2)
    return items


def generate_reviews(cfg: DataConfig, users: List[Dict[str, object]], products: List[Dict[str, object]]) -> List[Dict[str, object]]:
    comments = [
        "Great quality!",
        "Met expectations.",
        "Would buy again.",
        "Not worth the price.",
        "Fast shipping and solid build.",
        "Packaging could be better.",
        "Exceeded expectations!",
    ]

    reviews = []
    for idx in range(1, cfg.num_reviews + 1):
        user = random.choice(users)
        product = random.choice(products)
        reviews.append(
            {
                "review_id": idx,
                "user_id": user["user_id"],
                "product_id": product["product_id"],
                "rating": random.randint(1, 5),
                "review_date": _random_date(120),
                "comment": random.choice(comments),
            }
        )
    return reviews


def generate_all_data(cfg: DataConfig | None = None) -> Dict[str, Dict[str, object]]:
    cfg = cfg or DataConfig()
    users = generate_users(cfg)
    products = generate_products(cfg)
    orders = generate_orders(cfg, users)
    order_items = generate_order_items(cfg, orders, products)
    reviews = generate_reviews(cfg, users, products)

    return {
        "users": {"fieldnames": list(users[0].keys()), "rows": users},
        "products": {"fieldnames": list(products[0].keys()), "rows": products},
        "orders": {"fieldnames": list(orders[0].keys()), "rows": orders},
        "order_items": {"fieldnames": list(order_items[0].keys()), "rows": order_items},
        "reviews": {"fieldnames": list(reviews[0].keys()), "rows": reviews},
    }


