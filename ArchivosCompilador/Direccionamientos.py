from io import open_code
from ArchivosCompilador.Utilidades import *

def IMM(linea:dict,Variables:dict,ContMemoria:hex,mnemonico:dict):
    operando = linea["contenido"][1]
    opcode = mnemonico["IMM"][0]
    compilado = ""
    
    if operando[1] == "$":  # Si el operando lleva "$" ya esta en hexadecimal
        compilado = opcode + operando[2:]
    elif operando[1] == "'":  # es un caracter ASCII
        dec = ord(operando[2])
        compilado = opcode + getHexString(dec)
    # La cadena son solo numeros, por tanto esta en dec
    elif operando[1:].isnumeric():
        # Obtiene el numero decimal para convertirlo a hexadecimal despues
        dec = operando[1:]
        compilado = opcode + getHexString(dec)
    else:  # esta utilizando una constante
        variable = operando[1:]
        if variable in Variables:  # si esta registrada existe
            compilado = opcode + Variables[variable]
        else:  # Variable no existe
            # Se deja pendiente por si es una etiqueta
            return SumHex(ContMemoria, int(mnemonico["IMM"][1]))

    if len(compilado)/2 == mnemonico["IMM"][1]:
        linea["compilado"] = "{} {}".format(getHexString(ContMemoria), compilado)
        return SumHex(ContMemoria, int(mnemonico["IMM"][1]))
    else:
        linea["compilado"] = "ERROR 007   MAGNITUD DE  OPERANDO ERRONEA"
        return ContMemoria


def INDX(linea: dict, Variables: dict, ContMemoria: hex, mnemonico: dict):
    operando = linea["contenido"][1]
    opcode = mnemonico["IND,X"][0]
    compilado = ""
    
    if operando[1] == "$":  # Si el operando lleva "$" ya esta en hexadecimal
        compilado = opcode + operando[1:-2]
    elif operando[1] == "'":  # es un caracter ASCII
        dec = ord(operando[1])
        compilado = opcode + getHexString(dec)
    # La cadena son solo numeros, por tanto esta en dec
    elif operando[1:-2].isnumeric():
        # Obtiene el numero decimal para convertirlo a hexadecimal despues
        dec = operando[1:-2]
        compilado = opcode + getHexString(dec)
    else:  # esta utilizando una constante
        variable = operando[1:-2]
        if variable in Variables:  # si esta registrada existe
            compilado = opcode + Variables[variable]
        else:  # Variable no existe
            linea["compilado"] = "ERROR 002 VARIABLE INEXISTENTE"
            return ContMemoria
    
    if len(compilado)/2 == mnemonico["IND,X"][1]:
        linea["compilado"] = "{} {}".format(getHexString(ContMemoria), compilado)
        return SumHex(ContMemoria, int(mnemonico["IND,X"][1]))
    else:
        linea["compilado"] = "ERROR 007   MAGNITUD DE  OPERANDO ERRONEA"
        return ContMemoria

def INDY(linea: dict, Variables: dict, ContMemoria: hex, mnemonico: dict):
    operando = linea["contenido"][1]
    opcode = mnemonico["IND,Y"][0]
    compilado = ""
    
    if operando[1] == "$":  # Si el operando lleva "$" ya esta en hexadecimal
        compilado = opcode + operando[1:-2]
    elif operando[1] == "'":  # es un caracter ASCII
        dec = ord(operando[1])
        compilado = opcode + getHexString(dec)
    # La cadena son solo numeros, por tanto esta en dec
    elif operando[1:-2].isnumeric():
        # Obtiene el numero decimal para convertirlo a hexadecimal despues
        dec = operando[1:-2]
        compilado = opcode + getHexString(dec)
    else:  # esta utilizando una constante
        variable = operando[1:-2]
        if variable in Variables:  # si esta registrada existe
            compilado = opcode + Variables[variable]
        else:  # Variable no existe
            linea["compilado"] = "ERROR 002 VARIABLE INEXISTENTE"
            return ContMemoria
    
    if len(compilado)/2 == mnemonico["IND,Y"][1]:
        linea["compilado"] = "{} {}".format(getHexString(ContMemoria), compilado)
        return SumHex(ContMemoria, int(mnemonico["IND,Y"][1]))
    else:
        linea["compilado"] = "ERROR 007   MAGNITUD DE  OPERANDO ERRONEA"
        return ContMemoria

def DIR_EXT(linea: dict, Variables: dict, ContMemoria: hex, mnemonico: dict):
    operando = linea["contenido"][1]
    dir_o_ext = None # Si es 1 es DIR, si es 2 es EXT
    hex_op = None
    compilado = ""
    if operando[0] == "$":  # Si el operando lleva "$" ya esta en hexadecimal
        hex_op = operando[1:]
        if len(hex_op) == 2:  # Si es de 8 bits es DIR
            dir_o_ext = 1
        elif len(hex_op) == 4:  # Si es de 16 bits es EXT
            dir_o_ext = 2

    elif operando[0] == "'":  # es un caracter ASCII
        dec = ord(operando[1])
        hex_op = getHexString(int(dec))
        if len(hex_op) >= 1 and len(hex_op) <= 2:  # es de 8 bits (DIR)
            dir_o_ext = 1
        elif len(hex_op) >= 3 and len(hex_op) <= 4:  # es de 16 bits (EXT)
            dir_o_ext = 2

    elif operando.isnumeric():  # Si son numeros Esta en dec y puede ser DIR o EXT
        # Obtiene el numero decimal para convertirlo a hexadecimal despues
        hex_op = getHexString(int(operando))
        if len(hex_op) == 2:  # Debe de ser de 8 bits para DIR
            dir_o_ext = 1
        elif len(hex_op) == 4:  # Debe de ser de 16 bits para EXT
            dir_o_ext = 2

    else:  # Es una variable:
        if operando in Variables:  # si esta registrada existe
            hex_op = getHexString(Variables[operando])
            if len(hex_op) == 2:  # Debe de ser de 8 bits para DIR
                dir_o_ext = 1
            elif len(hex_op) == 4:  # Debe de ser de 16 bits para EXT
                dir_o_ext = 2
        else: # No esta registrada y puede ser una etiqueta
            # Se deja pendiente por si es una etiqueta
            return SumHex(ContMemoria, 2) # NOTA: Aqui duda porque no se si es DIR o EXT
    
    if dir_o_ext == 1: # Es DIR
        opcode = mnemonico["DIR"][0]
        compilado = opcode + hex_op
        if len(compilado)/2 == mnemonico["DIR"][1]:
            linea["compilado"] = "{} {}".format(getHexString(ContMemoria), compilado)
            return SumHex(ContMemoria, int(mnemonico["DIR"][1]))
        else:
            linea["compilado"] = "ERROR 007   MAGNITUD DE  OPERANDO ERRONEA"
            return ContMemoria
    elif dir_o_ext == 2: # Es EXT
        opcode = mnemonico["EXT"][0]
        compilado = opcode + hex_op
        if len(compilado)/2 == mnemonico["EXT"][1]:
            linea["compilado"] = "{} {}".format(getHexString(ContMemoria), compilado)
            return SumHex(ContMemoria, int(mnemonico["EXT"][1]))
        else:
            linea["compilado"] = "ERROR 007   MAGNITUD DE  OPERANDO ERRONEA"
            return ContMemoria
    else: # NO es ni EXT ni DIR
        linea["compilado"] = "ERROR 007   MAGNITUD DE  OPERANDO ERRONEA"
        return ContMemoria