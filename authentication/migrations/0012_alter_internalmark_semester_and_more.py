# Generated by Django 5.1.4 on 2025-06-14 22:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_internalmark_semester_alter_internalmark_subject'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='internalmark',
            name='semester',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='internalmark',
            name='subject',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='StudentMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('full_marks', models.IntegerField()),
                ('obtained_marks', models.IntegerField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
