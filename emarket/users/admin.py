from django.contrib import admin

from .models.models import Notifications, UserProfile, DistributionDeliveredMessage

admin.site.register(Notifications)
admin.site.register(UserProfile)
admin.site.register(DistributionDeliveredMessage)
