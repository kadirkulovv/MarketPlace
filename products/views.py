from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Category, Product
from .filters import ProductFilter


def home_view(request):
    products = Product.objects.filter(is_active=True).select_related('category', 'seller')
    
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'popular':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('-created_at')

    product_filter = ProductFilter(request.GET, queryset=products)
    filtered_qs = product_filter.qs

    paginator = Paginator(filtered_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    root_categories = Category.objects.filter(is_active=True, parent__isnull=True).prefetch_related('children')
    featured_categories = Category.objects.filter(is_active=True)[:6]

    context = {
        'page_obj': page_obj,
        'filter': product_filter,
        'root_categories': root_categories,
        'featured_categories': featured_categories,
        'current_sort': sort,
        'total_count': filtered_qs.count(),
    }
    return render(request, 'products/home.html', context)


def category_products_view(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    categories = category.get_descendants(include_self=True)
    products = Product.objects.filter(category__in=categories, is_active=True).select_related('category', 'seller')

    sort = request.GET.get('sort', 'newest')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')

    product_filter = ProductFilter(request.GET, queryset=products)
    filtered_qs = product_filter.qs

    paginator = Paginator(filtered_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
        'filter': product_filter,
        'current_sort': sort,
        'total_count': filtered_qs.count(),
    }
    return render(request, 'products/category_products.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category', 'seller').prefetch_related('images'),
        slug=slug,
        is_active=True
    )
    related_categories = product.category.get_descendants(include_self=True)
    related_products = Product.objects.filter(
        category__in=related_categories,
        is_active=True
    ).exclude(pk=product.pk)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)
