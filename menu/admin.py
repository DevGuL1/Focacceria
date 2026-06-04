from django.contrib import admin
from .models import MenuCategory, MenuItem, AddOn

admin.site.register(MenuCategory)
admin.site.register(MenuItem)
admin.site.register(AddOn)
