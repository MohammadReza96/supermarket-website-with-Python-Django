from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from .compare import CompareProduct
from apps.products.models import Product

#------------------------------------------------------------- shop card status in navbar
def status_compare_product(request):
    compare_product=CompareProduct(request)
    return HttpResponse(compare_product.item_count)

#------------------------------------------------------------- for showing the list of product for comparing
class CompareListView(View):
    def get(self,request,*args,**kwargs):
        compare_list=CompareProduct(request)
        context={'compare_list':compare_list}
        return render(request,'compare_app/compare_product_list.html',context)

#------------------------------------------------------------- render partial  show compare list refresh
def compare_products(request):
    compare_list=CompareProduct(request)
    products=[]
    
    for product_id in compare_list.compare_product:
        product=Product.objects.get(id=product_id)
        products.append(product)
        
    features=[]
    for product in products:
        for item in product.product_features.all():
            if item.product_feature_feature not in features:
                features.append(item.product_feature_feature)
    
    context={'products':products,'features':features}
    return render(request,'compare_app/compare_product.html',context)

#------------------------------------------------------------- render partial  add to compare product
def add_to_product_compare(request):
    product_id=int(request.GET.get('product_id'))
    compare_list=CompareProduct(request)
    
    #--- for checking whether the products has the same group or not
    if compare_list.compare_product:
        product_1=Product.objects.get(id=product_id)
        product_2=Product.objects.get(id=compare_list.compare_product[0])
        #--- because I set the product_group field as a manayTomany type in Product model , I use the below algorithm
        if product_1.product_group.all()[0] != product_2.product_group.all()[0]:
                return HttpResponse('کالا با گروه کالایی نا برابر قابل مقایسه نیست')
        else:
            pass
    
    compare_list.add_to_compare_product(product_id)
    return HttpResponse('کالا به لیست مقایسه اضافه شد')

#------------------------------------------------------------- render partial  remove from compare product
def delete_from_product_compare(request):
    product_id=int(request.GET.get('product_id'))
    compare_list=CompareProduct(request)
    compare_list.delete_from_compare_product(product_id)
    return redirect('compare:compare_product')