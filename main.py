from client_manager import ClientManager
from product_manager import ProductManager
from purchase_manager import PurchaseManager
from menu import Menu
from terminal_utils import TerminalUtils


# Carrega o clientManager com os dados do arquivo
client_manager = ClientManager('data/clients.csv', 'data/clients_vip.csv')
# Carrega o productManager com os dados do arquivo
product_manager = ProductManager('data/products_by_unit.csv', 'data/products_by_weight.csv')

purchase_manager = PurchaseManager(client_manager, product_manager)

# Cria os menus
main_menu = Menu()
client_menu = Menu()
products_menu = Menu()

main_menu.set_title("MENU")
main_menu.add_entry("1", "Produtos", products_menu.exec)
main_menu.add_entry("2", "Clientes", client_menu.exec)
main_menu.add_entry("3", "Fazer compra", purchase_manager.menu_register_purchase)
main_menu.add_entry("0", "Sair do programa", Menu.back_option)

# Clientes ----> [1] Cadastrar [2] Editar [3] Informações [4] Remover
client_menu.set_title("Clientes")
client_menu.add_entry("1", "Cadastrar", client_manager.menu_register_client)
client_menu.add_entry("2", "Editar", client_manager.menu_edit_client)
client_menu.add_entry("3", "Informações", client_manager.menu_lookup)
client_menu.add_entry("4", "Remover", client_manager.menu_remove_client)
client_menu.add_entry("0", "Voltar", Menu.back_option)

# Produtos ----> [1] Estoque [2] Adicionar Produto [3] Remover Produto [4] Repor Estoque [5] Consultar produto [0] Voltar
products_menu.set_title("Produtos")
products_menu.add_entry("1", "Estoque", product_manager.menu_stock)
products_menu.add_entry("2", "Adicionar produto", product_manager.menu_add_product)
products_menu.add_entry("3", "Remover produto", product_manager.menu_remove_product)
products_menu.add_entry("4", "Repor estoque", product_manager.menu_stock_refil)
products_menu.add_entry("5", "Consultar produto", product_manager.menu_lookup)
products_menu.add_entry("0", "Voltar", Menu.back_option)



# Executa o menu principal
main_menu.exec()
