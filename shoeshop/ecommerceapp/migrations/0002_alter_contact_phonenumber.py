# Generated by Django 5.1.5 on 2025-04-09 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phonenumber',
            field=models.IntegerField(),
        ),
    ]
