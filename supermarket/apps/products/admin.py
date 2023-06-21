from django.contrib import admin
from apps.products.models import Brand,Feature,Product,ProductGroup,ProductFeature,ProductGallary,FeatureValue
from django.db.models.aggregates import Count,Sum,Max,Min
from django.http import HttpResponse  
from django.core import serializers   
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from django.contrib.admin.actions import delete_selected
from django.db.models import Q
from django.contrib.admin import SimpleListFilter
from admin_decorators import short_description,order_field 


#--------------------------------------------------------------------------------------------------------------------- brand admin
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display=('brand_name','brand_slug')
    list_filter=('brand_name',)
    search_fields=('brand_name',)
    ordering=('brand_name',)
#--------------------------------------------------------------------------------------------------------------------- productGroup admin
########################################################### actions for product group
@admin.action(description='غیر فعال کردن گروه های انتخاب شده')
def deactive_product_group(modeladmin,request,queryset):
    res=queryset.update(group_isactive=False)
    message=f'تعداد {res} کالا غیر فعال شد'
    modeladmin.message_user(request,message)
@admin.action(description='فعال کردن گروه های انتخاب شده')
def active_product_group(modeladmin,request,queryset):
    res=queryset.update(group_isactive=True)
    message=f'تعداد {res} کالا  فعال شد'
    modeladmin.message_user(request,message)
@admin.action(description='خروجی جیسون از گروه های انتخاب شده')   
def export_json(modeladmin,request,queryset):
    response=HttpResponse(content_type='applicaton/json')
    serializers.serialize('json',queryset,stream=response)
    return response
delete_selected.short_description = 'پاک کردن مدل های انتخاب شده'
########################################################### inlines for productGroup
class ProductGroupInlineAdmin(admin.TabularInline): 
    model=ProductGroup
    extra=1
#--- this class is for creating special filter (lookups and queryset must declare)
class GroupFilter(SimpleListFilter):
    title='گروه محصولات'
    parameter_name='Group'
    
    def lookups(self,request:any,model_admin:any):
        sub_group=ProductGroup.objects.filter(~Q(group_parent=None))
        groups=set(item.group_parent for item in sub_group)
        return [ (item.id,item.group_name) for item in groups]

    def queryset(self,request,queryset):
        if self.value()!=None:
            return queryset.filter(group_parent=self.value())
        return queryset
#----------------------------------
@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display=('id','group_name','group_slug','group_isactive','group_parent','product_registerdate','product_update_date','count_sub_group','count_sub_product_group')
    list_filter=(GroupFilter,'group_isactive')
    search_fields=('group_name',)
    ordering=('group_parent__id','group_name',)
    inlines=[ProductGroupInlineAdmin] 
    actions=[deactive_product_group,active_product_group,export_json] 
    list_editable=['group_isactive'] 
    #####################################
    def get_queryset(self,*args,**kwargs): # for creating an special field that does not exist in model  
        qs=super(ProductGroupAdmin,self).get_queryset(*args,**kwargs)
        qs=qs.annotate(sub_group=Count('groups'),sub_product_group=Count('products_of_group'))
        return qs
    
    @short_description('تعداد زیر گروه ها')
    def count_sub_group(self,obj):  # for adding in model
        return obj.sub_group
    
    @short_description('تعداد محصولات هر زیر گروه')   # for changing the name of this field  (second way)
    def count_sub_product_group(self,obj):  # for adding in model
        return obj.sub_product_group
    #####################################
#--------------------------------------------------------------------------------------------------------------------- product admin
########################################################### actions for product
@admin.action(description='غیر فعال کردن گروه های انتخاب شده')
def deactive_product(modeladmin,request,queryset):
    res=queryset.update(product_isactive=False)
    message=f'تعداد {res} کالا غیر فعال شد'
    modeladmin.message_user(request,message)
@admin.action(description='فعال کردن گروه های انتخاب شده')
def active_product(modeladmin,request,queryset):
    res=queryset.update(product_isactive=True)
    message=f'تعداد {res} کالا  فعال شد'
    modeladmin.message_user(request,message)
delete_selected.short_description = 'پاک کردن مدل های انتخاب شده'
########################################################### inlines for product
class ProductFeatureInlineAdmin(admin.TabularInline):
    model=ProductFeature
    extra=1
class ProductGalleryInlineAdmin(admin.TabularInline):
    model=ProductGallary
    extra=5
#--- this class is for creating special filter (lookups and queryset must declare)
class GroupFilter(SimpleListFilter):
    title='گروه محصولات'
    parameter_name='Group'
    
    #--- this function is for showing options for select
    def lookups(self,request:any,model_admin:any):
        sub_group=ProductGroup.objects.filter(~Q(group_parent=None))
        groups=set(item for item in sub_group)
        return [ (item.group_name,item.group_name) for item in groups]
    #--- this function is for seting the selected option  (self.value)  with the product_group field in each Product
    def queryset(self,request,queryset):  
        if self.value()!=None:             # return  ProductGroup name (it depends of item.group_name )
            return queryset.filter(product_group__group_name=self.value())
        return queryset

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','product_brand','product_price','product_isactive','product_update_date','product_expire_date','list_product_group')
    list_filter=(('product_brand', RelatedDropdownFilter),GroupFilter)
    search_fields=('product_name',)
    ordering=('product_update_date','product_name')
    actions=[deactive_product,active_product]
    inlines=[ProductFeatureInlineAdmin,ProductGalleryInlineAdmin]
    list_editable=['product_isactive']    
    
    #--- this function show us the groups that the product is related to    
    @short_description('گروه های کالا')
    def list_product_group(self,obj):
        return '-'.join([item.group_name for item in obj.product_group.all()])
    
    #--- this function is for not showing mainfathers in productgroup 
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name=='product_group':
            kwargs['queryset']=ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field,request,**kwargs)
    
    #--- this part for arranging the product form view in admin panel
    fieldsets =(
        ('اطلاعات محصول',{'fields':('product_name','product_slug','product_price','product_image',('product_group','product_brand','product_isactive'),'product_summery_description','product_description')}),
        ('تاریخ و زمان',{'fields':('product_publish_date','product_expire_date')}),
    )
#--------------------------------------------------------------------------------------------------------------------- feature admin
########################################################### actions for feature
@admin.action(description='غیر فعال کردن گروه های انتخاب شده')
def deactive_product(modeladmin,request,queryset):
    res=queryset.update(product_isactive=False)
    message=f'تعداد {res} کالا غیر فعال شد'
    modeladmin.message_user(request,message)
@admin.action(description='فعال کردن گروه های انتخاب شده')
def active_product(modeladmin,request,queryset):
    res=queryset.update(product_isactive=True)
    message=f'تعداد {res} کالا  فعال شد'
    modeladmin.message_user(request,message)
delete_selected.short_description = 'پاک کردن مدل های انتخاب شده'
########################################################### inlines for feature
class FeatureValueInlineAdmin(admin.TabularInline):
    model=FeatureValue
    extra=1

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display=('feature_name','display_group','display_feature_value')
    list_filter=('feature_name',)
    search_fields=('feature_name',)
    ordering=('feature_name',)
    actions=[deactive_product,active_product]
    inlines=[FeatureValueInlineAdmin]
    
    #--- this function remove the groups that has the group parrent none when we want to select in admin panel   
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name=='product_group':
            kwargs['queryset']=ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    #--- this function show us the groups that the feature is related to    
    @short_description('گروه های دارای این ویژگی')
    def display_group(self,obj):
        return ','.join([group.group_name for group in obj.product_group.all()])
    
    #--- this function show us the possible value for each feature    
    @short_description('مقادیر ممکن برای این ویژگی')
    def display_feature_value(self,obj):
        return ','.join([feature_value.value_title for feature_value in obj.feature_value.all()])