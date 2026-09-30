import os
import shutil
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from products.models import Category, Product, ProductImage
from orders.models import Order, OrderItem

User = get_user_model()


class Command(BaseCommand):
    help = "Demonstratsion ma'lumotlar bazasini (seed data) yaratadi: foydalanuvchilar, MPTT kategoriyalar, mahsulotlar va buyurtmalar."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(">>> Demo ma'lumotlarni yaratish boshlandi..."))

        # 1. Superuser
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@marketplace.uz',
                'first_name': 'Boshqaruvchi',
                'last_name': 'Admin',
                'role': 'buyer',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("[OK] Admin yaratildi: admin / admin123"))
        else:
            self.stdout.write("[INFO] Admin mavjud: admin")

        # 2. Sellers
        seller1, created = User.objects.get_or_create(
            username='seller1',
            defaults={
                'email': 'seller1@techzone.uz',
                'first_name': 'Akmal',
                'last_name': 'Rahimov',
                'role': 'seller',
                'shop_name': 'TechZone Official',
                'is_verified': True,
                'phone': '+998901234567',
            }
        )
        if created:
            seller1.set_password('seller123')
            seller1.save()
            self.stdout.write(self.style.SUCCESS("[OK] Sotuvchi 1 yaratildi: seller1 (TechZone Official) / seller123"))

        seller2, created = User.objects.get_or_create(
            username='seller2',
            defaults={
                'email': 'seller2@modastil.uz',
                'first_name': 'Malika',
                'last_name': 'Karimova',
                'role': 'seller',
                'shop_name': 'Moda & Stil Butigi',
                'is_verified': True,
                'phone': '+998935557799',
            }
        )
        if created:
            seller2.set_password('seller123')
            seller2.save()
            self.stdout.write(self.style.SUCCESS("[OK] Sotuvchi 2 yaratildi: seller2 (Moda & Stil Butigi) / seller123"))

        # 3. Buyers
        buyer1, created = User.objects.get_or_create(
            username='buyer1',
            defaults={
                'email': 'buyer1@gmail.com',
                'first_name': 'Sardor',
                'last_name': 'Aliyev',
                'role': 'buyer',
                'phone': '+998971112233',
            }
        )
        if created:
            buyer1.set_password('buyer123')
            buyer1.save()
            self.stdout.write(self.style.SUCCESS("[OK] Xaridor yaratildi: buyer1 / buyer123"))

        # 4. Media setup for products
        media_products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
        os.makedirs(media_products_dir, exist_ok=True)
        default_prod_src = os.path.join(settings.BASE_DIR, 'static', 'images', 'default-product.jpg')
        sample_img_dest = os.path.join(media_products_dir, 'sample.jpg')
        if os.path.exists(default_prod_src) and not os.path.exists(sample_img_dest):
            shutil.copyfile(default_prod_src, sample_img_dest)

        prod_image_rel = 'products/sample.jpg' if os.path.exists(sample_img_dest) else ''

        # 5. MPTT Categories (3-level tree minimum)
        self.stdout.write("[*] 3 darajali MPTT kategoriyalar daraxti yaratilmoqda...")

        # Level 1: Elektronika
        cat_elec, _ = Category.objects.get_or_create(name="Elektronika", defaults={'parent': None})
        # Level 2
        cat_phones, _ = Category.objects.get_or_create(name="Telefonlar va Gadjetlar", defaults={'parent': cat_elec})
        cat_laptops, _ = Category.objects.get_or_create(name="Noutbuklar va Kompyuterlar", defaults={'parent': cat_elec})
        # Level 3
        cat_smartphones, _ = Category.objects.get_or_create(name="Smartfonlar", defaults={'parent': cat_phones})
        cat_watches, _ = Category.objects.get_or_create(name="Aqlli soatlar", defaults={'parent': cat_phones})
        cat_gaming_laptops, _ = Category.objects.get_or_create(name="O'yin noutbuklari", defaults={'parent': cat_laptops})

        # Level 1: Kiyim & Aksessuarlar
        cat_cloth, _ = Category.objects.get_or_create(name="Kiyim va Aksessuarlar", defaults={'parent': None})
        # Level 2
        cat_men, _ = Category.objects.get_or_create(name="Erkaklar kiyimi", defaults={'parent': cat_cloth})
        # Level 3
        cat_suits, _ = Category.objects.get_or_create(name="Klassik kostyumlar", defaults={'parent': cat_men})
        cat_sport, _ = Category.objects.get_or_create(name="Sport kiyimlari", defaults={'parent': cat_men})

        # Level 1: Maishiy texnika
        cat_home, _ = Category.objects.get_or_create(name="Maishiy texnika", defaults={'parent': None})
        # Level 2
        cat_kitchen, _ = Category.objects.get_or_create(name="Oshxona jihozlari", defaults={'parent': cat_home})
        # Level 3
        cat_coffee, _ = Category.objects.get_or_create(name="Kofe mashinalari", defaults={'parent': cat_kitchen})

        self.stdout.write(self.style.SUCCESS("[OK] MPTT kategoriyalar daraxti muvaffaqiyatli saqlandi."))

        # 6. Sample Products
        self.stdout.write("[*] Namuna mahsulotlar yaratilmoqda...")

        demo_products = [
            {
                'seller': seller1,
                'category': cat_smartphones,
                'name': "iPhone 15 Pro Max 256GB Titanium",
                'description': "Apple A17 Pro protsessoriga ega titan korpusli eng so'nggi flagman smartfon. Dynamic Island va 48MP professional kamera.",
                'price': Decimal('15500000.00'),
                'discount_price': Decimal('14800000.00'),
                'stock': 12,
            },
            {
                'seller': seller1,
                'category': cat_smartphones,
                'name': "Samsung Galaxy S24 Ultra 512GB Grey",
                'description': "Galaxy AI imkoniyatlari, Snapdragon 8 Gen 3 for Galaxy, titanium rom va o'rnatilgan S-Pen stilus.",
                'price': Decimal('14900000.00'),
                'discount_price': Decimal('13900000.00'),
                'stock': 8,
            },
            {
                'seller': seller1,
                'category': cat_watches,
                'name': "Apple Watch Series 9 GPS 45mm",
                'description': "S9 SiP chipi, Double Tap gesture boshqaruvi va doimiy faol Retina displey. Yurak ritmi monitoringi.",
                'price': Decimal('5200000.00'),
                'discount_price': None,
                'stock': 15,
            },
            {
                'seller': seller1,
                'category': cat_gaming_laptops,
                'name': "ASUS ROG Strix SCAR 16 (i9 / 32GB / RTX 4080)",
                'description': "Professional kibersport noutbuki. 240Hz Mini LED Nebula HDR ekran va suyuq metall sovutish tizimi.",
                'price': Decimal('32000000.00'),
                'discount_price': Decimal('29900000.00'),
                'stock': 4,
            },
            {
                'seller': seller2,
                'category': cat_suits,
                'name': "Premium Erkaklar Klassik Slim Fit Kostyumi",
                'description': "Italiya matosidan tayyorlangan 100% tabiiy jun gazlamali biznes va tantanalar uchun kostyum-shim jamlanmasi.",
                'price': Decimal('2200000.00'),
                'discount_price': Decimal('1850000.00'),
                'stock': 20,
            },
            {
                'seller': seller2,
                'category': cat_sport,
                'name': "Nike Tech Fleece Erkaklar Sport Kostyumi",
                'description': "Yengil va issiqlikni saqlovchi innovatsion Tech Fleece materiali. Kundalik va sport mashg'ulotlari uchun ideal.",
                'price': Decimal('1350000.00'),
                'discount_price': None,
                'stock': 25,
            },
            {
                'seller': seller2,
                'category': cat_coffee,
                'name': "DeLonghi Magnifica S Avtomatik Kofe Mashinasi",
                'description': "Donador qahvani bir zumda yangi maydalab, mukammal espresso va kremsimon kapuchino tayyorlaydi.",
                'price': Decimal('6800000.00'),
                'discount_price': Decimal('6200000.00'),
                'stock': 6,
            }
        ]

        created_prods = []
        for p_data in demo_products:
            prod, p_created = Product.objects.get_or_create(
                seller=p_data['seller'],
                name=p_data['name'],
                defaults={
                    'category': p_data['category'],
                    'description': p_data['description'],
                    'price': p_data['price'],
                    'discount_price': p_data['discount_price'],
                    'stock': p_data['stock'],
                    'main_image': prod_image_rel,
                    'is_active': True,
                }
            )
            created_prods.append(prod)

        self.stdout.write(self.style.SUCCESS(f"[OK] {len(created_prods)} ta mahsulot bazaga kiritildi."))

        # 7. Sample Orders for Dashboard Stats
        if created_prods and not Order.objects.filter(user=buyer1).exists():
            self.stdout.write("[*] Dashboard statistikalari uchun namunaviy buyurtma yaratilmoqda...")
            prod1 = created_prods[0]  # iPhone
            prod2 = created_prods[2]  # Watch

            order = Order.objects.create(
                user=buyer1,
                full_name="Sardor Aliyev",
                phone="+998971112233",
                address="Toshkent shahri, Yunusobod tumani, Amir Temur shoh ko'chasi 45-uy",
                notes="Eshik oldiga kelganda qo'ng'iroq qiling",
                status='tasdiqlangan'
            )

            OrderItem.objects.create(
                order=order,
                product=prod1,
                price=prod1.current_price,
                quantity=1
            )
            OrderItem.objects.create(
                order=order,
                product=prod2,
                price=prod2.current_price,
                quantity=1
            )
            self.stdout.write(self.style.SUCCESS("[OK] Namuna buyurtma yaratildi (ID: #1000)."))

        self.stdout.write(self.style.SUCCESS("\n[SUCCESS] Seed data muvaffaqiyatli yakunlandi! Tizim to'liq tayyor."))
