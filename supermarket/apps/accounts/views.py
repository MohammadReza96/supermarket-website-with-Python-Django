from django.shortcuts import render,redirect
from apps.accounts.forms import RegisterUserForm,VerifyRegisterForm,LoginUserForm,ChangePassword,RememberPassword
from apps.accounts.models import CustomUser
from django.db.models import Q
from django.views import View
from modules.kavehnegar_module import send_sms
from modules.random_code_maker import code_maker
from django.contrib import messages
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserDetailModify
from django.http import HttpResponse
from apps.orders.models import Order,OrderDetails
from apps.payments.models import Payment
from django.core.paginator import Paginator

#----------------------------------------------------------------------------------------------- sign up user
class RegisterUserView(View):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index:home')
        return super().dispatch(request,*args,*kwargs)
    
    def get(self,request,*args,**kwargs):
        register_form=RegisterUserForm()
        return render(request,'account_app/register_user_form.html',{'register_form':register_form})
    
    def post(self,request,*args,**kwargs):
        get_form=RegisterUserForm(request.POST)
        if get_form.is_valid():
            user=get_form.cleaned_data                            # first clean data
            active_code=code_maker(6)                     # second create active code
            CustomUser.objects.create_user(                       # third create user
                user_name=user['user_name'],
                mobile_number=user['mobile_number'],
                active_code=active_code,
                password=user['password'],
                # name=user['name'],
                # family=user['family'],
                # email=user['email']
            )
            send_sms(user['mobile_number'],f'کد فعال سازی حساب شما {active_code} می باشد')       # fourth send active code sms
            
            request.session['user_session']={                     # fifth create session for verifying user in verfiy page
                'active_code':str(active_code),
                'user_name':str(user['user_name']),
                'mobile_number':str(user['mobile_number']),
                'remember_password': False
            }
            

            messages.success(request,'اطلاعات شما با موفقیت ثبت شد. لطفا کد فعال سازی پیامک شده را وارد کنید','success')
            return redirect('accounts:verify')
        
        return render(request,'account_app/register_user_form.html',{'register_form':get_form})

#---------------------------------------------------ajax function (checking user_name validation in database)
def check_user_name_validation_ajax(request):
    user_name=request.GET.get("user_name")
    user_exist=CustomUser.objects.filter(user_name=user_name).exists()
    if not user_exist:
        return HttpResponse('ok')
    return HttpResponse('no')
#----------------------------------------------------------------------------------------------- verify user
class VerifyRegisterUserView(View):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index:home')
        return super().dispatch(request,*args,*kwargs)
    
    def get(self,request,*args,**kwargs):
        verify_register_form=VerifyRegisterForm()
        return render(request,'account_app/verify_register_form.html',{'verify_register_form':verify_register_form})
    
    def post(self,request,*args,**kwargs):
        get_form=VerifyRegisterForm(request.POST)
        if get_form.is_valid():
            verify_user=get_form.cleaned_data
            user_sessions=request.session['user_session']
            if verify_user['active_code']==user_sessions['active_code']:
                if user_sessions['remember_password'] ==False:
                    user=CustomUser.objects.get(user_name=user_sessions['user_name'])
                    user.is_active=True
                    user.active_code=code_maker(6)
                    user.save()
                    messages.success(request,'ثبت نام با موفقیت انجام شد','success')
                    return redirect('accounts:login')
                else:
                    return redirect('accounts:changepassword')
                
            else:
                messages.error(request,'کد وارد شده معتبر نیست','danger')
                return render(request,'account_app/verify_register_form.html',{'verify_register_form':get_form})
            
        messages.error(request,'اطلاع وارد شده معتبر نیست','danger')
        return render(request,'account_app/verify_register_form.html',{'verify_register_form':get_form})

#----------------------------------------------------------------------------------------------- login user
class LoginUserView(View):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index:home')
        return super().dispatch(request,*args,*kwargs)
    
    def get(self,request,*args,**kargs):
        login_form=LoginUserForm()
        return render(request,'account_app/login_user_form.html',{'login_form':login_form})
    
    def post(self,request,*args,**kargs):
        get_form=LoginUserForm(request.POST)
        if get_form.is_valid():
            user=get_form.cleaned_data
            user_data=authenticate(username=user['user_name'],password=user['password'])
            if user_data is not None:
                db_user=CustomUser.objects.get(user_name=user['user_name'])
                if db_user.is_active==True:
                    if db_user.is_admin==False :
                        messages.success(request,'ورود با موفقیت انجام شد','success')
                        
                        login(request,user_data)
                        
                        next_url=request.GET.get('next')
                        if next_url is not None:
                            return redirect(next_url)
                        else:
                            return redirect('index:home')
                        
                    else:
                        messages.error(request,'کاربر ادمین نمی تواند از این بخش وارد شود','warning')
                        return render(request,'account_app/login_user_form.html',{'login_form':get_form})
                else:
                    # print('index-not_active')  # for testing
                    messages.error(request,'حساب کاربری شما فعال نمی باشد','danger')
                    return render(request,'account_app/login_user_form.html',{'login_form':get_form})
            else:
                # print('index-mistake')   # for testing
                messages.error(request,' نام کاربری یا رمز عبور را به درستی وارد نکرده اید!','danger')
                return render(request,'account_app/login_user_form.html',{'login_form':get_form})
        else:
            # print('index-mistake-FIRST')   # for testing
            return render(request,'account_app/login_user_form.html',{'login_form':get_form})

#-----------------------------------------------------------------------------------------------  user change password
class ChangePasswordView(View):
    
    def get(self,request,*args,**kargs):
        change_password=ChangePassword()
        return render(request,'account_app/change_password.html',{'change_password':change_password})
    
    def post(self,request,*args,**kargs):
        get_form=ChangePassword(request.POST)
        if get_form.is_valid():
            user_data=get_form.cleaned_data
            user_sessions=request.session['user_session']
            try:
                user=CustomUser.objects.get(user_name=user_sessions['user_name'])
                user.set_password(user_data['password'])
                user.active_code=code_maker(6)
                user.save()
                messages.success(request,'رمز شما با موفقیت  تغییر کرد','success')
                
                request.session['user_session']={
                                'active_code':'',
                                'mobile_number':'',
                                'user_name':'',
                                'remember_password': False}
                return redirect('accounts:login')
            except:
                messages.error(request,' نام کابری موجود نیست','danger')
                return render(request,'account_app/change_password.html',{'change_password':get_form})

        else:
            messages.error(request,'رمز ها یکسان نیست','danger')
            return render(request,'account_app/change_password.html',{'change_password':get_form})

#-----------------------------------------------------------------------------------------------  user remember password
class RememberPasswordView(View):
    
    def get(self,request,*args,**kargs):
        remember_password=RememberPassword()
        return render(request,'account_app/remember_password.html',{'remember_password':remember_password})
    
    def post(self,request,*args,**kargs):
        get_form=RememberPassword(request.POST)
        if get_form.is_valid():
            user_data=get_form.cleaned_data
            try:
                user=CustomUser.objects.get(user_name=user_data['user_name'])
                active_code=code_maker(6)
                user.active_code=active_code
                user.save()
                send_sms(user_data['mobile_number'],f'کد تایید شماره موبایل شما {active_code} است')
                
                request.session['user_session']={
                    'active_code':str(active_code),
                    'user_name':str(user_data['user_name']),
                    'mobile_number':str(user_data['mobile_number']),
                    'remember_password': True
                }
                
                messages.success(request,'جهت تغییر رمز عبور خود  کد دریافت شده را وارد کنید','success')
                return redirect('accounts:verify')
            except:
                messages.error(request,'نام کاربری موجود نیست','danger')
                return render(request,'account_app/remember_password.html',{'remember_password':get_form})
        else:
            messages.error(request,'فیلد ها را به درستی وارد کنید','danger')
            return render(request,'account_app/remember_password.html',{'remember_password':get_form})

#----------------------------------------------------------------------------------------------- logout user
class LogoutUser(View):
    #--- use for check in user is log in /log out / register /verify already
    def dispatch(self, request, *args, **kwargs): 
        if not request.user.is_authenticated:
            return redirect('index:home')
        return super().dispatch(request,*args,*kwargs)
    
    def get(self,request,*args,**kwargs):
        user_id=request.user.id
        try:
            session_data=request.session[f'shop_card_{user_id}']
        except:
            pass
        logout(request)
        # request.session[f'shop_card_{user_id}']=session_data
        try:
            session_data=request.session[f'shop_card_{user_id}']
        except:
            pass
        return redirect('index:home')

#-----------------------------------------------------------------------------------------------  userpanel
class UserPanelView(LoginRequiredMixin,View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index:home')
        return super().dispatch(request,*args,*kwargs)
    
    def get(self,request,*args,**kwargs):
        return render(request,'account_app/user_panel_block/user_details.html',{'user':request.user})
#-----------------------------------------------------------------------------------------------  userpanel
class UserPanelOrdersView(LoginRequiredMixin,View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index:home')
        return super().dispatch(request,*args,*kwargs)
    
    def get(self,request,*args,**kwargs):
        order_payments=Payment.objects.filter(Q(customer=request.user)).order_by('-register_date')
        
        pagienator=Paginator(order_payments,6) 
        page_number=request.GET.get('page')     #--- get current page number
        page_obj=pagienator.get_page(page_number) 

        return render(request,'account_app/user_panel_block/user_orders.html',{'page_obj':page_obj})
    
#-----------------------------------------------------------------------------------------------  userpanel-updateuserinformations
class UserUpdateDetail(LoginRequiredMixin,View):
    
    def dispatch(self, request, *args, **kwargs): 
        if not request.user.is_authenticated:
            return redirect('index:home')
        return super().dispatch(request,*args,*kwargs)
    
    def get(self,request,*args,**kwargs):
        user=request.user
        user_current_image=user.image
        user_details={
            'user_name': user.user_name,
            'mobile_number': user.mobile_number,
            'name': user.name,
            'family': user.family,
            'email': user.email,
            'province': user.province,
            'city': user.city,
            'address': user.address,
            'postal_code': user.postal_code
        }
        user_detail_form=UserDetailModify(initial=user_details)
        return render(request,'account_app/user_panel_block/user_modify.html',{'user_detail_form':user_detail_form,'user_current_image':user_current_image})

    def post(self,request,*args,**kwargs):
        user_modified_detail_form=UserDetailModify(request.POST,request.FILES)
        if user_modified_detail_form.is_valid():
            clean_data=user_modified_detail_form.cleaned_data
            user=request.user
            user_1=CustomUser.objects.get(user_name=user.user_name)
            user_1.name=clean_data['name']
            user_1.family=clean_data['family']
            user_1.email=clean_data['email']
            user_1.mobile_number=clean_data['mobile_number']
            user_1.province=clean_data['province']
            user_1.city=clean_data['city']
            user_1.address=clean_data['address']
            user_1.postal_code=clean_data['postal_code']
            if  clean_data['image'] :
                user_1.image=clean_data['image']

            user_1.save()

            messages.success(request,'اطلاعات شما با موفقیت بروزرسانی شد','success')
            return redirect("accounts:userpanel")
        
        messages.success(request,'در بروزرسانی اطلاعات شما مشکلی پیش آمده است','danger')
        return render(request,'account_app/user_panel_block/user_modify.html',{'user_detail_form':user_modified_detail_form})

#-----------------------------------------------------------------------------------------------  userpanel-changepassword
class UserPasswordChange(LoginRequiredMixin,View):
    
    def dispatch(self, request, *args, **kwargs): 
        if not request.user.is_authenticated:
            return redirect('index:home')
        return super().dispatch(request,*args,*kwargs)
    
    def get(self,request,*args,**kwargs):
        user_password_details=ChangePassword()
        return render(request,'account_app/user_panel_block/user_password_modify.html',{'user_detail_password_form':user_password_details})
    
    def post(self,request,*args,**kwargs):
        user_modified_password_form=ChangePassword(request.POST)
        if user_modified_password_form.is_valid():
            clean_data=user_modified_password_form.cleaned_data
            user=request.user
            user_1=CustomUser.objects.get(user_name=user.user_name)
            user_1.set_password(clean_data['password'])
            user_1.active_code=code_maker(6)
            user_1.save()
            messages.success(request,'رمز شما با موفقیت  تغییر کرد','success')
            return redirect('accounts:login')
        
        return render(request,'account_app/user_panel_block/user_password_modify.html',{'user_detail_password_form':user_modified_password_form})