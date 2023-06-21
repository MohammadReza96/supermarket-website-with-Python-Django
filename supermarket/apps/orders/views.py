from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .shop_card import ShopCard
from apps.products.models import Product
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order,OrderDetails,PaymentType,DeilveryTime
from apps.products.models import ProductGroup
from apps.accounts.models import CustomUser
from .forms import OrderForm,DeliveyDayForm
from apps.discounts.forms import CoupenForm
from apps.discounts.models import Coupon
from django.db.models import Q,Count
import datetime
from django.contrib import messages
from modules.price_discount_tax import get_price_delivery_tax
from apps.warehouses.models import Warehouse,WarehouseType
from apps.payments.models import Payment
#-------------------------------------------------------------------------------------------  update shopcard status in navbar
def status_shop_card(request):
    user_id=request.user.id
    shop_card=ShopCard(request,user_id)
    return HttpResponse(shop_card.item_count)

#-------------------------------------------------------------------------------------------  shop card page
class ShopCardView(View):
    def get(self,request,*args,**kwargs):
        user_id=request.user.id
        shop_card=ShopCard(request,user_id)
        
        return render(request,'orders_app/shop_card.html',{'shop_card':shop_card})
    
#------------------------------------------------------------------------------------------- render partials  ** for updating shopcard list **
def show_shop_card(request):
    user_id=request.user.id
    shop_card=ShopCard(request,user_id)
    product_count=shop_card.item_count
    total_price=shop_card.cal_total_price()
    # delivery_price= 0 if total_price>200 else 250    ####
    # tax_price=int(total_price*0.09)
    # final_price=total_price+delivery_price+tax_price
    final_price,delivery_price,tax_price=get_price_delivery_tax(total_price)
    
    return render(request,'orders_app/partials/show_shop_card.html',{'shop_card':shop_card,'product_count':product_count,'total_price':total_price,'delivery_price':delivery_price,'tax_price':tax_price,'final_price':final_price})

#-------------------------------------------------------------------------------------------  ajax function  for adding to shopcard
def add_to_shop_card(request):
    product_id=request.GET.get('product_id')
    number=request.GET.get('number')
    
    product=get_object_or_404(Product,id=product_id)
    user_id=request.user.id
    shop_card=ShopCard(request,user_id)
    shop_card.add_to_shop_card(product,number)
    
    return HttpResponse(shop_card.item_count)

#-------------------------------------------------------------------------------------------  ajax function  for deleting a product from a shopcard
def delete_from_shop_card(request):
    product_id=request.GET.get('product_id')
    product=get_object_or_404(Product,id=product_id)

    user_id=request.user.id
    shop_card=ShopCard(request,user_id)
    shop_card.delete_from_shop_card(product)

    return redirect('orders:show_shop_cards')

#-------------------------------------------------------------------------------------------  ajax function  for adding extra number of product in shopcard
def add_more_product(request):
    product_id=request.GET.get('product_id')
    number=request.GET.get('number')
    product=get_object_or_404(Product,id=product_id)
    
    user_id=request.user.id
    shop_card=ShopCard(request,user_id)
    shop_card.add_more_product(product,number)
    
    return redirect('orders:show_shop_cards')

#-------------------------------------------------------------------------------------------  create order view
class CreateOrderView(LoginRequiredMixin,View):
    
    def get(self,request,*args,**kwargs):
        user=request.user
        customer=get_object_or_404(CustomUser,id=user.id)
        #--- create an order 
        order=Order.objects.create(customer=customer)
        shop_card=ShopCard(request,user.id)
        for item in shop_card:
            OrderDetails.objects.create(
                order=order,
                product=item['product'],
                price=item['final_price'],
                number=item['number']
            )
        return redirect('orders:checkout',order.id)

#------------------------------------------------------------------------------------------- checkout page view
class CheckOutView(LoginRequiredMixin,View):
    
    def get(self,request,*args,**kwargs):
        user=request.user
        #--- get information from user login to fill the form automaticly when the form page load
        data={
            'name':user.name,
            'family':user.family,
            'phone_number':user.mobile_number,
            'email':user.email,
            'address':user.address,
            'city':user.city,
            'province':user.province,
            'postal_number':user.postal_code,
        }
        shop_card=ShopCard(request,user.id)
        order=get_object_or_404(Order,id=kwargs['order_id'])
        total_price=shop_card.cal_total_price()
        delivery_price= 0 if total_price>200 else 250    ####
        tax_price=int(total_price*0.09)
        final_price=total_price+delivery_price+tax_price
        
        if order.discount > 0:
            final_price=(final_price*order.discount)/100
            
        form=OrderForm(data)
        context={
            'shop_card':shop_card,
            'total_price':total_price,
            'delivery_price':delivery_price,
            'tax_price':tax_price,
            'final_price':final_price,
            'form':form,
        }
        return render(request,'orders_app/checkout2.html',context)
    
    def post(self,request,*args,**kwargs):
        order=Order.objects.get(id=kwargs['order_id'])
        user=request.user
        form_data=OrderForm(request.POST)
        if form_data.is_valid():
            clean_form_data=form_data.cleaned_data
            #--- update  customer  data
            customer=CustomUser.objects.get(id=user.id)
            customer.name=clean_form_data['name']
            customer.family=clean_form_data['family']
            customer.email=clean_form_data['email']
            customer.phone_number=clean_form_data['phone_number']
            customer.address=clean_form_data['address']
            customer.city=clean_form_data['city']
            customer.province=clean_form_data['province']
            customer.postal_code=clean_form_data['postal_number']
            customer.save()
            #--- update order set payment type
            order=Order.objects.get(id=order.id)
            order.payment_type=get_object_or_404(PaymentType,id=clean_form_data['payment_type'])
            order.discription=clean_form_data['discription']
            order.save()
            
            return redirect('orders:coupon_apply',order.id)

            # if clean_form_data['payment_type']==2:
            #     message='سفارش شما با موفقیت در سیستم ثبت شد و در زمان تعیین شده برای شما ارسال خواهد شد'
            #     return redirect('payments:show_verify_message',{{'message':message}})
#------------------------------------------------------------------------------------------- coupon apply view
class CoupenApplyView(View):
    
    def get(self,request,*args,**kwargs):
        user=request.user
        order_id=kwargs['order_id']
        shop_card=ShopCard(request,user.id)
        order=get_object_or_404(Order,id=int(order_id))
        if order.is_finally==True:
            messages.warning(request,'سفارش ثبت شده رد سیستم موجود نیست','warning')
        total_price=shop_card.cal_total_price()
        # delivery_price= 0 if total_price>200 else 250   ####
        # tax_price=int(total_price*0.09)
        final_price,delivery_price,tax_price=get_price_delivery_tax(total_price)
        if order.discount > 0:
            final_price=final_price-((final_price*order.discount)/100)
  
        form2=CoupenForm()
        
        context={
            'shop_card':shop_card,
            'total_price':total_price,
            'delivery_price':delivery_price,
            'tax_price':tax_price,
            'final_price':final_price,
            'form2':form2,
            'order_id':order_id,
            'order':order
        }
        return render(request,'discount_app/discount.html',context)

    def post(self,request,*args,**kwargs):
        order_id=kwargs['order_id']
        coupon_form=CoupenForm(request.POST)
        if coupon_form.is_valid():
            cp=coupon_form.cleaned_data
            coupon_code=cp['coupen_code']
            coupon=Coupon.objects.filter(Q(coupon_code=coupon_code) & Q(is_active=True) & Q(start_date__lte=datetime.datetime.now()) & Q(end_date__gte=datetime.datetime.now()))
            discount=0
            try:
                order=Order.objects.get(id=int(order_id))
                if order.is_finally==True :
                    messages.warning(request,'سفارش ثبت شده رد سیستم موجود نیست','warning')
                    return redirect('orders:coupon_apply',order_id)
                if coupon:
                    discount=coupon[0].discount
                    order.discount=discount
                    order.save()
                    messages.success(request,'کوپن با موفقیت اعمال شد')
                    return redirect('orders:coupon_apply',order_id)
                else:
                    order.discount=discount
                    order.save()
                    messages.error(request,'کوپن وارد شده معتبر نیست','danger')
                    return redirect('orders:coupon_apply',order_id)

            except:
                messages.error(request,'سفارش موجود نیست')
            return redirect('orders:coupon_apply',order_id)

#------------------------------------------------------------------------------------------- delivery time view
class DeliveryDaySetView(View):
    
        def get(self,request,*args,**kwargs):
            order_id=kwargs['order_id']
            order=Order.objects.get(id=int(order_id))

            delivery_form=DeliveyDayForm()
            return render(request,'orders_app/delivery_time.html',{'delivery_form':delivery_form,'order':order})
        
        def post(self,request,*args,**kwargs):
            user_id=request.user.id
            order_id=kwargs['order_id']
            delivery_form_data=DeliveyDayForm(request.POST)
            if delivery_form_data.is_valid():
                delivery_form_data_cleaned=delivery_form_data.cleaned_data
                order=Order.objects.get(id=int(order_id))
                order.delivery_day=delivery_form_data_cleaned['delivery_day']
                order.save()
                if order.payment_type.id==1:
                    print('-------hello------')
                    return redirect('payments:zarinpal_payment',order_id)
                else:
                    payment=Payment.objects.create(
                        order=order,
                        customer=CustomUser.objects.get(id=user_id),
                        amount=order.order_final_price(),
                        discription='پرداخت در محل انجام خواهد شد'
                    )
                    for item in order.order_details.all():
                        Warehouse.objects.create(
                            warehouse_type=WarehouseType.objects.get(id=2),
                            user_register=request.user,
                            product=item.product,
                            number=item.number,
                            price=item.price
                        )
                    shop_card=ShopCard(request,user_id)
                    for item in shop_card: 
                        shop_card.delete_from_shop_card(item['product']) 
                    message='سفارش شما با موفقیت در سیستم ثبت شد و در زمان تعیین شده برای شما ارسال خواهد شد'
                    return redirect('payments:show_verify_message',message=message,order_deliver_day=order.delivery_day)
