import math
from client import Client

class ClientVip(Client):
    def __init__(self, cpf, full_name, total_purchase):
        super().__init__(cpf, full_name, total_purchase)
 
    def buy(self, purchase):
        total = purchase.get_total()
        old_cashback = self.get_total_purchase()
        
        # Cashback arredondado para baixo e multiplo de 5
        rounded_cashback = math.floor(old_cashback / 5) * 5
        
        total_with_cashback = max(total - rounded_cashback, total / 2 )
        
        used_cashback = total - total_with_cashback 
        cashback = total / 20
        
        self.set_total_purchase(old_cashback + cashback - used_cashback)
        return total_with_cashback
    
    def print(self):
        print(f"Nome: {self.get_full_name()}")
        print(f"CPF: {self.get_cpf()}")
        print(f"Client VIP")
        print(f'Cashback Acumulado: R$ {self.get_total_purchase()}')
    
    def copy(self):
        return ClientVip(*self.get_all_attributes())