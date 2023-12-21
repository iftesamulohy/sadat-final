from django.db import models
from django.utils.text import slugify
import math
from .custom_fields import ApiDataField
# Create your models here.
class SubsubCategory(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="upload")
    def __str__(self):
        return f"{self.name}"
class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="upload")
    sub_category = models.ManyToManyField(SubsubCategory)
    def __str__(self):
        return f"{self.name}"
class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="upload")
    sub_category = models.ManyToManyField(SubCategory)
    def __str__(self):
        return f"{self.name}"
class Market(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.name}"
class Image(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="upload")
    def __str__(self):
        return f"{self.name}"
class SliderItem(models.Model):
    title = models.CharField(max_length=200)
    image = models.ForeignKey(Image,on_delete=models.CASCADE,null=True,blank=True)
    text = models.TextField(max_length=500)
    button = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.title}"
    class Meta:
        verbose_name = "Slider Items"
class Slider(models.Model):
    title = models.CharField(max_length=200)
    slider_item = models.ManyToManyField(SliderItem)
    def __str__(self):
        return f"{self.title}"
    class Meta:
        verbose_name = "Slider"
class Reviews(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    pros = models.TextField()
    cons = models.TextField()
    rating = models.FloatField()
    def __str__(self):
        return f"{self.name}"
class Prices(models.Model):
    price = models.FloatField()
    market = models.ForeignKey(Market,on_delete=models.CASCADE)
    affiliate_link = models.URLField()
    def __str__(self):
        return f"{self.price}"
class Products(models.Model):
    name = models.CharField(max_length=200)
    short_descriptions = models.TextField()
    long_descriptions = models.TextField()
    product_image = models.ManyToManyField(Image)
    prices = models.ManyToManyField(Prices)
    reviews = models.ManyToManyField(Reviews)
    market = models.ManyToManyField(Market)
    slug = models.SlugField(unique=True, blank=True, null=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Products, self).save(*args, **kwargs)
    def get_highest_price(self):
        if self.prices.exists():
            return max(price.price for price in self.prices.all())
        return None

    def get_lowest_price(self):
        if self.prices.exists():
            return min(price.price for price in self.prices.all())
        return None
    def get_average_rating(self):
        """
        Calculates the average rating for the product, rounding fractional averages down to the nearest integer.
        """
        if not self.reviews.exists():
            return None

        total_rating = sum(review.rating for review in self.reviews.all())
        average_rating = total_rating / self.reviews.count()

        # Round the average rating down to the nearest integer
        return int(math.floor(average_rating))

    def __str__(self):
        return f"{self.name}"

