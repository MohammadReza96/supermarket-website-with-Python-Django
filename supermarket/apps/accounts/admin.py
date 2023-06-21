from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.accounts.forms import UserCreationForm,UserChangeForm
from apps.accounts.models import CustomUser
#---------------------------------------------- 

class CustomUserAdmin(UserAdmin):
    form =UserChangeForm
    add_form =UserCreationForm
    list_display= ('user_name','mobile_number','email','name','family','is_active','is_admin')
    list_filter=('is_active','is_admin','family')
    
    # modify user
    fieldsets =(
        ('login details',{'fields':('user_name','password')}),
        ('personal info',{'fields':('mobile_number','email','name','family','image','address','city','province','postal_code','active_code')}),
        ('permissions',{'fields':('is_active','is_admin','is_superuser','groups','user_permissions')})
    )
    
    # create user
    add_fieldsets =(
        ('account details',{'fields':('user_name','mobile_number','email','name','family','password','re_password')}),
    )
    
    search_fields=('user_name',)
    ordering = ('user_name',)
    filter_horizontal =('groups','user_permissions')

admin.site.register(CustomUser,CustomUserAdmin)