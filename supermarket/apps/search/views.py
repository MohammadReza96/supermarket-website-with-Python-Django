from django.shortcuts import render
from django.views import View
from django.db.models import Q,Avg,Max,Min
from apps.products.models import Product
from apps.blogs.models import Blog

#----------------------------------------------------- search view (base on product & blogs)
class SearchResultView(View):
    def get(self,request,*args,**kwargs):
        search_value=request.GET.get('search')
        product_list=Product.objects.filter(Q(product_name__icontains=search_value))
        blog_list=Blog.objects.filter(Q(blog_title__icontains=search_value))
        return render(request,'search_app/search_app.html',{'product':product_list,'blog_list':blog_list})
        