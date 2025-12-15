import asyncio
import os
import uuid 
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models import User, Address, Product, Order

async def seed_initial_data():
    """Асинхронное заполнение начальных данных"""
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:secret_password@localhost:5432/lab2_db")
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    async with async_session() as session:
        from sqlalchemy import select
        result = await session.execute(select(User))
        existing_users = result.scalars().all()
        
        if existing_users:
            print(f"В базе уже есть {len(existing_users)} пользователей")
            return
        
        print("Добавляем начальные данные...")
        
        
        users_data = [
            {"username": "Vyacheslav_kor", "email": "Vyacheslav.kor@example.com"},
            {"username": "Vlad_Dolgich", "email": "Vlad.Dolgich@example.com"},
            {"username": "Alex_Perar", "email": "Alex.Perar@example.com"},
            {"username": "Islam_Makhachev", "email": "Islam.Makhachev@example.com"},
            {"username": "Petr_Yan", "email": "Petr.Yan@example.com"},
        ]

        users = []
        for data in users_data:
            user = User(username=data["username"], email=data["email"])
            
            session.add(user)
            users.append(user)

        await session.flush()
        
        addresses_data = [
            {"user_id": users[0].id, "street": "15 Rue de Rivoli", "city": "Paris", "country": "France"},
            {"user_id": users[1].id, "street": "27 Oxford Street", "city": "London", "country": "UK"},
            {"user_id": users[2].id, "street": "42 Alexanderplatz", "city": "Berlin", "country": "Germany"},
            {"user_id": users[3].id, "street": "5 Shinjuku Street", "city": "Tokyo", "country": "Japan"},
            {"user_id": users[4].id, "street": "88 Marina Bay", "city": "Singapore", "country": "Singapore"},
        ] 

        addresses = []
        for data in addresses_data:
            address = Address(
                user_id=data["user_id"],
                street=data["street"],
                city=data["city"],
                country=data["country"]
            )
            
            
            session.add(address)
            addresses.append(address)

        await session.flush()
        
        descriptions = [
            "Full-stack разработчик, увлекается микросервисной архитектурой",
            "UX/UI дизайнер, специализируется на мобильных приложениях",
            "Data scientist, работает с машинным обучением и Big Data",
            "DevOps инженер, автоматизирует процессы CI/CD",
            "Python-разработчик, автор нескольких open-source библиотек"
        ]    
        
        for i, user in enumerate(users):
            user.description = descriptions[i]
        
        products_data = [
            {"name": "Игровая видеокарта RTX 4080", "price": 89999.99, "description": "16GB GDDR6, для 4K гейминга"},
            {"name": "Монитор 34'' изогнутый", "price": 45999.50, "description": "UWQHD, 144Hz, HDR400"},
            {"name": "Механическая клавиатура", "price": 8999.00, "description": "Cherry MX Red, RGB подсветка"},
            {"name": "Внешний SSD 2TB", "price": 12999.00, "description": "NVMe, скорость до 2000 МБ/с"},
            {"name": "Веб-камера 4K", "price": 8999.00, "description": "Автофокус, шумоподавление микрофона"},
        ]

        products = []
        for data in products_data:
            product = Product(
                name=data["name"], 
                price=data["price"], 
                description=data["description"]
            )
            
            
            session.add(product)
            products.append(product)
        
        await session.flush()
        
        for i in range(5):
            order = Order(
                user_id=users[i].id,
                address_id=addresses[i].id,
                product_id=products[i].id,
                quantity=1,
                status="pending"
            )
            
            session.add(order)
        
        await session.commit()
        
        print("Созданы пользователи, адреса, описания, продукты, заказы")

if __name__ == "__main__":
    asyncio.run(seed_initial_data())