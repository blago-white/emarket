from django.contrib import admin

from .models.models import Notifications, UserProfile

admin.site.register(Notifications)
admin.site.register(UserProfile)
