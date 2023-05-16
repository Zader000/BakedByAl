from django.db import models
import json


# Create your models here.


class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateTimeField(auto_now_add=True)

    ORDER_STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Confirmed'),
        ('F', 'Fulfilled'),
        ('X', 'Cancelled')
    ]

    order_status = models.CharField(max_length=1, choices=ORDER_STATUS_CHOICES, default='P')

    def __str__(self):
        return self.name

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class OrderItem(models.Model):
    product = models.ForeignKey('GalleryItem', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class GalleryItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='gallery-images/', default="no-image.png", blank=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
