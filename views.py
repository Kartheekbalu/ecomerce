from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, WishItem
from django.core.paginator import Paginator

# Create your views here.

#Home page
def home(request):
    return render(request,'home.html')

#Authentication Pages
def login(request):
    if request.method=='POST':
        user_name=request.POST['username']
        pasw=request.POST['password']
        user=auth.authenticate(username=user_name,password=pasw)
        
        if user is not None:
            auth.login(request,user)
            mess=messages.info(request,'Login Successful!')
            return render(request,'user.html')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('login')
    else:
        return render(request,'login.html')

def register(request):
    if request.method=='POST':
        name=request.POST['username']
        pass1=request.POST['password1']
        pass2=request.POST['password2']
        email=request.POST['email']
        if pass1==pass2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already exist')
                return redirect('register')
            elif User.objects.filter(username=name).exists():
                messages.error(request, 'Username is already taken')
                return redirect('register')
            else:
                user=User.objects.create_user(username=name, email=email, password=pass1)
                user.save()
                #mess=messages.info(request,'Registration successful')
                return redirect('login')
        else:
            messages.info(request,'Password not same')
            return redirect('register')
    return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def user(request):
    items=Product.objects.all()
    p=Paginator(items,6)
    page=request.GET.get('page')
    item=p.get_page(page)
    name=request.user.username
    return render(request,'user.html',{'items':item,'name':name})

#product show

#Orders, Cart, Wishlist

from django.http import JsonResponse

def add_to_cart(request, product_id):
    try:
        # Get the product with the given ID
        product = Product.objects.get(pk=product_id)
        #global user_name
        if CartItem.objects.filter(name=product.name).exists():
            return JsonResponse({'success': False})
        # Create a new cart item
        else:
            cart_item = CartItem.objects.create(
            name=product.name,
            description=product.description,
            price=product.price,
            username = request.user
            )
            # Return a success JSON response
            return JsonResponse({'success': True})
    
    except Product.DoesNotExist:
        # Return a failure JSON response if the product doesn't exist
        return JsonResponse({'success': False, 'error': 'Product not found'})

def cart(request):
    user=CartItem.objects.all()
    return render(request,'cart.html',{'products':user})

def remove_cart(request, product_id):
    try:
        user = CartItem.objects.get(pk=product_id)
        user.delete()
        return JsonResponse({'success':True})
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found'})


def add_to_wish(request, product_id):
    try:
        # Get the product with the given ID
        product = Product.objects.get(pk=product_id)
        #global user_name
        if WishItem.objects.filter(name=product.name).exists():
            return JsonResponse({'success': False})
        # Create a new cart item
        else:
            wish_item = WishItem.objects.create(
            user=request.user,
            name=product.name,
            description=product.description,
            price=product.price,
            )
            wish_item.save()
            # Return a success JSON response
            return JsonResponse({'success': True})
    
    except Product.DoesNotExist:
        # Return a failure JSON response if the product doesn't exist
        return JsonResponse({'success': False, 'error': 'Product not found'})

def wishlist(request):
    userdetail= WishItem.objects.filter(user=request.user)
    return render(request,'wishlist.html',{'products':userdetail})

def remove_wish(request, product_id):
    try:
        user = WishItem.objects.get(pk=product_id)
        user.delete()
        return JsonResponse({'success':True})
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found'})

def orders(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.price for item in cart_items)
    return render(request, 'orders.html', {'pk': cart_items, 'amt': total_price})

def search(request):
    query=request.GET['q']
    data=Product.objects.filter(name__icontains=query)
    items=Product.objects.all()
    return render(request,'user.html',{'results':data,'items':items})