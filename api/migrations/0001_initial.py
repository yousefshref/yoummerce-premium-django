# Generated by Django 4.2.1 on 2023-05-29 18:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('order_status', models.CharField(blank=True, choices=[('arrived', 'Arrived'), ('on_the_way', 'On the way'), ('pending', 'Pending')], default='pending', max_length=20, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('shipping_address', models.CharField(blank=True, max_length=200, null=True)),
                ('shipping_address2', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('phone2', models.CharField(blank=True, max_length=20, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.categories')),
                ('related_products', models.ManyToManyField(blank=True, null=True, to='api.product')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('shipping_price', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Var',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Var_name', models.CharField(blank=True, max_length=50)),
                ('buy_price', models.IntegerField(blank=True, default=0, null=True)),
                ('sell_price', models.IntegerField(blank=True, default=0, null=True)),
                ('earning', models.IntegerField(blank=True, default=0, null=True)),
                ('consumer_commission', models.IntegerField(blank=True, default=0, null=True)),
                ('stock', models.IntegerField(blank=True, default=0, null=True)),
                ('add_stock', models.IntegerField(blank=True, default=0, null=True)),
                ('remove_stock', models.IntegerField(blank=True, default=0, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Var', to='api.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images/')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='api.product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('shipping_price', models.IntegerField(blank=True, default=0, null=True)),
                ('total_products_price', models.IntegerField(blank=True, default=0, null=True)),
                ('total_order_price', models.IntegerField(blank=True, default=0, null=True)),
                ('total_earning', models.IntegerField(blank=True, default=0, null=True)),
                ('total_commession', models.IntegerField(blank=True, default=0, null=True)),
                ('Var', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.var')),
                ('Var_all', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Var_all', to='api.var')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='api.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.product')),
                ('product_all', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_all', to='api.product')),
                ('shipping_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='api.state')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('total', models.IntegerField(blank=True, null=True)),
                ('Var', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.var')),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='api.cart')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.product')),
            ],
        ),
    ]
