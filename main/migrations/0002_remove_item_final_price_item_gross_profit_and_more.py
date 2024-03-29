# Generated by Django 4.0.3 on 2022-07-26 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='final_price',
        ),
        migrations.AddField(
            model_name='item',
            name='gross_profit',
            field=models.CharField(default='0', max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='additional_fees',
            field=models.CharField(default='0', max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='date_sold',
            field=models.CharField(default='0', max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='selling_platform',
            field=models.CharField(default='0', max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='shipping_fee',
            field=models.CharField(default='0', max_length=100),
        ),
    ]
