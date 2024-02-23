from django.contrib import admin
from .models import Size, Pizza

class PizzaAdmin(admin.ModelAdmin):
    list_display = ("topping1", "topping2", "size", "pk")

admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Size)