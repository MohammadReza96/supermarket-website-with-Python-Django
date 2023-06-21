from apps.products.models import Product

class CompareProduct:
    
    def __init__(self,request):                       # for access to session
        self.session=request.session
        compare_product=self.session.get('compare_product')
        if not compare_product:                                  # if compare_product list is empty
            self.session['compare_product']=[]
            compare_product=self.session['compare_product']
            
        self.compare_product=compare_product
        self.item_count=len(compare_product)
    
    #--- add product in shopcard
    def add_to_compare_product(self,product_id):
        product_id=int(product_id)
        if product_id not in self.compare_product:         # check product_id as a key is exist in compare_product or not
            self.compare_product.append(product_id)
        self.item_count=len(self.compare_product)
        self.session.modified=True                          # for updating session
        
    #--- deleting product from compare_product list
    def delete_from_compare_product(self,product_id):
        product_id=int(product_id)
        self.compare_product.remove(product_id)
        self.session.modified=True

    #--- geting finall price of whole  shopcard          
    def clear_compare_product(self):
        del self.session['compare_product']
        self.session.modified=True
        
    #--- for converting this class object to iterator for using loop
    def __iter__(self):    
        compare_product=self.compare_product.copy()
        for item in compare_product:
            yield item