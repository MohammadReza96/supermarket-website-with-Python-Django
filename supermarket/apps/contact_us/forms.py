from django import forms


choices=[('انتقاد','انتقاد'),('پیشنهاد','پیشنهاد'),('محصول','محصول'),('ارسال','ارسال'),('در خواست موجودی','در خواست موجودی')]

class ContactUsForm(forms.Form):
    name=forms.CharField(max_length=20,widget=forms.TimeInput(attrs={'class':'form-control','placeholder':'نام'}),label='نام')
    family=forms.CharField(max_length=20,widget=forms.TimeInput(attrs={'class':'form-control','placeholder':'نام خانوادگی'}),label='نام خانوادگی')
    email=forms.EmailField(max_length=50,widget=forms.TimeInput(attrs={'class':'form-control','placeholder':'ایمیل'}),label='ایمیل کاربر')
    topic=forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control',"id":"form-subject"}),choices=choices,label='موضوع پیام')
    text=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'متن پیام','rows':'4'}),label='متن پیام')