from django import forms

class CoupenForm(forms.Form):
    coupen_code=forms.CharField(label='',error_messages={'required':"این فیلد نمی تواند خالی باشد"},widget=forms.TextInput(attrs={'class':'form-control','placeholder':'کد تخفیف'}))