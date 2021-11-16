from posixpath import splitext
from ArchivosCompilador.Direccionamientos import *
from ArchivosCompilador.Utilidades import *

# Entra una linea -> {espacio=, contenido=[],compilado=,localidad=}
def Precompilado(linea: dict, Mnemonicos: dict, Variables: dict,ContMemoria:hex):
    
    parametros = linea["contenido"] # Se obtiene la lista del indice 1-.. debido a que se omite el primer indice que ya no nos es util aquí
    
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
                linea["localidad"] = ContMemoria
                return SumHex(ContMemoria,int(float(bytes))) # ejemplo:  

        elif "REL" in mnemoni:
            if len(parametros) == 2:  # ["mnemonico","Parametros"] SALTOS PARA ATRAS
                if parametros[1] in Variables:
                    etiqueta = Variables[parametros[1]]
                    origen = SumHex(ContMemoria,2)
                    salto = ResHex(etiqueta,origen)
                    opcode = mnemoni["REL"][0]
                    linea["compilado"] = "{} {}{}".format(getHexString(ContMemoria),opcode, getHexString(salto))
                    linea["localidad"] = ContMemoria
                    return SumHex(ContMemoria, int(float(mnemoni["REL"][1])))
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
                    return IMM(linea,Variables,ContMemoria,mnemoni) #Devuelve el ContMemoria

                elif ",x" in operando:  # Es IND,X
                    return INDX(linea,Variables,ContMemoria,mnemoni)

                elif ",y" in operando:  # Es IND,Y
                    return INDY(linea,Variables,ContMemoria,mnemoni)

                else:  # Puede ser DIR o EXT
                    return DIR_EXT(linea,Variables,ContMemoria,mnemoni)
            else:
                linea["compilado"] = "ERROR 005"
                linea["localidad"] = ContMemoria
                return ContMemoria


    else:  # error mnemonico inexistente
        linea["compilado"] = "ERROR 004"
        linea["localidad"] = ContMemoria
        return ContMemoria


def PostCompilado(linea: dict, Mnemonicos: dict, Variables: dict):
    parametros = linea["contenido"] # Se obtiene la lista del indice 1-.. debido a que se omite el primer indice que ya no nos es util aquí
    nombre_mnemo = parametros[0]  # Se obtiene el nombre del mnemonico
    mnemonico = Mnemonicos[nombre_mnemo]
    ContMemoria = linea["localidad"]

    if "REL" in mnemonico:
        if parametros[1] in Variables:
            # CAMBIAR A SALTOS PARA ADELANTE 
            etiqueta = Variables[parametros[1]]
            origen = SumHex(ContMemoria,2)
            salto = ResHex(etiqueta,origen)
            opcode = mnemonico["REL"][0]
            linea["compilado"] = "{} {}{}".format(getHexString(ContMemoria),opcode, getHexString(salto))
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
                compilado = opcode + Variables[variable]
            else:  # Variable no existe
                linea["compilado"] = "ERROR 001, 002 o 003"

            if len(compilado)/2 == mnemonico["IMM"][1]:
                linea["compilado"] = "{} {}".format(getHexString(ContMemoria), compilado)
            else:
                linea["compilado"] = "ERROR 007"

        else:  # Puede ser DIR o EXT
            if operando in Variables:  # si esta registrada existe
                hex_op = getHexString(Variables[operando])
                if len(hex_op) == 2:  # Debe de ser de 8 bits para DIR
                    dir_o_ext = 1
                elif len(hex_op) == 4:  # Debe de ser de 16 bits para EXT
                    dir_o_ext = 2

            else: # No esta registrada
                linea["compilado"] = "ERROR 001, 002 o 003"

        if dir_o_ext == 1: # Es DIR
            opcode = mnemonico["DIR"][0]
            compilado = opcode + hex_op
            if len(compilado)/2 == mnemonico["DIR"][1]:
                linea["compilado"] = "{} {}".format(getHexString(ContMemoria), compilado)
            else:
                linea["compilado"] = "ERROR 007"
        elif dir_o_ext == 2: # Es EXT
            opcode = mnemonico["EXT"][0]
            compilado = opcode + hex_op
            if len(compilado)/2 == mnemonico["EXT"][1]:
                linea["compilado"] = "{} {}".format(getHexString(ContMemoria), compilado)
            else:
                linea["compilado"] = "ERROR 007"
        else: # NO es ni EXT ni DIR
            linea["compilado"] = "ERROR 007"

def Escritura(lineas_comp:list,lineas_orig:list,filename):
    texto_final = ""
    for i in range(len(lineas_comp)):
        if len(lineas_comp[i]["compilado"].strip()) <=8 and len(lineas_comp[i]["compilado"].strip()) >= 6:
            texto_final += "{} {}   \t\t\t {}".format(i+1,lineas_comp[i]["compilado"],lineas_orig[i])
        else:
            texto_final += "{} {} \t\t\t {}".format(i+1,lineas_comp[i]["compilado"],lineas_orig[i])
    filename = splitext(filename)[0]
    with open("Salida/"+filename+".ASC","w") as archivo:
        archivo.write(texto_final)