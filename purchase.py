from terminal_utils import TerminalUtils

class Purchase:
    def __init__(self):
        self.products = []

    def get_products(self):
        return self.products
    
    def find_product_in_purchase(self, product):
        for product_in_list in self.products:
            if product_in_list.get_id() == product.get_id():
                return product_in_list
        return None
    
    def remove_product_by_id(self, product_id):
        for product_in_list in self.products:
            if product_in_list.get_id() == product_id:
                self.products.remove(product_in_list)
                return True
        return False
    
    def add_product(self, product, quantity):
        product_in_purchase = self.find_product_in_purchase(product)
        if product_in_purchase is None:
            copy_of_product = product.copy()
            copy_of_product.set_quantity(quantity)
            product_in_purchase = copy_of_product
            self.products.append(copy_of_product)
        else:
            product_in_purchase.add_quantity(quantity)
        if(product_in_purchase.get_quantity() > product.get_quantity()):
            TerminalUtils.set_text_style(foreground_color="yellow", bold=True)
            print("A quantidade desse produto supera a quantidade total no estoque!")
            product_in_purchase.set_quantity(product.get_quantity())
            TerminalUtils().reset_style()
        if product_in_purchase.get_quantity() == 0:
            self.products.remove(product_in_purchase)
            
    def get_total(self):
        total = 0
        for product in self.products:
            total += product.get_total_price()
        return total
    
    def print_list(self):
        if len(self.products) == 0:
            print("A lista de compras está vazia!")
        else:
            print(f'{"ID":5} | {"NOME":25} | {"PREÇO UN.":9} | {"QUANT.":7} | {"PREÇO TOTAL":9} ')
            for product in self.products:
                product.print_purchase()
        