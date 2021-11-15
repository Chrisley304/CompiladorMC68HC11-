from ArchivosCompilador.Direccionamientos import *
from ArchivosCompilador.Utilidades import *

def Precompilado(linea: dict, Mnemonicos: dict, Variables: dict,ContMemoria:hex):
    
    parametros = linea["contenido"] # Se obtiene la lista del indice 1-.. debido a que se omite el primer indice que ya no nos es util aquí
    
    nombre_mnemo = parametros[0]  # Se obtiene el nombre del mnemonico

    if nombre_mnemo in Mnemonicos:  # Busca si esta en la lista de Mnemonicos del Excel
        # Si entra en la condicion sabemos que es una instruccion
        
        mnemoni = Mnemonicos[nombre_mnemo]

        if "INH" in mnemoni:  # Es una intruccion en INH
            if len(parametros) > 1:  # ["mnemonico","OPERANDOS"]
                linea["compilado"] = "ERROR 006   INSTRUCCIÓN NO LLEVA OPERANDO(S)"
                return ContMemoria
            else:
                opcode = mnemoni["INH"][0]
                bytes = mnemoni["INH"][1]
                linea["compilado"] = "{} {}".format(getHexString(ContMemoria),opcode)
                
                return SumHex(ContMemoria,int(bytes)) # ejemplo: 8000 + 1 = 8001


        elif "REL" in mnemoni:
            if len(parametros) > 1:  # ["mnemonico","OPERANDOS"]
                if parametros[1] in Variables:
                    etiqueta = Variables[parametros[1]]
                    origen = SumHex(ContMemoria,2)
                    salto = ResHex(etiqueta,origen)
                    opcode = mnemoni["REL"][0]
                    linea["compilado"] = "{} {}{}".format(getHexString(ContMemoria),opcode, getHexString(salto))
                    return SumHex(ContMemoria, int(mnemoni["REL"][1]))
                else:
                    # Se deja pendiente para el post compilado
                    return SumHex(ContMemoria,2)
            else:
                linea["compilado"] = "ERROR 005   INSTRUCCIÓN CARECE DE OPERANDO(S)"
                return ContMemoria

        # Es una instruccion en otro tipo de direccionamiento (NO INH o REL)
        else:
            #direccionMem = codigo[1]
            # VerificarDirecciona(direccionMem)
            operando = parametros[1]

            if operando[0] == "#":  # Si inicia con '#' es IMM
                return IMM(linea,Variables,ContMemoria,mnemoni) #Devuelve el ContMemoria

            elif ",x" in operando:  # Es IND,X
                return INDX(linea,Variables,ContMemoria,mnemoni)

            elif ",y" in operando:  # Es IND,Y
                return INDY(linea,Variables,ContMemoria,mnemoni)

            else:  # Puede ser DIR o EXT
                

                    else:  # Variable no existe
                        linea["compilado"] = "Error", "002 VARIABLE INEXISTENTE"

    else:  # error mnemonico inexistente
        linea["compilado"] = "ERROR 004 MNEMÓNICO INEXISTENTE"

    # Esta funcion solo va a regresar el valor de cont memoria, ya que se pasa por valor y no por ref.
    return ContMemoria

