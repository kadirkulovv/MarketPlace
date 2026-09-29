from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Category, Product, ProductImage


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'category__name', 'seller__username', 'price', 'discount_price', 'stock', 'is_active', 'created_at')
        export_order = ('id', 'name', 'slug', 'category__name', 'seller__username', 'price', 'discount_price', 'stock', 'is_active', 'created_at')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ('image', 'alt_text')


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug', 'is_active')
    list_display_links = ('indented_title',)
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ('name', 'seller', 'category', 'price', 'discount_price', 'stock', 'is_active', 'created_at')
    list_editable = ('price', 'discount_price', 'stock', 'is_active')
    list_filter = ('seller', 'category', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'seller__username', 'seller__shop_name')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    ordering = ('-created_at',)
    list_per_page = 20


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image', 'alt_text')
    list_filter = ('product',)
