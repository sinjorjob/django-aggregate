from django.contrib import admin

from .models import Category, Product, User, OrderItem, OrderItemDetail

class ProductAdmin(admin.ModelAdmin):
    list_display=('pk','name','price', 'category')

class CategoryAdmin(admin.ModelAdmin):
    list_display=('pk','name')

class InvoiceDetailInline(admin.TabularInline):
    model = OrderItemDetail
    extra = 0

class OrderItemDetailAdmin(admin.ModelAdmin):
    list_display=('pk','created_date', 'invoice', 'product', 'quantity','category_name')

    def category_name(self, obj):
        return obj.product.category
    category_name.short_description = 'カテゴリ名'
    category_name.admin_order_field = 'product__category' 

class OrderItemAdmin(admin.ModelAdmin):
    list_display=('pk', 'user','created_date', 'price')
    inlines = [InvoiceDetailInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderItemDetail, OrderItemDetailAdmin)