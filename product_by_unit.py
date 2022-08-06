from product import Product

class ProductByUnit(Product):

    def get_type(self):
        return 'Unidade'

    def print_purchase(self):
        print(f'{str(self.get_id()):5} | {self.get_name():25} | {"R$ " + str(self.get_price()):9} | {str(self.get_quantity()) + " un":7} | {"R$ " + str(self.get_total_price()):9}')

    def print_stock(self):
        print(f'{str(self.get_id()):5} | {self.get_name():25} | {"R$ " + str(self.get_price()):9} | {self.get_quantity():7} un')

        
    
    def set_quantity(self, quantity):
        # Como a quantidade não pode ser negativa, logo fazemos o máximo entre o valor e 0
        super().set_quantity(round(quantity))
    
    
    def copy(self):
        return ProductByUnit(self.get_id(), self.get_name(), self.get_price(), self.get_quantity())