from django.contrib import admin
from .models import Recipe, User, Recipe_User


# Register your models here.
admin.site.register(Recipe)
admin.site.register(User)
admin.site.register(Recipe_User)


