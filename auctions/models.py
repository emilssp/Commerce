from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length=32)
    def __str__(self):
        return f"{self.title}"

class Item(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_price= models.DecimalField(max_digits=8, decimal_places=2)
    is_closed = models.BooleanField(default=False)
    image = models.ImageField(upload_to='items', default='items/default.jpg')

    watch=models.ManyToManyField(User, related_name='watch', blank=True, null=True)
    creator = models.ForeignKey(User, related_name='listings',blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, related_name='listings', on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.title}"

    def add_to_watchlist (self,id):
        self.watch.add(id)

    def remove_from_watchlist (self,id):
        self.watch.remove(id)


class Bid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, related_name='bids',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.bidder} {self.price}"

class Comment(models.Model):
    post = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, default="Unknown", on_delete=models.SET_DEFAULT, related_name='author')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(User, related_name='upvotes', blank=True)
    def __str__(self):
        return self.text

    def like (self):
        pass

    def dislike (self):
        pass
