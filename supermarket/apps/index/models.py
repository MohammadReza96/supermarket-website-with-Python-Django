from django.db import models
from django.utils import timezone
from modules.file_upload_module import FileUploader

#------------------------------------------------------ sliderimage view
########################################################################
############################################## for changing slider image
########################################################################

class SliderImage(models.Model):
    file_upload=FileUploader('images','slides')
    slider_name=models.CharField(max_length=30,verbose_name='نام اسلایدر')
    slider_title=models.CharField(max_length=30,verbose_name='عنوان اسلایدر')
    slider_short_text=models.TextField(verbose_name='متن کوتاه اسلایدر')
    slider_image=models.FileField(upload_to=file_upload.upload_to,verbose_name='عکس اسلایدر')
    register_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ ثبت')
    is_active=models.BooleanField(default=False,verbose_name='وضعیت اسلایدر')
    
    def __str__(self):
        return f"{self.slider_name}"
    
    class Meta:
        verbose_name='اسلایدر'
        verbose_name_plural='اسلایدر ها'
        