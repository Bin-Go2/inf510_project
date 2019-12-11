from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Flight)
admin.site.register(models.City)
admin.site.register(models.User)