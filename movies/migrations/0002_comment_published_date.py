# Generated by Django 2.2 on 2019-05-23 17:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='published_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
