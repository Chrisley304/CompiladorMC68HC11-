import json 
from os import error, waitpid

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

def EliminarComentarios(codigo:list):
    for i in len(codigo):
        if "*" in i:


def TipodeInstruccion(codigo,Mnemonicos): #Recibe una lista con cadenas correspondientes a una linea del codigo y devuelve que tipo de instruccion es
    # Puede haber: Variables, funciones (MAIN ETC) y parametros con MNEMONICOS
    contenido = True
    lineas = len(codigo)
    while contenido:
        inicial = codigo[0]
        if Mnemonicos[inicial.lower()]: # Busca si esta en la lista de Mnemonicos del Excel
            # Si entra en la condicion sabemos que es una instruccion
            # Una instruccion correctamente escrita tiene la siguiente forma: 
            #       LDS   #$00FF *COMENTARIO
            #       [mnemonico]  [Direccion/Valor] [Comentario OPCIONAL]
            # Por tanto se buscara a estos atributos para ver si son correctos
            
            


        else:



def Main():
    Mnemonicos = getJSON()
    # print(Mnemonicos['aba'])
    lineas = getPrograma("ProgramasEjemplo/prueba.txt")
    Variables = {}
    Funciones = {}
    for inf in lineas:
        if len(inf.strip()) != 0:   # Que la línea no este vacía
            # print(inf)
            intr = inf.split()  #Tokeniza a la linea por espacios
            TipodeInstruccion(intr)




Main()


""" 
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
