from django.db import models
from django.contrib.auth.models import User


# STATES
class State(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100)
    shipping_price = models.IntegerField(null=True, blank=True,default=0)

    def __str__(self):
        return f"{self.name}"
# STATES

class InsufficientStock(Exception):
    """Raised when there is not enough stock for an order item"""
# PRODUCTS
class Product(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey('Categories', null=True, blank=True, on_delete=models.CASCADE)
    related_products = models.ManyToManyField('self', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.id} || {str(self.name)}'



class Var(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='Var', null=True, blank=True)
    Var_name = models.CharField(max_length=50, blank=True)
    buy_price = models.IntegerField(null=True, blank=True,default=0)
    sell_price = models.IntegerField(null=True, blank=True,default=0)
    earning = models.IntegerField(null=True, blank=True,default=0)
    consumer_commission = models.IntegerField(null=True, blank=True,default=0)
    stock = models.IntegerField(null=True, blank=True,default=0)
    add_stock = models.IntegerField(null=True, blank=True, default=0)
    remove_stock = models.IntegerField(null=True, blank=True, default=0)

    def decrease_stock(self, quantity):
        if self.stock - quantity < 0: 
            raise InsufficientStock(f"انت تختار كميات اكبر من المتاحد من المنتج '{str(self.product.name)}'")
        self.stock -= quantity
        self.save()

    def increase_stock(self, quantity):
        self.stock += quantity
        self.save()  

    def save(self, *args, **kwargs):
        if self.add_stock is not None:
            self.stock += self.add_stock
            self.add_stock = 0
        if self.remove_stock is not None:
            self.stock -= self.remove_stock
            self.remove_stock = 0
        self.earning = self.sell_price - self.buy_price
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.id} || {str(self.Var_name)} || stock: {str(self.stock)} || comm: {str(self.consumer_commission)} || price: {str(self.sell_price)}'


class Categories(models.Model):
    category = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.category)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(
        upload_to='product_images/', null=True, blank=True)
# PRODUCTS


# CART
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.user)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    Var = models.ForeignKey(Var, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    total = models.IntegerField(null=True, blank=True, default=0)
    total_commission = models.IntegerField(null=True, blank=True, default=0)

    def save(self, *args, **kwargs):
        self.total = self.Var.sell_price * self.quantity
        self.total_commission = self.Var.consumer_commission * self.quantity
        super().save(*args, **kwargs)
# CART


# ORDER
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    ORDER_STATUS = (
        ('arrived', 'Arrived'),
        ('on_the_way', 'On the way'),
        ('pending', 'Pending')
    )
    order_status = models.CharField(
        max_length=20, choices=ORDER_STATUS, blank=True, null=True, default='pending')
    name = models.CharField(max_length=100, blank=True, null=True)
    shipping_address = models.CharField(max_length=200, blank=True, null=True)
    shipping_address2 = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    phone2 = models.CharField(max_length=11, blank=True, null=True)
    shipping_to = models.ForeignKey(
        State,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders'
    )
    shipping_price = models.IntegerField(blank=True, null=True,default=0)
    total_order_price = models.IntegerField(
        blank=True, null=True,default=0)  # total products + shipping

    def save(self, *args, **kwargs):
        # calculate shipping price
        if self.shipping_to:
            self.shipping_price = self.shipping_to.shipping_price

        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f'{str(self.user)} #{self.id}'
    
class OrderItem(models.Model):    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True,related_name='order_items')   
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    product_all = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True,related_name='product_all')
    Var_all = models.ForeignKey(Var, on_delete=models.CASCADE, null=True, blank=True, related_name='Var_all')
    Var = models.ForeignKey(Var, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True,default=0)
    total_products_price = models.IntegerField(
        blank=True, null=True,default=0)  # total products
    total_earning = models.IntegerField(blank=True, null=True,default=0)
    total_commession = models.IntegerField(blank=True, null=True,default=0)


    def save(self, *args, **kwargs):
        try:
            if self.id:  
                original = OrderItem.objects.get(id=self.id)           
                diff = self.quantity - original.quantity       
                self.Var.decrease_stock(diff)
                
            else:   
                self.Var.decrease_stock(self.quantity)
        except InsufficientStock as e:
            raise

        # # Calculate total products price
        if self.Var and self.quantity:
            self.total_products_price = self.Var.sell_price * self.quantity

        # # calculate earning
        if self.Var and self.quantity:
            self.total_earning = self.Var.earning * self.quantity

        # # calculate commission
        if self.Var and self.quantity:
            self.total_commession = self.Var.consumer_commission * self.quantity
            
        self.product_all = self.product
        self.Var_all = self.Var

        super().save(*args, **kwargs)



    def delete(self, *args, **kwargs):       
        self.Var.increase_stock(self.quantity)       
        super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.order)
# ORDER


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Product)
def save_Vars(sender, instance, **kwargs):
    for Var in instance.Var.all():
        Var.save()



from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)  
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)