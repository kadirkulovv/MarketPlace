from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, F
from django.http import JsonResponse
from products.models import Product
from orders.models import OrderItem
from .mixins import seller_required
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy


class SellerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_seller

@seller_required
def seller_update_stock_view(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        stock = request.POST.get('stock')
        if stock is not None:
            product.stock = max(0, int(stock))
            product.save(update_fields=['stock'])
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'stock': product.stock})
            messages.success(request, f"'{product.name}' qoldig'i yangilandi: {product.stock}")
    return redirect('dashboard:seller_products')

@seller_required
def seller_orders_view(request):
    order_items = OrderItem.objects.filter(
        product__seller=request.user
    ).select_related('order', 'product', 'order__user').order_by('-order__created_at')
    return render(request, 'dashboard/orders_list.html', {'order_items': order_items})


@seller_required
def seller_dashboard_view(request):
    my_products = Product.objects.filter(seller=request.user)
    seller_items = OrderItem.objects.filter(product__seller=request.user)

    total_sold = seller_items.aggregate(total=Sum('quantity'))['total'] or 0
    total_revenue = seller_items.aggregate(
        revenue=Sum(F('price') * F('quantity'))
    )['revenue'] or 0

    top_product = my_products.annotate(sold=Sum('order_items__quantity')).order_by('-sold').first()

    recent_orders = seller_items.select_related('order', 'product').order_by('-order__created_at')[:5]

    context = {
        'total_products': my_products.count(),
        'total_sold': total_sold,
        'total_revenue': total_revenue,
        'top_product': top_product,
        'recent_orders': recent_orders,
    }
    return render(request, 'dashboard/seller_dashboard.html', context)

class ProductCreateView(SellerRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'dashboard/product_form.html'
    success_url = reverse_lazy('dashboard:seller_products')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        messages.success(self.request, f"'{form.instance.name}' mahsuloti muvaffaqiyatli qo'shildi!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Yangi mahsulot qo'shish"
        context['active_menu'] = 'add_product'
        return context
    
    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)


class ProductDeleteView(SellerRequiredMixin, DeleteView):
    model = Product
    template_name = 'dashboard/product_confirm_delete.html'
    success_url = reverse_lazy('dashboard:seller_products')
    success_message = "Mahsulot muvaffaqiyatli o'chirildi!"

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, self.success_message)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Mahsulotni o'chirish"
        return context
    
    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)


class ProductUpdateView(SellerRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm 
    template_name = 'dashboard/product_form.html'
    success_url = reverse_lazy('dashboard:seller_products')
    success_message = "Mahsulot muvaffaqiyatli yangilandi!"

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Mahsulotni tahrirlash"
        context['active_menu'] = 'add_product'
        return context
    
    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)



class ProductListView(SellerRequiredMixin, ListView):
    model = Product
    template_name = 'dashboard/products_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)
