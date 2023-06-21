from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from apps.products.models import Product
from apps.accounts.models import CustomUser

#------------------------------------------------------------------------------------ score model
class Scoring(models.Model):
    #--- foriegnkeys or manytomanyfields
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='کالا',related_name='product_score')
    scoring_user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_score',verbose_name='کاربر امتیاز دهنده')
    # models attributes
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت')
    score=models.PositiveSmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)],verbose_name='امتیاز کاربر')
    
    def __str__(self):
        return f'{self.product} - {self.scoring_user} - {self.score}'
    
    class Meta:
        verbose_name='امتیاز'
        verbose_name_plural='امیازات'