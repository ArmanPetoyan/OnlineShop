from django.db import models
from django.contrib.auth.models import User 


class Slider(models.Model):
    text1 = models.CharField('Slider text1', max_length=100)
    text2 = models.CharField('Slider text2', max_length=100)
    img = models.ImageField('Slider image', upload_to='slider')

    def __str__(self):
        return f'Slider N{self.id}'

class Category(models.Model):
    name = models.CharField('Category name', max_length=60)

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField('Size name', max_length=10)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cat_prod')
    image = models.ImageField('Product image', upload_to='products')
    name = models.CharField('Product name', max_length=100)
    color = models.ManyToManyField(Color) 
    size = models.ManyToManyField(Size)
    price = models.PositiveIntegerField('Product price')
    discount = models.PositiveIntegerField('Product discount')
    description = models.TextField()

    def __str__(self):
        return self.name

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField('Cart product count', default=1)
    total_price = models.PositiveIntegerField('Cart total_price')

    def __str__(self):
        return f'Cart product N{self.id}'


class Info(models.Model):
    text = models.TextField('Info text')
    address = models.TextField(max_length=60)
    phone = models.CharField(max_length=60)
    email = models.EmailField()

    def __str__(self):
        return self.address
    

class Contact(models.Model):
    name = models.CharField('Contact name', max_length=60)
    email = models.EmailField('Contact email')
    text = models.TextField('Contact text')

    def __str__(self):
        return f'{self.name} - {self.email}'
