from django.shortcuts import render,get_object_or_404
from django.views import View
from django.http import HttpResponse
from apps.products.models import Product
from .models import Scoring
from django.db.models import Avg

#---------------------------------------------------------------------- scoring view
class UserScoreView(View):
    def get(self,request,*args,**kwargs):
        product_id=request.GET.get('product_id')
        score=request.GET.get('score')
        product=Product.objects.get(id=int(product_id))
        #--- creating score value for special product
        Scoring.objects.create(
            product=product,
            scoring_user=request.user,
            score=int(score)
        )
        return HttpResponse('امتیاز شما با موفقیت ثبت شد')

#--------------------------------------------------------------------- claculate score avg
def score_avg(request,*args,**kwargs):
    product_id=request.GET.get('product_id')
    product=get_object_or_404(Product,id=int(product_id))
    #--- calculating average_value
    average_score=Scoring.objects.filter(product=product).aggregate(average_score=Avg('score'))['average_score']
    #--- round value 
    final_average_score_value = round(average_score,2)
    return HttpResponse(final_average_score_value)
