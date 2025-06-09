from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class Food(models.Model):
    food_name = models.CharField(max_length=100)  # Changed to CharField for clarity
    food_image = models.ImageField(upload_to='pics')
    expiry_date = models.DateField(null=True, blank=True) 
    quantity = models.TextField(default="0")  # Stored as a string (e.g., "3 packets")
    pickup_window = models.TextField(default="0")
    
    


    def __str__(self):
        return self.food_name

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('donor', 'Donor'),
        ('recipient', 'Recipient'),
    ]

    SUBROLE_CHOICES = [
        ('individual', 'Individual'),
        ('restaurant', 'Restaurant'),
        ('grocery', 'Grocery Store'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    sub_role = models.CharField(max_length=20, choices=SUBROLE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.user.username

class FoodBooking(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True)
    # Use Food, not FoodItem
    user = models.ForeignKey(User, on_delete=models.CASCADE)       # User who booked
    recipient_name = models.CharField(max_length=100)
    recipient_location = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    quantity = models.PositiveIntegerField()
    booking_time = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return f"Booking by {self.recipient_name} for {self.food.food_name}"
class DeliveryRequest(models.Model):
    food_booking = models.ForeignKey(FoodBooking, on_delete=models.CASCADE, null=True, blank=True)  # <-- Add this line
    food_item = models.CharField(max_length=200)
    pickup_location = models.CharField(max_length=255)
    delivery_location = models.CharField(max_length=255)
    
    status_choices = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='Pending')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.food_item

