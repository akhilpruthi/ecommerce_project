from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home_page,name = 'home_page'),
    path('about_page/',views.about_page,name = 'about_page'),
    path('register_request/',views.register_request,name = 'register_request'),
    path('loginUser/',views.loginUser,name = 'loginUser'),
    path('logoutUser/',views.logoutUser,name = 'logoutUser'),
    path('addProduct/', views.addProduct, name='addProduct'),
    path('viewProduct/', views.viewProduct, name='viewProduct'),
    path('productdetail/<str:pk>', views.productdetail, name='productdetail'),
    path('searchitem/<str:pk>', views.searchitem, name='searchitem'),
    # path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('add_to_cart/<str:pid>/<int:quantity>/', views.add_to_cart, name='add_to_cart'),
    # path('add_to_cart/<str:pid>/<int:quantity>', views.add_to_cart, name='add_to_cart'),
    # path('productcheckout/', views.productcheckout, name='productcheckout'),

]
