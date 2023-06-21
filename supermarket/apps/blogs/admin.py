from django.contrib import admin
from admin_decorators import short_description
from .models import Author,BlogGroup,Blog,Like,DisLike,CommentBlog,Tag,BlogGallary
from apps.accounts.models import CustomUser
#---------------------------------------------------------------------------------------------------  admin author
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display=('author_name','author_family','author_email','author_phone','auhtor_is_active')
    list_filter=('auhtor_is_active','author_name','author_family')
    search_fields=('author_family',)
#--------------------------------------------------------------------------------------------------- admin blog group
admin.site.register(BlogGroup)
#---------------------------------------------------------------------------------------------------  blog admin
############################################################ actions blog
@admin.action(description='غیر فعال کردن گروه های انتخاب شده')  
def deactive_blog_group(modeladmin,request,queryset):
    res=queryset.update(blog_is_active=False)
    message=f'تعداد {res} مقاله غیر فعال شد'
    modeladmin.message_user(request,message)
@admin.action(description='فعال کردن گروه های انتخاب شده')
def active_blog_group(modeladmin,request,queryset):
    res=queryset.update(blog_is_active=True)
    message=f'تعداد {res} مقاله  فعال شد'
    modeladmin.message_user(request,message)
########################################################### inlines for blog
class BlogGallaryinlineadmin(admin.TabularInline):
    model=BlogGallary
    extra=1
class BlogTaginlineadmin(admin.TabularInline):
    model=Tag
    extra=1

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display=('blog_title','blog_group','blog_view_number','blog_publish_date_jalai_type','blog_update_date','blog_is_active','author_list')
    list_filter=('blog_title',)
    ordering=('blog_publish_date',)
    search_fields=('blog_title',)
    list_editable=('blog_is_active',)
    inlines=[BlogTaginlineadmin,BlogGallaryinlineadmin] 
    actions=[deactive_blog_group,active_blog_group]
    
    #--- this functions is for adding a field to model in admin panel that gives us all the authors of 1 blog
    @short_description('نویسندگان مقاله')
    def author_list(self,obj):
        return ','.join([author.author_family for author in obj.blog_author.all()])

#--------------------------------------------------------------------------------------------------- like admin
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display=('user','blog','register_date')
    ordering=('register_date',)
#--------------------------------------------------------------------------------------------------- dislike admin
@admin.register(DisLike)
class DisLikeAdmin(admin.ModelAdmin):
    list_display=('user','blog','register_date')
    ordering=('register_date',)
#--------------------------------------------------------------------------------------------------- comment admin
@admin.register(CommentBlog)
class CommentBlogAdmin(admin.ModelAdmin):
    list_display=('user','blog','register_date','is_active')
    list_editable=('is_active',)
    ordering=('register_date',)
    
    #--- this function is for showing the only admin who is login and not other admins to confirm the comments
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user_admin':
            kwargs['queryset'] = CustomUser.objects.filter(mobile_number=request.user.mobile_number)
            return super(CommentBlogAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
