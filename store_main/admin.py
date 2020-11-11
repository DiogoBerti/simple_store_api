from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Client)
admin.site.register(models.Product)
admin.site.register(models.SaleOrder)
admin.site.register(models.SaleOrderLine)