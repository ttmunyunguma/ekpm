# Generated by Django 2.2.6 on 2019-11-18 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0020_auto_20191118_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='lease',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lease', to='manager.Lease'),
        ),
    ]
