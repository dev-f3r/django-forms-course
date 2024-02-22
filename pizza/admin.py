from django.contrib import admin
from .models import Size, Pizza

admin.site.register(Pizza)
admin.site.register(Size)