# Generated by Django 4.2.8 on 2024-07-10 12:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('license', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='licenseId',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
