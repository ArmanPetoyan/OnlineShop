from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Product, Color, Category, Size, Cart, Contact

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('name', 'get_colors', 'price', 'discount')

    def get_colors(self, obj):
        """Display colors as a comma-separated string."""
        return ", ".join([color.name for color in obj.color.all()])

    get_colors.short_description = 'Colors'

admin.site.register(Color)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Cart)
admin.site.register(Contact)