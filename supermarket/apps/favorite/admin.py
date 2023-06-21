from django.contrib import admin
from .models import Favorite
#------------------------------------------------------ Favorite admin set up
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display=['product','user_favorite']