from Compilador_back import getHexString,

def IMM(linea:dict,Variables:dict,ContMem:hex,mnemonico:dict):
    operando = linea["contenido"][1]
    if operando[1] == "$":  # Si el operando lleva "$" ya esta en hexadecimal
        opcode = mnemonico["IMM"][0]
        linea["compilado"] = "{} {}{}".format(
            getHexString(ContMemoria), opcode, operando[2:])
        return [nombre_mnemo, "IMM", [hex(int(operando[1:]))]]
    elif operando[1] == "'":  # es un caracter ASCII
        dec = ord(operando[2])
        # hex -> 0x[hex]
        return [nombre_mnemo, "IMM", [hex(int(dec))]]
    # La cadena son puros numeros, por tanto esta en dec
    elif operando[1:].isnumeric():
        # Obtiene el numero decimal para convertirlo a hexadecimal despues
        dec = operando[1:]
        return [nombre_mnemo, "IMM", [hex(int(dec))]]
    else:  # esta utilizando una constante
        variable = operando[1:]
        if variable in Variables:  # si esta registrada existe
            return [nombre_mnemo, "IMM", [Variables[variable]]]
        else:  # Variable no existe
            return ["Error", "002 VARIABLE INEXISTENTE", []]
