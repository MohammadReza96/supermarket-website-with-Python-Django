from django.urls import path
from .views import AddToFavoriteView,FavoriteProductView,favorite_product_list,delete_from_favorite_list,favorite_list_status
app_name='favorite'

urlpatterns = [
    path('add_to_favorite/',AddToFavoriteView.as_view(),name='add_to_favorite'),
    path('favorite_product_list/',FavoriteProductView.as_view(),name='favorite_product'),
    path('favorite_product/',favorite_product_list,name='favorite_product_list'),
    path('favorite_list_status/',favorite_list_status,name='favorite_list_status'),
    path('delete_from_favorite_list/',delete_from_favorite_list,name='delete_from_favorite_list'),
]