from django.contrib import admin

# Register your models here.

from yrt import models
admin.site.register(models.user)
admin.site.register(models.studio)
admin.site.register(models.schedule1)
admin.site.register(models.schedule2)
admin.site.register(models.schedule3)
admin.site.register(models.schedule4)
admin.site.register(models.seat1)
admin.site.register(models.seat2)
admin.site.register(models.seat3)
admin.site.register(models.seat4)
admin.site.register(models.customer)
admin.site.register(models.opera)
admin.site.register(models.ticket)
admin.site.register(models.order)
