# Generated by Django 2.2.6 on 2019-11-18 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0021_auto_20191118_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='lease',
            name='entire_property',
            field=models.BooleanField(default=False),
        ),
    ]
