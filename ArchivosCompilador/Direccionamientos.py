from io import open_code
from ArchivosCompilador.Utilidades import *

def IMM(linea:dict,Variables:dict,Etiquetas:dict,ContMemoria:hex,mnemonico:dict):
    if linea["contenido"][0] in Etiquetas: 
        operando = linea["contenido"][2]
    else:
        operando = linea["contenido"][1]
    opcode = mnemonico["IMM"][0]
    compilado = ""
    
    if operando[1] == "$":  # Si el operando lleva "$" ya esta en hexadecimal
        hex_temp = ConvertHex(operando[2:])
        compilado = opcode + getHexString(hex_temp)
        linea["operando"] = getHexString(hex_temp)
    elif operando[1] == "'":  # es un caracter ASCII
        dec = ord(operando[2])
        compilado = opcode + getHexStringInt(dec)
        linea["operando"] = getHexStringInt(dec)
    # La cadena son solo numeros, por tanto esta en dec
    elif operando[1:].isnumeric():
        # Obtiene el numero decimal para convertirlo a hexadecimal despues
        dec = operando[1:]
        compilado = opcode + getHexStringInt(dec)
        linea["operando"] = getHexStringInt(dec)
    else:  # esta utilizando una constante
        variable = operando[1:]
        if variable in Variables:  # si esta registrada existe
            hex_op = getHexString(Variables[variable])
            if len(hex_op) == 2:
                hex_op = "00{}".format(hex_op)
            compilado = opcode + hex_op
            linea["operando"] = Variables[variable]
        elif variable in Etiquetas:
            hex_op = getHexString(Etiquetas[variable])
            if len(hex_op) == 2:
                hex_op = "00{}".format(hex_op)
            compilado = opcode + hex_op
            linea["operando"] = Etiquetas[variable]
        else:  # Variable no existe
            # Se deja pendiente por si es una etiqueta
            linea["localidad"] = ContMemoria
            return SumHex(ContMemoria, int(float(mnemonico["IMM"][1])))
    # OPCODE HEXADECIMAL 
    if len(compilado)/2 == mnemonico["IMM"][1]:
        linea["compilado"] = "{} {}".format(getHexString(ContMemoria), compilado)
        linea["OPCODE"] = opcode
        linea["localidad"] = ContMemoria
        return SumHex(ContMemoria, int(float(mnemonico["IMM"][1])))
    else:
        linea["compilado"] = "ERROR 007"
        linea["localidad"] = ContMemoria
        return ContMemoria


def INDX(linea: dict, Variables: dict,Etiquetas:dict, ContMemoria: hex, mnemonico: dict):
    if linea["contenido"][0] in Etiquetas: 
        operando = linea["contenido"][2]
    else:
        operando = linea["contenido"][1]
    opcode = mnemonico["IND,X"][0]
    compilado = ""

    if operando[0] == "$":  # Si el operando lleva "$" ya esta en hexadecimal
        compilado = opcode + operando[-2]
        linea["operando"] = operando[-2].upper()
    elif operando[0] == "'":  # es un caracter ASCII
        dec = ord(operando[1])
        compilado = opcode + getHexStringInt(dec)
        linea["operando"] = getHexStringInt(dec)
    # La cadena son solo numeros, por tanto esta en dec
    elif operando[-2].isnumeric():
        # Obtiene el numero decimal para convertirlo a hexadecimal despues
        dec = operando[-2]
        compilado = opcode + getHexStringInt(dec)
        linea["operando"] = getHexString(dec)
    else:  # esta utilizando una constante
        variable = operando[-2]
        if variable in Variables:  # si esta registrada existe
            compilado = opcode + Variables[variable]
            linea["operando"] = Variables[variable]
        else:  # Variable no existe
            linea["compilado"] = "ERROR 001/002"
            linea["localidad"] = ContMemoria
            return ContMemoria
    
    if len(compilado)/2 == mnemonico["IND,X"][1]:
        linea["compilado"] = "{} {}".format(getHexString(ContMemoria), compilado)
        linea["OPCODE"] = opcode
        linea["localidad"] = ContMemoria
        return SumHex(ContMemoria, int(float(mnemonico["IND,X"][1])))
    else:
        linea["compilado"] = "ERROR 007"
        linea["localidad"] = ContMemoria
        return ContMemoria

def INDY(linea: dict, Variables: dict,Etiquetas:dict, ContMemoria: hex, mnemonico: dict):
    if linea["contenido"][0] in Etiquetas: 
        operando = linea["contenido"][2]
    else:
        operando = linea["contenido"][1]
    opcode = mnemonico["IND,Y"][0]
    compilado = ""
    
    if operando[0] == "$":  # Si el operando lleva "$" ya esta en hexadecimal
        compilado = opcode + operando[1:-2]
        linea["operando"] = operando[1:-2].upper()
    elif operando[0] == "'":  # es un caracter ASCII
        dec = ord(operando[1])
        compilado = opcode + getHexStringInt(dec)
        linea["operando"] = getHexStringInt(dec)
    # La cadena son solo numeros, por tanto esta en dec
    elif operando[-2].isnumeric():
        # Obtiene el numero decimal para convertirlo a hexadecimal despues
        dec = operando[-2]
        compilado = opcode + getHexStringInt(dec)
        linea["operando"] = getHexString(dec)
    else:  # esta utilizando una constante
        variable = operando[-2]
        if variable in Variables:  # si esta registrada existe
            compilado = opcode + Variables[variable]
            linea["operando"] = Variables[variable]
        else:  # Variable no existe
            linea["compilado"] = "ERROR 001/002"
            linea["localidad"] = ContMemoria
            return ContMemoria
    
    if len(compilado)/2 == mnemonico["IND,Y"][1]:
        linea["compilado"] = "{} {}".format(getHexString(ContMemoria), compilado)
        linea["OPCODE"] = opcode
        linea["localidad"] = ContMemoria
        return SumHex(ContMemoria, int(float(mnemonico["IND,Y"][1])))
    else:
        linea["compilado"] = "ERROR 007"
        linea["localidad"] = ContMemoria
        return ContMemoria

def DIR_EXT(linea: dict, Variables: dict,Etiquetas:dict, ContMemoria: hex, mnemonico: dict):
    if linea["contenido"][0] in Etiquetas: 
        operando = linea["contenido"][2]
    else:
        operando = linea["contenido"][1]
    dir_o_ext = None # Si es 1 es DIR, si es 2 es EXT
    hex_op = None
    compilado = ""

    if operando[0] == "$":  # Si el operando lleva "$" ya esta en hexadecimal
        hex_op = operando[1:]
        linea["operando"] = hex_op.upper()
        if len(hex_op) == 2:  # Si es de 8 bits es DIR
            dir_o_ext = 1
        elif len(hex_op) == 4:  # Si es de 16 bits es EXT
            dir_o_ext = 2

    elif operando[0] == "'":  # es un caracter ASCII
        dec = ord(operando[1])
        hex_op = getHexStringInt(int(dec))
        linea["operando"] = hex_op
        if len(hex_op) == 2:  # es de 8 bits (DIR)
            dir_o_ext = 1
        elif len(hex_op) == 4:  # es de 16 bits (EXT)
            dir_o_ext = 2

    elif operando.isnumeric():  # Si son numeros Esta en dec y puede ser DIR o EXT
        # Obtiene el numero decimal para convertirlo a hexadecimal despues
        hex_op = getHexStringInt(int(operando))
        linea["operando"] = hex_op

        if len(hex_op) == 2:  # Debe de ser de 8 bits para DIR
            dir_o_ext = 1
        elif len(hex_op) == 4:  # Debe de ser de 16 bits para EXT
            dir_o_ext = 2

    else:  # Es una variable:
        if operando in Variables:  # si esta registrada existe
            hex_op = getHexString(Variables[operando])
            linea["operando"] = hex_op
            dir_o_ext = 2
        elif operando in Etiquetas:
            hex_op = getHexString(Etiquetas[operando])
            linea["operando"] = hex_op
            dir_o_ext = 2
        
        else: # No esta registrada y puede ser una etiqueta
            # Se deja pendiente por si es una etiqueta
            linea["localidad"] = ContMemoria
            loc_str = getHexString(ContMemoria)
            return SumHex(ContMemoria, int(float(mnemonico["EXT"][1])))
    
    if operando in Variables or operando in Etiquetas:
        if len(hex_op) == 2:
            hex_op = "00{}".format(hex_op)

    if dir_o_ext == 1: # Es DIR
        opcode = mnemonico["DIR"][0]
        compilado = opcode + hex_op
        if len(compilado)/2 == int(float(mnemonico["DIR"][1])):
            linea["operando"] = hex_op
            linea["OPCODE"] = opcode
            linea["compilado"] = "{} {}".format(getHexString(ContMemoria), compilado)
            
            linea["localidad"] = ContMemoria
            return SumHex(ContMemoria, int(float(mnemonico["DIR"][1])))
        else:
            linea["compilado"] = "ERROR 007"
            linea["localidad"] = ContMemoria
            return ContMemoria
    elif dir_o_ext == 2: # Es EXT
        opcode = mnemonico["EXT"][0]
        compilado = opcode + hex_op
        if len(compilado)/2 == mnemonico["EXT"][1]:
            linea["compilado"] = "{} {}".format(getHexString(ContMemoria), compilado)
            linea["OPCODE"] = opcode

            linea["localidad"] = ContMemoria
            return SumHex(ContMemoria, int(float(mnemonico["EXT"][1])))
        else:
            linea["compilado"] = "ERROR 007"
            linea["localidad"] = ContMemoria
            return ContMemoria
    else: # NO es ni EXT ni DIR
        linea["compilado"] = "ERROR 007"
        linea["localidad"] = ContMemoria
        return ContMemoria


def Especiales(linea: dict, Variables: dict,Etiquetas:dict, ContMemoria: hex, mnemonico: dict):
    
    operandos = linea["contenido"][1].split(",")
    primero = None
    segundo = None
    opcode = None
    direcc = ""
    
    #Directo
    if(len(operandos) == 2):
        opcode = mnemonico["DIR"][0]
        direcc = "DIR"
        primero = operandos[0]
        segundo = operandos[1]
        
    #Ind,x o Ind, y
    elif(len(operandos) == 3):
        if(operandos[1] == "x"):
            opcode = mnemonico["IND,X"][0]
            direcc = "IND,X"
            primero = operandos[0]
            segundo = operandos[2]

        elif(operandos[1] == "y"):
            opcode = mnemonico["IND,Y"][0]
            direcc = "IND,Y"
            primero = operandos[0]
            segundo = operandos[2]

    #Error de sintaxis
    if opcode == None:
        linea["compilado"] = "ERROR 011"
        linea["localidad"] = ContMemoria
        return ContMemoria
    
    if segundo[0] != "#":
        linea["compilado"] = "ERROR 011"
        linea["localidad"] = ContMemoria
        return ContMemoria
    
    # Si llegas aqui, todo va chido

    if primero[0] == "$":  # Si el operando lleva "$" ya esta en hexadecimal
        hex_op = primero[1:]
        linea["operando"] = hex_op.upper()

    elif primero[0] == "'":  # es un caracter ASCII
        dec = ord(primero[1])
        hex_op = getHexStringInt(int(dec))
        linea["operando"] = hex_op.upper()

    elif primero.isnumeric():  # Si son numeros Esta en dec y puede ser DIR o EXT
        # Obtiene el numero decimal para convertirlo a hexadecimal despues
        hex_op = getHexStringInt(int(primero))
        linea["operando"] = hex_op.upper()

    # Se esta rompiendo aca
    else:
        linea["compilado"] = "ERROR 007"
        linea["localidad"] = ContMemoria
        return ContMemoria

    if segundo[1] == "$":  # Si el operando lleva "$" ya esta en hexadecimal
        hex_op2 = segundo[2:]
        linea["operando"] += hex_op2.upper()

    elif segundo[1] == "'":  # es un caracter ASCII
        dec = ord(segundo[2])
        hex_op2 = getHexStringInt(int(dec))
        linea["operando"] += hex_op2.upper()

    elif segundo[1:].isnumeric():  # Si son numeros Esta en dec y puede ser DIR o EXT
        # Obtiene el numero decimal para convertirlo a hexadecimal despues
        hex_op2 = getHexStringInt(int(segundo[1:]))
        linea["operando"] += hex_op2.upper()

    else:
        linea["compilado"] = "ERROR 007"
        linea["localidad"] = ContMemoria
        return ContMemoria    
    
    # instruccion de 2 operandos
    if len(linea["contenido"]) == 2:

        if linea["contenido"][0] == "brclr" or linea["contenido"][0] == "brset":
            linea["compilado"] = "ERROR 005"
            linea["localidad"] = ContMemoria
            return ContMemoria    
        
    elif len(linea["contenido"]) == 3:

        if linea["contenido"][0] == "bclr" or linea["contenido"][0] == "bset":
            linea["compilado"] = "ERROR 012"
            linea["localidad"] = ContMemoria
            return ContMemoria    

        etiqueta = linea["contenido"][2]
        
        if etiqueta in Etiquetas:  # si esta registrada se calcula el salto hacia atras
            hex_etiq = Etiquetas[etiqueta]
            origen = ContMemoria

            # if(CheckHex(etiqueta, origen, CheckSalto(hex_etiq, SumHex(origen, mnemonico[direcc][1])))): 
            salto = ResHex(hex_etiq,SumHex(origen,mnemonico[direcc][1]))
            opcode = mnemonico[direcc][0]
            
            if salto == None:
                linea["compilado"] = "ERROR 008"
                return ContMemoria
            else:
                linea["operando"] += getHexString(salto)

        else:  # Etiqueta puede aun no declararse (salto posterior, se deja pendiente, en el post se calculará)
            linea["localidad"] = ContMemoria
            linea["direcc"] = direcc
            return SumHex(ContMemoria, int(float(mnemonico[direcc][1])))
    
    else:
        linea["compilado"] = "ERROR 011"
        linea["localidad"] = ContMemoria
        return ContMemoria
    
    if len(opcode + linea["operando"])/2 == mnemonico[direcc][1]:
            # Compila
            linea["OPCODE"] = opcode
            linea["localidad"] = ContMemoria
            linea["compilado"] = "{} {}{}".format(getHexString(ContMemoria) , opcode ,linea["operando"])
            return SumHex(ContMemoria, int(float(mnemonico[direcc][1])))
    else:
        linea["compilado"] = "ERROR 007"
        linea["localidad"] = ContMemoria
        return ContMemoria


""" Instrucciones especiales:
Casos de 3: 
- BRCLR (3 operandos)
- BRSET (3 operandos)
    ej. 15,#12 Etiqueta
        [DIR,INDXoY de 8 bits][IMM] [Etiqueta] <- La etiqueta se calcula como relativa
        15,x,#12 Etiqueta
        15,y,#12 Etiqueta

Casos de 2:
- BRCLR (3 operandos) * etiquetas pendiente                    EJ. $16,#$15 etiqueta o  $16,y,#$15 etiqueta o $16,x,#$15 etiqueta
- BRSET (3 operandos) * etiquetas pendiente                    3 operandos -> Viene dir/indx/indy luego viene inmediato y luego etiqueta 
- BCLR (2 operandos)
- BSET (2 operandos)
    ej. 15,#12 
        15,x,#12 
        15,y,#12 """