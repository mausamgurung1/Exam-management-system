# Generated by Django 5.1.2 on 2025-04-17 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_profile_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(default=' ', max_length=255),
        ),
    ]
