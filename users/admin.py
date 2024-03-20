from django.contrib import admin

from users.models import User, Payment, Subscription

admin.site.register(User)

admin.site.register(Payment)

admin.site.register(Subscription)