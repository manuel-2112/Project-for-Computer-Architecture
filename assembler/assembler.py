#from iic2343 import Basys3
from os.path import join
from opcodes import OPCODES

def change_to_ascii(new_line):
    for elem in new_line:
        if elem[0] == "'" and elem[-1] == "'":
            new_line[new_line.index(elem)] = str(ord(elem[1:-1]))
    return new_line
class Assembler:

    def __init__(self):
        self.data = []
        self.code = []

    def read_file(self, path:str):
        with open(path, "r", encoding="UTF-8") as file:
                    data = False
                    code = False

                    for line in file.readlines():
                        line = self.clean_line(line)
                        if line != None:
                            if data:
                                if len(line) == 1:
                                    if line[0] == 'CODE:':
                                        True
                                    else:
                                        self.data[len(self.data)-1].append(line[0])
                                else:
                                    change_to_ascii(line)
                                    if len(line) > 2:
                                        line.append('0')
                                    self.data.append(line)
                            elif code:
                                if len(line) > 1:
                                    if ":" in line[0]:
                                        self.code.append([line[0]])
                                        self.code.append(line[1:])
                                        continue
                                change_to_ascii(line)
                                self.code.append(line)
                            
                            if "DATA:" in line:
                                data = True

                            if "CODE:" in line:
                                data = False
                                code = True
                                
        
        
    
    def clean_line(self, line):
        if '//' in line:
            position = line.index('//')
            line = line[:position]
        line = line.strip()
        line = " ".join(line.split())
        
        new_line = ""
        aux_bool = False
        aux_bool_str = False
        string = False
        for character in line:
            # print(character)
            if aux_bool and character != " ":
                new_line += character
            elif aux_bool_str:
                if character == " ":
                    new_line += "@"
                    new_line += " "
                elif character == '"':
                    character
                else:
                    new_line += "'" + character + "'"
                    new_line += " "
            elif not aux_bool:
                new_line += character

            if character == "(" and not string:
                aux_bool = True
            elif character == ")" and not string:
                aux_bool = False

            if character == '"':
                string = not string
                aux_bool_str = not aux_bool_str
                new_line = new_line[:-1]
        # print("----------------------------------------------------")
        new_line = new_line.replace(",", " ")
        new_line = " ".join(new_line.split())
        new_line = new_line.split(" ")
        new_line = list(map(lambda x: x.replace("@", "' '"), new_line))

        if new_line == [""]:
            return None


        #print(new_line)
        return new_line



if __name__ == "__main__":
    assembler = Assembler()
    assembler.read_file(path=join("testeo_entrega", "Test 0 - Mínimo.txt"))

    print(f'Variables: {assembler.data}')
    print(f'Instrucciones: {assembler.code}')