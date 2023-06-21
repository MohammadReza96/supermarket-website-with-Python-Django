from django.db import models
from apps.accounts.models import CustomUser
from apps.products.models import Product
from django.utils import timezone
import uuid
from modules.price_discount_tax import get_price_delivery_tax


#------------------------------------------------------------------------------------------- paymenttype model
class PaymentType(models.Model):
    # models attributes
    pyment_title=models.CharField(max_length=100,verbose_name='نوع پرداخت')
    ## fields from oneTomany or manyTomany relationship --------------
    # payment_type=...
    
    def __str__(self):
        return f'{self.pyment_title}'
    
    class Meta:
        verbose_name='نوع پرداخت'
        verbose_name_plural='انواع روش پرداخت'
        
#------------------------------------------------------------------------------------------- deliverytime model
class DeilveryTime(models.Model):
    # models attributes
    delivery_day=models.CharField(max_length=50,verbose_name='زمان ارسال')
    is_active=models.BooleanField(default=False,verbose_name='وضعیت روز')
    
    def __str__(self):
        return f'{self.delivery_day}'
    
    class Meta:
        verbose_name='زمان ارسال'
        verbose_name_plural='زمان ارسال'
         
#------------------------------------------------------------------------------------------- order model
class Order(models.Model):
    # models attributes
    register_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ ثبت سفارش')
    update_date=models.DateTimeField(auto_now=True,verbose_name='تاریخ ویرایش سفارش')
    is_finally=models.BooleanField(default=False,verbose_name='نهایی شدن خرید')
    order_code=models.UUIDField(unique=True,default=uuid.uuid4,editable=False,verbose_name='کد تولیدی برای سفارش')  # for creating a special long code
    discount=models.IntegerField(default=0,blank=True,null=True,verbose_name='تخفیف روی فاکتور')
    discription=models.TextField(blank=True,null=True,verbose_name='توضیحات')
    #--- foriegnkeys or manytomanyfields
    customer=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='مشتری',blank=True,null=True,related_name='orders')
    payment_type=models.ForeignKey(PaymentType,on_delete=models.CASCADE,verbose_name='روش پرداخت',null=True,blank=True,related_name='payment_type')
    delivery_day=models.CharField(max_length=50,verbose_name='زمان ارسال',null=True,blank=True)
    is_delivered=models.BooleanField(default=False,verbose_name='وضعیت تحویل')
    ## fields from oneTomany or manyTomany relationship --------------
    # order_details=...
    # payment_order= ...
    
    #--- for calculating the final price after adding discounts in terminal
    def order_final_price(self):
        sum=0
        for item in self.order_details.all():
            sum+=item.product.get_finall_price_with_discount()*item.number
        # for getting the final_price & delivery & tax form external module
        final_price,delivery,tax=get_price_delivery_tax(sum,self.discount)
        
        return int(final_price*10)
        

    def __str__(self):
        return f'{self.id}\t{self.customer}\t{self.is_finally}'
    
    class Meta:
        verbose_name='سفارش'
        verbose_name_plural='سفارشات'

#------------------------------------------------------------------------------------------- orderdetails model
class OrderDetails(models.Model):
    #--- foriegnkeys or manytomanyfields    
    order=models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name='سفارش',related_name='order_details')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='کالا',related_name='order_details_product')
    # models attributes
    number=models.PositiveIntegerField(default=1,verbose_name='تعداد')
    price=models.IntegerField(verbose_name='قیمت کالا در فاکتور')
    
    def __str__(self):
        return f'{self.order}\t{self.product}'