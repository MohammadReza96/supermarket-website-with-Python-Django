from django.contrib import admin
from .models import DiscountBasket,DiscountBasketDetails,Coupon
from django.contrib.admin.actions import delete_selected
from django.http import HttpResponse  
from django.core import serializers   

#--------------------------------------------------------------------------------------------------------------------- coupon admin
########################################################### actions for discountbasket
@admin.action(description='غیر فعال کردن گروه های انتخاب شده')
def deactive_coupon(modeladmin,request,queryset):
    res=queryset.update(group_isactive=False)
    message=f'تعداد {res} کالا غیر فعال شد'
    modeladmin.message_user(request,message)
@admin.action(description='فعال کردن گروه های انتخاب شده')
def active_coupon(modeladmin,request,queryset):
    res=queryset.update(group_isactive=True)
    message=f'تعداد {res} کالا  فعال شد'
    modeladmin.message_user(request,message)
@admin.action(description='خروجی جیسون از گروه های انتخاب شده')   
def export_json(modeladmin,request,queryset):
    response=HttpResponse(content_type='applicaton/json')
    serializers.serialize('json',queryset,stream=response)
    return response
delete_selected.short_description = 'پاک کردن مدل های انتخاب شده'

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display=('coupon_code','start_date','end_date','discount','is_active')
    ordering=('is_active',)
    list_editable=['is_active',] 
    actions=[deactive_coupon,active_coupon,export_json] 

#--------------------------------------------------------------------------------------------------------------------- discountbasket admin
########################################################### actions for discountbasket
@admin.action(description='غیر فعال کردن گروه های انتخاب شده')
def deactive_discount_basket(modeladmin,request,queryset):
    res=queryset.update(group_isactive=False)
    message=f'تعداد {res} کالا غیر فعال شد'
    modeladmin.message_user(request,message)
@admin.action(description='فعال کردن گروه های انتخاب شده')
def active_discount_basket(modeladmin,request,queryset):
    res=queryset.update(group_isactive=True)
    message=f'تعداد {res} کالا  فعال شد'
    modeladmin.message_user(request,message)
@admin.action(description='خروجی جیسون از گروه های انتخاب شده')   
def export_json(modeladmin,request,queryset):
    response=HttpResponse(content_type='applicaton/json')
    serializers.serialize('json',queryset,stream=response)
    return response
delete_selected.short_description = 'پاک کردن مدل های انتخاب شده'
########################################################### inlines for discountbasket
class DiscountBasketDetailsinline(admin.TabularInline):   # for adding product to this DiscountBasket
    model=DiscountBasketDetails
    extra=2

@admin.register(DiscountBasket)
class DiscountBasketAdmin(admin.ModelAdmin):
    list_display=('discount_title','start_date','end_date','discount','is_active')
    ordering=('is_active',)
    inlines=(DiscountBasketDetailsinline,)
    actions=[deactive_discount_basket,active_discount_basket,export_json] 
    list_editable=['is_active',] 

