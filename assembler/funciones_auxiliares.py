def to_binary(n, t):
    if t == "d":
        n = bin(int(n))[2:]
    elif t == "b":
        return n
    elif t == "h":
        n = bin(int(n, 16))[2:]
    else:
        n = bin(int(n))[2:]
    return n

def check_type(num):
    if "d" == num[-1] or "h" == num[-1] or "b" == num[-1]:
        number = to_binary(num[:-1], num[-1])
    else:
        number = to_binary(num, "d")
    return number.zfill(16)

def get_inst(instruction, Var1="", Var2=""):
    final_inst = ""

    if Var1 == "B" or Var1 == "A" or Var1 == "(B)":       # ['MOV', 'B', '(v4)']
        final_inst = instruction + "_" + Var1
    elif "(" in Var1:
        final_inst = instruction + "_" + "DIR"
    elif Var1 == "":
        final_inst = instruction
    else:
        final_inst = instruction + "_" + "LIT"

    if Var2 == "B" or Var2 == "A" or Var2 == "(B)":
        final_inst = final_inst + "_" + Var2
    elif "(" in Var2:
        final_inst = final_inst + "_" + "DIR"
    elif Var2 == "":
        final_inst = final_inst
    else:
        final_inst = final_inst + "_" + "LIT"

    return final_inst


def get_dir(number, direcciones):
    for key in direcciones:
        if direcciones[key][0] == number:
            return direcciones[key][0]