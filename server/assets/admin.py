from django.contrib import admin

# Register your models here.
from .models import Asset


class AssetsAdmin(admin.ModelAdmin):
    readonly_fields = ('asset_id',)


admin.site.register(Asset, AssetsAdmin)
