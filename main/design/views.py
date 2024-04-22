from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Product
from .forms import ProductForm
from django.contrib.auth import authenticate, login,logout

from django.core.mail import send_mail
from django.conf import settings


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
        form = ProductForm(request.POST,request.FILES,user=request.user)
        if form.is_valid():
            form.save()
            return redirect('/viewProduct/')
    
    else:
        form = ProductForm(user = request.user)

    context = {"form" : form}
    return render (request,'addproduct.html',context)


def viewProduct(request):
    productObj = Product.objects.all()
    context = {"productlist" : productObj}

    return render(request, 'viewproducts.html',context)
