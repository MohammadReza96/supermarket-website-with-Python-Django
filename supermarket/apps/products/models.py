from django.db import models

from django.db import models
from modules.file_upload_module import FileUploader
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
import datetime
from middlewares.middlewares import RequestMiddleware
from django.db.models import Q,Sum,Avg

# #----------------------------------------------------------------------------------------------------   Brand
class Brand(models.Model):
    # upload_image module
    file_upload=FileUploader('images','Brand')
    # models attributes
    brand_name=models.CharField(max_length=50,verbose_name='نام برند')
    brand_slug=models.SlugField(max_length=50,null=True)
    brand_image=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر برند')
    ## fields from oneTomany or manyTomany relationship --------------
    # brands= .....
    
    def __str__(self):
        return self.brand_name
    
    class Meta:
        verbose_name='برند'
        verbose_name_plural='برند ها'
        
# #----------------------------------------------------------------------------------------------------  ProductGroup
class ProductGroup(models.Model):
    # upload_image module
    file_upload=FileUploader('images','product_group')
    # models attributes
    group_name=models.CharField(max_length=50,verbose_name='عنوان گروه کالا')
    group_slug=models.SlugField(max_length=50,null=True,verbose_name='شناسه گروه کالا')
    group_image=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر گروه کالا')
    group_isactive=models.BooleanField(default=False,verbose_name='وضعیت گروه',blank=True) #
    product_registerdate=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    product_publish_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ انتشار')
    product_update_date=models.DateTimeField(auto_now=True,verbose_name='تاریخ بروزرسانی')
    #--- foriegnkeys or manytomanyfields
    group_parent=models.ForeignKey('ProductGroup',on_delete=models.CASCADE,verbose_name='والد گروه کالا',blank=True,null=True,related_name='groups') # way 1
    # group_parent=models.ForeignKey('self',on_delete=models.CASCADE,verbose_name='والد گروه کالا',blank=True,null=True,related_name='groups') # way 2
    ## fields from oneTomany or manyTomany relationship --------------
    # groups=...
    # products_of_group=.....
    # features_of_group=.....
    
    def __str__(self):
        return self.group_name
    
    class Meta:
        verbose_name='گروه محصول'
        verbose_name_plural='گروه های محصولات'

# #----------------------------------------------------------------------------------------------------  Feature
class Feature(models.Model):
    # models attributes
    feature_name=models.CharField(max_length=50,verbose_name='نام ویژگی')
    feature_slug=models.SlugField(max_length=100,verbose_name='شناسه ویژگی',null=True,blank=True)
    product_group=models.ManyToManyField(ProductGroup,verbose_name='گروه کالا',related_name='features_of_group')
    ## fields from oneTomany or manyTomany relationship --------------
    # feature_value=...
    
    def __str__(self):
        return self.feature_name
    
    class Meta:
        verbose_name='ویژگی'
        verbose_name_plural='ویژگی ها'
        
# #----------------------------------------------------------------------------------------------------  Product
class Product(models.Model):
    # upload_image module
    file_upload=FileUploader('images','product')
    # models attributes
    product_name=models.CharField(max_length=300,verbose_name='نام محصول')
    product_summery_description=RichTextUploadingField(verbose_name='خلاصه توضیحات کالا',blank=True,null=True)  # with ckeditor
    product_description=RichTextUploadingField(verbose_name='توضیحات کالا',blank=True,null=True)  # with ckeditor
    product_image=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر محصول')
    product_price=models.PositiveBigIntegerField(default=0,verbose_name='قیمت محصول')
    product_isactive=models.BooleanField(default=False,verbose_name='وضعیت کالا',blank=True)
    product_slug=models.SlugField(max_length=50,null=True,verbose_name='شناسه کالا')
    product_registerdate=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    product_publish_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ انتشار')
    product_expire_date=models.DateField(default=timezone.now,verbose_name='تاریخ انقضا')
    product_update_date=models.DateTimeField(auto_now=True,verbose_name='تاریخ بروزرسانی')
    #--- foriegnkeys or manytomanyfields
    product_brand=models.ForeignKey(Brand,on_delete=models.CASCADE,null=True,related_name='brands')
    product_feature=models.ManyToManyField(Feature,through='ProductFeature') #
    product_group=models.ManyToManyField(ProductGroup,verbose_name='گروه کالا',related_name='products_of_group')
    # fields from oneTomany or manyTomany relationship --------------
    # product_features= ...
    # product_gallary= ...
    # product_favorites= ...                         from favorite app
    # warehouse_products=...                         from warehouses app
    # discount_basket_detail_product=...             from discount app
    # products_comments=...                          from comment app
    # product_score=...                              from scoring app
    # blog_product=...                               from blog app
    # order_details_product=...                      from order app
    
    def __str__(self):
        return self.product_name
        
    #--- for having product link to detail each time
    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"slug": self.product_slug})
    
    #--- for getting favorite for each product  for each user
    def get_user_favorite(self):
        request=RequestMiddleware(get_response=None)
        request=request.thread_local.current_request
        # output is True/False
        flag=self.product_favorites.filter(user_favorite=request.user).exists()
        return flag
    
    #--- getting number of product in warehouse
    def get_warehouse_status(self):
        num_buy=self.warehouse_products.filter(warehouse_type=1).aggregate(num_buy=Sum('number'))
        num_sell=self.warehouse_products.filter(warehouse_type=2).aggregate(num_sell=Sum('number'))
        num_reject=self.warehouse_products.filter(warehouse_type=3).aggregate(num_reject=Sum('number'))
        num_issued=self.warehouse_products.filter(warehouse_type=4).aggregate(num_issued=Sum('number'))
        num_lent=self.warehouse_products.filter(warehouse_type=5).aggregate(num_lent=Sum('number'))
        num_borrowed=self.warehouse_products.filter(warehouse_type=6).aggregate(num_borrowed=Sum('number'))
        
        input,output,rejected,issued,lent,borrowed=0,0,0,0,0,0
        if num_buy['num_buy']!=None:
            input=num_buy['num_buy']
        if num_sell['num_sell']!=None:
            output=num_sell['num_sell']
        if num_reject['num_reject']!=None:
            rejected=num_reject['num_reject']
        if num_issued['num_issued']!=None:
            issued=num_sell['num_issued']
        if num_lent['num_lent']!=None:
            lent=num_lent['num_lent']
        if num_borrowed['num_borrowed']!=None:
            borrowed=num_borrowed['num_borrowed']
            
        return input-output+borrowed+rejected-lent-issued
    
    #--- for getting price with discount
    def get_finall_price_with_discount(self):
        current_price=self.product_price
        time_now=datetime.datetime.now()
        discount_list=[]
        discount_get=self.discount_basket_detail_product.all()
        
        for item in discount_get:
            if item.discount_basket.is_active==True and item.discount_basket.end_date>=time_now and item.discount_basket.start_date<=time_now :
                discount_list.append(item.discount_basket.discount)
        
        final_discount=0
        if len(discount_list)>0:
            final_discount=max(discount_list)
        
        return current_price-((current_price*final_discount)/100)

    #--- for getting all active comment for a product
    def get_product_comments(self):
        all_comments=self.products_comments.filter(is_active=True)
        return all_comments
    
    #--- for getting all active blogs for a product
    def get_product_blogs(self):
        all_blogs=self.blog_product.filter(is_active=True)
        return all_blogs

    #--- for getting the score of each product by each user
    def get_score_product_for_each_user(self):
        request=RequestMiddleware(get_response=None)
        request=request.thread_local.current_request        
        score=0
        user_score=self.product_score.filter(scoring_user=request.user)
        if user_score.count()>0:
            score=user_score[0].score
        return score
    
    #--- for getting the average score of each product 
    def get_average_score_for_each_product(self):
        average_score=0
        average_score_product=self.product_score.all().aggregate(average_score=Avg('score'))['average_score']
        if average_score_product!=None:
            average_score="{:.2f}".format(average_score_product)  # formating for having only 2 decimal number
        return average_score
                
                
                
    class Meta:
        verbose_name='محصول'
        verbose_name_plural='محصولات'

# #----------------------------------------------------------------------------------------------------  FeatureValue
class FeatureValue(models.Model):    # we can use this model in inline mode in feature model
    # models attributes
    value_title=models.CharField(max_length=100,verbose_name='مقدار ویژگی')
    #--- foriegnkeys or manytomanyfields
    feature=models.ForeignKey(Feature,on_delete=models.CASCADE,verbose_name='ویژگی',null=True,blank=True,related_name='feature_value')
    ## fields from oneTomany or manyTomany relationship --------------
    # filter_values=...
    
    def __str__(self):
        return f'{self.value_title}'
    
    class Meta:
        verbose_name='مقدار ویژگی'
        verbose_name_plural='مقدار ویژگی ها'
        
# #----------------------------------------------------------------------------------------------------   ProductFeature
class ProductFeature(models.Model):  # we can use this model in inline mode in product model
    # models attributes
    value=models.CharField(max_length=100,verbose_name='مقدار ویژگی محصول')
    #--- foriegnkeys or manytomanyfields
    product_feature_product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='محصول',related_name='product_features')
    product_feature_feature=models.ForeignKey(Feature,on_delete=models.CASCADE,verbose_name='ویژگی')
    filter_value=models.ForeignKey(FeatureValue,null=True,blank=True,on_delete=models.CASCADE,verbose_name='مقدار فیلتر',related_name='filter_values')
    def __str__(self):
        return f'{self.product_feature_feature}'
    
    class Meta:
        verbose_name='ویژگی محصول'
        verbose_name_plural='ویژگی های محصولات'
# #----------------------------------------------------------------------------------------------------  ProductGallary
class ProductGallary(models.Model):
    # upload_image
    file_upload=FileUploader('images','product_gallary')
    #--- foriegnkeys or manytomanyfields
    product_gallary_product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='',related_name='product_gallary')
    # models attributes
    product_gallary_image=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر محصول')

    def __str__(self):
        return str(self.product_gallary_image)
    
    class Meta:
        verbose_name='تصویر محصول'
        verbose_name_plural='تصویر های محصول'

# #----------------------------------------------------------------------------------------------------
