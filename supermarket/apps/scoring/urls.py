from django.urls import path
from .views import UserScoreView,score_avg
app_name='scoring'

urlpatterns = [
    path('user_score/',UserScoreView.as_view(),name='user_score'),
    path('average_score_update/',score_avg,name='average_score_update'),
]