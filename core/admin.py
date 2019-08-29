from django.contrib import admin

# Register your models here.
from core.models import Plant, Datapoint

admin.site.register(Plant)
admin.site.register(Datapoint)