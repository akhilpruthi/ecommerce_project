from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home_page,name = 'home_page'),
    path('about_page/',views.about_page,name = 'about_page'),
    path('register_request/',views.register_request,name = 'register_request'),
    path('loginUser/',views.loginUser,name = 'loginUser'),
    path('logoutUser/',views.logoutUser,name = 'logoutUser'),
]
