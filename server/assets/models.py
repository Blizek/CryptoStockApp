import uuid

from django.db import models
from authentication.models import User

# Create your models here.

class Asset(models.Model):
    asset_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    cryptocurrency_name = models.CharField(max_length=255, null=False)
    cryptocurrency_code = models.CharField(max_length=5, null=False)
    cryptocurrency_amount = models.DecimalField(max_digits=10, decimal_places=5, null=False)

    def __str__(self):
        return (str(self.owner) + " has " + str(self.cryptocurrency_amount) + " " + str(self.cryptocurrency_name)
                + "(" + str(self.cryptocurrency_code) + ")")