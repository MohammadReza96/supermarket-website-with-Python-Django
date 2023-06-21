from django.shortcuts import render,redirect
from django.views import View
from .models import ContactUsModel
from .forms import ContactUsForm
from django.contrib import messages
#---------------------------------------------------- contact us page view
class ContactUsView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'contactUs_app/contact_us.html')
#---------------------------------------------------- contact us form  view  as a render partial
class ContactUsFormView(View):
    def get(self,request,*args,**kwargs):
        user=request.user
        
        initial_data={
            'name':user.name,
            'family':user.family,
            'email':user.email
        }
        contact_us_form=ContactUsForm(initial=initial_data)
        
        return render(request,'contactUs_app/partials/contact_us_form.html',{'contact_us_form':contact_us_form})
    
    def post(self,request,*args,**kwargs):
        contact_us_form_data=ContactUsForm(request.POST,request.FILES)
        if contact_us_form_data.is_valid():
            contact_us_form_clean_data=contact_us_form_data.cleaned_data
            contact_us_model=ContactUsModel()
            contact_us_model.name=contact_us_form_clean_data['name']
            contact_us_model.family=contact_us_form_clean_data['family']
            contact_us_model.email=contact_us_form_clean_data['email']
            contact_us_model.topic=contact_us_form_clean_data['topic']
            contact_us_model.text=contact_us_form_clean_data['text']
            contact_us_model.save()
            
            messages.success(request,'نظر شما با موفقیت ثبت شد')
            return redirect('contact_us:contact_us')
        messages.success(request,'خطا در ارسال نظر','danger')
        return render(request,'contactUs_app/partials/contact_us_form.html',{'contact_us_form':contact_us_form_data})
