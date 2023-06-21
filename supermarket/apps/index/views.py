from django.shortcuts import render
from django.conf import settings
from django.views import View
from apps.blogs.models import Blog
from .models import SliderImage
from apps.products.models import Brand
from apps.products.models import ProductGroup
from django.db.models import Q
from apps.products.views import get_product_group
#--------------------------------------------------------- for loading media_url anywhere & everytime    ( add this function in TEMPLATES variable in setting)
def media_admin(request):
    return {'media_url':settings.MEDIA_URL}

#--------------------------------------------------------- for loading the product groups in navbar anywhere & everytime   ( add this function in TEMPLATES variable in setting)
def menu_loading(request):
    product_group_items=ProductGroup.objects.filter(~Q(group_parent=None) & Q(group_isactive=True))
    product_group_parrent=ProductGroup.objects.filter(Q(group_parent=None) & Q(group_isactive=True)).order_by('product_publish_date')
    return {'product_group_parrent':product_group_parrent,'product_group_items':product_group_items}

#--------------------------------------------------------- index page show
class IndexView(View):
    def get(self,request,*args,**kwargs):
        blogs=Blog.objects.filter(blog_is_active=True).order_by('blog_publish_date')
        brands=Brand.objects.all()
        slider_image=SliderImage.objects.filter(is_active=True).order_by('-register_date')
        product_group=get_product_group()
        
        return render(request,'index_app/index.html',{'slider_image':slider_image,'blogs':blogs,'brands':brands,'product_group':product_group})
