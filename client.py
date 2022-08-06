class Client:
    def __init__(self, cpf, full_name, total_purchase):
        # Atributos
        self.set_all_attributes(cpf, full_name, total_purchase)
    
    def get_cpf(self):
        return self.cpf
    
    def set_cpf(self, cpf):
        self.cpf = cpf
    
    def set_full_name(self, fullname):
        self.full_name = fullname

    def get_full_name(self):
        return self.full_name

    def get_total_purchase(self):
        return self.total_purchase
        
    def set_total_purchase(self, total_purchase):
        self.total_purchase = total_purchase

    def get_all_attributes(self):
        return self.get_cpf(), self.get_full_name(), self.get_total_purchase()

    def set_all_attributes(self, cpf, full_name, total_purchase):
        self.set_cpf(cpf)
        self.set_full_name(full_name)
        self.set_total_purchase(total_purchase)

    def copy(self):
        return Client(*self.get_all_attributes())

    def print(self):
        print(f"Nome: {self.full_name}")
        print(f"CPF: {self.cpf}")
        print(f"Client não VIP")
        print(f'Cashback Acumulado: R$ {self.total_purchase}')

    def buy(self, purchase):
        return purchase.get_total()
        