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



# Error: mnemónico no existe | Constante / varibale no existe
# Devuelve lista tipo -> ['mnemónico', 'modo de direccionamiento', [Operandos]] (en operandos van las direcciones en hexadecimal (cambiar de decimal a hexadecimal o escribir la dirección  
#                                                                                de constantes o variables en hexadecimal) o el nombre de la etiqueta)
# Si es error de constante inexistente -> ['Error', 'mensajeDeError',[]]
def Identificador(linea,Mnemonicos): #Recibe una lista con cadenas correspondientes a una linea del codigo y devuelve que tipo de instruccion es
    # Puede haber: Variables, funciones/etiquetas (MAIN ETC) y parametros con MNEMONICOS
    
    parametros = linea[1:] # lista[desdeDondeInclusive:HastaDondeExclusiv] es == lista.copy de intervalo
    
    inicial = linea[1] # es 1, debido a que en 0 se encuentra el indicador si lleva espacio o no.
    
    if Mnemonicos[inicial.lower()]: # Busca si esta en la lista de Mnemonicos del Excel
        # Si entra en la condicion sabemos que es una instruccion
        # Una instruccion correctamente escrita tiene la siguiente forma: 
        #       LDS   #$00FF *COMENTARIO
        #       [mnemonico]  [Direccion/Valor * Excepcion INH] [Comentario OPCIONAL]
        # Por tanto se buscara a estos atributos para ver si son correctos
        mnemoni = Mnemonicos[inicial.lower()]
        if parametros == 1 and mnemoni['INH']: # Es una intruccion en INH
            print("Es INH")
        
        if parametros >1: # Es una instruccion en otro tipo de direccionamiento
            #direccionMem = codigo[1]
            # VerificarDirecciona(direccionMem)
            pass
        


    # else:
    
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