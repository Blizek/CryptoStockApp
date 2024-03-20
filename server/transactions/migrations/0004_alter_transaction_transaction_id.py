# Generated by Django 3.2.5 on 2023-09-19 19:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_alter_transaction_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
