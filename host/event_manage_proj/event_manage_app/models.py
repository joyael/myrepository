from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField()
    address = models.TextField()
    district = models.CharField(max_length=255)
    pincode = models.CharField(max_length=6)
    date_of_birth = models.DateField()
    age = models.PositiveIntegerField()
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Organizer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField()
    address = models.TextField()
    licenseid = models.CharField(max_length=10)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class Venue(models.Model):
    name = models.CharField(max_length=255)
    image = models.FileField()
    address = models.TextField()
    district = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    pincode = models.CharField(max_length=6)
    gmaplink = models.CharField(max_length=255,default="www.chat.openai.com")
    maxparticipants = models.PositiveIntegerField()


class EventCategory(models.Model):
    name = models.CharField(max_length=255)
    OPTION_ONE = 'organizer'
    OPTION_TWO = 'userandorganizer'

    OPTIONS = [
        (OPTION_ONE, 'Organizer level'),
        (OPTION_TWO, 'User Level'),
    ]

    level = models.CharField(
        max_length=50,
        choices=OPTIONS,
        default=OPTION_ONE,
    )
    priceperhour = models.PositiveIntegerField()


class Event(models.Model):
    name = models.CharField(max_length=255)
    image = models.FileField()
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True)
    organizer = models.ForeignKey(Organizer, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True)
    ticketprice = models.PositiveIntegerField()
    maxparticipants = models.PositiveIntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    details = models.TextField()
    approvedbyadmin = models.BooleanField(default=False)
    payed = models.BooleanField(default=False)
    participants=models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=100,default='pending')
    statusreason = models.TextField(default='Admin waiting to approve')
    approveddate = models.DateTimeField(null=True, blank=True)
    price=models.PositiveIntegerField(default=0)
    isrefunded = models.BooleanField(default=False)
    refunddate = models.DateTimeField(null=True, blank=True)
    refundid = models.CharField(max_length=150,default='nil')
    refundprice = models.PositiveIntegerField(default=0)


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_id = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    npersons = models.IntegerField(default=1)
    total_price = models.PositiveIntegerField(default=0)
    payment_id = models.CharField(max_length=100)
    cancelticket = models.BooleanField(default=False)
    tempcancellable = models.BooleanField(default=True)
    isrefunded = models.BooleanField(default=False)
    refunddate = models.DateTimeField(null=True, blank=True)
    refundid = models.CharField(max_length=150,default='nil')


class PasswordReset(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    #security
    token=models.CharField(max_length=4)

class PasswordResetOrganizer(models.Model):
    organizer=models.ForeignKey(Organizer,on_delete=models.CASCADE)
    #security
    token=models.CharField(max_length=4)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Refers to the user purchasing the event tickets
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # Refers to the event being booked
    # Personal Details
    so_fname = models.CharField(max_length=20, null=False)  # Name of the person placing the order
    so_email = models.EmailField(null=False)  # Email of the person placing the order
    so_phone = models.CharField(max_length=15, null=False)  # Phone number of the person placing the order
    so_address = models.TextField(null=False)  # Address of the person placing the order
    so_district = models.CharField(max_length=20, null=False)
    so_pincode = models.CharField(max_length=6, null=False)

    # Order Information
    add_message = models.CharField(max_length=250, blank=True)  # Any additional message
    order_status_choices = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=150, choices=order_status_choices, default='Pending')  # Order status
    type = models.CharField(max_length=150, blank=True)
    ticketprice=models.PositiveIntegerField(default=1)
    quantity = models.PositiveIntegerField(null=False)  # Number of tickets being purchased
    total_price = models.FloatField(null=False)  # Total price for the order
    payment_mode = models.CharField(max_length=150, null=False)  # Mode of payment (e.g., card, UPI, etc.)
    payment_id = models.CharField(max_length=150, null=True)  # Transaction ID after payment
    order_id = models.CharField(max_length=150, null=False, unique=True)  # Unique order ID
    tracking_no = models.CharField(max_length=150, null=True, blank=True)  # For tracking (if needed)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # Order creation time
    updated_at = models.DateTimeField(auto_now=True)  # Last update time

# create other examples like :
# {
# name : Classical Fusion Nights
# Category: Music Concert or Birthday Party or Food Festival or Science Fair or Art Exhibition or Cultural Festival
# Venue: Inclusive Convention Hall, Thrissur or Accessible Community Center, Kochi or Barrier-Free Auditorium, Thiruvananthapuram
# Location: Convention Center
# Ticket Price: ₹5000
# Start: 09 Sep 2024, 06:00 PM
# End: 09 Sep 2024, 08:00 PM
# Participants limit:
# Event Details : (two sentences)
# }

