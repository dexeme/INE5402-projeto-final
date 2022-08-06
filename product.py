from decimal import Decimal

class Product:
    def __init__(self, id, name, price, quantity):
        self.set_all_attributes(id, name, price, quantity)

    def get_all_attributes(self):
        return self.get_id(), self.get_name(), self.get_price(), self.get_quantity()

    def get_total_price(self):
        return Decimal(round(self.price * self.quantity, 2))

    def set_all_attributes(self, id, name, price, quantity):
        self.id = id
        self.set_name(name)
        self.set_price(price)
        self.set_quantity(quantity)

    def set_quantity(self, quantity):
        # Como a quantidade não pode ser negativa, logo fazemos o máximo entre o valor e 0
        self.quantity = max(0, quantity)

    def get_quantity(self):
        return self.quantity
    
    def add_quantity(self, quantity):
        self.set_quantity(self.get_quantity() + quantity)
        
    def print_info(self):
        print(f'ID: {self.get_id()}')
        print(f'Nome: {self.get_name()}')
        print(f'Preço: {self.get_price()}')
        print(f'Tipo: {self.get_type()}')
        print(f'Quantidade: {self.get_quantity()}')
    


    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_price(self):
        return self.price

    def set_price(self, price):
        self.price = price