from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Blog,CommentBlog,Tag
from .forms import BlogForm
#------------------------------------------------------------------------------ blogs page  view 
class BlogsView(View):
    def get(self,request,*args,**kwargs):
        blogs=Blog.objects.filter(blog_is_active=True).order_by('blog_publish_date')
        blog_recents=Blog.objects.filter(blog_is_active=True).order_by('blog_publish_date')[:3]
        blog_tags=Tag.objects.filter().values('tag_name').distinct()  # distict method does not work properly in sqlit data base so I mix it with value method to slove this issue

        pagienator=Paginator(blogs,3) 
        page_number=request.GET.get('page')     # get current page number
        page_obj=pagienator.get_page(page_number) 
        return render(request,'blogs_app/blogs.html',{"page_obj":page_obj,'blog_recents':blog_recents,'blog_tags':blog_tags})

#------------------------------------------------------------------------------ blog page  view 
class BlogView(View):
    def get(self,request,*args,**kwargs):
        blog=get_object_or_404(Blog,blog_slug=kwargs['slug'])
        blog.blog_view_number+=1
        blog.save()
        blog_comment=CommentBlog.objects.filter(is_active=True).order_by('register_date')

        return render(request,'blogs_app/blog.html',{"blog":blog,'blog_comments':blog_comment})
    
#------------------------------------------------------------------------------ blog comment page  render partial 
class BlogFormView(View):
    def get(self,request,*args,**kwargs):
        slug=kwargs['slug']
        blog_form=BlogForm()
        return render(request,'blogs_app/blog_comment.html',{"blog_form":blog_form,'slug':slug})
    
    def post(self,request,*args,**kwargs):
        blog=get_object_or_404(Blog,blog_slug=kwargs['slug'])
        form_data=BlogForm(request.POST,request.FILES)
        if form_data.is_valid():
            clean_from_data=form_data.cleaned_data
            
            CommentBlog.objects.create(
                blog=blog,
                user=request.user,
                user_comment=clean_from_data['blog_comment'],
            )
            messages.success(request,'نظر شما با موفقیت ثبت شد')
            return redirect('blogs:blog',kwargs['slug'])
        
        messages.success(request,'خطا در ارسال نظر','danger')
        return redirect('blogs:blog',kwargs['slug'])

