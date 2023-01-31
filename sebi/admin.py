from django.contrib import admin
from . import models

# Register your models here.


class CustomShareAdmin(admin.ModelAdmin):
    readonly_fields = ('unique_id',)

admin.site.register(models.Share, CustomShareAdmin)