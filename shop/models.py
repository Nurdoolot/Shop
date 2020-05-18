from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse('product_by_category', args=[self.slug])


class Product(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='product/', blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'))
    
    def get_absolute_url(self):
        return reverse('detail', args=[self.id, self.slug])
