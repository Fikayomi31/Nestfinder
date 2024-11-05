from django.contrib import admin
from api import models

# Register your models here.
#admin.site.register(models.Agent)
admin.site.register(models.Property)
admin.site.register(models.Category)
admin.site.register(models.PropertyImage)
admin.site.register(models.Booking)
admin.site.register(models.Transaction)
admin.site.register(models.Review)
admin.site.register(models.SavedSearch)
admin.site.register(models.Notification)
admin.site.register(models.Message)
