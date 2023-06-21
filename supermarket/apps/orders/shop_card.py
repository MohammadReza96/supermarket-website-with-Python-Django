from apps.products.models import Product
#------------------------------------------- create shop_card 
class ShopCard:
    def __init__(self,request,user_id):                       # for access to session
        self.user=user_id
        self.session=request.session
        temp=self.session.get(f'shop_card_{self.user}')
        if not temp:                                  # if shop is empty
            self.session[f'shop_card_{self.user}']={}
            temp=self.session[f'shop_card_{self.user}']
        self.shop_card=temp
        self.item_count=len(self.shop_card.keys())    # keys calculate the number of key inside a list 
    
    #----------------------------------------- add product in shopcard
    def add_to_shop_card(self,product,number):
        product_id=str(product.id)
        if product_id not in self.shop_card.keys():         # check product_id as a key is exist in shop_cad or not
            self.shop_card[product_id]={'number':0,'price':product.product_price,'final_price':product.get_finall_price_with_discount()}
        self.shop_card[product_id]['number']+=int(number)   
        self.item_count=len(self.shop_card.keys())
        self.session.modified=True                          # for updating session
        
    #----------------------------------------- deleting product from shopcard    
    def delete_from_shop_card(self,product):
        product_id=str(product.id)
        del self.shop_card[product_id]
        self.session.modified=True
        
    #----------------------------------------- add more number of product in shopcard     
    def add_more_product(self,product,number):
        product_id=str(product.id)
        self.shop_card[product_id]['number']=int(number)
        self.session.modified=True

    #----------------------------------------- for converting this class object to iterator for using loop
    def __iter__(self):    
        list_id=self.shop_card.keys()
        products=Product.objects.filter(id__in=list_id)   # id__in ~ id in list
        temp=self.shop_card.copy()
        
        for product in products:
            temp[str(product.id)]['product']=product      # for getting the special product_id and add product keys in it 
        for item in temp.values():
            item['total_price']=int(item['final_price'])*item['number']
            yield item 
    
    #----------------------------------------- geting finall price of whole  shopcard          
    def cal_total_price(self):
        sum=0
        for item in self.shop_card.values():
            sum+=int(item['final_price'])*item['number']
        return sum