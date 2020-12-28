from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.


class ProductInfo(models.Model):
    title = models.CharField(max_length=15)
    image = models.TextField()
    price = models.CharField(max_length=5)

    def __str__(self):
        return self.title + '| ' + str(self.id)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    proceed = models.BooleanField(default=True)

    def __str__(self):
        return self.item.title + ' | ' + self.user.username + ' | ' + str(self.id)


class BoughtItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.user.username + ' | ' + self.item.title
