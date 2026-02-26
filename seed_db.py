from app import create_app, db, bcrypt
from app.models.product import Product
from app.models.user import User

app = create_app()

def seed_data():
    with app.app_context():
        # Create database tables
        db.create_all()

        # Check if products already exist
        if Product.query.first():
            print("Database already seeded.")
            return

        # Create admin user
        admin_pw = bcrypt.generate_password_hash("admin123").decode("utf-8")
        admin_user = User(
            username="admin",
            email="admin@auxyyskart.com",
            password_hash=admin_pw,
            is_admin=True
        )
        db.session.add(admin_user)

        products = [
            # ==================== Clothings ====================
            Product(name="Premium Black Hoodie", description="Luxury cotton blend hoodie, perfect for comfort and style.", price=89.99, category="Clothings", stock=50,
                    image_url="https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=600&h=400&fit=crop"),
            Product(name="Slim Fit Denim", description="High-quality indigo denim with a modern slim fit.", price=120.00, category="Clothings", stock=30,
                    image_url="https://images.unsplash.com/photo-1542272604-787c3835535d?w=600&h=400&fit=crop"),
            Product(name="Classic White T-Shirt", description="Essential crew-neck tee made from 100% organic cotton.", price=29.99, category="Clothings", stock=100,
                    image_url="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&h=400&fit=crop"),
            Product(name="Winter Puffer Jacket", description="Warm insulated jacket with water-resistant shell for cold days.", price=199.99, category="Clothings", stock=20,
                    image_url="https://images.unsplash.com/photo-1544923246-77307dd270cb?w=600&h=400&fit=crop"),
            Product(name="Linen Summer Shirt", description="Breathable linen blend shirt perfect for summer outings.", price=59.99, category="Clothings", stock=45,
                    image_url="https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600&h=400&fit=crop"),
            Product(name="Jogger Track Pants", description="Comfortable tapered joggers with elastic waistband.", price=49.99, category="Clothings", stock=60,
                    image_url="https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=600&h=400&fit=crop"),
            Product(name="Formal Blazer", description="Tailored single-breasted blazer for professional occasions.", price=179.99, category="Clothings", stock=15,
                    image_url="https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=600&h=400&fit=crop"),

            # ==================== Sneakers ====================
            Product(name="Aura Runners X1", description="Next-gen running shoes with superior cushioning.", price=150.00, category="Sneakers", stock=25,
                    image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&h=400&fit=crop"),
            Product(name="Urban Street Low", description="Classic minimalist sneakers for everyday wear.", price=110.00, category="Sneakers", stock=40,
                    image_url="https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=600&h=400&fit=crop"),
            Product(name="Trail Blazer Hiking Shoes", description="Rugged all-terrain shoes with ankle support and grip sole.", price=175.00, category="Sneakers", stock=20,
                    image_url="https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=600&h=400&fit=crop"),
            Product(name="Canvas Slip-Ons", description="Lightweight canvas shoes with memory foam insole.", price=55.00, category="Sneakers", stock=60,
                    image_url="https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=600&h=400&fit=crop"),
            Product(name="Retro High Tops", description="Vintage-inspired high-top sneakers with suede accents.", price=130.00, category="Sneakers", stock=30,
                    image_url="https://images.unsplash.com/photo-1607522370275-f14206abe190?w=600&h=400&fit=crop"),
            Product(name="Sports Running Pro", description="Professional running shoes with carbon fiber plate technology.", price=220.00, category="Sneakers", stock=15,
                    image_url="https://images.unsplash.com/photo-1539185441755-769473a23570?w=600&h=400&fit=crop"),

            # ==================== Fashion ====================
            Product(name="Gold Accent Watch", description="Elegant timepiece with gold-plated finish.", price=299.99, category="Fashion", stock=15,
                    image_url="https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=600&h=400&fit=crop"),
            Product(name="Leather Crossbody Bag", description="Genuine leather bag for urban professionals.", price=180.00, category="Fashion", stock=20,
                    image_url="https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600&h=400&fit=crop"),
            Product(name="Aviator Sunglasses", description="Premium polarized sunglasses with UV400 protection.", price=89.99, category="Fashion", stock=50,
                    image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=600&h=400&fit=crop"),
            Product(name="Silk Scarf Collection", description="Hand-painted pure silk scarf with vibrant patterns.", price=65.00, category="Fashion", stock=30,
                    image_url="https://images.unsplash.com/photo-1601924921557-45e6dea0c178?w=600&h=400&fit=crop"),
            Product(name="Diamond Stud Earrings", description="Sparkling cubic zirconia studs set in sterling silver.", price=120.00, category="Fashion", stock=25,
                    image_url="https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=600&h=400&fit=crop"),
            Product(name="Designer Belt", description="Genuine leather belt with brushed metal buckle.", price=75.00, category="Fashion", stock=40,
                    image_url="https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&h=400&fit=crop"),

            # ==================== Groceries ====================
            Product(name="Organic Coffee Blend", description="Fair-trade artisan coffee beans from Ethiopia.", price=25.50, category="Groceries", stock=100,
                    image_url="https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=600&h=400&fit=crop"),
            Product(name="Manuka Honey 500g", description="Premium medicinal grade honey from New Zealand.", price=45.00, category="Groceries", stock=60,
                    image_url="https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=600&h=400&fit=crop"),
            Product(name="Extra Virgin Olive Oil 1L", description="Cold-pressed premium olive oil from Mediterranean groves.", price=18.99, category="Groceries", stock=80,
                    image_url="https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=600&h=400&fit=crop"),
            Product(name="Organic Green Tea Pack", description="100 bags of antioxidant-rich Japanese green tea.", price=12.99, category="Groceries", stock=120,
                    image_url="https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=600&h=400&fit=crop"),
            Product(name="Dark Chocolate Assortment", description="Premium 70% cacao dark chocolate gift box, 12 pieces.", price=22.50, category="Groceries", stock=50,
                    image_url="https://images.unsplash.com/photo-1549007994-cb92caebd54b?w=600&h=400&fit=crop"),
            Product(name="Mixed Dry Fruits 1kg", description="Almonds, cashews, walnuts and raisins premium mix.", price=35.00, category="Groceries", stock=70,
                    image_url="https://images.unsplash.com/photo-1599599810694-b5b37304c041?w=600&h=400&fit=crop"),
            Product(name="Granola & Oats Pack", description="Crunchy granola with honey, nuts, and dried berries.", price=9.99, category="Groceries", stock=90,
                    image_url="https://images.unsplash.com/photo-1517093728432-a0440f8d45af?w=600&h=400&fit=crop"),

            # ==================== Electronics ====================
            Product(name="Noise Cancel Buds", description="Wireless earbuds with active noise cancellation.", price=199.00, category="Electronics", stock=35,
                    image_url="https://images.unsplash.com/photo-1590658268037-6bf12f032f55?w=600&h=400&fit=crop"),
            Product(name="Ultra HD Smart Display", description="4K HDR crystal clear display for modern homes.", price=899.00, category="Electronics", stock=10,
                    image_url="https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=600&h=400&fit=crop"),
            Product(name="Portable Power Bank 20000mAh", description="Fast-charging power bank with USB-C and dual USB-A ports.", price=49.99, category="Electronics", stock=75,
                    image_url="https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=600&h=400&fit=crop"),
            Product(name="Bluetooth Speaker Pro", description="360-degree surround sound waterproof speaker.", price=129.00, category="Electronics", stock=40,
                    image_url="https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=600&h=400&fit=crop"),
            Product(name="Smart Watch Series 5", description="Fitness tracker with heart rate, GPS, and AMOLED display.", price=349.00, category="Electronics", stock=20,
                    image_url="https://images.unsplash.com/photo-1546868871-af0de0ae72be?w=600&h=400&fit=crop"),
            Product(name="Wireless Charging Pad", description="Qi-certified fast wireless charger for all devices.", price=29.99, category="Electronics", stock=100,
                    image_url="https://images.unsplash.com/photo-1586816879360-004f5b0c51e3?w=600&h=400&fit=crop"),
            Product(name="Mechanical Gaming Keyboard", description="RGB backlit keyboard with Cherry MX switches.", price=159.00, category="Electronics", stock=30,
                    image_url="https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=600&h=400&fit=crop"),

            # ==================== Basic Needs ====================
            Product(name="Basmati Rice 5kg", description="Premium aged long-grain basmati rice, aromatic and fluffy.", price=12.99, category="Basic Needs", stock=200,
                    image_url="https://images.unsplash.com/photo-1586201375761-83865001e31c?w=600&h=400&fit=crop"),
            Product(name="Whole Wheat Flour 2kg", description="Stone-ground whole wheat flour for chapatis and bread.", price=5.49, category="Basic Needs", stock=180,
                    image_url="https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=600&h=400&fit=crop"),
            Product(name="Refined Sunflower Oil 1L", description="Light and healthy cooking oil for everyday meals.", price=4.99, category="Basic Needs", stock=150,
                    image_url="https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=600&h=400&fit=crop"),
            Product(name="Toor Dal 1kg", description="Premium split pigeon pea lentils, cleaned and polished.", price=3.99, category="Basic Needs", stock=200,
                    image_url="https://images.unsplash.com/photo-1613758947307-f3b8f5d80711?w=600&h=400&fit=crop"),
            Product(name="White Sugar 1kg", description="Fine-grain refined white sugar for cooking and beverages.", price=2.49, category="Basic Needs", stock=250,
                    image_url="https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=600&h=400&fit=crop"),
            Product(name="Iodized Table Salt 1kg", description="Free-flowing iodized salt, essential for daily cooking.", price=1.29, category="Basic Needs", stock=300,
                    image_url="https://images.unsplash.com/photo-1518110925495-5fe2571e78e0?w=600&h=400&fit=crop"),
            Product(name="Fresh Milk 1L", description="Pasteurized full-cream milk, farm fresh daily.", price=1.99, category="Basic Needs", stock=100,
                    image_url="https://images.unsplash.com/photo-1563636619-e9143da7973b?w=600&h=400&fit=crop"),
            Product(name="Bread Loaf (Whole Wheat)", description="Soft and fresh whole wheat sandwich bread, 400g.", price=2.29, category="Basic Needs", stock=120,
                    image_url="https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&h=400&fit=crop"),
            Product(name="Eggs (Pack of 12)", description="Farm-fresh free-range eggs, rich in protein.", price=4.49, category="Basic Needs", stock=150,
                    image_url="https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=600&h=400&fit=crop"),
            Product(name="Butter 500g", description="Creamy unsalted butter, perfect for cooking and spreading.", price=5.99, category="Basic Needs", stock=80,
                    image_url="https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=600&h=400&fit=crop"),
            Product(name="Bathing Soap (Pack of 3)", description="Moisturizing bath soap with natural Aloe Vera extracts.", price=3.49, category="Basic Needs", stock=200,
                    image_url="https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec?w=600&h=400&fit=crop"),
            Product(name="Toothpaste 150g", description="Cavity protection toothpaste with fluoride and mint freshness.", price=2.99, category="Basic Needs", stock=180,
                    image_url="https://images.unsplash.com/photo-1559131397-f94da358f7ca?w=600&h=400&fit=crop"),
            Product(name="Shampoo 250ml", description="Anti-dandruff shampoo with tea tree oil and keratin.", price=5.99, category="Basic Needs", stock=120,
                    image_url="https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=600&h=400&fit=crop"),
            Product(name="Laundry Detergent 1kg", description="Powerful stain-removing detergent powder, gentle on fabrics.", price=6.49, category="Basic Needs", stock=100,
                    image_url="https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=600&h=400&fit=crop"),
            Product(name="Dish Wash Liquid 500ml", description="Grease-cutting dishwash gel with lemon fragrance.", price=3.29, category="Basic Needs", stock=140,
                    image_url="https://images.unsplash.com/photo-1585441695325-21557ef06464?w=600&h=400&fit=crop"),
            Product(name="Toilet Cleaner 500ml", description="Disinfecting toilet cleaner with fresh pine scent.", price=2.99, category="Basic Needs", stock=130,
                    image_url="https://images.unsplash.com/photo-1585421514738-01798e348b17?w=600&h=400&fit=crop"),
            Product(name="Hand Wash 250ml", description="Antibacterial hand wash with moisturizing formula.", price=2.49, category="Basic Needs", stock=160,
                    image_url="https://images.unsplash.com/photo-1584305574647-0cc949a2bb9f?w=600&h=400&fit=crop"),
            Product(name="Tissue Paper (Pack of 4)", description="Soft 2-ply tissue rolls, 200 sheets each.", price=4.99, category="Basic Needs", stock=180,
                    image_url="https://images.unsplash.com/photo-1584556812952-905ffd0c611a?w=600&h=400&fit=crop"),
            Product(name="Drinking Water 5L Pack", description="Purified mineral water, BIS certified for daily hydration.", price=1.49, category="Basic Needs", stock=250,
                    image_url="https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=600&h=400&fit=crop"),
            Product(name="Instant Noodles (Pack of 6)", description="Quick-cook masala flavor noodles, ready in 2 minutes.", price=3.99, category="Basic Needs", stock=200,
                    image_url="https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=600&h=400&fit=crop"),
        ]

        db.session.bulk_save_objects(products)
        db.session.commit()
        print("Database seeded successfully!")
        print("Admin user: admin@auxyyskart.com / admin123")

if __name__ == "__main__":
    seed_data()
