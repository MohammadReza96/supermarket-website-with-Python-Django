from django.db import models
from apps.products.models import Product
from apps.accounts.models import CustomUser
#---------------------------------------------------------------------------  create warehousetype like (معیوبی \ قرضی \ ...)
class WarehouseType(models.Model):
    warehouse_type_title=models.CharField(max_length=50,verbose_name='نوع انبار')
    # fields from oneTomany or manyTomany relationship --------------
    # warehouses=...    
    
    def __str__(self):
        return self.warehouse_type_title
    
    class Meta:
        verbose_name='نوع انبار'
        verbose_name_plural='انواع روش های انبار داری'
#--------------------------------------------------------------------------- create warehouse model
class Warehouse(models.Model):
    #--- foriegnkeys or manytomanyfields
    warehouse_type=models.ForeignKey(WarehouseType,on_delete=models.CASCADE,verbose_name='انبار',related_name='warehouses')
    user_register=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='کاربر انبار دار',related_name='warehouse_registered')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='کالا',related_name='warehouse_products')
    # models attributes
    number=models.IntegerField(verbose_name='تعداد کالا',default=0)
    price=models.IntegerField(default=0,verbose_name='قیمت واحد',null=True,blank=True)
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت')
    
    def __str__(self):
        return f'{self.warehouse_type} \t {self.product}'
    
    class Meta:
        verbose_name='انبار'
        verbose_name_plural='انبارها'