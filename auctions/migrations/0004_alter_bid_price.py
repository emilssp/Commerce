# Generated by Django 4.0.6 on 2022-08-12 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_bid_bidder_bid_bidder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='price',
            field=models.DecimalField(decimal_places=3, max_digits=8),
        ),
    ]