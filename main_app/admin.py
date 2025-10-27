from django.contrib import admin
from .models import Part, Car, User, Review

# Register your models here.
admin.site.register(Part)
admin.site.register(Car)
admin.site.register(Review)

