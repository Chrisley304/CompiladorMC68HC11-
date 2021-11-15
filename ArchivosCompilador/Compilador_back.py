from Direccionamientos import *
from Utilidades import *

def Precompilado(linea: dict, Mnemonicos: dict, Variables: dict,ContMemoria:hex):
    
    parametros = linea["contenido"] # Se obtiene la lista del indice 1-.. debido a que se omite el primer indice que ya no nos es util aquí
    
    nombre_mnemo = parametros[0]  # Se obtiene el nombre del mnemonico

    if nombre_mnemo in Mnemonicos:  # Busca si esta en la lista de Mnemonicos del Excel
        # Si entra en la condicion sabemos que es una instruccion
        
        mnemoni = Mnemonicos[nombre_mnemo]

        if "INH" in mnemoni:  # Es una intruccion en INH
            if len(parametros) > 1:  # ["mnemonico","OPERANDOS"]
                linea["compilado"] = "006   INSTRUCCIÓN NO LLEVA OPERANDO(S)"
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
                linea["compilado"] = "005   INSTRUCCIÓN CARECE DE OPERANDO(S)"
                return ContMemoria

        # Es una instruccion en otro tipo de direccionamiento (NO INH o REL)
        else:
            #direccionMem = codigo[1]
            # VerificarDirecciona(direccionMem)
            operando = parametros[1]

            if operando[0] == "#":  # Si inicia con '#' es IMM
                return IMM(linea,Variables,ContMemoria,mnemoni) #Devuelve el ContMemoria

            elif ",x" in operando:  # Es IND,X
                if operando[0] == "$":  # Si el operando lleva "$" ya esta en hexadecimal
                    return [nombre_mnemo, "IND,X", [hex(int(operando[1:-2]))]]

                elif operando[0] == "'":  # es un caracter ASCII
                    dec = ord(operando[1])
                    return [nombre_mnemo, "IND,X", [hex(int(dec))]]
                elif operando[1:-2].isnumeric():  # Esta en dec
                    # Obtiene el numero decimal para convertirlo a hexadecimal despues
                    dec = operando[1:-2]
                    return [nombre_mnemo, "IND,X", [hex(int(dec))]]
                else:
                    variable = operando[1:-2]
                    if variable in Variables:  # si esta registrada existe
                        return [nombre_mnemo, "IND,X", [Variables[variable]]]
                    else:  # Variable no existe
                        return ["Error", "002 VARIABLE INEXISTENTE", []]

            elif ",y" in operando:  # Es IND,Y
                if operando[0] == "$":  # Si el operando lleva "$" ya esta en hexadecimal
                    return [nombre_mnemo, "IND,Y", [hex(int(operando[1:]))]]

                elif operando[0] == "'":  # es un caracter ASCII
                    dec = ord(operando[1])
                    return [nombre_mnemo, "IND,Y", [hex(int(dec))]]
                elif operando[1:-2].isnumeric():  # Esta en dec
                    # Obtiene el numero decimal para convertirlo a hexadecimal despues
                    dec = operando[1:-2]
                    return [nombre_mnemo, "IND,Y", [hex(int(dec))]]
                else:
                    variable = operando[1:-2]
                    if variable in Variables:  # si esta registrada existe
                        return [nombre_mnemo, "IND,Y", [Variables[variable]]]
                    else:  # Variable no existe
                        return ["Error", "002 VARIABLE INEXISTENTE", []]

            else:  # Puede ser DIR o EXT
                if operando[0] == "$":  # Si el operando lleva "$" ya esta en hexadecimal
                    if len(operando[1:]) == 2:  # Si es de 8 bits es DIR
                        return [nombre_mnemo, "DIR", [operando[1:]]]
                    elif len(operando[1:]) == 4:  # Si es de 16 bits es EXT
                        return [nombre_mnemo, "EXT", [operando[1:]]]
                    else:
                        return ['Error', 'el mnemonico "{}" su operando no es ni de 8 o 16 bits.'.format(
                            nombre_mnemo), []]

                elif operando[0] == "'":  # es un caracter ASCII
                    dec = ord(operando[1])
                    hex_op = getHexString(int(dec))
                    if len(hex_op) >= 1 and len(hex_op) <= 2:  # es de 8 bits (DIR)
                        return [nombre_mnemo, "DIR", hex(int(dec))]
                    elif len(hex_op) >= 3 and len(hex_op) <= 4:  # es de 16 bits (EXT)
                        return [nombre_mnemo, "EXT", hex(int(dec))]
                    else:  # ERROR
                        return ['Error', 'el mnemonico "{}" su operando no es ni de 8 o 16 bits.'.format(
                            nombre_mnemo), []]

                elif operando.isnumeric():  # Si son numeros Esta en dec y puede ser DIR o EXT
                    # Obtiene el numero decimal para convertirlo a hexadecimal despues
                    hex_num = getHexString(int(operando))
                    if len(hex_num) == 2:  # Debe de ser de 8 bits para DIR
                        return [nombre_mnemo, "DIR", hex(int(operando))]
                    elif len(hex_num) == 4:  # Debe de ser de 16 bits para EXT
                        return [nombre_mnemo, "EXT", hex(int(operando))]
                    else:
                        return ['Error', 'el operando de "{}" no es de 8 o 16 bits.'.format(
                            nombre_mnemo), []]

                else:  # Es una variable:
                    if operando in Variables:  # si esta registrada existe
                        # Quita el 0x del valor hex de Python
                        temp_var = str(Variables[operando])[2:]
                        hex_num = getHexString(int(temp_var))
                        if len(hex_num) == 2:  # Debe de ser de 8 bits para DIR
                            return [nombre_mnemo, "DIR",  [Variables[operando]]]
                        elif len(hex_num) == 4:  # Debe de ser de 16 bits para EXT
                            return [nombre_mnemo, "EXT", [Variables[operando]]]

                    else:  # Variable no existe
                        linea["compilado"] = "Error", "002 VARIABLE INEXISTENTE"

    else:  # error mnemonico inexistente
        linea["compilado"] = "Error 004 MNEMÓNICO INEXISTENTE"

    # Esta funcion solo va a regresar el valor de cont memoria, ya que se pasa por valor y no por ref.
    return ContMemoria

