import uuid

from django.db import models
from authentication.models import User


# Create your models here.

class Transaction(models.Model):
    TRANSACTION_OPTIONS = [
        ('SELLING', 'SELLING'),
        ('BUYING', 'BUYING')
    ]

    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    type_of_transaction = models.CharField(choices=TRANSACTION_OPTIONS, max_length=255, null=False)
    cryptocurrency_name = models.CharField(max_length=255, null=False)
    cryptocurrency_code = models.CharField(max_length=10, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=5, null=False)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        ordering: ['-created_at']

    def __str__(self):
        return str(self.owner) + " is " + str(self.type_of_transaction) + " " + str(self.cryptocurrency_name) \
            + " (" + str(self.cryptocurrency_code) + ") at " + str(self.created_at)


