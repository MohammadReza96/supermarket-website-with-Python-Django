from django.contrib import admin
from .models import SliderImage

#------------------------------------------------------ sliderimage admin
@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display=('slider_name','slider_title','register_date','is_active')
    ordering=('register_date',)
