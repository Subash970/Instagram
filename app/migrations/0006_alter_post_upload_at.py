# Generated by Django 5.0 on 2024-04-14 08:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_post_upload_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='upload_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 14, 14, 18, 33, 75076)),
        ),
    ]
