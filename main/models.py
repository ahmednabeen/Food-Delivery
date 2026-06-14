from django.db import models
from django.contrib.auth.models import User


def star_string(n):
    return '\u2605' * n + '\u2606' * (5 - n)


class Order(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    items = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.name}"


class Food(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    time = models.CharField(max_length=20, default='30 mins')
    rating = models.IntegerField(default=4, choices=[(i, star_string(i)) for i in range(1, 6)])
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

    def display_price(self):
        return f"Rs. {self.price}"
    display_price.short_description = 'Price'

    def star_rating(self):
        return star_string(self.rating)
    star_rating.short_description = 'Rating'


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
