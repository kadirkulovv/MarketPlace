from django.db import models
from django.conf import settings
from products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='cart',
        verbose_name="Foydalanuvchi"
    )
    session_key = models.CharField(max_length=100, null=True, blank=True, verbose_name="Sessiya kaliti")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Savatcha"
        verbose_name_plural = "Savatchalar"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_count(self):
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        if self.user:
            return f"Savat ({self.user.username})"
        return f"Savat ({self.session_key})"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Savatcha"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name="Mahsulot"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Miqdori")

    class Meta:
        verbose_name = "Savatchadagi mahsulot"
        verbose_name_plural = "Savatchadagi mahsulotlar"
        unique_together = ('cart', 'product')

    def get_total_price(self):
        price = self.product.current_price
        return price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
