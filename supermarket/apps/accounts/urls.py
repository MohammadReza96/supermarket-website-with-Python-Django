from django.urls import path
from .views import RegisterUserView,VerifyRegisterUserView,LoginUserView,ChangePasswordView,RememberPasswordView,LogoutUser,UserPanelView,UserPanelOrdersView,UserUpdateDetail,UserPasswordChange,check_user_name_validation_ajax
app_name='accounts'

urlpatterns = [
    path('register/',RegisterUserView.as_view(),name='register'),
    path('verify/',VerifyRegisterUserView.as_view(),name='verify'),
    path('login/',LoginUserView.as_view(),name='login'),
    path('logout/',LogoutUser.as_view(),name='logout'),
    path('change_password/',ChangePasswordView.as_view(),name='changepassword'),
    path('remember_password/',RememberPasswordView.as_view(),name='rememberpassword'),
    path('userpanel/',UserPanelView.as_view(),name='userpanel'),
    path('userpanel_orders/',UserPanelOrdersView.as_view(),name='userpanel_orders'),
    path('userdetail_modify_informations/',UserUpdateDetail.as_view(),name='userdetail_modify_informations'),
    path('userdetail_modify_password/',UserPasswordChange.as_view(),name='userdetail_modify_password'),
    path('username_form_validation/',check_user_name_validation_ajax,name='username_form_validation'),
]