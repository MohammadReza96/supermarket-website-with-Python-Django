from django import forms
#------------------------------------------------------------
class BlogForm(forms.Form):
    blog_comment=forms.CharField(label='',error_messages={'required':'این فیلد نمی تواند خالی باشد'},widget=forms.Textarea(attrs={'class':'form-control','placeholder':'متن نظر','rows':'4'}))
#------------------------------------------------------------