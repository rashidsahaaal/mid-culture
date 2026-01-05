from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Home Page with Category Filter
def home(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    return render(request, 'home.html', {
        'categories': categories,
        'products': products,
        'selected_category': int(category_id) if category_id else None
    })




# Add Product to Cart
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart = request.session.get('cart', {})
    cart[str(product.id)] = cart.get(str(product.id), 0) + 1
    request.session['cart'] = cart
    return redirect('store:cart')  # ✅ use namespaced URL here


# Cart Page
@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    total = 0
    for p in products:
        qty = cart.get(str(p.id), 0)
        total += p.price * qty

    return render(request, 'cart.html', {
        'products': products,
        'cart': cart,
        'total': total,
    })


# Increase Quantity
def increase_qty(request, id):
    cart = request.session.get('cart', {})
    cart[str(id)] = cart.get(str(id), 0) + 1
    request.session['cart'] = cart
    return redirect('store:cart')


# Decrease Quantity
def decrease_qty(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        if cart[str(id)] > 1:
            cart[str(id)] -= 1
        else:
            del cart[str(id)]
    request.session['cart'] = cart
    return redirect('store:cart')


# Remove Item
def remove_item(request, id):
    cart = request.session.get('cart', {})
    cart.pop(str(id), None)
    request.session['cart'] = cart
    return redirect('store:cart')


# ------------------ Signup ------------------
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        else:
            User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, "Account created successfully!")
            return redirect(request, 'store:login')

    return render(request, 'signup.html')


# ------------------ Login ------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('store:home')
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, 'login.html')  # ✅ FIXED


# ------------------ Logout ------------------
def logout_view(request):
    logout(request)
    return redirect('store:login')
