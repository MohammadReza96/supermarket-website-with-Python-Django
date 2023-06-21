from django.urls import path
from .views import cheapest_product,newest_product,favorite_product,related_product,ProductGroupView,ProductDetailView,get_product_group_filter,get_brand,get_other_features_for_each_group,ProductByGroupView,topsell_product
app_name='products'

urlpatterns = [
    path('cheapest_product/',cheapest_product,name='cheapest_product'),
    path('newest_product/',newest_product,name='newest_product'),
    path('topsell_product/',topsell_product,name='topsell_product'),
    path('favorite_product/',favorite_product,name='favorite_Product'),
    path('related_product/<slug:slug>/',related_product,name='related_product'),
    path('product_group/',ProductGroupView.as_view(),name='product_group'),
    path('product_detail/<slug:slug>/',ProductDetailView.as_view(),name='product_detail'),
    path('product_groups_partial/',get_product_group_filter,name='product_groups_partial'),
    path('product_groups_brand/<slug:slug>',get_brand,name='product_groups_brand'),
    path('product_other_filter/<slug:slug>',get_other_features_for_each_group,name='product_other_filter'),
    path('products_by_group/<slug:slug>',ProductByGroupView.as_view(),name='products_by_group'),
]