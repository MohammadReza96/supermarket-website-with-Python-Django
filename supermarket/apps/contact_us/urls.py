from django.urls import path
from .views import ContactUsView,ContactUsFormView
app_name='contact_us'

urlpatterns = [
    path('',ContactUsView.as_view(),name='contact_us'),
    path('contact_us_form/',ContactUsFormView.as_view(),name='contact_us_form'),
]