# Generated by Django 3.2.19 on 2023-07-30 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cake_shop', '0005_alter_cake_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='mail',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Почта'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=12, unique=True, verbose_name='Телефон'),
        ),
    ]
