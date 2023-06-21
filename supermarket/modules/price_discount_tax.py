def get_price_delivery_tax(price,discount=0):
    delivery=250
    if price > 200:
        delivery=0
    tax=price*0.09
    sum=price+delivery+tax
    new_sum=sum-(sum*discount/100)
    return int(new_sum),delivery,int(tax)