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


# Error: Constante / varibale no existe
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
            direccionMem = codigo[1]
            # VerificarDirecciona(direccionMem)
        
        


    # else:

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
#'          ldca       $1243  * comentario'->formater-> [1,'ldca','$1243']
#'ADR2   EQU   $1032'->formater-> [0,'ADR2','EQU','$1032']
def formater(line):
    formatedLine = []
    if(line[0] == ' ' or line[0] == '\t'):
        formatedLine.append(1)
    else:
        formatedLine.append(0)

    for word in line.split():
        if(word.startswith('*')):
            break
        formatedLine.append(word)
    return formatedLine


def Main():
    Mnemonicos = getJSON()
    lineas = getPrograma("ProgramasEjemplo/prueba.txt")
    Variables = {}  # {'variable/constante' : direcciónDememoria}
    Etiquetas = {}  # {'Etiqueta' : True} || {'Etiqueta' : direcciónDeMemoria}
    flagDeEnd = True
    for linea in lineas:
        
        if not isEmpty(linea):   # Que la línea no este vacía
            formatedLine = formater(linea)
    
            # Si comienza con espacio -> es directiva (ORG, END, FCB) o instrucción (EQU no, porque es la declaración de constantes/varibales y no lleva espacio)
            if(formatedLine[0] == 1):
                
                pass

            # No tiene espacio
            else:
                if(formatedLine[1] in Mnemonicos):  # or (formatedline[1] in DirectivasDeEnsamblador) <- falta agregar este caso
                    #temporal.write('Error instrucción carece de espacios')
                    pass
                else:
                    # Comprueba si es constante/variable o etiqueta
                    # Se añade al mapa de constantes/variable o etiquetas
                    # temporal.write('vacio')
                    pass
            
        # La línea está vacía o solo tiene comentario   
        else:
            #temporal.write('vacio')
            pass
            
    if(flagDeEnd):
        pass
        #temporal.write('Error, se llegó al final sin encontrar end')




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