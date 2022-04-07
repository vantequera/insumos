# Generated by Django 4.0.3 on 2022-04-07 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_pais', models.CharField(max_length=200)),
                ('codigo_pais', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_departamento', models.CharField(max_length=200)),
                ('codigo_dane_departamento', models.IntegerField()),
                ('pais', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Pais', to='vmi.country')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_ciudad', models.CharField(max_length=200)),
                ('codigo_dane_ciudad', models.IntegerField()),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Departamento', to='vmi.department')),
            ],
        ),
    ]
