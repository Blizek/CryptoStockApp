from django.contrib import admin

# Register your models here.
from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('transaction_id',)


admin.site.register(Transaction, TransactionAdmin)
