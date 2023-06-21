from django import forms
from apps.orders.models import PaymentType,DeilveryTime

#--------------------------------------------------------------------- orderform for changing customer information
class OrderForm(forms.Form):
    name=forms.CharField(max_length=100,label='نام',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام'}),error_messages={'required':'نام خود را وارد کنید'})
    family=forms.CharField(max_length=100,label='نام خانوادگی',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام خانوادگی'}),error_messages={'required':'فامیلی خود را وارد کنید'})
    email=forms.CharField(max_length=100,label='ایمیل',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'ایمیل'}),error_messages={'required':'این فیلد نمی تواند خالی باشد'},required=False)
    address=forms.CharField(max_length=100,label='ادرس',widget=forms.Textarea(attrs={'class':'form-control','placeholder':'ادرس'}),error_messages={'required':'آدرس خود را به دقت وارد کنید'})
    phone_number=forms.CharField(max_length=100,label='شماره موبایل',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل'}))
    discription=forms.CharField(max_length=100,label='توضیحات',widget=forms.Textarea(attrs={'class':'form-control','placeholder':'توضیحات'}),required=False)
    postal_number=forms.CharField(max_length=100,label='کد پستی',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'کد پستی'}),error_messages={'required':'کدپستی خود را به دقت وارد کنید'})
    city=forms.CharField(max_length=100,label='شهر',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شهر'}),error_messages={'required':'این فیلد نمی تواند خالی باشد'},required=False)
    province=forms.CharField(max_length=100,label='استان',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'استان'}),error_messages={'required':'این فیلد نمی تواند خالی باشد'},required=False)
    payment_type=forms.ChoiceField(label='روش پرداخت',choices=[ (item.id,item) for item in PaymentType.objects.all() ],widget=forms.RadioSelect(),error_messages={'required':'یک روش پرداخت را انتخاب کنید'})  #

#--------------------------------------------------------------------- deliveryform for setting the delivery day
class DeliveyDayForm(forms.Form):
    delivery_day=forms.ChoiceField(label='',choices=[ (item,item) for item in DeilveryTime.objects.all() ],widget=forms.Select(attrs={'class':'form-control'}),error_messages={'required':'یک روش پرداخت را انتخاب کنید'})  #
