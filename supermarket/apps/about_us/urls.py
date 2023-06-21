from django.urls import path
from .views import AboutUsView
app_name='about_us'

urlpatterns = [
    path('',AboutUsView.as_view(),name='about_us'),
]