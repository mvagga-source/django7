from django.contrib import admin
from restaurants.models import *

admin.site.register(Location)
admin.site.register(LocationDetail)
admin.site.register(FoodCategory)
admin.site.register(FoodType)
admin.site.register(Restaurant)
admin.site.register(RestaurantOperTime)
admin.site.register(FoodMenu)
admin.site.register(Img)
admin.site.register(Comment)