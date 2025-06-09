from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from .models import Food
from .models import FoodBooking
from django.shortcuts import get_object_or_404
from .models import DeliveryRequest


import re

def extract_number(text):
    match = re.search(r'\d+', text)  # Looks for the number in a string like "1 packet"
    return int(match.group()) if match else 0


#
def index(request):
    return render(request, 'Donations/index.html')
@login_required
def add_food(request):
    if request.method == 'POST':
        food_name = request.POST['food_name']
        quantity = request.POST['quantity']
        expiry_date = request.POST['expiry_date']
        pickup_window = request.POST['pickup_window']
        
        food_image = request.FILES.get('food_image')

        food = Food(
            food_name=food_name,
            quantity=quantity,
            expiry_date=expiry_date,
            pickup_window=pickup_window,
            
            food_image=food_image
        )
        food.save()
        return redirect('donor_home')  # ✅ Use URL name, not template filename

    return render(request, "donor_home.html")

def register(request):
    if request.method == "POST":
        name = request.POST["name"]
        username = request.POST["username"]
        password1 = request.POST["password"]
        password2 = request.POST["confirm_password"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        role = request.POST["role"]
        sub_role = request.POST.get("sub_role", None)
  # Use .get() to avoid KeyError

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists! Please try another one.")
                return render(request, "register.html")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists! Please try another one.")
                return render(request, "register.html")
            else:
                user = User.objects.create_user(username=username, password=password1, email=email)
                user.save()

                profile = UserProfile.objects.create(
                    user=user,
                    name=name,
                    phone=phone,
                    address=address,
                    role=role,
                    sub_role=sub_role  # Could be None if not applicable
                )
                profile.save()

                messages.success(request, "Registration Successful! You can now login.")
                return redirect("login")
        else:
            messages.error(request, "Password didn't match with Confirm password")

    return render(request, "register.html")

    
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")

            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == "donor":
                    return redirect("donor_home")
                elif profile.role == "recipient":
                    return redirect("recipient_home")
                else:
                    messages.error(request, "Invalid role. Contact admin.")
                    return redirect("login")
            except UserProfile.DoesNotExist:
                messages.error(request, "Profile not found. Contact admin.")
                return redirect("login")
        else:
            messages.error(request, "Enter Correct Credentials!")
            return redirect("login")

    return render(request, "login.html")
def user_logout(request):
    logout(request)
    return render(request,'login.html')                    
@login_required
def recipient_home(request):
    items = Food.objects.exclude(quantity="0 packet(s)")
    return render(request, 'recipient_home.html', {'items': items})

def recent_donations(request):
    items = Food.objects.exclude(quantity="0 packet(s)")
    return render(request, 'recent_donations.html', {'items': items}) 

@login_required
def book(request, food_id):
    item = get_object_or_404(Food, id=food_id)

    if request.method == 'POST':
        recipient_name = request.POST['recipient_name']
        recipient_location = request.POST['recipient_location']
        phone = request.POST['phone']
        quantity = int(request.POST['quantity'])

        available_quantity = extract_number(item.quantity)

        if quantity > available_quantity:
            error_message = f"Only {available_quantity} available. You requested {quantity}."
            return render(request, 'book.html', {
                'item': item,
                'error_message': error_message
            })

        booking = FoodBooking(
            food=item,
            recipient_name=recipient_name,
            recipient_location=recipient_location,
            phone=phone,
            quantity=quantity,
            user=request.user
        )
        booking.save()
        DeliveryRequest.objects.create(
            food_booking=booking,
            food_item=item.food_name,
            pickup_location=item.pickup_window,
            delivery_location=recipient_location,
            status='Pending',
            assigned_to=None  # Explicitly set this to None to make sure it's not assigned yet
        )


        print("Delivery Request Created for:", item.food_name)
        # Calculate new quantity
        new_quantity = available_quantity - quantity

        # If zero, delete from DB
        if new_quantity == 0:
            item.delete()
        else:
            item.quantity = f"{new_quantity} packet(s)"
            item.save()

        return render(request, 'booking_comformation.html', {'item': item, 'booking': booking})

    return render(request, 'book.html', {'item': item})


def booking_comformation(request):
    return render(request, 'booking_comformation.html')    
def deliveryboy_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('deliveryboy_dashboard')  # Replace with your dashboard view
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'deliveryboy_login.html')

def deliveryboy_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('deliveryboy_register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('deliveryboy_register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('deliveryboy_login')

    return render(request, 'deliveryboy_register.html')
@login_required
def deliveryboy_dashboard(request):
    requests = DeliveryRequest.objects.filter(status='Pending', assigned_to__isnull=True)
    return render(request, 'deliveryboy_dashboard.html', {'requests': requests})


@login_required
def accept_request(request, request_id):
    req = get_object_or_404(DeliveryRequest, id=request_id)
    req.status = 'Accepted'
    req.assigned_to = request.user
    req.save()
    return redirect('deliveryboy_dashboard')

@login_required
def reject_request(request, request_id):
    req = get_object_or_404(DeliveryRequest, id=request_id)
    req.status = 'Rejected'
    req.assigned_to = request.user
    req.save()
    return redirect('deliveryboy_dashboard')    
def deliveryboy_logout(request):
    logout(request)
    return render(request,'deliveryboy_login.html')     
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
