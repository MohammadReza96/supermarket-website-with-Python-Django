from django.db import models
from apps.orders.models import Order
from apps.accounts.models import CustomUser
from django.utils import timezone
from extensions.jalai_converter_maker import jalali_converter

#--------------------------------------------------------------------- payment view
class Payment(models.Model):
    #--- foriegnkeys or manytomanyfields
    order=models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name='سفارش',related_name='payment_order')
    customer=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='مشتری',related_name='payment_customer')
    # models attributes
    register_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ پرداخت')
    update_date=models.DateTimeField(auto_now=True,verbose_name='تاریخ ویرایش پرداخت')
    amount=models.IntegerField(verbose_name='مبلغ پرداخت')
    discription=models.TextField(verbose_name='توضیحات پرداخت')
    is_finaly=models.BooleanField(default=False,verbose_name='وضعیت پرداخت')
    status_code=models.IntegerField(verbose_name='کد وضعیت درگاه',null=True,blank=True)
    ref_id=models.CharField(max_length=50,verbose_name='شماره پیگیری پرداخت',null=True,blank=True)
    
    
    
    def __str__(self):
        return f'{self.order}\t{self.customer}\t{self.ref_id}'

    def Payment_register_date_jalai_type(self):
        return jalali_converter(self.register_date)
    Payment_register_date_jalai_type.short_description = 'زمان انتشار'
    
    class Meta :
        verbose_name='پرداخت'
        verbose_name_plural='پرداخت ها'