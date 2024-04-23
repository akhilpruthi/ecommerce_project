from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True, editable=False,null=False,unique=True)
    # user = models.ForeignKey(User, on_delete = models.CASCADE,null=True,default =None) # Foreign key to the User model

    product_brand = models.ForeignKey('Brand',on_delete = models.CASCADE)
     
    product_image = models.ImageField(null=True,blank=True,default='default.png')
    product_name = models.CharField(max_length=200)
    product_description = models.TextField()
    product_price = models.FloatField()

    product_usage_for = models.ForeignKey('UsageFor',on_delete = models.CASCADE)

    def __str__(self):
        return self.product_title
    
    class Meta:
        ordering = ['-id']

class Brand(models.Model):
    brand_name = models.CharField(max_length=200)

    def __str__(self):
        return self.brand_name
    
    
class UsageFor(models.Model):
    usagefor_name = models.CharField(max_length=200)

    def __str__(self):
        return self.usagefor_name