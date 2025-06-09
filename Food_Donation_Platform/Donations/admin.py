from django.contrib import admin
from .models import Food, FoodBooking,UserProfile,DeliveryRequest

admin.site.register(Food)
admin.site.register(FoodBooking)
admin.site.register(UserProfile)
admin.site.register(DeliveryRequest)