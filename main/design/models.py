from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True, editable=False,null=False,unique=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE,null=True,default =None) # Foreign key to the User model
    category = models.CharField(max_length=100, null= True,blank = True, default =None)
    image = models.ImageField(null=True,blank=True,default='default.png')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()