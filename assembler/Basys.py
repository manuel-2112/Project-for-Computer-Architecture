from iic2343 import Basys3
from assembler import Assembler
from os.path import join
from opcodes import OPCODES
from funciones_auxiliares import *

#119 : 0000000000010000 00000000000001001111
#121 : 0000000000010000 00000000000001001111
#123 : 0000000001111101 00000000000001001111

def write_to_rom(instructions):
    instance = Basys3()
    instance.begin(1)
    n_line = 0
    line_white = "000000000000000000000000000000000000"
    for line in instructions:
        #print("\"" + line + "\",")
        #if "0111010" in line:
        #    print(n_line, ":", line)
        byte_array = int(line, 2).to_bytes((len(line) + 7) // 8, byteorder='big')
        instance.write(n_line, bytearray(byte_array))
        n_line += 1
    for i in range(700):
        byte_array = int(line_white, 2).to_bytes((len(line_white) + 7) // 8, byteorder='big')
        instance.write(n_line, bytearray(byte_array))
        n_line += 1
    instance.end()


def translate_lines(opcodes, data, code):
    lines_binary = []

    #direcciones = {"Nombre variable" : ["Dirección", "Valor"]}
    direcciones = {}

    #leer linea y traducirla a 36 bits
    contador_direccion_RAM = 0

    for line in data:
        if len(line) > 2:
            direcciones[line[0]] = [bin(contador_direccion_RAM)[2:].zfill(16), check_type(line[1])]
            contador_direccion_RAM += 1

            count = 2
            while count < len(line):
                string = line[0] + "_" + str(count)
                direcciones[string] = [bin(contador_direccion_RAM)[2:].zfill(16), check_type(line[count])]
                count += 1
                contador_direccion_RAM += 1
        
        elif len(line) <= 2:
            number = check_type(line[1])
            direcciones[line[0]] = [bin(contador_direccion_RAM)[2:].zfill(16), number] # bin(line[1])[2:].zfill(16) para guardalo como bit
            contador_direccion_RAM += 1 
        
    for elem in direcciones:
        lines_binary.append(direcciones[elem][1] + opcodes["MOV_A_LIT"])
        lines_binary.append(direcciones[elem][0] + opcodes["MOV_DIR_A"])
    lines_binary.append("0000000000000000" + opcodes["MOV_A_LIT"])


    i = (contador_direccion_RAM * 2) + 1
    for line in code:
        # guardar direcciones de labels
        if len(line) == 1:
            if line[0] == "RET":
                i += 2
                continue
            direcciones[line[0][:-1]] = [bin(i)[2:].zfill(16), line[0]]
            i -= 1
        if len(line) == 2:
            if "POP" == line[0]:
                i += 1
        i += 1
            

    for line in code:
        ##############################################################################################################

        if len(line) == 1:
            if line[0] == "RET":
                lines_binary.append("0000000000000000" + opcodes["RET"])
                lines_binary.append("0000000000000000" + opcodes["RET_2"])

        ##############################################################################################################
        if len(line) == 2:
            # Cuando A o B o (B)
            if line[1] == "B" or line[1] == "A" or line[1] == "(B)":
                ##############################################################################################################

                if line[0] == "POP":
                    lines_binary.append("0000000000000000" + opcodes["POP_" + line[1]])
                    lines_binary.append("0000000000000000" + opcodes["POP_" + line[1] + "2"])

                ##############################################################################################################
                elif line[0] == "CALL":
                    lines_binary.append(direcciones[line[1]][1] + opcodes["CALL"])
                else:
                    lines_binary.append("0000000000000001" + opcodes[line[0] + "_" + line[1]])

            # Cuando es una dirección o label
            else:
                try:
                    lines_binary.append(direcciones[line[1]][0] + opcodes[line[0]])
                except KeyError:
                    if line[1][1:-1] not in direcciones:
                        number = check_type(line[1][1:-1])
                        dir = get_dir(number, direcciones)
                    else:
                        dir = direcciones[line[1][1:-1]][0]
                    lines_binary.append(dir + opcodes[line[0] + "_" + "DIR"])

        elif len(line) == 3:
            instruction = get_inst(line[0], line[1], line[2])
            

            # cuando A,B o B,A o A,(B) o (B),A o B,(B) o (B), A
            if (line[1] == "B" or line[1] == "A" or line[1] == "(B)") and (line[2] == "B" or line[2] == "A" or line[2] == "(B)"):
                lines_binary.append("0000000000000000" + opcodes[instruction])

            # cuando A,Dir o B,Dir o Dir,A o Dir,B
            elif "A_DIR" in instruction or "B_DIR" in instruction:
                if line[2][1:-1] not in direcciones:
                    number = check_type(line[2][1:-1])
                    dir = get_dir(number, direcciones)
                else:
                    dir = direcciones[line[2][1:-1]][0]
                lines_binary.append(dir + opcodes[instruction])
            
            elif "DIR_A" in instruction or "DIR_B" in instruction:
                if line[1][1:-1] not in direcciones:
                    number = check_type(line[1][1:-1])
                    dir = get_dir(number, direcciones)
                else:
                    dir = direcciones[line[1][1:-1]][0]
                lines_binary.append(dir + opcodes[instruction])

            # cuando A,LIT o B,LIT o (B),LIT
            elif "A_LIT" in instruction or "(B)_LIT" in instruction:
                try:
                    number = check_type(line[2])
                    lines_binary.append(number.zfill(16) + opcodes[instruction])
                except:
                    lines_binary.append(direcciones[line[2]][0] + opcodes[instruction])
            
            elif "B_LIT" in instruction: 
                try:
                    number = check_type(line[2])
                    lines_binary.append(number.zfill(16) + opcodes[instruction])
                except:
                    lines_binary.append(direcciones[line[2]][0] + opcodes[instruction])
                        
    return lines_binary

TESTS = {
    1: join("testeo_entrega", "Test 0 - Mínimo.txt"),
    2: join("testeo_entrega", "Test 1 - Ram y Status.txt"),
    3: join("testeo_entrega", "Test 2 - Indirecto y Stack.txt"),
    4: join("testeo_entrega", "Test 3 - Entrada y Salida.txt"),
    5: join("testeo_entrega", "piero.txt"),
    6: join("test canvas", "e2_t1.txt"),
    7: join("test canvas", "e2_t2.txt"),
    8: join("test canvas", "e3_t3.txt"),
    9: join("juegos", "Juego_Profe.txt"),
    10: join("juegos", "Juego_2.txt"),


if __name__ == "__main__":
    assembler = Assembler()
    assembler.read_file(path=TESTS[10])

    lineas_binario = translate_lines(OPCODES, assembler.data, assembler.code)
    print(lineas_binario)
    count = 0
    # write_to_rom(lineas_binario)
