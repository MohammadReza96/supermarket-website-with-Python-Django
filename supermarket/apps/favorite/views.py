from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from django.db.models import Q,Max,Min,Avg
from apps.products.models import Product
from .models import Favorite
#---------------------------------------------------------------------------------------- add to favorite list 
class AddToFavoriteView(View):
    def get(self,request,*args,**kwargs):
        product_id=request.GET.get('product_id')
        product_select=Product.objects.get(id=int(product_id))
        
        flag=Favorite.objects.filter(Q(user_favorite__id=request.user.id) & Q(product__id=product_id)).exists()
        
        # for checking that user like that special product berfore not 
        if  not flag :
            Favorite.objects.create(
                product=product_select,
                user_favorite=request.user
            )
            return HttpResponse('این کالا به لیست علایق شما اضافه شد')
        return HttpResponse('این کالا قبلا به لیست علایق شما اضافه شده است')
#---------------------------------------------------------------------------------------- favorite list view
class FavoriteProductView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'favorite_app/favorite_product_list.html')
#---------------------------------------------------------------------------------------- render partials for favorite list
#----------------------------------------------------- update favorite list count
def favorite_list_status(request,*args,**kwargs):
    favorite_list_count=Favorite.objects.filter(user_favorite__id=request.user.id).count()
    return HttpResponse(favorite_list_count)
#----------------------------------------------------- show favorite list 
def favorite_product_list(request,*args,**kwargs):
    favorite_product_list=Product.objects.filter(product_favorites__user_favorite_id=request.user.id)
    return render(request,'favorite_app/partials/favorite_list.html',{'favorite_product_list':favorite_product_list})
#----------------------------------------------------- delete product from favorite list
def delete_from_favorite_list(request,*args,**kwargs):
    product_id=int(request.GET.get('product_id'))
    Favorite.objects.filter(product__id=product_id).delete()
    return redirect("favorite:favorite_product_list")
