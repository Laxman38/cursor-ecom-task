from __future__ import annotations

import random
from pathlib import Path

import pandas as pd
from faker import Faker


NUM_USERS = 100
NUM_PRODUCTS = 50
NUM_ORDERS = 200
NUM_ORDER_ITEMS = 500
NUM_REVIEWS = 150


def sanitize_address(address: str) -> str:
    return " ".join(address.splitlines())


def main() -> None:
    faker = Faker()
    Faker.seed(42)
    random.seed(42)

    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

    users = [
        {
            "id": idx,
            "name": faker.name(),
            "email": faker.unique.email(),
            "address": sanitize_address(faker.address()),
        }
        for idx in range(1, NUM_USERS + 1)
    ]
    pd.DataFrame(users).to_csv(data_dir / "users.csv", index=False)
    print(f"Generated {len(users)} users.")

    categories = ["Electronics", "Home", "Outdoors", "Beauty", "Fitness", "Toys", "Books"]
    products = [
        {
            "id": idx,
            "name": faker.unique.catch_phrase(),
            "category": random.choice(categories),
            "price": round(random.uniform(5.0, 500.0), 2),
        }
        for idx in range(1, NUM_PRODUCTS + 1)
    ]
    pd.DataFrame(products).to_csv(data_dir / "products.csv", index=False)
    print(f"Generated {len(products)} products.")

    orders = [
        {
            "id": idx,
            "user_id": random.randint(1, NUM_USERS),
            "order_date": faker.date_between(start_date="-1y", end_date="today").isoformat(),
            "total": round(random.uniform(20.0, 1500.0), 2),
        }
        for idx in range(1, NUM_ORDERS + 1)
    ]
    pd.DataFrame(orders).to_csv(data_dir / "orders.csv", index=False)
    print(f"Generated {len(orders)} orders.")

    order_items = [
        {
            "id": idx,
            "order_id": random.randint(1, NUM_ORDERS),
            "product_id": random.randint(1, NUM_PRODUCTS),
            "quantity": random.randint(1, 5),
        }
        for idx in range(1, NUM_ORDER_ITEMS + 1)
    ]
    pd.DataFrame(order_items).to_csv(data_dir / "order_items.csv", index=False)
    print(f"Generated {len(order_items)} order items.")

    reviews = [
        {
            "id": idx,
            "product_id": random.randint(1, NUM_PRODUCTS),
            "user_id": random.randint(1, NUM_USERS),
            "rating": random.randint(1, 5),
            "comment": faker.sentence(nb_words=12),
        }
        for idx in range(1, NUM_REVIEWS + 1)
    ]
    pd.DataFrame(reviews).to_csv(data_dir / "reviews.csv", index=False)
    print(f"Generated {len(reviews)} reviews.")


if __name__ == "__main__":
    main()


