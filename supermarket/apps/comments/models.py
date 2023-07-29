from django.db import models
from apps.products.models import Product
from apps.accounts.models import CustomUser
from django.core.validators import MaxValueValidator,MinValueValidator
from extensions.jalai_converter_maker import jalali_converter

#------------------------------------------------------------------------------- comment model
class Comment(models.Model):
    #--- foriegnkeys or manytomanyfields    
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='کالا',related_name='products_comments')
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='کاربر',related_name='main_user_comment')
    user_admin=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='ادمین تایید کننده',null=True,blank=True,related_name='extra_user_comment')
    comment_parent=models.ForeignKey('Comment',on_delete=models.CASCADE,null=True,blank=True,verbose_name='نظر فرعی',related_name='child_comments')
    # models attributes
    user_comment=models.TextField(verbose_name='نظر کاربر')
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج نظر')
    is_active=models.BooleanField(default=False,verbose_name='وضعیت نظر',)
    ## fields from oneTomany or manyTomany relationship --------------
    # child_comments=...
    
    def __str__(self):
        return f'{self.product} - {self.user_comment}'

    def comment_publish_date_jalai_type(self):
        return jalali_converter(self.register_date)
    comment_publish_date_jalai_type.short_description = 'زمان انتشار'
    
    class Meta:
        verbose_name='نظر در مورد کالا ها'
        verbose_name_plural='نظرات در مورد کالا ها'
#-------------------------------------------------------------------------------
