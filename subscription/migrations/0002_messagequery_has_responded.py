# Generated by Django 4.2.8 on 2024-01-22 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagequery',
            name='has_responded',
            field=models.BooleanField(default=False),
        ),
    ]
