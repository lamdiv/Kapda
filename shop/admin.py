from django.contrib import admin
from .models import Category,Type,Brand,Color,Material,Product,Size



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Type)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Material)
admin.site.register(Size)


    