# Generated by Django 4.0.3 on 2022-04-08 16:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vmi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
