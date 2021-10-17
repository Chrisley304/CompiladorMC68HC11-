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
                        bit.pop'''

            
        

    
def TipodeInstruccion(codigoConComentarios,Mnemonicos): #Recibe una lista con cadenas correspondientes a una linea del codigo y devuelve que tipo de instruccion es
    # Puede haber: Variables, funciones/etiquetas (MAIN ETC) y parametros con MNEMONICOS
    codigo = EliminarComentarios(codigoConComentarios)
    parametros = len(codigo)
        
    inicial = codigo[0]
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
    # print(Mnemonicos['aba'])
    lineas = getPrograma("ProgramasEjemplo/prueba.txt")
    Variables = {}  # {'variable/constante' : direcciónDememoria}
    Etiquetas = {}  # {'Etiqueta' : True} || {'Etiqueta' : direcciónDeMemoria}
    for linea in lineas:
        
        if not isEmpty(linea):   # Que la línea no este vacía
            formatedLine = formater(linea)
    
            # Si comienza con espacio -> es directiva o instrucción
            if(formatedLine[0] == 1):
                pass

            # Si comienza con espacio -> es directiva o instrucción
            else:
                if(formatedLine[1] in Mnemonicos):  # or (formatedline[1] in DirectivasDeEnsamblador) <- falta agregar este caso
                    #temporal.write('Error instrucción carece de espacios')
                    pass
                else:
                    # Comprueba si es constante/variable o etiqueta
                    # Se añade al mapa de constantes/variable o etiquetas
                    # temporal.write('Lo que pasó')
                    pass
            
        # La línea está vacía o solo tiene comentario   
        else:
            #temporal.write('vacio')
            pass





# Main()


""" 
    Constantes deben estar siempre pegadas,
    directivas deben tener al menos uno.
    
    NOTAS:

    La salida del programa es de este tipo:
    1 A                 ********************************** 
    2 A                 *PROGRAMA DE EJEMPLO 
    3 A                 ********************************** 
    4 A      1026       PACTL     EQU       $1026                 
    5 A      1027       PACNT     EQU       $1027                 
    6 A      1030       ADCTL     EQU       $1030                 
    7 A      1031       ADR1      EQU       $1031                 
    8 A      1032       ADR2      EQU       $1032
    
    Donde: 
    [Numero de linea] [EL A no c que es jajaja] [OPCODE+DireccionMemoria] [Lo que estaba en el codigo de entrada]



"""
