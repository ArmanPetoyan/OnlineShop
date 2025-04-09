from modeltranslation.translator import register, TranslationOptions
from .models import Product, Color

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Color)
class ColorTranslationOptions(TranslationOptions):
    fields = ('name',) 