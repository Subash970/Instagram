# Generated by Django 5.0 on 2024-04-14 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='caption',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]
