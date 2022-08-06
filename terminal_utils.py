class TerminalUtils:

    background_colors = {
        'black': '40',
        'blue': '44',
        'green': '42',
        'cyan': '46',
        'red': '41',
        'magenta': '45',
        'yellow': '43',
        'gray': '47',
        'light_gray': '100',
        'light_blue': '104',
        'light_green': '102',
        'light_cyan': '106',
        'light_red': '101',
        'light_magenta': '105',
        'light_yellow': '103',
        'white': '107'
    }

    foreground_colors = {
        'black': '30',
        'blue': '34',
        'green': '32',
        'cyan': '36',
        'red': '31',
        'magenta': '35',
        'yellow': '33',
        'gray': '37',
        'light_gray': '90',
        'light_blue': '94',
        'light_green': '92',
        'light_cyan': '96',
        'light_red': '91',
        'light_magenta': '95',
        'light_yellow': '93',
        'white': '97'
    }

    @staticmethod
    def use_again(msg):
        option = input(msg).strip().lower()
        if option == 's':
            return True
        else:
            print()
            return False

    @staticmethod
    def reset_style():
        print('\033[0;0;0m', end='')

    @staticmethod
    def set_text_style(foreground_color = "black", background_color = "black", bold = None):
        codes = []
        if bold == True:
            codes.append('1')
        elif bold == False:
            codes.append('0')
        
        background_code = TerminalUtils.background_colors.get(background_color, None)
        if background_code is not None:
            codes.append(background_code)    
        
        foreground_code = TerminalUtils.foreground_colors.get(foreground_color, None)
        if foreground_code is not None:
            codes.append(foreground_code)

        
        codes_str = ';'.join(codes)
        print(f'\033[{codes_str}m', end='')
        
