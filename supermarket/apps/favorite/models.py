from django.db import models
from apps.products.models import Product
from apps.accounts.models import CustomUser

#------------------------------------------------------------ create model for favorite list
class Favorite(models.Model):
    #--- foriegnkeys or manytomanyfields
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='کالا',related_name='product_favorites')
    user_favorite=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='کاربر علاقه مند',related_name='user_favorites')
    # models attributes
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت')
    
    def __str__(self):
        return f'{self.product} - {self.user_favorite} '

    class Meta:
        verbose_name='علاقه'
        verbose_name_plural='علاقه مندی ها'