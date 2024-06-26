from django.contrib import admin

from .models import User


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('user_id',)


admin.site.register(User, UserAdmin)
