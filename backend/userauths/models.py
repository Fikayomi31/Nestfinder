from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.conf import settings

# Choices for user_type
USER_TYPE = (
    ('Agent', 'Agent'),
    ('Tenant', 'Tenant')
)

class User(AbstractUser):
    """Custom User model with user_type for Agent and Tenant."""
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200, blank=True)
    otp = models.CharField(max_length=100, null=True, blank=True)
    refresh_token = models.CharField(max_length=100, null=True, blank=True)
    user_type = models.CharField(max_length=255, choices=USER_TYPE, default="Tenant")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Automatically set full_name and username if they are empty
        if not self.full_name:
            self.full_name = self.username
        if not self.username:
            self.username = self.email.split('@')[0]
        
        # Use the simplified call to super() without arguments
        super().save(*args, **kwargs)

        if self.user_type == 'Agent':
            # Check if the user already has an agent profile
            if not hasattr(self, 'agent_profile'):
                AgentProfile.objects.create(user=self, full_name=self.full_name)
        elif self.user_type == 'Tenant':
            # Check if the user already has a tenant profile
            if not hasattr(self, 'tenant_profile'):
                TenantProfile.objects.create(user=self, full_name=self.full_name)

# Agent profile model
class AgentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agent_profile')
    image = models.ImageField(upload_to='user_folder', default='default.jpg', null=True, blank=True)
    full_name = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    agency_name = models.CharField(max_length=255, null=True, blank=True)
    license_number = models.CharField(max_length=100, null=True, blank=True)
    properties_listed = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.full_name or self.user.username
    
    def save(self, *args, **kwargs):
        # Ensure full_name in profile is the same as in the user model
        if not self.full_name:
            self.full_name = self.user.full_name
        super().save(*args, **kwargs)  # Correctly call super()

# Tenant profile model
class TenantProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tenant_profile')
    image = models.ImageField(upload_to='user_folder', default='default.jpg', null=True, blank=True)
    full_name = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    preferences = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.full_name or self.user.username
    
    def save(self, *args, **kwargs):
        # Ensure full_name in profile is the same as in the user model
        if not self.full_name:
            self.full_name = self.user.full_name
        super().save(*args, **kwargs)  # Correctly call super()

# Signals to ensure profile is created for every user
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create profile when a user is created."""
    if created:
        if instance.user_type == 'Agent':
            AgentProfile.objects.create(user=instance)
        elif instance.user_type == 'Tenant':
            TenantProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
