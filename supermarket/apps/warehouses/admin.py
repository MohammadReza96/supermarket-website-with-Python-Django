from django.contrib import admin
from .models import Warehouse,WarehouseType
from apps.accounts.models import CustomUser
from django.contrib.admin.actions import delete_selected
from django.core import serializers   
from django.http import HttpResponse  

#------------------------------------------------------------------------------------------------ warehouse admin 
########################################################### actions for warehouse
@admin.action(description='غیر فعال کردن گروه های انتخاب شده')
def deactive_warehouse(modeladmin,request,queryset):
    res=queryset.update(group_isactive=False)
    message=f'تعداد {res} کالا غیر فعال شد'
    modeladmin.message_user(request,message)
@admin.action(description='فعال کردن گروه های انتخاب شده')
def active_warehouse(modeladmin,request,queryset):
    res=queryset.update(group_isactive=True)
    message=f'تعداد {res} کالا  فعال شد'
    modeladmin.message_user(request,message)
@admin.action(description='خروجی جیسون از گروه های انتخاب شده')   
def export_json(modeladmin,request,queryset):
    response=HttpResponse(content_type='applicaton/json')
    serializers.serialize('json',queryset,stream=response)
    return response
delete_selected.short_description = 'پاک کردن مدل های انتخاب شده'
########################################################### inlines for warehouse

@admin.register(WarehouseType)
class WarehouseTypeAdmin(admin.ModelAdmin):
    list_display=['warehouse_type_title',]
    
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display=['product','warehouse_type','user_register','number','price','register_date']
    actions=[deactive_warehouse,active_warehouse,export_json] 

    
    #--- for auto selecting the user base on login 
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user_register':
            kwargs['queryset'] = CustomUser.objects.filter(mobile_number=request.user.mobile_number)
        return super(WarehouseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)