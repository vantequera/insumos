# Generated by Django 4.0.3 on 2022-03-25 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vmi', '0008_rename_idereferencia_facturasmov_idreferencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidosmov',
            name='cantidad',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]