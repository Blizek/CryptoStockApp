# Generated by Django 3.2.5 on 2023-08-31 16:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20230831_1836'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_stuff',
            new_name='is_staff',
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.UUIDField(default=uuid.UUID('9ad14f24-b5f7-4bf1-8058-bce4016a0fe9'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
