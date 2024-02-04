
from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category_images', blank=True, null=True, default="item_images/default-image.png")

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    image_2 = models.ImageField(upload_to='item_images', blank=True, null=True, default="item_images/default-image.png")
    image_3 = models.ImageField(upload_to='item_images', blank=True, null=True, default="item_images/default-image.png")
    image_4 = models.ImageField(upload_to='item_images', blank=True, null=True, default="item_images/default-image.png")
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  
    locatie = models.CharField(max_length=100, blank=False, default="Locatie nespecificata")
    access_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name