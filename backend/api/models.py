from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from userauths.models import User, AgentProfile, TenantProfile
from shortuuid.django_fields import ShortUUIDField


PROPERTY_TYPE_CHOICES = (
    ('rental', 'Rental'),
    ('sale', 'Sale'),
)

CATEORY_TYPE = (
    ('Deplex', 'DEPLEX'),
    ('3 Bedroom flat', '3 BEDROOM FLAT'),
    ('2 Bedroom flat', '2 BEDROOM FLAT'),
    ('A Room Self contain', 'A ROOM SELF CONTAIN'),
    ('Room and Parlow Self Contain', 'ROOM AND PARLAW SELF CONTAIN')
)

PROPERTY_STATUS = (
    ('Available', 'AVAILABE'),
    ('Rent', 'RENT'),
    ('Sold', 'SOLD'),
)

BOOKING_STATUS =(
    ('Pending', 'PENDING'),
    ('Approved', 'APPROVED'),
    ('Rejected', 'REJECTED'),
)

PAYMENT_STATUS = (
    ('Processing', 'PROCESSING'),
    ('Approved', 'APPROVED'),
    ('Rejected', 'REJECTED'),
  
) 

RATING = (
    ('1', '1 star'),
    ('2', '2 star'),
    ('3', '3 star'),
    ('4', '4 star'),
    ('5', '5 star'),
)

NOTI_TYPE= (
    ('New Booking', 'NEW BOOKING'),
    ('New Message', 'NEW MESSAGE'),
    ('New Review', 'NEW REVIEW'),
)
""" 
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='agent_folder', default='default.jpg', null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(max_length=200, blank=True, null=True)
    licence_number = models.CharField(max_length=100)
    agency_name = models.CharField(max_length=100)
    bio = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.agency_name} - Agent"

    def property(self):
        return Property.objects.filter(agent=self)

    def review(self):
        return Review.objects.filter(agent=self).count()
    
    def booking(self):
        return Booking.objects.filter(agent=self)
  """ 

class Category(models.Model):
    title = models.CharField(max_length=200, choices=CATEORY_TYPE, default='3 Bedroom Flat')
    image_url = models.ImageField(upload_to='catergories_images/', null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['-title']
        
    def __str__(self):
        return self.title
    
    def property(self):
        return Property.objects.filter(category=self).count()
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title)
        super(Category, self).save()


class Property(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    video_url = models.FileField(upload_to="property_file")
    slug = models.SlugField(unique=True, null=True, blank=True)
    property_id  = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    price = models.DecimalField(max_digits=15, decimal_places=2)
    Agent_fess = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True, blank=True)
    caution_fee =  models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True, blank=True)
    agreement_fee = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    type_of_property = models.CharField(max_length=200, choices=PROPERTY_TYPE_CHOICES, default='Rental')
    property_status = models.CharField(max_length=200, choices=PROPERTY_STATUS, default='Available')
    bedrooms = models.IntegerField(null=False, blank=False)
    bathrooms = models.IntegerField(null=False, blank=False)
    available_from = models.DateField(null=False, blank=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = ['Properties']

    def __str__(self):
        return self.title
    
    
    def save(self, *args, **kwargs):
        # Validate price, bedrooms, and bathrooms
        if self.price <= 0:
            raise ValueError("Price must be greater than 0.")

        if self.bathrooms <= 0:
            raise ValueError("Bathrooms can't be 0")

        if self.bedrooms <= 0:
            raise ValueError("Bedrooms can't be 0")

        # Assign slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)

        # Call the parent class's save method
        super().save(*args, **kwargs)

    def tenant(self):
        return Booking.objects.filter(property=self)
    
    def review(self):
        return Review.objects.filter(property=self, active=True)
    

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to='property_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"Image for {self.property.title}"


class Booking(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='PENDING')
    created_at = models.DateField(auto_now_add=True)
    booking_id  = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")


    def __str__(self):
        return f"Booking for {self.property.title} by {self.tenant.name}"
    
class Message(models.Model):
    sender_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='sent_messages')
    sender_object_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    sender = GenericForeignKey('sender_content_type', 'sender_object_id')

    receiver_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='received_messages')
    receiver_object_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")
    receiver = GenericForeignKey('receiver_content_type', 'receiver_object_id')

    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True)
    message_text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return f"Message from {self.sender}"


class Inquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inquiries')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 

    
class SavedSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_criteria = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Saved search by {self.user.name}"
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_by_tenant')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews_by_agent')
    rating = models.CharField(max_length=200, choices=RATING, default=None)
    review_text = models.TextField()
    reply = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.property.title
    
    def profile(self):
        return Profile.objects.filter(user=self.user)

class Transaction(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_by_tenant')
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_by_agent')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tax_fee = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=200, choices=PAYMENT_STATUS, default="Processing")
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    stripe_session_id = models.CharField(max_length=2000, null=True, blank=True)
    transaction_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="1234567890")

    def __str__(self):
        return f"Transaction of {self.amount} by {self.tenant.name}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    review = models.ForeignKey(Review, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True)
    inquiry = models.ForeignKey(Inquiry, on_delete=models.  SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=100, choices=NOTI_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.type
    