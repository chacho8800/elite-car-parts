from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return f"{self.make} {self.model} {self.year}"

# Create your models here.
class Part(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    img = models.ImageField(upload_to='parts_images/', blank=True, null=True)
    price = models.IntegerField()
    part_number = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.part_number}"

 
class Review(models.Model):
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)

    def __str__(self):
        return f"Review By {self.user.username} for {self.part.name}"



