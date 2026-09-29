from .models import Category


def categories_processor(request):
    try:
        # Barcha faol ota kategoriyalar va ularning avlodlari
        all_categories = Category.objects.filter(is_active=True).prefetch_related('children')
        root_categories = [c for c in all_categories if c.parent_id is None]
    except Exception:
        root_categories = []
        all_categories = []

    return {
        'nav_categories': root_categories,
        'all_active_categories': all_categories,
    }
