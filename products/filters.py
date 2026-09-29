import django_filters
from django import forms
from .models import Product, Category


class ProductFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Qidirish',
        widget=forms.TextInput(attrs={
            'placeholder': 'Mahsulot nomi bo\'yicha qidiring...',
            'class': 'filter-input'
        })
    )
    min_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Min narx',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Min so\'m',
            'class': 'filter-input'
        })
    )
    max_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Maks narx',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Maks so\'m',
            'class': 'filter-input'
        })
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.filter(is_active=True),
        label='Kategoriya',
        empty_label='Barcha kategoriyalar',
        widget=forms.Select(attrs={'class': 'filter-select'})
    )
    in_stock = django_filters.BooleanFilter(
        field_name='stock',
        method='filter_in_stock',
        label='Faqat omborda borlar',
        widget=forms.CheckboxInput(attrs={'class': 'filter-checkbox'})
    )

    class Meta:
        model = Product
        fields = ['q', 'category', 'min_price', 'max_price', 'in_stock']

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset
