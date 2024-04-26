from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Q
from django.contrib import messages
from .forms import UserRegisterForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Product,Brand,UsageFor,Cart,CartItem
from .forms import ProductForm
from django.contrib.auth import authenticate, login,logout

from django.core.mail import send_mail
from django.conf import settings

from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db import IntegrityError

import logging

logger = logging.getLogger(__name__)

# Create your views here.

def home_page(request):
    return render(request,'home.html')

def about_page(request):
    return render(request,'about.html')


def register_request(request):
    if request.user.is_authenticated:
        return redirect("home_page") 

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # print("username::::::::::::::::::::",form['username'].value)
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            username1 = email.split('@')[0]

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered.")
                return redirect('register')

            # Check if username already exists
            if User.objects.filter(username=username1).exists():
                messages.error(request, "Username is already taken.")
                return redirect('register')

            # Compare passwords
            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return redirect('register')
            
            # All validations passed, save the user
            user = User.objects.create_user(username=username1, email=email, password=password1,first_name = first_name,last_name = last_name)
            user.save()

            #Send Email to customer on new login
            send_mail(
                'Welcome to E-commerce website',
                "Hello {}! \n your account has been successully created ".format(first_name),
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )
                

            username = user.username
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('loginUser')
        
        # else:
        #     # Form is not valid, render the registration template with form errors
        #     messages.error(request, "Invalid registration form. Please check the errors below.")
        return render(request, 'signupform.html', {'form': form})

    else:
        form = UserRegisterForm()
    return render(request, 'signupform.html', {'form': form})


def loginUser(request):
    if request.user.is_authenticated:
        return redirect("home_page") 

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        username = email.split('@')[0]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"Username doesn't exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("user logged in ::::::::::::::::::::::::::::::;;")
            login(request, user)
            return redirect ('home_page')
        else:
             messages.error(request,"Username or Password is incorrect")

    return render(request , 'loginform.html')

def logoutUser(request):
    logout(request)
    messages.error(request,"User successfully logged out ")
    return redirect('loginUser')

# crud of products
 
def addProduct(request):
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/viewProduct/')
    
    else:
        form = ProductForm()

    context = {"form" : form}
    return render (request,'addproduct.html',context)

def viewProduct(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

  

    # productObj = Product.objects.all()
    productObj = Product.objects.filter(
        Q(product_name__icontains = search_query) |
        Q(product_brand__brand_name__icontains=search_query) |
        Q(product_usage_for__usagefor_name__icontains=search_query)
        )
    
    brandsObj = Brand.objects.all()
    usageforObj = UsageFor.objects.all()
    # we need to get page manually from the user
    page = request.GET.get('page')
    result = 2
    paginator = Paginator(productObj,result)

    try:
        productObj = paginator.page(page)

    except PageNotAnInteger: #exception for if no value for page varibale is given 
        page = 1
        productObj = paginator.page(page)

    except EmptyPage: #exception for if user tries to manually override the pagination
        page = paginator.num_pages
        productObj = paginator.page(page)


    context = {"productlist" : productObj, "brandlist" : brandsObj,"usagelist" :usageforObj, "search_query" : search_query ,"paginator" : paginator}

    return render(request, 'viewproducts.html',context)


def productdetail(request,pk):
    productObj = Product.objects.filter(id = pk)
    context={'productDetailList':productObj}
    return render(request,'productdetail.html',context)


def searchitem(request, pk):
    models_list = [Product, Brand, UsageFor]
    results = []
    related_products = []


    for model in models_list:
        # Get the model name in lowercase
        model_name = model.__name__.lower()
        print("MODEL NAME::::::::::",model_name)

        try:
            field_name = model_name +"_name"
            result = model.objects.filter(**{field_name: pk})
           
        
            print("RESULT:::::::::::::::::",result)
        
            results.extend(result)
        except AttributeError:
            # If the field doesn't exist in the model, move on to the next one
            continue
    
    condition = Q()
    for result in results:
        if isinstance(result, Brand):
            condition |= Q(product_brand=result)
        elif isinstance(result, UsageFor):
            condition |= Q(product_usage_for=result)

    # Filter Product objects based on the combined condition
    products = Product.objects.filter(condition)

    # products = Product.objects.filter(product_brand__in=results)
    brandsObj = Brand.objects.all()
    usageforObj = UsageFor.objects.all()
    context = {'productlist': products,"brandlist" : brandsObj,"usagelist" :usageforObj}
    return render(request, 'viewproducts.html', context)



# @login_required
# def add_to_cart(request, pk):
#     # Get the product object
#     product = get_object_or_404(Product, id=pk)
    
#     # Get the user's cart or create a new one
#     cart, created = Cart.objects.get_or_create(user=request.user)
    
#     # Check if the product is already in the cart
#     cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
#     if not item_created:
#         # Product already exists in the cart, you may want to adjust the quantity here
#         logger.info(f"Product '{product.product_name}' already exists in the cart for user '{request.user.username}'.")
    
#     # Get all cart items for the user
#     cart_items = CartItem.objects.filter(cart=cart)
    
#     # Pass the cart items to the productcheckout template
#     return render(request, 'productcheckout.html', {'cart_items': cart_items})

@login_required
def add_to_cart(request, pk):
    # Get the product object
    product = get_object_or_404(Product, id=pk)
    
    # Get the user's cart or create a new one
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Set the user for the cart item
    try:
        cart_item = CartItem.objects.create(cart=cart, product=product, user=request.user)
    except IntegrityError as e:
        # Handle the case where the cart item already exists
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
        # Redirect to the productcheckout page
        return redirect('/productcheckout/')
    
    # Redirect to the productcheckout page
    return redirect('/productcheckout/')

def productcheckout(request):
    # productObj = Product.objects.filter(id = pk)
    cartItemObj = CartItem.objects.all()
    context={'cartItemList':cartItemObj}
    return render(request,'productcheckout.html',context)