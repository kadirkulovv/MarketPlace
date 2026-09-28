# 🛒 MarketPlace — Zamonaviy Ko'p Sotuvchili E-Commerce Platformasi

Ushbu loyiha texnik topshiriq (TZ) asosida ishlab chiqilgan bo'lib, **Django**, **django-mptt** (cheksiz daraxtsimon kategoriyalar), **django-jazzmin** (zamonaviy admin paneli), **django-filter**, **django-import-export** va to'liq interaktiv **JavaScript & animatsiyalar** (AJAX savatcha, ombor qoldig'ini bir zumda tahrirlash, toast xabarlar, status timeline) bilan boyitilgan to'liq ishlaydigan elektron tijorat platformasidir.

---

## 🌟 Asosiy Imkoniyatlar va Funksiyalar

1. **Foydalanuvchilar Tizimi (Rolli model):**
   - **Xaridor (Buyer):** Mahsulotlarni ko'radi, qidiradi, filtrlaydi, savatga qo'shadi, buyurtma beradi va shaxsiy kabinetida o'z buyurtmalari tarixini hamda holatini (progress timeline) kuzatadi.
   - **Sotuvchi (Seller):** Ro'yxatdan o'tishda o'z do'koni nomini kiritadi. Shaxsiy "Sotuvchi kabineti" (Dashboard) orqali faqat o'ziga tegishli mahsulotlarni boshqaradi (CRUD), mahsulot qoldig'ini (stock) sahifadan chiqmasdan AJAX orqali o'zgartiradi, har bir tovar bo'yicha qancha sotilganini va umumiy tushum statistikasini ko'radi.
   - **Administrator (Staff / Superuser):** `django-jazzmin` asosidagi qulay admin paneli orqali barcha mahsulotlar, kategoriyalar daraxti, buyurtmalar va foydalanuvchilarni boshqaradi, Excel/CSV formatida eksport/import qiladi.

2. **Daraxtsimon Kategoriyalar (MPTT):**
   - Cheksiz chuqurlikdagi ota-bola-nabira kategoriyalar tuzilishi (masalan: *Elektronika ➔ Telefonlar va gadjetlar ➔ Smartfonlar*).
   - Kategoriya tanlanganda uning o'zi va barcha quyi (ichki) bo'limlaridagi mahsulotlar avtomatik yig'ilib ko'rsatiladi (`get_descendants(include_self=True)`).
   - Sayt yuqorisidagi navigatsiya menyusida ichma-ich chiroyli ochiluvchi daraxt menyusi.

3. **Savatcha va Buyurtmalar (Interaktiv JS):**
   - **AJAX Add to Cart:** Mahsulotni sahifani qayta yuklamasdan savatga qo'shish, savatcha indikatorining dinamik yangilanishi va animatsiyali Toast xabarlar.
   - **Savatcha sahifasi:** Miqdorni oshirish/kamaytirish (+/-) tugmalari va to'g'ridan-to'g'ri umumiy narx hisob-kitobi.
   - **Buyurtma rasmiylashtirish:** Ism, telefon, manzil va kuryer uchun izoh kiritiladi. Buyurtma tasdiqlangach, mahsulot ombor qoldig'i (stock) avtomatik kamaytiriladi va savat tozalanadi.
   - **Buyurtma holatlari:** `yangi` ➔ `tasdiqlangan` ➔ `yetkazilmoqda` ➔ `yakunlangan` (yoki `bekor qilingan`) vizual timeline ko'rinishida kuzatiladi.

4. **Sotuvchi Kabineti (Dashboard):**
   - Jami mahsulotlar soni, jami sotilgan mahsulot donasi soni, jami tushum (summa) va eng ko'p sotilgan mahsulot statistikasi.
   - Har bir mahsulot bo'yicha sotilgan donalar soni (`Sum(OrderItem.quantity)`).
   - Ombordagi qoldiqni ro'yxatdan turib `[+]` va `[-]` tugmalari orqali sahifani yangilamasdan (AJAX) o'zgartirish.
   - Sotuvchiga kelib tushgan buyurtmalar alohida jadvalda aks etadi.

5. **Admin Panel (django-jazzmin & import-export):**
   - Chiroyli va zamonaviy Jazzmin interfeysi.
   - Kategoriyalar daraxti drag-and-drop / indent boshqaruvi.
   - Mahsulotlar ro'yxatidan turib narx va qoldiqni tezkor tahrirlash (`list_editable`).
   - Mahsulot ichida galereya rasmlari (Inline).
   - Buyurtmalar ichida mahsulotlar jadvali va statusni to'g'ridan-to'g'ri o'zgartirish.
   - Excel va CSV formatida import/eksport qilish imkoniyati.

---

## 🚀 O'rnatish va Ishga Tushirish Qadamlari

### 1. Repozitoriyni klonlash va loyiha papkasiga o'tish
```bash
git clone <repo-url>
cd TZ
```

### 2. Virtual muhit (venv) yaratish va faollashtirish
**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. Muhit o'zgaruvchilari (.env)
Loyihada maxfiy kalitlar kod ichida emas, `.env` faylida saqlanadi. 
`.env.example` dan nusxa olib `.env` yaratilganligiga ishonch hosil qiling:
```env
SECRET_KEY=django-insecure-m@rketpl@ce_super_secret_key_2026_x!98#kzq01
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Ma'lumotlar bazasi migratsiyalarini bajarish
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Boshlang'ich ma'lumotlarni yuklash (Seed Data)
Loyihada tayyor kategoriyalar daraxti (3 darajali), test sotuvchilar, xaridorlar, rasmli mahsulotlar va buyurtmalarni yaratish uchun maxsus komandadan foydalaning:
```bash
python manage.py seed_data
```

### 7. Loyihani ishga tushirish
```bash
python manage.py runserver
```

Brauzerda oching:
- **Sayt vitrinasi (Bosh sahifa):** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Sotuvchi kabineti:** [http://127.0.0.1:8000/seller-dashboard/](http://127.0.0.1:8000/seller-dashboard/)
- **Admin panel (Jazzmin):** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 👥 Tayyor Sinov Foydalanuvchilari (Demo Accounts)

| Rol | Login (username) | Parol | Tavsif |
| :--- | :--- | :--- | :--- |
| **Bosh Admin** | `admin` | `admin123` | Barcha huquqlarga ega superuser, Jazzmin admin panel |
| **Sotuvchi 1** | `seller1` | `seller123` | "TechZone Official" do'koni egasi (gadjet va noutbuklar) |
| **Sotuvchi 2** | `seller2` | `seller123` | "Moda & Stil Butigi" do'koni egasi (maishiy va kiyimlar) |
| **Xaridor 1** | `buyer1` | `buyer123` | Xaridor, tayyor buyurtmalar tarixi bilan |
| **Xaridor 2** | `buyer2` | `buyer123` | Xaridor, yangi buyurtmalar berish uchun |

---

## 🧪 Avtomatlashtirilgan Testlarni Ishga Tushirish

Loyiha arxitekturasi va biznes logikasi to'liq testlar bilan qoplangan:
```bash
python manage.py test
```
*Testlar MPTT daraxti, chegirma hisoblash, AJAX savatcha logikasi, sotuvchi mahsulotlarining izolyatsiyasi va checkout vaqtida ombor qoldig'i kamayishini tekshiradi.*

---

## 📁 Loyiha Strukturasi

```text
├── accounts/               # Foydalanuvchilar (Custom User, role: seller/buyer, shop_name)
├── products/               # MPTT Kategoriyalar, Mahsulotlar, Rasmlar, django-filter
├── cart/                   # Savatcha, CartItem va AJAX bilan ishlash logikasi
├── orders/                 # Buyurtma berish, OrderItem va statuslar monitoringi
├── dashboard/              # Sotuvchi kabineti, tezkor stock tahrirlash, tushum statistikasi
├── config/                 # Django asosiy sozlamalari (settings.py, urls.py, wsgi.py)
├── static/
│   ├── css/main.css        # Zamonaviy dizayn tizimi, animatsiyalar, responsivlik
│   └── js/main.js          # AJAX savat, stock yangilash, toastlar, interaktiv menyu
├── templates/              # HTML shablonlar (Bosh sahifa, kabinet, savat, buyurtma)
├── requirements.txt        # Loyiha kutubxonalari
├── .env.example            # Muhit sozlamalari namunasi
└── manage.py
```
