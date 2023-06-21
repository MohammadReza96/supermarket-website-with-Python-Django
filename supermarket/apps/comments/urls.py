from django.urls import path
from .views import CommentView
app_name='comments'

urlpatterns = [
    path('create_comment/<slug:slug>',CommentView.as_view(),name='create_comment'),
]