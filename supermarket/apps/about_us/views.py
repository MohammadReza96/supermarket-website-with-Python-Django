from django.shortcuts import render
from django.views import View

#---------------------------------------------------- about us page view
class AboutUsView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'aboutUs_app/about_us.html')