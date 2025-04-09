from django.shortcuts import render,  redirect
from .models import Slider, Category, Product, Cart, Contact, Color, Size, Info
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.filters import SearchFilter,OrderingFilter
from django.db.models import Q
from django.contrib.auth.models import User 

def get_items_count_in_cart(user=None):
    count_sum = 0
    price_sum = 0
    if user and user.is_authenticated:
        cart_items = Cart.objects.filter(user=user)
    else:
        cart_items = Cart.objects.none()  
    
    for item in cart_items:
        count_sum += item.count
        price_sum += item.total_price
    return [count_sum, price_sum]


def index(request):

    info = Info.objects.first()
    slider_active = Slider.objects.first()
    slider = Slider.objects.all()[1:]
    category_list = Category.objects.all()
    cart_list = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    cart_list_count = get_items_count_in_cart(request.user)[0]
    product_list = Product.objects.all()

    paginator = Paginator(product_list, 6)
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number) 
    
    return render(request, 'index.html', context={
        'nav_item': 'index',
        'slider_active': slider_active,
        'slider': slider,
        'category_list': category_list,
        'cart_list_count':cart_list_count,
        'product_list': product_list,
        'product_list': page_obj, 
        'cart_list': cart_list,
        'info': info

    })


def cart(request):
    info = Info.objects.first()
    category_list = Category.objects.all()
    cart_list = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    
    cart_list_count = get_items_count_in_cart(request.user)[0]
    cart_list_price_sum = get_items_count_in_cart(request.user)[1]

    shipping_price = 10  
    full_price = cart_list_price_sum + shipping_price  
    
    return render(request, 'cart.html', context={
        'nav_item': 'cart',
        'category_list': category_list,
        'cart_list_count': cart_list_count,
        'cart_list': cart_list,
        'cart_list_price_sum': cart_list_price_sum,
        'info': info,
        'shipping_price': shipping_price,
        'full_price': full_price
    })



def checkout(request):

    info = Info.objects.first()
    category_list = Category.objects.all()
    cart_list = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    cart_list_count = get_items_count_in_cart(request.user)[0]

    return render(request, 'checkout.html', context={
        'nav_item': 'checkout',
        'category_list': category_list,
        'cart_list_count':cart_list_count,
        'cart_list': cart_list,
        'info': info

    })


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email, text=message)
        return redirect('contact')

    info = Info.objects.first()
    category_list = Category.objects.all()
    cart_list = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    cart_list_count = get_items_count_in_cart(request.user)[0]

    return render(request, 'contact.html', context={
        'nav_item': 'contact',
        'category_list': category_list,
        'cart_list_count':cart_list_count,
        'cart_list': cart_list,
        'info': info

    })


def shop_filter(request, id):

    info = Info.objects.first()
    category_list = Category.objects.all()
    cart_list = Cart.objects.all()
    cart_list = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    cart_list_count = get_items_count_in_cart(request.user)[0]
    product_list = Product.objects.filter(category_id=id)


    return render(request, 'shop.html', context={
        'category_list': category_list,
        'product_list': product_list,
        'cart_list_count':cart_list_count,
        'cart_list': cart_list,
        'info': info

    })

def detail(request, id):

    info = Info.objects.first()
    category_list = Category.objects.all()
    product = Product.objects.get(pk=id)
    cart_list = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    cart_list_count = get_items_count_in_cart(request.user)[0]


    return render(request, 'detail.html', context={
        'nav_item': 'detail',
        'category_list': category_list,
        'product': product,
        'cart_list_count':cart_list_count,
        'cart_list': cart_list,
        'info': info

    })


def shop(request):
    category_filter = request.GET.get('category', None)
    color_filter = request.GET.getlist('color', [])
    size_filter = request.GET.getlist('size', [])
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    search_term = request.GET.get('search', '')
    
    color_list = Color.objects.all()
    size_list = Size.objects.all()
    category_list = Category.objects.all()
    info = Info.objects.first()
    cart_list = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    cart_list_count = get_items_count_in_cart(request.user)[0]
    product_list = Product.objects.all()
    
    if search_term:
        product_list = product_list.filter(
            Q(name__icontains=search_term) |
            Q(description__icontains=search_term) | 
            Q(name_en__icontains=search_term) | 
            Q(name_hy__icontains=search_term) |
            Q(name_ru__icontains=search_term) |
            Q(description_en__icontains=search_term) |
            Q(description_hy__icontains=search_term) |
            Q(description_ru__icontains=search_term)
        )
    
    if category_filter:
        product_list = product_list.filter(category_id=category_filter)
    
    if color_filter:
        product_list = product_list.filter(color__in=color_filter)
    
    if size_filter:
        product_list = product_list.filter(size__in=size_filter)
    
    if min_price:
        product_list = product_list.filter(price__gte=min_price)
    if max_price:
        product_list = product_list.filter(price__lte=max_price)
    
    paginator = Paginator(product_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'shop.html', {
        'nav_item': 'shop',
        'category_list': category_list,
        'product_list': page_obj,
        'cart_list_count': cart_list_count,
        'cart_list': cart_list,
        'info': info,
        'size_list': size_list,
        'color_list': color_list,
    })


def register_request(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if user already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "User already exists!")
            return redirect("register")

        # Create new user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()

        
        login(request, user)

        return redirect("index")  

    return render(request, "login_register.html")

def login_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")  
        else:
            messages.error(request, "Invalid credentials!")
            return redirect("login_register.html")

    return render(request, "login_register.html")


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out")
    return redirect("index")  


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        prod = Product.objects.get(id=product_id)

        if not request.user.is_authenticated:
            return redirect('login') 
        one_user = request.user  

        cart_item = Cart.objects.filter(product=prod, user=one_user).first()

        if cart_item:
            cart_item.count += 1
            cart_item.total_price = cart_item.product.discount * cart_item.count
            cart_item.save()
        else:
            Cart.objects.create(product=prod, user=one_user, count=1, total_price=prod.discount)

        return redirect('shop')



def delete_from_cart(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        Cart.objects.filter(id=cart_id).delete()
        return redirect('cart')


@csrf_exempt
def add_product_count(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        cart_object = Cart.objects.get(id=cart_id)
        cart_object.count += 1
        cart_object.total_price = cart_object.product.discount * cart_object.count
        cart_object.save()
        return redirect('cart')


@csrf_exempt
def subtract_product_count(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        cart_object = Cart.objects.get(id=cart_id)
        cart_object.count -= 1
        cart_object.total_price = cart_object.product.discount * cart_object.count
        cart_object.save()
        return redirect('cart')


