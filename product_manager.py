from decimal import Decimal
from terminal_utils import TerminalUtils
from CSV_file_manager import CSVFileManager
from product_by_unit import ProductByUnit
from product_by_weight import ProductByWeight

class ProductManager():
    def __init__(self, product_by_unit_file_path, product_by_weight_file_path):
        self.product_by_unit_file_manager = CSVFileManager(product_by_unit_file_path, (int, str, Decimal, int))
        self.product_by_weight_file_manager = CSVFileManager(product_by_weight_file_path, (int, str, Decimal, Decimal))
        self._products = []
        self.current_id = 0
        self.restore_clients_from_file()

    def restore_clients_from_file(self):
        max_id = -1
        
        for product_data in self.product_by_unit_file_manager.read_file():
            product = ProductByUnit(*product_data)
            self._products.append(product)
            max_id = max(max_id, product.get_id())
        for product_data in self.product_by_weight_file_manager.read_file():
            product = ProductByWeight(*product_data)
            self._products.append(product)
            max_id = max(max_id, product.get_id())
        
        self._products.sort(key=lambda product: product.get_id())
        self.current_id = max_id

    def save_products_files(self):
        product_by_unit_data = []
        product_by_weight_data = []

        for product in self._products:
            if type(product) is ProductByUnit:
                product_by_unit_data.append(product.get_all_attributes())
            elif type(product) is ProductByWeight:
                product_by_weight_data.append(product.get_all_attributes())

        self.product_by_unit_file_manager.save_file(product_by_unit_data)
        self.product_by_weight_file_manager.save_file(product_by_weight_data)

    def get_product_by_id(self, product_id):
        for product in self._products:
            if product_id == product.get_id():
                return product
        return None
    
    def menu_lookup(self): 
        while True:
            id = int(input('Digite o ID: '))
            product = self.get_product_by_id(id)
            if not (product is None):
                print('\nExibindo informações do produto')
                print(f'ID: {product.get_id()}')
                print(f'Nome: {product.get_name()}')
                print(f'Preço: {product.get_price()}')
                print(f'Tipo: {product.get_type()}')
                print(f'Quantidade: {product.get_quantity()}')
                if not TerminalUtils.use_again("\nConsultar outro produto? [S/N]\n>>> "):
                    break
            elif not TerminalUtils.use_again("Produto não encontrado!\nDeseja tentar novamente? [S/N]\n>>> "):
                break

# * Produto (nome) está quase acabando!
    def menu_stock(self):
        if len(self._products) == 0:
            if TerminalUtils.use_again('A lista de produtos está vazia.\nDeseja cadastrar um novo produto? [S/N]\n>>> '):
                self.add_product()
        else:
            print('\nLista de produtos\n')
            print(f'{"ID":5} | {"NOME":25} | {"PREÇO":9} | ESTOQUE')
            for product in self._products:
                if product.get_quantity() < 5:
                    TerminalUtils.set_text_style(foreground_color = "red", bold = True)
                    product.print_stock()
                    TerminalUtils.reset_style()
                else:
                    product.print_stock()

            input('\nPressione enter para continuar...')


    def print_product_list(self):
        if len(self._products) == 0:
            if TerminalUtils.use_again('A lista de produtos está vazia.\nDeseja cadastrar um novo produto? [S/N]\n>>> '):
                self.add_product()
        else:
            print('\nLista de produtos\n')
            print(f'{"ID":5} | {"NOME":25} | {"PREÇO":9} | ESTOQUE')
            for product in self._products:
                product.print_stock()


    def get_new_id(self):
        self.current_id += 1
        return self.current_id
    
    def menu_add_product(self):
        while True:
            product_name = (input('\nNome do produto: ')).title()
            product_id = self.get_new_id()
            product_price_input = input('Preço do produto: ').strip()
            
            # O .2f serve para trucar o preço em duas casa decimais
            product_price = Decimal(f"{Decimal(product_price_input):.2f}")
            
            while True:
                product_type = input('Tipo do produto\n[1] Por peso\n[2] Por unidade\n>>> ').strip()
                if product_type == '1':
                    product_stock = input('Quantidade do produto no estoque (kg):\n>>> ').strip()
                    new_product = ProductByWeight(product_id, product_name, product_price, Decimal(product_stock))
                    break
                elif product_type == '2':
                    product_stock = input('Quantidade do produto no estoque (unidades):\n>>> ').strip()
                    new_product = ProductByUnit(product_id, product_name, product_price, Decimal(product_stock))
                    break
                else: 
                    print('Opção inválida')
    
            selection = input('\n[1] Confirmar\n[2] Editar\n[3] Cancelar\n>>> ')
            if selection == '1':
                print('Produto cadastrado!\n')
                self._products.append(new_product)
                self.save_products_files()
                if not TerminalUtils.use_again("Registrar outro produto? [S/N]\n>>> "):
                    break
            elif selection == '2':
                while True:
                    new_product.print_info()
                    new_name = input("Digite o novo nome ou enter para manter o mesmo >>> ").strip()
                    new_product_type = input('Digite o novo tipo ou enter para manter o mesmo tipo\n[1] Por peso\n[2] Por unidade\n>>> ').strip()
                    new_product_price = Decimal(input('Digite o novo preço ou enter para manter o mesmo preço do produto: ').strip())
                    new_product_stock = int(input('Digite a nova quantidade ou enter para manter a mesma quantidade: ').strip())

                    if not new_name:
                        new_name = product_name
                    
                    if not new_product_type:
                        new_product_type = product_type
                    
                    if not new_product_price:
                        new_product_price = product_price

                    if not new_product_stock:
                        new_product_stock = product_stock
                    
                    if new_product_type == '1':
                        new_product = ProductByWeight(product_id, product_name, product_price, Decimal(product_stock))

                    elif new_product_type == '2':
                        new_product = ProductByUnit(product_id, product_name, product_price, int(product_stock))                  
                    
                    if TerminalUtils.use_again("Confirmar edição? [S/N]\n>>> "):
                        self._products.append(new_product)
                        self.save_products_files()
                        break
                break
            elif selection == '3':
                break
            else:
                print("Opçao inválida!")


    def menu_remove_product(self):
        while True:
            id = int(input('ID do produto que desejas remover:\n>>> '))
            product = self.get_product_by_id(id)
            if product:
                product_name = product.get_name()
                if TerminalUtils.use_again(f"Remover {product_name} do sistema? [S/N]\n>>> "):
                    self._products.remove(product)
                    self.save_products_files()
                    print(f"Produto {product_name} removido do sistema!")
                    if not TerminalUtils.use_again("Deseja remover mais algum produto? [S/N]\n>>> "):
                        break
                elif not TerminalUtils.use_again("Tentar novamente? [S/N]\n>>> "):
                    break
            elif not TerminalUtils.use_again("Produto não cadastrado!\nDeseja tentar novamente? [S/N]\n>>> "):
                break

    def menu_stock_refil(self):
        while True:
            product_id = int(input("Digite o id do produto:\n>>> "))
            product = self.get_product_by_id(product_id)
            if product:
                product.print_info()
                quantity = Decimal(input(f'Digite a quantidade a ser adicionada no estoque: ').strip())
                product.add_quantity(quantity)
                self.save_products_files()
                if not TerminalUtils.use_again("Deseja repor o estoque de outro produto? [S/N]\n>>> "):
                    break
            elif not TerminalUtils.use_again("Produto não encontrado, deseja tentar novamente? [S/N]\n>>> "):
                break

