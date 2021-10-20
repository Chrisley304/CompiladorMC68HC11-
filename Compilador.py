import json 
from os import error, remove, waitpid

def getJSON():
    mnemonicos = None
    with open('mnemonicos.txt') as json_file:
        mnemonicos = json.load(json_file)
    
    return mnemonicos

def getPrograma(fileName):
    lines = None
    with open(fileName, 'r') as input:
        lines = input.readlines()
    return lines

def EliminarComentarios(codigo:list): # Regresara una lista sin los comentarios 
    lista_sincomments = codigo.copy()
    for i in range(len(codigo)):
        if "*" in lista_sincomments[i]: # SI tiene comentarios
            print("hola {}".format(i))
            for j in range(len(codigo)-1,i-1,-1):
                del lista_sincomments[j]
            return lista_sincomments

    return lista_sincomments

'''def datosLinea(linea,mnemonicos):
    CNA=[$,#]
    token=linea.split()
    if token[0] in mnemonicos:
        for instruction in token[1:len(token)-1]):
            characters=list(instruction)
            bit=characters-CNA
            size=len(bit)/2
            bytes=[]
            rl=[]
                for i in size:
                    for y in bit:
                        rl.append(bit[0]+bit[1])
                        bit.pop(0)
                        bit.pop(1) '''

def getHex(number):
    hex_dec = hex(number)
    return str(hex_dec.replace('0x', ''))


#Entrada es la salida de formater:
#       ldca       $1243  * comentario'->formater-> [1,'ldca','$1243']
#       ADR2   EQU   $1032'->formater-> [0,'adr2','equ','$1032']
# Devuelve lista tipo -> ['mnemónico', 'modo de direccionamiento', [Operandos]] (en operandos van las direcciones en hexadecimal (cambiar de decimal a hexadecimal o escribir la dirección  
#                                                                                de constantes o variables en hexadecimal) o el nombre de la etiqueta)
# Errores: mnemónico no existe | Constante / variable no existe
# Salida error -> ['Error', 'mensajeDeError',[]]
def Identificador(linea,Mnemonicos): #Recibe una lista con cadenas correspondientes a una linea del codigo y devuelve que tipo de instruccion es
    # Puede haber: Variables, funciones/etiquetas (MAIN ETC) y parametros con MNEMONICOS
    
    if linea[0] == 1: # Si hay espacio debe ser una instruccion
    
        parametros = linea[1:] # lista[desdeDondeInclusive:HastaDondeExclusiv] es == lista.copy de intervalo
                            # Se obtiene la lista del indice 1-.. debido a que se omite el primer indice que ya no nos es util aquí
        nombre_mnemo = parametros[0].lower() # Se obtiene el nombre del mnemonico en minuscula ya que en el map asi se encuentran.
        
        if Mnemonicos[nombre_mnemo]:  # Busca si esta en la lista de Mnemonicos del Excel
            # Si entra en la condicion sabemos que es una instruccion
            # Una instruccion correctamente escrita tiene la siguiente forma: 
            #       LDS   #$00FF
            #       [mnemonico]  [Direccion/Valor * Excepcion INH]
            # Por tanto se buscara a estos atributos para ver si son correctos
            mnemoni = Mnemonicos[nombre_mnemo]
            if parametros == 1 and mnemoni['INH']: # Es una intruccion en INH
                salida = [nombre_mnemo, 'INH', ]
                return salida
            
            elif len(parametros) >1: # Es una instruccion en otro tipo de direccionamiento
                #direccionMem = codigo[1]
                # VerificarDirecciona(direccionMem)
                operando = parametros[1]
                
                if operando[0] == "#":  # Si inicia con '#' es IMM 
                    if mnemoni['IMM']:  # se verifica que el mnemonico sea IMM
                        if operando[1] == "$": #Si el operando lleva "$" ya esta en hexadecimal
                            return [nombre_mnemo,"IMM",operando[1:]]
                        elif operando[1] == "'": # es un caracter ASCII
                            dec = ord(operando[2])
                            return [nombre_mnemo,"IMM",getHex(int(dec))]
                        else: #Esta en dec
                            dec = operando[1:] #Obtiene el numero decimal para convertirlo a hexadecimal despues
                            if len(dec) == 2 or len(dec) == 4: #Debe de ser de 8 ó 16 bits
                                return [nombre_mnemo, "IMM", getHex(int(dec))]
                            else:
                                return ['Error', 'el operando de "{}" no es de 8 ó 16 bits.'.format(
                                    nombre_mnemo), []]
                    else:
                        return ['Error', 'el mnemonico "{}" no es de IMM y su operando comienza con "#".'.format(
                            nombre_mnemo), []]

                elif ",X" in operando or ",x" in operando:  # Es IND,X
                    if operando[0] == "$":  # Si el operando lleva "$" ya esta en hexadecimal
                        if len(operando[1:]) == 2:
                            return [nombre_mnemo, "IND,X", operando[1:]]
                        else:
                            return ['Error', 'el mnemonico "{}" es IND,X pero su operando no es de 8 bits.'.format(
                                nombre_mnemo), []]
                    elif operando[0] == "'": # es un caracter ASCII
                        dec = ord(operando[1])
                        return [nombre_mnemo,"IND,X",getHex(dec)]
                    else: #Esta en dec
                        dec = operando[1:] #Obtiene el numero decimal para convertirlo a hexadecimal despues
                        if len(dec) == 2: #Debe de ser de 8 bits
                            return [nombre_mnemo, "IND,X", getHex(int(dec))]
                        else:
                            return ['Error', 'el operando de "{}" no es de 8 bits.'.format(
                                nombre_mnemo), []]
                
                elif ",Y" in operando or ",y" in operando:  # Es IND,X
                    if operando[0] == "$":  # Si el operando lleva "$" ya esta en hexadecimal
                        if len(operando[1:]) == 2:
                            return [nombre_mnemo, "IND,Y", operando[1:]]
                        else:
                            return ['Error', 'el mnemonico "{}" es IND,Y pero su operando no es de 8 bits.'.format(
                                nombre_mnemo), []]
                    elif operando[0] == "'":  # es un caracter ASCII
                        dec = ord(operando[1])
                        return [nombre_mnemo, "IND,Y", getHex(int(dec))]
                    else:  # Esta en dec
                        # Obtiene el numero decimal para convertirlo a hexadecimal despues
                        dec = operando[1:]
                        if len(dec) == 2:  # Debe de ser de 8 bits
                            return [nombre_mnemo, "IND,Y", getHex(int(dec))]
                        else:
                            return ['Error', 'el operando de "{}" no es de 8 bits.'.format(
                                nombre_mnemo), []]

                else: # Puede ser DIR o EXT o REL
                    if operando[0] == "$":  # Si el operando lleva "$" ya esta en hexadecimal
                        if len(operando[1:]) == 2:  # Si es de 8 bits es DIR
                            return [nombre_mnemo, "DIR", operando[1:]]
                        elif len(operando[1:]) == 4:  # Si es de 16 bits es EXT
                            return [nombre_mnemo, "EXT", operando[1:]]
                        else:
                            return ['Error', 'el mnemonico "{}" su operando no es ni de 8 o 16 bits.'.format(
                                nombre_mnemo), []]
                    elif operando[0] == "'":  # es un caracter ASCII
                        dec = ord(operando[1])
                        hex_op = getHex(dec)
                        if len(hex_op) >= 1 and len(hex_op) <= 2: # es de 8 bits (DIR)
                            return [nombre_mnemo, "DIR", hex_op]
                        elif len(hex_op) >= 3 and len(hex_op) <= 4: # es de 16 bits (EXT)
                            return [nombre_mnemo, "EXT", hex_op]
                        else: #ERROR
                            return ['Error', 'el mnemonico "{}" su operando no es ni de 8 o 16 bits.'.format(
                                nombre_mnemo), []]

                    elif operando.isnumeric():  # Si son numeros Esta en dec y puede ser DIR o EXT
                        # Obtiene el numero decimal para convertirlo a hexadecimal despues
                        hex_num = getHex(int(operando))
                        if len(hex_num) == 2:  # Debe de ser de 8 bits para DIR
                            return [nombre_mnemo, "IND,Y", hex_num]
                        elif len(hex_num) == 4:  # Debe de ser de 16 bits para EXT
                            return [nombre_mnemo, "IND,Y", hex_num]
                        
                        else:
                            return ['Error', 'el operando de "{}" no es de 8 o 16 bits.'.format(
                                nombre_mnemo), []]
                    
                    else: #Si incluye letras significa que es una etiqueta y es REL
                        # Aquí es lo que no supe que onda xd
                        return [nombre_mnemo, "REL", operando]



            
            else:
                return ['Error', 'el mnemonico "{}" no es INH y carece de operandos.'.format(
                    nombre_mnemo), []]

        else: #error mnemonico inexistente
            ['Error', 'el mnemonico "{}" no existe.'.format(nombre_mnemo), []]

    else: # Si no hay espacio es una variable o una etiqueta
        parametros = linea[1:]
        parametros[0]
        



#  Error: mnemónico no lleva operandos | mnemónico faltan operandos | magnitud errónea de operandos
#  Devuelve lista tipo -> ['mnemónico', 'modo de direccionamiento', [Operandos]] (La misma de identificador si no hay errores)
#  De otra manera devuelve ['Error', 'mensajeDeError', []]
def verificador(linea,Mnemonicos):
    # No lleva operandos
    if linea[1] == 'INH':
        if len(linea[2]) > 0:
            return ['Error', '006 INSTRUCCIÓN NO LLEVA OPERANDO(S)', []]

    else:
        # Todas los demas modos llevan 1 operando
        if len(linea[2]) == 0:
            return ['Error', '005 CARECE DE OPERANDO(S)', []]

        # Puede tener operando de 1 o 2 bytes, se analiza cada caso
        if linea[1] == 'IMM':

            bytesDeOPCODE = 1 if len(Mnemonicos[linea[0]][linea[1]][0] <= 2) else 2

            # Operando de 1 byte
            if len(linea[2][0]) - 2 == 2 and Mnemonicos[linea[0]][linea[1]][1] != bytesDeOPCODE + 1:
                return ['Error', '007 MAGNITUD DE OPERANDO ERRONEA', []]

            # Operando de 2 bytes
            else:
                if Mnemonicos[linea[0]][linea[1]][1] != bytesDeOPCODE + 2:
                    return ['Error', '007 MAGNITUD DE OPERANDO ERRONEA', []]
            
        # Los modos DIR e IND llevan operando de 1 byte
        if len(linea[2][0]) - 2 >= 2:
            if linea[1] == 'DIR' or linea[1] == 'IND,X' or linea[1] == 'IND,Y':
                return ['Error', '007 MAGNITUD DE OPERANDO ERRONEA', []]

        # El modo EXT Lleva operando de 2 bytes
        else:
            if linea[1] == 'EXT':
                return ['Error', '007 MAGNITUD DE OPERANDO ERRONEA', []]

            # Modo REL
            else:
                if len(linea[2]) > 1:
                    return ['Error', '007 MAGNITUD DE OPERANDO ERRONEA', []]

    return linea




#  Procesa la instrucción y la retorna compilada (string que se escribirá en temp.txt)
def procesador(linea, org):
    pass        


#Funcionamiento de isEmpty
#Si encuentra una palabra no antecedida por * la línea se debe trabajar
def isEmpty(line):
    for word in line.split():
        if(word.startswith('*')):
            break
        return False
    return True


#Funcionamiento de formater
# 0 -> No hay espacio inicial
# 1 -> Hay espacio inicial
# pone en minúsculas las palabras
#'          ldca       $1243  * comentario'->formater-> [1,'ldca','$1243']
#'ADR2   EQU   $1032'->formater-> [0,'adr2','equ','$1032']
def formater(line):
    formatedLine = []
    if(line[0] == ' ' or line[0] == '\t'):
        formatedLine.append(1)
    else:
        formatedLine.append(0)

    for word in line.split():
        if(word.startswith('*')):
            break
        formatedLine.append(word.lower())
    return formatedLine


def Main():
    
    Mnemonicos = getJSON()
    lineas = getPrograma("ProgramasEjemplo/prueba.txt")
    
    Variables = {}  # {'variable/constante' : direcciónDememoria}
    Etiquetas = set()  # {'Etiqueta' : True}
    
    org = hex(0)
    flagDeEnd = True
    
    writer = open("temp.txt","w")
    
    for linea in lineas:
        
        if not isEmpty(linea):   # Que la línea no este vacía
            formatedLine = formater(linea)
    
            # Si comienza con espacio -> es directiva (ORG, END, FCB) o instrucción (EQU no, porque es la declaración de constantes/varibales y no lleva espacio)
            if(formatedLine[0] == 1):
                
                # Directiva END, dejar de compilar
                if formatedLine[1] == 'end':
                    writer.write("Vacío")
                    flagDeEnd = False
                    break
                
                # Directiva FCB, no hace nada el compilador
                elif formatedLine[1] == 'fcb':
                    writer.write("Vacío")
                    break
                
                # Directiva ORG, inicializar contador de dirección de memoria
                elif formatedLine[1] == 'org':
                    writer.write("Vacío")
                    
                    # Es una constante/variable definida?
                    if formatedLine[2] in Variables:
                        org = hex(int(Variables[formatedLine[2]],16))
                        
                    # El valor se encuentra en hexadecimal?
                    elif formatedLine[2][0] == '$':
                        org = hex(int(formatedLine[2][1:],16))
                    
                    # El valor es decimal, se transforma a hexadecimal
                    else:
                        org = hex(int(formatedLine[2],10))
                
                # Es un mnemónico
                else:
                    # Identifica el modo de direccionamiento y enlista operandos en hexadecimal o etiquetas
                    formatedLine = Identificador(formatedLine, Mnemonicos)
                    
                    # Si el mnemónico o constante/variable no existe
                    if(formatedLine[0] == 'Error'):
                        writer.write(formatedLine[1])
                        
                    else:
                        # Se verifica errores de magnitud/cantidad de operandos
                        formatedLine = verificador(formatedLine, Mnemonicos)
                        
                        # magnitud errónea, faltan operandos, no lleva operandos
                        if(formatedLine[0] == 'Error'):
                            writer.write(formatedLine[1])
                        
                        # La información es correcta, se procesa la instrucción
                        else:
                            writer.write(procesador(formatedLine, org))

            # No tiene espacio
            else:
                if (formatedLine[1].lower() in Mnemonicos) or (formatedLine[1] == 'org' or formatedLine[1] == 'end' or formatedLine[1] == 'fcb'):
                    writer.write('009 INSTRUCCIÓN CARECE DE ALMENOS UN ESPACIO RELATIVO AL MARGEN')
                else:
                    # Se trata de una etiqueta [0,etiqueta]
                    if(len(formatedLine) == 2):
                        Etiquetas.add(formatedLine[1])
                    # Se declara una variable o constante
                    else:
                        Variables[formatedLine[1]] = hex(int(formatedLine[-1][1:], 16))
            
        # La línea está vacía o solo tiene comentarios  
        else:
            writer.write("Vacío")
    
            
    if(flagDeEnd):
        writer.write("010 NO SE ENCUENTRA END")
        
    writer.close()


    # Proceso de cálculo de saltos y elaboración de archivos finales ...



# Main()


""" 
    Organización:
    ✓   - Leer línea 
    ✓   - FormatoQuitaEspaciosYComentarios -> Finalizado
        - Identificador -> FALTA (hay lógica para identificar espacio (inicial) y si es mnemónico sin espacio)
        - Verificador -> FALTA
        - Procesador -> FALTA
        - Escritor -> FALTA
    
    NOTAS:
    Constantes deben estar siempre pegadas,
    directivas deben tener al menos uno.
    
"""


# ==== PRUEBAS =====

""" def Prueba(diccionario:dict, lista:list):
    diccionario['nuevo'] = "Hola"
    lista.append("Que pedo")


dicc1 = {"prueba":5}
lista1 =[1,2]

Prueba(dicc1,lista1)
Prueba(dicc1,lista1)

print(dicc1)
print(lista1)
"""
# operando = "65"
# dec = operando
# print(dec)
# hex_dec = hex(int(dec))
# print(getHex(1531))
# print(hex_dec)
# print(hex_dec.replace('x', ''))

print("45785748574".isnumeric())
