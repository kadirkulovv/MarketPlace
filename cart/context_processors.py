from .utils import get_or_create_cart


def cart_processor(request):
    try:
        cart = get_or_create_cart(request)
        cart_total_count = cart.get_total_count()
        cart_total_price = cart.get_total_price()
    except Exception:
        cart_total_count = 0
        cart_total_price = 0

    return {
        'nav_cart_count': cart_total_count,
        'nav_cart_total': cart_total_price,
    }
