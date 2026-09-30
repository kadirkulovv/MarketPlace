from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ('yangi', 'Yangi'),
        ('tasdiqlangan', 'Tasdiqlangan'),
        ('yetkazilmoqda', 'Yetkazilmoqda'),
        ('yakunlangan', 'Yakunlangan'),
        ('bekor qilingan', 'Bekor qilingan'),
    )

    STATUS_BADGES = {
        'yangi': 'badge-primary',
        'tasdiqlangan': 'badge-info',
        'yetkazilmoqda': 'badge-warning',
        'yakunlangan': 'badge-success',
        'bekor qilingan': 'badge-danger',
    }

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Buyurtmachi"
    )
    full_name = models.CharField(max_length=200, verbose_name="To'liq ism-familiya")
    phone = models.CharField(max_length=20, verbose_name="Telefon raqami")
    address = models.TextField(verbose_name="Yetkazib berish manzili")
    notes = models.TextField(blank=True, verbose_name="Qo'shimcha izoh")
    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default='yangi',
        verbose_name="Buyurtma holati"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created_at']

    @property
    def total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    @property
    def total_items_count(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def status_badge_class(self):
        return self.STATUS_BADGES.get(self.status, 'badge-secondary')

    def __str__(self):
        return f"Buyurtma #{self.id} - {self.full_name} ({self.get_status_display()})"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Buyurtma"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name="Mahsulot"
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Sotib olingan narx (so'm)"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Miqdori")

    class Meta:
        verbose_name = "Buyurtma mahsuloti"
        verbose_name_plural = "Buyurtma mahsulotlari"

    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
