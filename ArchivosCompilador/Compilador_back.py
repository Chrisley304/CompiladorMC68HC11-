from posixpath import splitext
from ArchivosCompilador.Direccionamientos import *
from ArchivosCompilador.Utilidades import *

# Entra una linea -> {espacio=, contenido=[],compilado=,localidad=}
def Precompilado(linea: dict, Mnemonicos: dict, Variables: dict,Etiquetas:dict,ContMemoria:hex):
    
    if linea["contenido"][0] in Etiquetas: 
        parametros = linea["contenido"][1:] # Se obtiene la lista del indice 1-.. debido a que se omite el primer indice que ya no nos es util aquí
    else:
        parametros = linea["contenido"]
    
    nombre_mnemo = parametros[0]  # Se obtiene el nombre del mnemonico

    if nombre_mnemo in Mnemonicos:  # Busca si esta en la lista de Mnemonicos del Excel
        # Si entra en la condicion sabemos que es una instruccion
        
        mnemoni = Mnemonicos[nombre_mnemo]
        # {INH:OPCODE; NBYTES}
        if "INH" in mnemoni:  # Es una intruccion en INH
            if len(parametros) > 1:  # ["mnemonico","OPERANDOS"]
                linea["compilado"] = "ERROR 006"
                linea["localidad"] = ContMemoria
                return ContMemoria
            else:
                opcode = mnemoni["INH"][0]
                bytes = mnemoni["INH"][1]
                linea["compilado"] = "{} {}".format(getHexString(ContMemoria),opcode)
                linea["OPCODE"] = opcode
                linea["localidad"] = ContMemoria
                return SumHex(ContMemoria,int(float(bytes))) # ejemplo:  

        elif "REL" in mnemoni:
            if len(parametros) == 2:  # ["mnemonico","Parametros"] SALTOS PARA ATRAS
                if parametros[1] in Etiquetas:
                    etiqueta = Etiquetas[parametros[1]]
                    origen = SumHex(ContMemoria,2)
                    salto = ResHex(etiqueta,origen)

                    if(CheckHex(etiqueta, origen, True)):
                        opcode = mnemoni["REL"][0]
                        linea["compilado"] = "{} {}{}".format(getHexString(ContMemoria),opcode, getHexString(salto))
                        linea["OPCODE"] = opcode
                        linea["operando"] = getHexString(salto)
                        linea["localidad"] = ContMemoria
                        return SumHex(ContMemoria, int(float(mnemoni["REL"][1])))

                    else:
                        # ERROR 008 SALTO RELATIVO MUY LEJANO
                        linea["compilado"] = "ERROR 008"
                        linea["localidad"] = ContMemoria
                        return ContMemoria
                else:
                    # Se deja pendiente para el post compilado
                    linea["localidad"] = ContMemoria
                    return SumHex(ContMemoria, int(float(mnemoni["REL"][1])))
            
            elif len(parametros) > 2:
                # ERROR 012 INSTRUCCIÓN CON EXCESO DE OPERANDO(S)
                linea["compilado"] = "ERROR 012"
                linea["localidad"] = ContMemoria
                return ContMemoria
            else:
                linea["compilado"] = "ERROR 005"
                linea["localidad"] = ContMemoria
                return ContMemoria

        # Es una instruccion en otro tipo de direccionamiento (NO INH o REL)
        else:
            #direccionMem = codigo[1]
            # VerificarDirecciona(direccionMem)
            if len(parametros) > 1:
                operando = parametros[1]

                if operando[0] == "#":  # Si inicia con '#' es IMM
                    return IMM(linea,Variables,Etiquetas,ContMemoria,mnemoni) #Devuelve el ContMemoria

                elif ",x" in operando:  # Es IND,X
                    return INDX(linea,Variables,Etiquetas,ContMemoria,mnemoni)

                elif ",y" in operando:  # Es IND,Y
                    return INDY(linea,Variables,Etiquetas,ContMemoria,mnemoni)

                else:  # Puede ser DIR o EXT
                    return DIR_EXT(linea,Variables,Etiquetas,ContMemoria,mnemoni)
            else:
                linea["compilado"] = "ERROR 005"
                linea["localidad"] = ContMemoria
                return ContMemoria


    else:  # error mnemonico inexistente
        linea["compilado"] = "ERROR 004"
        linea["localidad"] = ContMemoria
        return ContMemoria

def PostCompilado(linea: dict, Mnemonicos: dict,Etiquetas:dict, Variables: dict):
    if linea["contenido"][0] in Etiquetas: 
        parametros = linea["contenido"][1:] # Se obtiene la lista del indice 1-.. debido a que se omite el primer indice que ya no nos es util aquí
    else:
        parametros = linea["contenido"]
    nombre_mnemo = parametros[0]  # Se obtiene el nombre del mnemonico
    mnemonico = Mnemonicos[nombre_mnemo]
    ContMemoria = linea["localidad"]

    if "REL" in mnemonico:
        if parametros[1] in Etiquetas:
            # CAMBIAR A SALTOS PARA ADELANTE 
            etiqueta = Etiquetas[parametros[1]]
            origen = ContMemoria

            if(CheckHex(etiqueta, origen, False)):
                salto = ResHex(etiqueta,origen)
                opcode = mnemonico["REL"][0]
                linea["OPCODE"] = opcode
                linea["operando"] = getHexString(salto)

                linea["compilado"] = "{} {}{}".format(getHexString(ContMemoria),opcode, getHexString(salto))
            else: 
                linea["compilado"] = "ERROR 008"
        else:
            linea["compilado"] = "ERROR 003"

    # Es una instruccion en otro tipo de direccionamiento (NO INH o REL)
    else:
        #direccionMem = codigo[1]
        # VerificarDirecciona(direccionMem)
        operando = parametros[1]
        dir_o_ext= None
        
        if operando[0] == "#":  # Si inicia con '#' es IMM
            variable = operando[1:]
            opcode = mnemonico["IMM"][0]
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
                linea["compilado"] = "ERROR 001/002/003"

            if len(compilado)/2 == mnemonico["IMM"][1]:
                linea["OPCODE"] = opcode
                linea["operando"] = Variables[variable]
                linea["compilado"] = "{} {}".format(getHexString(ContMemoria), compilado)
            else:
                linea["compilado"] = "ERROR 007"

        else:  # Puede ser DIR o EXT
            
            if operando in Variables:  # si esta registrada existe
                hex_op = getHexString(Variables[operando])
                dir_o_ext = 2
            
            elif operando in Etiquetas:  # si esta registrada existe
                hex_op = getHexString(Etiquetas[operando])
                dir_o_ext = 2

            else: # No esta registrada
                linea["compilado"] = "ERROR 001/002/003"

            if operando in Variables or operando in Etiquetas:
                if len(hex_op) == 2:
                    hex_op = "00{}".format(hex_op)

            if dir_o_ext == 1: # Es DIR
                opcode = mnemonico["DIR"][0]
                compilado = opcode + hex_op
                if len(compilado)/2 == mnemonico["DIR"][1]:
                    linea["OPCODE"] = opcode
                    linea["operando"] = hex_op
                    linea["compilado"] = "{} {}".format(getHexString(ContMemoria), compilado)
                else:
                    linea["compilado"] = "ERROR 007"
            elif dir_o_ext == 2: # Es EXT
                opcode = mnemonico["EXT"][0]
                compilado = opcode + hex_op
                if len(compilado)/2 == mnemonico["EXT"][1]:
                    linea["OPCODE"] = opcode
                    linea["operando"] = hex_op
                    linea["compilado"] = "{} {}".format(getHexString(ContMemoria), compilado)
                else:
                    linea["compilado"] = "ERROR 007"
            else: # NO se encontro la variable o etiqueta
                linea["compilado"] = "ERROR 001/002/003"

def EscrituraLST(lineas_comp:list,lineas_orig:list,filename):
    texto_final = ""
    for i in range(len(lineas_comp)):
        if len(lineas_comp[i]["compilado"].strip()) <=8 and len(lineas_comp[i]["compilado"].strip()) >= 6:
            texto_final += "{} {}   \t\t\t\t {}".format(i+1,lineas_comp[i]["compilado"],lineas_orig[i])
        elif len(lineas_comp[i]["compilado"].strip()) > 11:
            texto_final += "{} {} \t\t {}".format(i+1,lineas_comp[i]["compilado"],lineas_orig[i])
        else:
            texto_final += "{} {} \t\t\t\t {}".format(i+1,lineas_comp[i]["compilado"],lineas_orig[i])

    texto_final += "\n\n=== Descripcion de errores ===\n001   CONSTANTE INEXISTENTE\n002   VARIABLE INEXISTENTE\n003   ETIQUETA INEXISTENTE\n004   MNEMÓNICO INEXISTENTE\n005   INSTRUCCIÓN CARECE DE  OPERANDO(S)\n006   INSTRUCCIÓN NO LLEVA OPERANDO(S)\n007   MAGNITUD DE  OPERANDO ERRONEA\n008   SALTO RELATIVO MUY LEJANO\n009   INSTRUCCIÓN CARECE DE ALMENOS UN ESPACIO RELATIVO AL MARGEN\n010   NO SE ENCUENTRA END\n011   SINTAXIS INCORRECTA\n012   INSTRUCCIÓN CON EXCESO DE OPERANDO(S)"
    
    filename = splitext(filename)[0]
    with open("Salida/"+filename+".LST","w",encoding="UTF-8") as archivo:
        archivo.write(texto_final)

def EscrituraHTML(lineas_comp:list,lineas_orig:list,filename):
    texto_final = '''<html>
        <head>
            <title>Document</title>
        </head>
        <body>'''
            
    
    for i in range(len(lineas_comp)):
        if not lineas_comp[i]["OPCODE"] == "":
            texto_final += Convert_to_HTML(i+1,getHexString(lineas_comp[i]["localidad"]),lineas_comp[i]["OPCODE"],lineas_comp[i]["operando"],lineas_orig[i])
        else:
             texto_final += "<p>{}: {}:{}</p>".format(i+1,lineas_comp[i]["compilado"],lineas_orig[i])
    texto_final += "<p>=== Descripcion de errores ===<br>001   CONSTANTE INEXISTENTE<br>002   VARIABLE INEXISTENTE<br>003   ETIQUETA INEXISTENTE<br>004   MNEMÓNICO INEXISTENTE<br>005   INSTRUCCIÓN CARECE DE  OPERANDO(S)<br>006   INSTRUCCIÓN NO LLEVA OPERANDO(S)<br>007   MAGNITUD DE  OPERANDO ERRONEA<br>008   SALTO RELATIVO MUY LEJANO<br>009   INSTRUCCIÓN CARECE DE ALMENOS UN ESPACIO RELATIVO AL MARGEN<br>010   NO SE ENCUENTRA END<br>011   SINTAXIS INCORRECTA<br>012   INSTRUCCIÓN CON EXCESO DE OPERANDO(S)</p></body></html>"
    
    filename = splitext(filename)[0]
    with open("Salida/"+filename+".html","w",encoding="UTF-8") as archivo:
        archivo.write(texto_final)


def EscrituraS19(lineas_comp:list,filename):
    texto_final = ""
    contadorDeMemoria = hex(0)
    counter = 0
    aux = []
    
    for i in range(len(lineas_comp)):

        # Si org, modificamos contDeMemo y counter
        if(len(lineas_comp[i]['contenido']) == 2 and lineas_comp[i]['contenido'][0].lower() == 'org'):
            contadorDeMemoria = ConvertHex(lineas_comp[i]['contenido'][1][1:])
            counter = 0

        else:
            # Es una instrucción compilada
            if not lineas_comp[i]["OPCODE"] == "":
                aux = Divide_str(lineas_comp[i]["OPCODE"])
                for item in aux:
                    if(counter == 0):
                        texto_final += "\n <{}>".format(getHexString(contadorDeMemoria))
                        counter = 16
                    texto_final += " " + item
                    contadorDeMemoria = SumHex(contadorDeMemoria, 1)
                    counter -= 1

                aux = Divide_str(lineas_comp[i]["operando"])

                for item in aux:
                    if(counter == 0):
                        texto_final += "\n <{}>".format(getHexString(contadorDeMemoria))
                        counter = 16
                
                    texto_final += " " + item
                    contadorDeMemoria = SumHex(contadorDeMemoria, 1)
                    counter -= 1


    filename = splitext(filename)[0]
    with open("Salida/"+filename+".S19","w",encoding="UTF-8") as archivo:
        archivo.write(texto_final)