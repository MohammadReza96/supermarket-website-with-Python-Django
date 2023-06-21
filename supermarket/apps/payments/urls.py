from django.urls import path
from .views import ZarinPalPaymentView,ZarinPalPaymentVerifyView,show_verify_message
app_name='payments'

urlpatterns = [
    path('zarinpal_payment/<int:order_id>',ZarinPalPaymentView.as_view(),name='zarinpal_payment'),
    path('verify/',ZarinPalPaymentVerifyView.as_view(),name='zarinpal_payment_verify'),
    path('show_verify_message/<str:message>/<str:order_deliver_day>/',show_verify_message,name='show_verify_message'),
]