from django.contrib import admin
from .models import Reminder, AdherenceRecord

admin.site.register(Reminder)
admin.site.register(AdherenceRecord)
