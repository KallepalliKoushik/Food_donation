from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),               # Root URL
    path('index/', views.index, name='index'),        # Also map /index
    path('recipent/', views.recipient_home, name='recipient_home'),
    path('donor/', views.add_food, name='donor_home'),
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('book/<int:food_id>/',views.book,name='book'),
    path('booking_comformation/',views.booking_comformation,name='booking_comformation'),
    path('recent_donations/',views.recent_donations,name="recent_donations"),
    path('deliveryboy_login/', views.deliveryboy_login, name='deliveryboy_login'),
    path('deliveryboy_register/', views.deliveryboy_register, name='deliveryboy_register'),
    path('deliveryboy/dashboard/', views.deliveryboy_dashboard, name='deliveryboy_dashboard'),
    path('deliveryboy/accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('deliveryboy/reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('deliveryboy_logout/', views.deliveryboy_logout, name="deliveryboy_logout"),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
 # <-- fixed duplicate path
]
