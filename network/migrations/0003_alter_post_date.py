# Generated by Django 4.0.4 on 2022-05-17 16:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 17, 9, 58, 22, 794646)),
        ),
    ]
