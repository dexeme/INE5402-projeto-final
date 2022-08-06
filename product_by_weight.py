from decimal import Decimal
from product import Product


class ProductByWeight(Product):
    
    def get_type(self):
        return 'Peso'
    
    def print_purchase(self):
        print(f'{str(self.get_id()):5} | {self.get_name():25} | {"R$ " + str(self.get_price()):9} | {str(self.get_quantity()) + " kg":7} | {"R$ " + str(self.get_total_price()):9}')

    def print_stock(self):
        print(f'{str(self.get_id()):5} | {self.get_name():25} | {"R$ " + str(self.get_price()):9} | {self.get_quantity():7} kg')

    def copy(self):
        return ProductByWeight(self.get_id(), self.get_name(), self.get_price(), self.get_quantity())
