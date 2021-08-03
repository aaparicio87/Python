from django.contrib import admin
from .models import Category, Product, Recharge, Contacto

# Register your models here.

admin.site.register([Category, Product, Contacto ])

@admin.register(Recharge)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'cellphone', 'nauta', 'paid','created', 'updated']
    list_filter = ['paid', 'created', 'updated']
