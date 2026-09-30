from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from cart.utils import get_or_create_cart
from .models import Order, OrderItem
from .forms import OrderCreateForm


@login_required
def checkout_view(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product')

    if not cart_items.exists():
        messages.warning(request, "Savat bo'sh! Buyurtma berish uchun mahsulot tanlang.")
        return redirect('products:home')

    for item in cart_items:
        if item.quantity > item.product.stock:
            messages.error(
                request,
                f"Kechirasiz, '{item.product.name}' mahsulotidan omborda faqat {item.product.stock} dona qolgan."
            )
            return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.save()

                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        price=item.product.current_price,
                        quantity=item.quantity
                    )
                    item.product.stock -= item.quantity
                    item.product.save(update_fields=['stock'])

                cart_items.delete()

            messages.success(request, f"Rahmat! Sizning #{order.id} raqamli buyurtmangiz muvaffaqiyatli qabul qilindi.")
            return redirect('orders:order_success', order_id=order.id)
    else:
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'phone': request.user.phone,
            'address': request.user.address,
        }
        form = OrderCreateForm(initial=initial_data)

    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.get_total_price(),
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related('items__product__seller'),
        id=order_id,
        user=request.user
    )
    return render(request, 'orders/order_detail.html', {'order': order})
