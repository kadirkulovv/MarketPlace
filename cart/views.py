from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from products.models import Product
from .models import CartItem
from .utils import get_or_create_cart


def cart_detail_view(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product', 'product__seller')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.get_total_price(),
        'total_count': cart.get_total_count(),
    }
    return render(request, 'cart/cart_detail.html', context)


@require_POST
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_or_create_cart(request)
    
    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        quantity = 1

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax'):
                return JsonResponse({
                    'status': 'error',
                    'message': f"Kechirasiz, omborda faqat {product.stock} dona mahsulot mavjud!",
                    'cart_count': cart.get_total_count()
                }, status=400)
            messages.warning(request, f"Kechirasiz, omborda faqat {product.stock} dona mavjud!")
            return redirect('cart:cart_detail')
        cart_item.quantity = new_quantity
        cart_item.save()
    else:
        if quantity > product.stock:
            cart_item.delete()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax'):
                return JsonResponse({
                    'status': 'error',
                    'message': f"Kechirasiz, omborda faqat {product.stock} dona mahsulot mavjud!",
                    'cart_count': cart.get_total_count()
                }, status=400)
            messages.warning(request, f"Kechirasiz, omborda faqat {product.stock} dona mavjud!")
            return redirect('cart:cart_detail')
        cart_item.quantity = quantity
        cart_item.save()

    total_count = cart.get_total_count()
    total_price = cart.get_total_price()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax'):
        return JsonResponse({
            'status': 'success',
            'message': f"{product.name} savatga qo'shildi!",
            'product_name': product.name,
            'cart_count': total_count,
            'cart_total': float(total_price),
            'item_quantity': cart_item.quantity
        })

    messages.success(request, f"{product.name} savatga qo'shildi!")
    return redirect('cart:cart_detail')


@require_POST
def update_cart_item_view(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    action = request.POST.get('action') # 'increase', 'decrease', or 'set'
    if action == 'increase':
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
        else:
            return JsonResponse({
                'status': 'warning',
                'message': f"Omborda boshqa qolmadi (maksimum: {cart_item.product.stock})",
                'item_quantity': cart_item.quantity,
                'item_total': float(cart_item.get_total_price()),
                'cart_total': float(cart.get_total_price()),
                'cart_count': cart.get_total_count(),
            })
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            return JsonResponse({
                'status': 'removed',
                'message': "Mahsulot savatdan olib tashlandi",
                'cart_total': float(cart.get_total_price()),
                'cart_count': cart.get_total_count(),
            })
    elif action == 'set':
        qty = int(request.POST.get('quantity', 1))
        if qty <= 0:
            cart_item.delete()
            return JsonResponse({
                'status': 'removed',
                'message': "Mahsulot savatdan olib tashlandi",
                'cart_total': float(cart.get_total_price()),
                'cart_count': cart.get_total_count(),
            })
        elif qty > cart_item.product.stock:
            cart_item.quantity = cart_item.product.stock
            cart_item.save()
            return JsonResponse({
                'status': 'warning',
                'message': f"Maksimal ombor miqdori belgilandi ({cart_item.product.stock})",
                'item_quantity': cart_item.quantity,
                'item_total': float(cart_item.get_total_price()),
                'cart_total': float(cart.get_total_price()),
                'cart_count': cart.get_total_count(),
            })
        else:
            cart_item.quantity = qty
            cart_item.save()

    return JsonResponse({
        'status': 'success',
        'message': 'Savat yangilandi',
        'item_quantity': cart_item.quantity,
        'item_total': float(cart_item.get_total_price()),
        'cart_total': float(cart.get_total_price()),
        'cart_count': cart.get_total_count(),
    })


@require_POST
def remove_from_cart_view(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax'):
        return JsonResponse({
            'status': 'success',
            'message': f"{product_name} savatdan o'chirildi",
            'cart_total': float(cart.get_total_price()),
            'cart_count': cart.get_total_count(),
        })

    messages.info(request, f"{product_name} savatdan o'chirildi.")
    return redirect('cart:cart_detail')
