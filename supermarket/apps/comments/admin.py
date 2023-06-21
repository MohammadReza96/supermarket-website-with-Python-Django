from django.contrib import admin
from .models import Comment
from apps.accounts.models import CustomUser

#------------------------------------------------------------- comment admin set up
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('product','register_date','user','user_admin','is_active')
    list_filter=('is_active',)
    list_editable=('is_active',)
    ordering=('register_date',)
    
    #--- for auto selecting the user base on login 
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user_admin':
            kwargs['queryset'] = CustomUser.objects.filter(mobile_number=request.user.mobile_number)
            return super(CommentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)