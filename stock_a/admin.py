from django.contrib import admin
from . import models

# Register your models here.

admin.site.register([models.Room, models.ChannelName, models.AllStock, models.Watchlist])