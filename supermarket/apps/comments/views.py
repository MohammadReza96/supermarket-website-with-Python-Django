from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib import messages
from .forms import CommentForm
from .models import Comment
from apps.products.models import Product

#------------------------------------------------- comment view 
class CommentView(View):
    def get(self,request,*args,**kwargs):
        comment_id=request.GET.get('comment_id')
        product_slug=kwargs['slug']
        
        dic_data={
            'comment_id':comment_id
        }
        main_from=CommentForm(initial=dic_data)
        return render(request,'comment_app/partials/create_comment.html',{'form':main_from,'slug':product_slug})
    
    def post(self,request,*args,**kwargs):
        product=get_object_or_404(Product,product_slug=kwargs.get('slug'))
        form_data=CommentForm(request.POST,request.FILES)
        if form_data.is_valid():
            clean_from_data=form_data.cleaned_data
            
            parent=None
            if clean_from_data['comment_id']:
                parent=Comment.objects.get(id=clean_from_data['comment_id'])
            
            Comment.objects.create(
                product=product,
                user=request.user,
                user_comment=clean_from_data['main_comment'],
                comment_parent=parent
            )
            messages.success(request,'نظر شما با موفقیت ثبت شد')
            return redirect('products:product_detail',product.product_slug)
        
        messages.success(request,'خطا در ارسال نظر','danger')
        return redirect('products:product_detail',product.product_slug)