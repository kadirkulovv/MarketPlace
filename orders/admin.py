from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Order, OrderItem


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        fields = ('id', 'user__username', 'full_name', 'phone', 'address', 'status', 'created_at', 'updated_at')
        export_order = ('id', 'user__username', 'full_name', 'phone', 'address', 'status', 'created_at', 'updated_at')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity', 'get_cost')
    can_delete = False

    def get_cost(self, obj):
        return f"{obj.get_cost():,.0f} so'm"
    get_cost.short_description = "Jami narx"


@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    resource_class = OrderResource
    list_display = ('id', 'full_name', 'phone', 'user', 'status', 'total_items_display', 'total_cost_display', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'full_name', 'phone', 'address', 'user__username')
    inlines = [OrderItemInline]
    ordering = ('-created_at',)
    list_per_page = 20

    def total_cost_display(self, obj):
        return f"{obj.total_cost:,.0f} so'm"
    total_cost_display.short_description = "Jami summa"

    def total_items_display(self, obj):
        return f"{obj.total_items_count} dona"
    total_items_display.short_description = "Mahsulotlar"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'price', 'quantity', 'get_cost')
    list_filter = ('order__status', 'created_at' if hasattr(OrderItem, 'created_at') else 'order__created_at')
    search_fields = ('product__name', 'order__id', 'order__full_name')
