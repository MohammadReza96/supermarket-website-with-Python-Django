from django.urls import path
from .views import BlogsView,BlogView,BlogFormView
app_name='blogs'

urlpatterns = [
    path('blogs/',BlogsView.as_view(),name='blogs'),
    path('blog/<slug:slug>',BlogView.as_view(),name='blog'),
    path('blog_comment/<slug:slug>',BlogFormView.as_view(),name='blog_comment'),
]