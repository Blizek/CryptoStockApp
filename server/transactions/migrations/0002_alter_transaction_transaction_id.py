# Generated by Django 3.2.5 on 2023-09-19 19:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.UUIDField(default=uuid.UUID('4ffcd008-c380-4d6c-806c-e2f0c6def0bc'), editable=False, primary_key=True, serialize=False),
        ),
    ]