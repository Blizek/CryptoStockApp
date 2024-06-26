# Generated by Django 3.2.5 on 2023-09-19 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.UUIDField(default=uuid.UUID('d033ee0d-c80c-47c3-b9e1-747dd4b8cf4b'), editable=False, primary_key=True, serialize=False, unique=True)),
                ('type_of_transaction', models.CharField(choices=[('SELLING', 'SELLING'), ('BUYING', 'BUYING')], max_length=255)),
                ('cryptocurrency_name', models.CharField(max_length=255)),
                ('cryptocurrency_code', models.CharField(max_length=10)),
                ('amount', models.DecimalField(decimal_places=5, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
