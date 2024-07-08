from django.contrib import admin

from users.models import User, Payment


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_staff', 'is_active', )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'lesson', 'paid_at', 'amount', 'method', )
    list_filter = ('user', 'method', )
