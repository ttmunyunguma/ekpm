# Generated by Django 2.2.6 on 2019-11-08 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0013_auto_20191107_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='acquisition_cost',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_type',
            field=models.CharField(choices=[('Residential', 'Residential'), ('Apartment Building', 'Apartment Building'), ('Office Building', 'Office Building'), ('Industrial', 'Industrial'), ('Commercial', 'Commercial'), ('Agricultural', 'Agricultural'), ('Land', 'Land'), ('Other', 'Other')], max_length=55),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_value',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='property',
            name='selling_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15),
        ),
    ]