from django.db import models
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from apps.products.models import Product


#--------------------------------------------------------------------------------------------------------------------  coupon code for 1 product
class Coupon(models.Model):
    # models attributes
    coupon_code=models.CharField(max_length=10,unique=True,verbose_name='کد کوپن')
    start_date=models.DateTimeField(verbose_name='تاریخ شروع')
    end_date=models.DateTimeField(verbose_name='تاریخ پایان')
    discount=models.IntegerField(verbose_name='درصد تخفیف',validators=[MinValueValidator(0),MaxValueValidator(100)],default=0)
    is_active=models.BooleanField(verbose_name='وضعیت',default=False)
    
    class Meta:
        verbose_name='کوپن'
        verbose_name_plural='کوپن ها'
        
    def __str__(self):
        return f'{self.coupon_code}'
#--------------------------------------------------------------------------------------------------------------------- coupon code for all product beacuse of a special event
class DiscountBasket(models.Model):
    # models attributes
    discount_title=models.CharField(max_length=100,verbose_name='عنوان سبد تخفیف')
    start_date=models.DateTimeField(verbose_name='تاریخ شروع')
    end_date=models.DateTimeField(verbose_name='تاریخ پایان')
    discount=models.IntegerField(verbose_name='درصد تخفیف',validators=[MinValueValidator(0),MaxValueValidator(100)])
    is_active=models.BooleanField(verbose_name='وضعیت',default=False)
    # fields from oneTomany or manyTomany relationship --------------
    # discount_basket_detail=...  

    class Meta:
        verbose_name='سبد تخفیف'
        verbose_name_plural='سبد های تخفیف'
        
    def __str__(self):
        return f'{self.discount_title}'
#---------------------------------------------------------------------------------------------------------------------
class DiscountBasketDetails(models.Model):
    #--- foriegnkeys or manytomanyfields
    discount_basket=models.ForeignKey(DiscountBasket,on_delete=models.CASCADE,verbose_name='سبد تخفیف',related_name='discount_basket_detail')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='کالا',related_name='discount_basket_detail_product')
    
    class Meta:
        verbose_name='جزعیات سبد تخفیف'
