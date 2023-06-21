from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.orders.models import Order
from apps.accounts.models import CustomUser
from apps.warehouses.models import Warehouse,WarehouseType
from apps.orders.shop_card import ShopCard
from modules.kavehnegar_module import send_sms
from .models import Payment
from django.http import HttpResponse
import requests
import json

#--------------------------------------------------------------------------------------- zarinpal 
# MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'  
# ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
# ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
# ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
#--------------------------------------------------------------------------------------- sandbox (for test)
MERCHANT = 'A2ABFDE0-89D6-4913-8DFC-4D8FF848346C'  
ZP_API_REQUEST = "https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://sandbox.banktest.ir/zarinpal/www.zarinpal.com/pg/StartPay/{authority}"
CallbackURL = 'http://127.0.0.1:8000/payments/verify/'

#---------------------------------------------------------------------------------------------------------
class ZarinPalPaymentView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        try:
            user=request.user
            order=get_object_or_404(Order,id=int(kwargs['order_id']))
            #--- for making an object from payment table to store some data in it
            payment=Payment.objects.create(
                order=order,
                customer=CustomUser.objects.get(id=user.id),
                amount=order.order_final_price(),
                discription='پرداخت از طریق درگاه زرین پال انجام شد'
            )
            payment.save()
            #--- for saving order and payment to use in ZarinPalPaymentVerifyView
            request.session[f'payment_session']={
                'order_id': order.id,
                'payment_id':payment.id,
                'user_id':user.id,
            }
            #--- print(order.order_final_price())
            req_data = {
                "merchant_id": MERCHANT,
                "amount": order.order_final_price(),
                "callback_url": CallbackURL,
                "description": 'پرداخت از طریق درگاه زرین پال انجام شد',
                "metadata": {"user_name": user.user_name, "mobile": user.mobile_number} # not neccesary
            }
            
            req_header = {"accept": "application/json","content-type": "application/json'"}
            req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
            authority = req.json()['data']['authority']
            
            if len(req.json()['errors']) == 0:
                return redirect(ZP_API_STARTPAY.format(authority=authority))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
        except :
            return redirect("payments:show_verify_message",message=f"خطا در اتصال به درگاه پرداخت",order_deliver_day='none')
        
#---------------------------------------------------------------------------------------------------------
class ZarinPalPaymentVerifyView(LoginRequiredMixin,View):
    
    def get(self,request,*args,**kwargs):
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        #--- check you have the authenticated payment_dargah
        if request.GET.get('Status') == 'OK':  
            #--- geting order and payment detail form sesseion
            order=Order.objects.get(id=request.session['payment_session']['order_id'])
            payment=Payment.objects.get(id=request.session['payment_session']['payment_id'])
            user_id=request.session['payment_session']['user_id']
            #--------------------
            req_header = {"accept": "application/json","content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": order.order_final_price(),
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                #--- when the payment is successful (update order table and payment table)
                if t_status == 100:
                    #--- for changing order status
                    order.is_finally=True
                    order.save()
                    #--- for changing payment status
                    payment.is_finaly=True
                    payment.status_code=t_status
                    payment.ref_id=str(req.json()['data']['ref_id'])
                    payment.save()
                    #---- for saving in warehouse 
                    for item in order.order_details.all():
                        Warehouse.objects.create(
                            warehouse_type=WarehouseType.objects.get(id=2),
                            user_register=request.user,
                            product=item.product,
                            number=item.number,
                            price=item.price
                        )
                    shop_card=ShopCard(request,user_id)
                    #--- for deleting selected product , after paying money 
                    for item in shop_card: 
                        shop_card.delete_from_shop_card(item['product']) 
                    #--- for returning to the site 
                    return redirect("payments:show_verify_message",message=f"پرداخت شما با موفقیت انجام شد . کد  رهگیری شما : {str(req.json()['data']['ref_id'])}",order_deliver_day=order.delivery_day)
                    # return HttpResponse('Transaction success.\nRefID: ' + str(req.json()['data']['ref_id']))
                # when the payment is successful (update order table and payment table)
                elif t_status == 101:
                    #------------------
                    order.is_finally=True
                    order.save()
                    #------------------
                    payment.is_finaly=True
                    payment.status_code=t_status
                    payment.ref_id=str(req.json()['data']['ref_id'])
                    payment.save()
                    #------------------
                    for item in order.order_details.all():
                        Warehouse.objects.create(
                            warehouse_type=WarehouseType.objects.get(id=2),
                            user_register=request.user,
                            product=item.product,
                            number=item.number,
                            price=item.price
                        )
                        
                    #--- for deleting selected product , after paying money 
                    shop_card=ShopCard(request,user_id)
                    for item in shop_card: 
                        shop_card.delete_from_shop_card(item['product']) 
                    #-------------------
                    return redirect("payments:show_verify_message",message=f"پرداخت شما با موفقیت انجام شد . کد  رهگیری شما : {str(req.json()['data']['ref_id'])}",order_deliver_day=order.delivery_day)
                #--- when the payment is unsuccessful 
                else:
                    #------------------
                    payment.status_code=t_status
                    payment.save()
                    #------------------
                    return redirect("payments:show_verify_message",message=f"خطا در فرایند پرداخت . کد  خطا : {t_status}",order_deliver_day='none')
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return redirect("payments:show_verify_message",message=f"خطا در فرایند پرداخت . کد  خطا : {e_code} پیام خطا : {e_message}",order_deliver_day='none')
        else:
            return redirect("payments:show_verify_message",message=f"خطا در فرایند پرداخت",order_deliver_day='none')
    
#-----------------------------------------------------------------------------------------
def show_verify_message(request,*args,**kwargs):
    user=request.user
    order_deliver_day=kwargs['order_deliver_day']
    order_message=kwargs['message']
    
    #--- if the payment was ok , a message will be sent customer
    if order_deliver_day!='none':
        send_sms(user.mobile_number,f' سفارش شما در تاریخ {order_deliver_day} ارسال خواهد شد')
    return render(request,'payments_app/verify_message.html',{'message':order_message})