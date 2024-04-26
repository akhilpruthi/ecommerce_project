from django.db import models
from django.contrib.auth.models import User


class Brand(models.Model):
    brand_name = models.CharField(max_length=200)

    def __str__(self):
        return self.brand_name
    
    
class UsageFor(models.Model):
    usagefor_name = models.CharField(max_length=200)

    def __str__(self):
        return self.usagefor_name


class Product(models.Model):
    product_brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_image = models.ImageField(null=True, blank=True, default='default.png')
    product_name = models.CharField(max_length=200)
    product_description = models.TextField()
    product_price = models.FloatField()
    product_usage_for = models.ForeignKey(UsageFor, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name
    
    class Meta:
        ordering = ['-id']


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    STATUS_CHOICES = (
        ('in_cart', 'In Cart'),
        ('wishlist', 'Wishlist'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, default='in_cart')  # 'in_cart' or 'wishlist'
    amount = models.FloatField(default=0)

    def __str__(self):
        return f"CartItem: {self.product.product_name} (Qty: {self.quantity})"

    def save(self, *args, **kwargs):
        # Calculate amount based on product price and quantity
        self.amount = self.product.product_price * self.quantity
        super(CartItem, self).save(*args, **kwargs)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    primary_key = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Wishlist for {self.user.username}"










# from django.db import models
# from django.contrib.auth.models import User


# # Create your models here.
# class Product(models.Model):
#     id = models.AutoField(primary_key=True, editable=False,null=False,unique=True)
#     # user = models.ForeignKey(User, on_delete = models.CASCADE,null=True,default =None) # Foreign key to the User model

#     product_brand = models.ForeignKey('Brand',on_delete = models.CASCADE)
     
#     product_image = models.ImageField(null=True,blank=True,default='default.png')
#     product_name = models.CharField(max_length=200)
#     product_description = models.TextField()
#     product_price = models.FloatField()

#     product_usage_for = models.ForeignKey('UsageFor',on_delete = models.CASCADE)

#     def __str__(self):
#         return self.product_name
    
#     class Meta:
#         ordering = ['-id']

# class Brand(models.Model):
#     brand_name = models.CharField(max_length=200)

#     def __str__(self):
#         return self.brand_name
    
    
# class UsageFor(models.Model):
#     usagefor_name = models.CharField(max_length=200)

#     def __str__(self):
#         return self.usagefor_name