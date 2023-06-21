from django.contrib import admin
from apps.orders.models import Order,OrderDetails,PaymentType,DeilveryTime
from django.contrib.admin.actions import delete_selected
from django.http import HttpResponse  
from django.core import serializers   

#--------------------------------------------------------------------------------------------------------------------- payment type admin
@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display=('pyment_title',)

#--------------------------------------------------------------------------------------------------------------------- delivery time admin
########################################################### actions for delivery time
@admin.action(description='غیر فعال کردن گروه های انتخاب شده')
def deactive_delivery_day(modeladmin,request,queryset):
    res=queryset.update(group_isactive=False)
    message=f'تعداد {res} کالا غیر فعال شد'
    modeladmin.message_user(request,message)
@admin.action(description='فعال کردن گروه های انتخاب شده')
def active_delivery_day(modeladmin,request,queryset):
    res=queryset.update(group_isactive=True)
    message=f'تعداد {res} کالا  فعال شد'
    modeladmin.message_user(request,message)
delete_selected.short_description = 'پاک کردن مدل های انتخاب شده'

@admin.register(DeilveryTime)
class DeliveyDayAdmin(admin.ModelAdmin):
    list_display=('delivery_day','is_active')
    actions=[deactive_delivery_day,active_delivery_day] 
    list_editable=['is_active'] 
#--------------------------------------------------------------------------------------------------------------------- order admin
########################################################### actions for order
@admin.action(description='خروجی جیسون از گروه های انتخاب شده')   
def export_json(modeladmin,request,queryset):
    response=HttpResponse(content_type='applicaton/json')
    serializers.serialize('json',queryset,stream=response)
    return response
delete_selected.short_description = 'پاک کردن مدل های انتخاب شده'
########################################################### inlines for order
class OrderDetailsInline(admin.TabularInline):
    model=OrderDetails
    extra=3

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('customer','register_date','is_finally','discount','payment_type','delivery_day','is_delivered')
    list_filter=('is_delivered',)
    inlines=(OrderDetailsInline,)
    actions=[export_json] 
