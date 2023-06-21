from django.contrib import admin
from .models import Scoring
from django.core import serializers   
from django.http import HttpResponse  
from django.contrib.admin.actions import delete_selected



#--------------------------------------------------------------------------------------------------------------------- score admin
########################################################### actions for product group
@admin.action(description='غیر فعال کردن گروه های انتخاب شده')
def deactive_score(modeladmin,request,queryset):
    res=queryset.update(group_isactive=False)
    message=f'تعداد {res} کالا غیر فعال شد'
    modeladmin.message_user(request,message)
@admin.action(description='فعال کردن گروه های انتخاب شده')
def active_score(modeladmin,request,queryset):
    res=queryset.update(group_isactive=True)
    message=f'تعداد {res} کالا  فعال شد'
    modeladmin.message_user(request,message)
@admin.action(description='خروجی جیسون از گروه های انتخاب شده')   
def export_json(modeladmin,request,queryset):
    response=HttpResponse(content_type='applicaton/json')
    serializers.serialize('json',queryset,stream=response)
    return response
delete_selected.short_description = 'پاک کردن مدل های انتخاب شده'

@admin.register(Scoring)
class ScoringAdmin(admin.ModelAdmin):
    list_display=('product','scoring_user','score')
    list_filter=('score',)
    actions=[deactive_score,active_score,export_json] 
