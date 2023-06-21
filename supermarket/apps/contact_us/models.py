from django.db import models
from django.utils import timezone

#-----------------------------------------------------------------------
class ContactUsModel(models.Model):
    name=models.CharField(max_length=20,verbose_name='نام')
    family=models.CharField(max_length=20,verbose_name='نام خانوادگی')
    email=models.EmailField(max_length=50,verbose_name='ایمیل کاربر')
    topic=models.CharField(max_length=50,verbose_name='موضوع پیام')
    text=models.TextField(verbose_name='متن پیام')
    register_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ ثیت نظر')
    
    def __str__(self):
        return f'{self.family} - {self.topic}'
    
    class Meta:
        verbose_name='نظر عمومی'
        verbose_name_plural='نظرات عمومی'