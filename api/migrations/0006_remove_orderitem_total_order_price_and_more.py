# Generated by Django 4.2.1 on 2023-05-29 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_orderitem_shipping_price_order_shipping_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='total_order_price',
        ),
        migrations.AddField(
            model_name='order',
            name='total_order_price',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]