from decimal import Decimal
from terminal_utils import TerminalUtils
from client import Client
from client_vip import ClientVip
from CSV_file_manager import CSVFileManager

class ClientManager:
    def __init__(self, client_file_path, client_vip_file_path):
        self.clients = []
        self.client_file_manager = CSVFileManager(client_file_path, (str, str, Decimal))
        self.client_vip_file_manager = CSVFileManager(client_vip_file_path, (str, str, Decimal))
        self.restore_clients_from_file()
    
    def restore_clients_from_file(self):
        for client_data in self.client_file_manager.read_file():
            self.clients.append(Client(*client_data))
        for client_data in self.client_vip_file_manager.read_file():
            self.clients.append(ClientVip(*client_data))

    def save_clients_files(self):
        clients_data = []
        clients_vip_data = []

        for client in self.clients:
            if type(client) is Client:
                clients_data.append(client.get_all_attributes())
            elif type(client) is ClientVip:
                clients_vip_data.append(client.get_all_attributes())

        self.client_file_manager.save_file(clients_data)
        self.client_vip_file_manager.save_file(clients_vip_data)

    def get_client_by_cpf(self, cpf):
        for client in self.clients:
            if cpf == client.get_cpf():
                return client
        return None

    def menu_lookup(self):
        while True:
            print (f'== Consulta de clientes ==\n')
            option = input(" [1] Listar todos os clientes\n [2] Consultar um cliente apenas\n\n>>> ").strip()
            if option == '1':
                if len(self.clients) == 0:
                    print(f'Não há cliente cadastrado')
                    
                else: 
                    print(f'VIP | {"CPF":16} | Nome')
                    for client in self.clients:
                        if type(client) is Client:
                            print("   ", end='')
                        elif type(client) is ClientVip:
                            print("VIP", end='')
                        print(f' | {client.get_cpf():16} | {client.get_full_name()}')
                input("\nPressione enter para voltar ao menu")
                break
            elif option == '2':
                cpf = (input('Digite o CPF: '))
                client = self.get_client_by_cpf(cpf)
                if not (client is None):
                    print('\nExibindo informações do cliente')
                    client.print()                    
                    if not TerminalUtils.use_again("\nProcurar por outro cliente? [S/N]\n>>> "):
                        break
                elif not TerminalUtils.use_again("Cliente não encontrado!\nDeseja tentar novamente? [S/N]\n>>> "):
                    break
            elif TerminalUtils.use_again("Opçao Inválida! Tentar novamente? [S/N]\n>>> "):
                break

    # Atributo que não pode ter repetido, sendo crucial fazer isso para não bugar o cadastro
    def input_valid_cpf(self, cpf, default_cpf= None):
        client_already_registered_with_same_cpf = self.get_client_by_cpf(cpf)
        while client_already_registered_with_same_cpf and cpf != default_cpf:
            cpf = input('CPF já em uso! Insira novamente\n>>> ').strip()
            client_already_registered_with_same_cpf = self.get_client_by_cpf(cpf)
        return cpf

    def register_client(self, full_name=None, cpf=None):
        if full_name is None:
            full_name = (input('\nNome completo: ')).title()
            
        if cpf is None:
            cpf = self.input_valid_cpf(input('CPF: ').strip())

        if TerminalUtils.use_again("Deseja tornar VIP [S/N]\n>>> "):
            new_client = ClientVip(cpf, full_name, 0)
        else: 
            new_client = Client(cpf, full_name, 0)

        while True:
            # Antes de inserir na lista de clientes, pergunta se os dados estão certos (confirmação)
            selection = input(
                '\n[1] Confirmar\n[2] Editar\n[3] Cancelar\n>>> ')
            if selection == '1':
                self.clients.append(new_client)
                self.save_clients_files()
                return new_client
            
            elif selection == '2':
                new_client_edited = self.edit_client(new_client)
                self.clients.append(new_client_edited)
                self.save_clients_files()
                return new_client_edited
            elif selection == '3':
                break
            input("Opçao inválida! Pressione enter para continuar")

        
    def menu_register_client(self):
        self.register_client()
        
        

    def menu_edit_client(self):
        while True:
            cpf = (input('Digite o CPF: '))
            client = self.get_client_by_cpf(cpf)
            if not (client is None):
                edited_client = self.edit_client(client)
                current_index_of_client_in_clients = self.clients.index(client)
                self.clients[current_index_of_client_in_clients] = edited_client
                self.save_clients_files()
                if not TerminalUtils.use_again("Deseja editar outro cliente? [S/N]\n>>> "):
                    break
            elif not TerminalUtils.use_again("Cliente não encontrado!\nDeseja tentar novamente? [S/N]\n>>> "):
                break

    def edit_client(self, client):
        while True:
            new_client = client.copy()
            new_client.print()
            new_name = input(
                "Digite o novo nome ou pressione enter para manter o atual >>> ").strip()
            if new_name != "":
                new_client.set_full_name(new_name)
            
            new_cpf = input(
                "Digite o novo CPF ou pressione enter para manter o atual >>> ").strip()
            if new_cpf != "":
                new_client.set_cpf(self.input_valid_cpf(new_cpf, client.get_cpf())) 
            
            if type(new_client) is Client:
                if TerminalUtils.use_again("Deseja tornar VIP [S/N]\n>>> "):
                    new_client = ClientVip(*new_client.get_all_attributes())
            elif type(new_client) is ClientVip:
                if TerminalUtils.use_again("Deseja remover o VIP [S/N]\n>>> "):
                    new_client = Client(*new_client.get_all_attributes())
            
            new_client.print()
            
            if TerminalUtils.use_again("Confirmar edição? [S/N]\n>>> "):
                return new_client
            else: 
                return client
            if not TerminalUtils.use_again("Deseja editar novamente? [S/N]\n>>> "):
                break
    

    def menu_remove_client(self):
        while True:
            cpf = input('CPF do cliente que deseja remover:\n>>> ')
            client = self.get_client_by_cpf(cpf)
            if client:
                client_name = client.get_full_name()
                if TerminalUtils.use_again(f"Remover {client_name} do sistema? [S/N]\n>>> "):
                    self.clients.remove(client)
                    self.save_clients_files()
                    print(f"Cliente {client_name} removido do sistema!")
                    if not TerminalUtils.use_again("Deseja remover mais algum cliente? [S/N]\n>>> "):
                        break
                elif not TerminalUtils.use_again("Tentar novamente? [S/N]\n>>> "):
                    break
            elif not TerminalUtils.use_again("Cliente não cadastrado!\nDeseja tentar novamente? [S/N]\n>>> "):
                break
