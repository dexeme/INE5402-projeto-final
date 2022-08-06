import os

class CSVFileManager():
    def __init__(self, file_path, format):
        self.file_path = file_path
        self.number_of_columns = len(format)
        self.format = format
        self.create_file_if_not_exists()
        self.read_file()

    @staticmethod
    def typeBool(content):
        if content == "TRUE":
            return True
        elif content == "FALSE":
            return False
        return None

    def read_file(self):
        content = []
        try:
            with open(self.file_path, 'r',  encoding="utf-8") as file:
                for line in file:
                    content.append(self._parse_line(line))
        except FileNotFoundError:
            pass
        return content

    def create_file_if_not_exists(self):
        try:
            with open(self.file_path, 'r'):
                pass
        except FileNotFoundError:
            dir_name = os.path.dirname(self.file_path)
            try:
                os.makedirs(dir_name)
            except FileExistsError:
                pass
            with open(self.file_path, 'w'):
                pass

    def _split_line(self, line):
        current_index = -1
        slices = []
        first_run = True
        while current_index != -1 or first_run:
            first_run = False

            current_index+= 1
            next_quote_index = line.find('"', current_index)
            next_double_quote_index = line.find('""', current_index)
            
            if next_quote_index == current_index:
                current_index += 1
                end_slice = current_index

                while True:
                    end_slice = line.find('"', end_slice)
                    next_double_quote_index = line.find('""', end_slice)
                    if next_double_quote_index == end_slice:
                        end_slice += 2
                    else:
                        break
                slices.append(line[current_index:end_slice].replace('""', '"'))
                current_index = line.find(',', end_slice)
            else:
                end_slice = line.find(',', current_index + 1)
                slices.append(line[current_index:end_slice])
                current_index = line.find(',', end_slice)
        return slices


    def _parse_line(self, line):
        fields = self._split_line(line)
        new_line = []
        if(len(fields) != self.number_of_columns):
            raise Exception('Number of columns does not match')
        for index in range(len(fields)):
            new_line.append(self.format[index](fields[index]))
        return new_line
            
    def save_file(self, content):
        with open(self.file_path, 'w',  encoding="utf-8") as file:
            for line in content:
                file.write(self._create_line(line) + '\n')
        

    def _create_line(self, data):
        line_slices = []
        index = 0
        for item in data:
            index += 1
            item_str = str(item)
            if ',' in item_str or '"' in item_str:
                item_str = '"' + item_str.replace('"', '""') + '"'
            line_slices.append(item_str)
        
        return ','.join(line_slices) + ',' * (self.number_of_columns - index)

