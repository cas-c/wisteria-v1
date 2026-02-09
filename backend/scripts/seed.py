"""Seed script — populates the database with an admin user and sample products.

Run from the backend directory:
    python -m scripts.seed

This script is idempotent: it checks for existing data before inserting.
If the admin user or products already exist, it skips them.

**Async pattern for standalone scripts:**
Unlike FastAPI routes (which get a session from dependency injection),
standalone scripts need to create their own async session. We use the
same `async_session` factory from `app.database` and wrap everything
in `asyncio.run()`.
"""

import asyncio

from sqlalchemy import select

from app.database import async_session
from app.models.admin_user import AdminUser
from app.models.product import Product, ProductCategory, ProductCondition
from app.utils.security import hash_password

ADMIN_EMAIL = "admin@wisteria.com"
ADMIN_PASSWORD = "admin123"

SAMPLE_PRODUCTS = [
    {
        "name": "Hatsune Miku Nendoroid #33",
        "slug": "hatsune-miku-nendoroid-33",
        "description": "The iconic Hatsune Miku in her classic outfit. Nendoroid #33 — one of the figures that started the Nendoroid craze. Comes with multiple face plates and accessories.",
        "price_cents": 4500,
        "condition": ProductCondition.LIKE_NEW,
        "category": ProductCategory.NENDOROID,
        "image_url": "https://images.unsplash.com/photo-1608889175123-8ee362201f81?w=600",
        "is_available": True,
        "quantity": 1,
    },
    {
        "name": "Rem 1/7 Scale Figure",
        "slug": "rem-1-7-scale-figure",
        "description": "Rem from Re:Zero in her maid outfit. Beautifully detailed 1/7 scale figure with flowing hair and dynamic pose. Approximately 23cm tall.",
        "price_cents": 18900,
        "condition": ProductCondition.NEW,
        "category": ProductCategory.SCALE_FIGURE,
        "image_url": "https://images.unsplash.com/photo-1613769049987-b31b641f25b1?w=600",
        "is_available": True,
        "quantity": 1,
    },
    {
        "name": "Pochacco Fluffy Plush",
        "slug": "pochacco-fluffy-plush",
        "description": "Adorable oversized Pochacco plush from Sanrio. Super soft and huggable. Approximately 30cm tall. Perfect for collectors and cuddlers alike.",
        "price_cents": 3200,
        "condition": ProductCondition.NEW,
        "category": ProductCategory.PLUSH,
        "image_url": "https://images.unsplash.com/photo-1559715541-5daf8a0296d0?w=600",
        "is_available": True,
        "quantity": 1,
    },
    {
        "name": "Sailor Moon Crystal Figuarts",
        "slug": "sailor-moon-crystal-figuarts",
        "description": "Sailor Moon from the Crystal series. S.H.Figuarts articulated figure with multiple hand parts and Moon Stick accessory. Incredibly poseable.",
        "price_cents": 7800,
        "condition": ProductCondition.USED,
        "category": ProductCategory.SCALE_FIGURE,
        "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=600",
        "is_available": True,
        "quantity": 1,
    },
    {
        "name": "Jujutsu Kaisen Gojo Nendoroid",
        "slug": "jujutsu-kaisen-gojo-nendoroid",
        "description": "Satoru Gojo Nendoroid with blindfold and sunglasses face plates. Includes Hollow Purple effect part and Domain Expansion hand gesture.",
        "price_cents": 5500,
        "condition": ProductCondition.NEW,
        "category": ProductCategory.NENDOROID,
        "image_url": "https://images.unsplash.com/photo-1601850494422-3cf14624b0b3?w=600",
        "is_available": True,
        "quantity": 1,
    },
    {
        "name": "Studio Ghibli Totoro Keychain Set",
        "slug": "studio-ghibli-totoro-keychain-set",
        "description": "Set of 3 miniature Totoro keychains — Big Totoro, Medium Totoro, and Small Totoro. Officially licensed Studio Ghibli merchandise.",
        "price_cents": 1800,
        "condition": ProductCondition.NEW,
        "category": ProductCategory.GOODS,
        "image_url": "https://images.unsplash.com/photo-1609372332255-611485350f25?w=600",
        "is_available": True,
        "quantity": 1,
    },
    {
        "name": "Evangelion Unit-01 1/4 Scale",
        "slug": "evangelion-unit-01-1-4-scale",
        "description": "Massive 1/4 scale Evangelion Unit-01 figure. LED eyes, incredible paint detail. A true centerpiece for any collection. Approximately 45cm tall.",
        "price_cents": 42000,
        "condition": ProductCondition.LIKE_NEW,
        "category": ProductCategory.SCALE_FIGURE,
        "image_url": "https://images.unsplash.com/photo-1531259683007-016a7b628fc3?w=600",
        "is_available": True,
        "quantity": 1,
    },
    {
        "name": "Spy x Family Anya Nendoroid",
        "slug": "spy-x-family-anya-nendoroid",
        "description": "Anya Forger with her signature smug face plate and peanut accessory. Also includes Chimera-san plush accessory and school uniform body.",
        "price_cents": 4800,
        "condition": ProductCondition.NEW,
        "category": ProductCategory.NENDOROID,
        "image_url": "https://images.unsplash.com/photo-1640006709862-b864e5e3e31e?w=600",
        "is_available": True,
        "quantity": 1,
    },
    {
        "name": "Kirby Dream Land Plush Collection",
        "slug": "kirby-dream-land-plush-collection",
        "description": "Extra soft Kirby plush from the Dream Land collection. Features the classic pink puffball in his iconic round shape. Approximately 20cm.",
        "price_cents": 2800,
        "condition": ProductCondition.LIKE_NEW,
        "category": ProductCategory.PLUSH,
        "image_url": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=600",
        "is_available": False,
        "quantity": 0,
    },
    {
        "name": "Demon Slayer Tanjiro Acrylic Stand",
        "slug": "demon-slayer-tanjiro-acrylic-stand",
        "description": "High-quality acrylic stand featuring Tanjiro Kamado in his Water Breathing pose. Approximately 15cm tall. Officially licensed.",
        "price_cents": 1500,
        "condition": ProductCondition.NEW,
        "category": ProductCategory.GOODS,
        "image_url": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=600",
        "is_available": True,
        "quantity": 1,
    },
]


async def seed() -> None:
    """Seed the database with sample data."""
    async with async_session() as session:
        # Seed admin user
        result = await session.execute(
            select(AdminUser).where(AdminUser.email == ADMIN_EMAIL)
        )
        existing_admin = result.scalar_one_or_none()

        if existing_admin is None:
            admin = AdminUser(
                email=ADMIN_EMAIL,
                password_hash=hash_password(ADMIN_PASSWORD),
            )
            session.add(admin)
            await session.commit()
            print(f"Created admin user: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
        else:
            print(f"Admin user already exists: {ADMIN_EMAIL}")

        # Seed products
        created_count = 0
        skipped_count = 0
        for product_data in SAMPLE_PRODUCTS:
            result = await session.execute(
                select(Product).where(Product.slug == product_data["slug"])
            )
            existing = result.scalar_one_or_none()

            if existing is None:
                product = Product(**product_data)
                session.add(product)
                created_count += 1
            else:
                skipped_count += 1

        await session.commit()
        print(f"Products: {created_count} created, {skipped_count} already existed")


if __name__ == "__main__":
    asyncio.run(seed())
