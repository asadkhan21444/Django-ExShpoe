from django.db import models
import datetime
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
   
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    
    
    def __str__(self):
        return self.name
    
    
# ================================================================================  
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField()
    image = models.ImageField(upload_to='products/') 
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)
    
    @staticmethod
    def get_all_products():
        return Product.objects.all()
    
    @staticmethod    
    def get_all_products_by_category_id(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()
    
    
# ================================================================================ 

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=110)
    
    
    def __str__(self):  
        return self.first_name + self.last_name
    
    
    def register(self):
        self.save()


# ====================================================

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    phone = models.CharField(max_length=40,default='',blank=True)
    email = models.CharField(max_length=40,default='',blank=True)
    price = models.IntegerField()
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.product} | {self.customer} | {self.price} |{self.email}|{self.phone}"
