from rest_framework import serializers
from .models import Transaction, User
from assets.models import Asset

from django.core.exceptions import ObjectDoesNotExist

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['transaction_id', 'owner', 'type_of_transaction', 'cryptocurrency_name', 'cryptocurrency_code',
                  'amount', 'price', 'created_at']

    def validate(self, attrs):
        user = attrs.get('owner', '')
        type_of_transaction = attrs.get('type_of_transaction', '')
        cryptocurrency_name = attrs.get('cryptocurrency_name', '')
        cryptocurrency_code = attrs.get('cryptocurrency_code', '')
        amount = attrs.get('amount', '')
        price = float(attrs.get('price', ''))

        try:
            user_asset = Asset.objects.get(owner=user, cryptocurrency_code=cryptocurrency_code)
        except ObjectDoesNotExist:
            user_asset = Asset(
                owner=user,
                cryptocurrency_name=cryptocurrency_name,
                cryptocurrency_code = cryptocurrency_code,
                cryptocurrency_amount = 0
            )


        if type_of_transaction == "SELLING":
            if amount > user_asset.cryptocurrency_amount:
                raise serializers.ValidationError(
                    "You don't have enough " + str(cryptocurrency_name) + " cryptocurrency for this transaction"
                )

            user.balance += price
            user_asset.cryptocurrency_amount -= amount
        elif type_of_transaction == "BUYING":
            if price > user.balance:
                raise serializers.ValidationError(
                    "You don't have enough money for this transaction"
                )

            user.balance -= price
            user_asset.cryptocurrency_amount += amount

        user.save()
        user_asset.save()

        return attrs