
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'email', 'city', 'address', 'created', 'updated']
    list_filter = ['created', 'updated']
    inlines = [OrderItemInLine]
