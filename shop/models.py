from django.db import models
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length=54, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args,**kwargs)

    def __str__(self):
        return self.name

class Type(models.Model):
    category = models.ForeignKey(Category,related_name="types", on_delete=models.CASCADE)
    name = models.CharField(max_length=54)
    
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=54,unique=True)
    
    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=54,unique=True)
    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=54,unique=True)
    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=54,unique=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)

    _type = models.ForeignKey(Type,on_delete=models.CASCADE)
    color = models.ManyToManyField(Color,blank=True)
    material = models.ForeignKey(Material,on_delete=models.SET_NULL,null=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
    size = models.ManyToManyField(Size,blank=True)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args,**kwargs)

    class Meta:
        ordering = ('name', )
        index_together = (('id', 'slug'), )

    def __str__(self):
        return self.name