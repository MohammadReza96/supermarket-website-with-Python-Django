from django.contrib import admin
from .models import ContactUsModel

@admin.register(ContactUsModel)
class ContactUsModelAdmin(admin.ModelAdmin):
    list_display=('name','family','email','topic','register_date')
    list_filter=('register_date',)
