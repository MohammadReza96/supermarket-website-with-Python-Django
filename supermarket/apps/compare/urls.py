from django.urls import path
from .views import CompareListView,add_to_product_compare,compare_products,delete_from_product_compare,status_compare_product
app_name='compare'

urlpatterns = [
    path('compare_products_list/',CompareListView.as_view(),name='compare_products_list'),
    path('compare_product/',compare_products,name='compare_product'),
    path('add_to_product_compare/',add_to_product_compare,name='add_to_product_compare'),
    path('delete_from_product_compare/',delete_from_product_compare,name='delete_from_product_compare'),
    path('status_compare_product/',status_compare_product,name='status_compare_product'),
]