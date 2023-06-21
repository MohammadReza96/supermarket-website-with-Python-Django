from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from modules.file_upload_module import FileUploader

#-----------------------------------------------------------------------------------------------------------------
class CustomUserManager(BaseUserManager): 
    def create_user(self,user_name,mobile_number,name='',family='',email='',image='',address='',city='',province='',postal_code='',active_code=None,password=None):
        if not user_name:
            raise ValueError('شماره موبایل باید وارد شود')
        user=self.model(
            user_name=user_name,
            mobile_number=mobile_number,            # for saveing mobile
            name=name,                              # for saveing name
            family=family,                          # for saveing family
            # mobile_number=self.normalize_email(email),  # for saveing email
            active_code=active_code,
        )
        user.set_password(password)                 # for saving password
        user.save(using=self._db)
        return user
    #-------------------------
    def create_superuser(self,user_name,mobile_number,name,family,email='',image=None,address=None,city=None,province=None,postal_code=None,password=None,active_code=None):
        user=self.create_user(
            user_name=user_name,
            mobile_number=mobile_number,
            name=name,
            family=family,
            active_code=active_code,
            password=password
                         )
        user.is_active=True
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

#-----------------------------------------------------------------------------------------------------------------
class CustomUser(AbstractBaseUser,PermissionsMixin):
    file_upload=FileUploader('images','user')
    # user_name
    user_name=models.CharField(max_length=20,unique=True,verbose_name='نام کاربری')
    # user_data_information ---------------------
    name=models.CharField(max_length=50,blank=True,verbose_name='نام')
    family=models.CharField(max_length=50,blank=True,verbose_name='نام خانوادگی')
    email=models.EmailField(max_length=200,blank=True,verbose_name='ایمیل')
    mobile_number=models.CharField(max_length=11,null=True,blank=True,verbose_name='شماره موبایل')
    image=models.ImageField(upload_to=file_upload.upload_to,verbose_name='عکس کاربر',null=True,blank=True)
    # user_data_location ---------------------
    address=models.TextField(null=True,blank=True,verbose_name='ادرس')
    city=models.CharField(max_length=50,null=True,blank=True,verbose_name='شهر')
    province=models.CharField(max_length=50,null=True,blank=True,verbose_name='استان')
    postal_code=models.CharField(max_length=12,null=True,blank=True,verbose_name='کدپستی')
    # user_data_date ---------------------
    register_date=models.DateField(default=timezone.now)
    is_active=models.BooleanField(default=False,verbose_name='وضعیت کاربر')
    active_code=models.CharField(max_length=100,null=True,blank=True)
    is_admin=models.BooleanField(default=False,verbose_name='وضعیت ادمینی')
    # to set username in fields ---------------------
    USERNAME_FIELD='user_name'
    
    # fields from oneTomany or manyTomany relationship --------------------
    # user_favorites=...                                from favorite app
    # warehouse_registered=...                          from warehouses app
    # user_score=...                                    from scoring app
    
    # to set what kind of questions ask when we create a user (5 question(1-mobile_number/2-name/3-family/4-email/5-password)) # password already exits in model
    REQUIRED_FIELDS=['name','family','mobile_number']
    objects=CustomUserManager()
    
    def __str__(self):
        return self.name+' '+self.family
    
    @property
    def is_staff(self): # set that user can access to admin panel or not
        return self.is_admin
    
    class Meta:
        verbose_name='کاربر'
        verbose_name_plural='کاربران'