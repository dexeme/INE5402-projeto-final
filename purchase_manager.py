import math
from decimal import Decimal
from terminal_utils import TerminalUtils
from purchase import Purchase
from client_vip import ClientVip

class PurchaseManager:
    def __init__(self, client_manager, product_manager):
        self.client_manager = client_manager
        self.product_manager = product_manager
        
    
    def menu_register_purchase(self):
        while True:
            cpf = input("Digite o CPF do cliente\n>>> ")
            client = self.client_manager.get_client_by_cpf(cpf)
            if not client:
                if TerminalUtils.use_again("Cliente não encontrado, deseja cadastrar o cliente? [S/N]\n>>> "):
                    # Se a pessoa escolheu cancelar no cadastro do cliente essa função retorna None
                    client = self.client_manager.register_client(cpf=cpf)
                    if client is None:
                        return
                elif TerminalUtils.use_again("Deseja tentar novamente? [S/N]\n>>> "):
                    # Se a pessoa escolheu tentar novamente, então ele irá para o começo do while novamente
                    continue
                else:
                    # Se a pessoa escolheu não tentar novamente, então ele encerra o while com o break e a função termina
                    break
            else:
                break
        
        print(' Cliente:', client.get_full_name())  
        purchase = Purchase()
            
        while True:
            entry = input("\n [ ] Digite o código do produto e a quantidade para adicionar na lista de compras\n [ ] Código do produto e R para remover um produto\n [L] Para listar os produtos comprados\n [T] Para listar todos os produtos\n [F] Para finalizar a compra\n [C] Para cancelar a compra\n>>> ").strip()
            if entry.lower() == 't':
                self.product_manager.print_product_list()
            elif entry.lower() == 'l':
                purchase.print_list()
            elif entry.lower() == 'c':
                if TerminalUtils.use_again("Deseja realmente cancelar a compra? [S/N]\n>>> "):
                    break
            elif entry.lower() == 'f':
                # Lista todos os produtos comprados
                purchase.print_list()
                
                print('\n----------------------------------\n')
                # Calcula o total da compra
                total = purchase.get_total()
                print('Total: R$', total)
                
                # Calcula o total da compra pelo cliente, dependendo do cliente ele poderá pagar um preço diferente.
                total_to_be_paid = client.buy(purchase)
                
                discount = total - total_to_be_paid
                print('Desconto: R$', discount)
                
                if type(client) is ClientVip:
                    # Cashback arredondado
                    print(f'Cashback acumulado: R$ {(math.floor(client.get_total_purchase() / 5) * 5):.2f}')
                
                print('Total a ser pago: R$', total_to_be_paid)
                
                # Reduz do estoque a quantidade comprada                      
                for product_in_purchase in purchase.get_products():
                    product_in_stock = self.product_manager.get_product_by_id(product.get_id())
                    product_in_stock.set_quantity(product_in_stock.get_quantity() - product_in_purchase.get_quantity())
                # Salva o arquivo do estoque
                self.product_manager.save_products_files()
                # Salva o cashback do cliente
                self.client_manager.save_clients_files()
                input("\nPressione enter para finalizar a compra")
                break
            else:
                split_entry = entry.split(' ')
                if len(split_entry) != 2:
                    print("Entrada inválida, por valor digite novamente.")
                else:
                    product_id = int(split_entry[0])
                    if split_entry[1].lower() == 'r':
                        if not purchase.remove_product_by_id(product_id):
                            TerminalUtils.set_text_style(foreground_color='red', bold=True)
                            print("Produto não encontrado!")
                            TerminalUtils.reset_style()
                            print()
                    else:
                        quantity = Decimal(split_entry[1])
                        product = self.product_manager.get_product_by_id(product_id)
                        if product:
                            purchase.add_product(product, quantity)
                        else:
                            TerminalUtils.set_text_style(foreground_color='red', bold=True)
                            print("Produto não encontrado!")
                            TerminalUtils.reset_style()
                            print()
            
            
            