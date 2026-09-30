from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def seller_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_seller:
            raise PermissionDenied("Bu sahifaga faqat tasdiqlangan sotuvchilar kira oladi.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
