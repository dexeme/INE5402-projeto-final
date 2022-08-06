from os import system, name as os_name


class Menu:
    def __init__(self):
        self.title = ''
        self.entries = []

    def set_title(self, title):
        self.title = title

    @staticmethod
    def back_option():
        return True

    @staticmethod
    def clear_screen():
        # Para windows
        if os_name == 'nt':
            system('cls')
        # Para linux, mac, etc
        elif os_name == 'posix':
            system('clear')

    def add_entry(self, entry_key_option, entry_name, entry_function):
        self.entries.append(
            {"name": entry_name, "key": entry_key_option, "function": entry_function})

    def _draw(self):
        Menu.clear_screen()
        maximum_length_key = 0
        maximum_length_name = 0

        for entry in self.entries:
            maximum_length_key = max(maximum_length_key, len(entry["key"]))
            maximum_length_name = max(maximum_length_name, len(entry["name"]))

        spacing = 5
        menu_size = maximum_length_key + maximum_length_name + spacing
        title_margin = max(0, ((menu_size - len(self.title)) // 2) - 1)
        print('=' * title_margin, self.title, '=' * title_margin)
        print()

        for entry in self.entries:
            print(
                f' [{entry["key"].rjust(maximum_length_key)}] {entry["name"].ljust(maximum_length_name)}')
        print('')
        print('=' * menu_size)

    def exec(self):
        while True:
            exit_from_menu = False
            found_option = False
            self._draw()
            option = input('>>> ')
            for entry in self.entries:
                if entry['key'] == option:
                    found_option = True
                    Menu.clear_screen()
                    exit_from_menu = entry['function']()
                    break
            if not found_option:
                input("Opçao inválida! Pressione enter para continuar ")
            if exit_from_menu:
                break

        return False
