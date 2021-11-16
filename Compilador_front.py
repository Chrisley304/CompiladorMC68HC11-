import json 
from os import error, remove, waitpid
from ArchivosCompilador.Compilador_back import *

def getJSON():
    mnemonicos = None
    with open('ArchivosCompilador/mnemonicos.json') as json_file:
        mnemonicos = json.load(json_file)
    
    return mnemonicos

def getPrograma(fileName):
    lines = None
    with open("ProgramasEjemplo/"+fileName, 'r') as input:
        lines = input.readlines()
    return lines

def Main():
    
    Mnemonicos = getJSON()
    # filename = "prueba.txt" # NOTA: debe de estar dentro de la carpeta "ProgramasEjemplo"
    filename = "prueba.txt" # NOTA: debe de estar dentro de la carpeta "ProgramasEjemplo"
    lineas = getPrograma(filename)
    
    Variables = {}  # {'variable/constante' : direcciónDememoria}
    flagDeEnd = False
    
    compilado_final = ""
    
    # Formateo de lineas
    lineas_formateadas = []
    
    for i in lineas:
        lineas_formateadas.append(formater(i))
    
    # Precompilado
    Cont_memoria = hex(0)

    for linea in lineas_formateadas:

        if len(linea["contenido"]) != 0:   # Que la línea no este vacía 

            # Si comienza con espacio -> es directiva (ORG, END, FCB) o instrucción
            if(linea["espacio"]):
                
                # Directiva END, dejar de compilar 
                if linea["contenido"][0] == 'end':
                    flagDeEnd = True
                    linea["compilado"] = ""
                    break

                if linea["contenido"][0] == 'fcb':
                    linea["compilado"] = ""

                # Directiva ORG, comienza el contador de memoria
                if linea["contenido"][0] == 'org':
                    Cont_memoria = ConvertHex(linea["contenido"][1][1:])
                    linea["compilado"] = "\t " + getHexString(Cont_memoria)
                    # Cont_memoria = hex(int('0x' + linea["contenido"][2][1:], 16))
                
                else: # se envia al precompilador
                    Cont_memoria = Precompilado(linea, Mnemonicos, Variables, Cont_memoria)

            # No tiene espacio
            else:
                if (linea["contenido"][0] in Mnemonicos) or (linea["contenido"][0] == 'org' or linea["contenido"][0] == 'end' or linea["contenido"][0] == 'fcb'):
                    linea["compilado"] = "ERROR 009 INSTRUCCIÓN CARECE DE ALMENOS UN ESPACIO RELATIVO AL MARGEN"
                else:
                    # Se trata de una etiqueta [0,etiqueta]
                    if(len(linea["contenido"]) == 1):
                        # Se pasa a compilar para almacenar en el dict. Variables el lugar
                        # Guardar como etiqueta
                        Variables[linea["contenido"][0]] = Cont_memoria
                        linea["compilado"] = getHexString(Cont_memoria)
                    
                    # Se declara una variable o constante
                    elif linea["contenido"][1] == "equ":
                        Variables[linea["contenido"][0]] = ConvertHex(linea["contenido"][2][1:])
                        linea["compilado"] = getHexString(Variables[linea["contenido"][0]])
                    
                    else: #Error algo escribio mal el usuario
                        linea["compilado"] = "ERROR 010 SINTAXIS INCORRECTA"

        else:
            linea["compilado"] = ""


    # Post compilado: (2da vuelta)
    # NOTAS: Directiva FCB, no hace nada el compilador, END TERMINA DE COMPILAR, ORG Inicia cont. memoria (inicia el programa)
    for linea in lineas_formateadas:
        if linea["compilado"] == None:
            PostCompilado(linea,Mnemonicos,Variables)    

    if not flagDeEnd:
        # Error no hay END
        lineas_formateadas.append({"compilado":"ERROR 010 NO SE ENCUENTRA END"})
        lineas.append(" ")
    
    Escritura(lineas_formateadas,lineas,filename)


Main()


""" 
    Errores:
	- Separar Etiquetas de Variables/Constante
    - Error salto muy grande
    - Poner mensaje de Compilado correcto
    - Poner descripcion de errores abajo
    - Arreglar mapa JSON ( Bytes )
    - Arreglar comparaciones de BYTES (Error 007)
    - Caso 4 instrucciones Especiales (Clase 23 sep)
    - Punto extra: Colores listado HTML

    Errores a buscar:
    001   CONSTANTE INEXISTENTE
    002   VARIABLE INEXISTENTE
    003   ETIQUETA INEXISTENTE
    004   MNEMÓNICO INEXISTENTE
    005   INSTRUCCIÓN CARECE DE  OPERANDO(S)
    006   INSTRUCCIÓN NO LLEVA OPERANDO(S)
    007   MAGNITUD DE  OPERANDO ERRONEA
    008   SALTO RELATIVO MUY LEJANO
    009   INSTRUCCIÓN CARECE DE ALMENOS UN ESPACIO RELATIVO AL MARGEN
    010   NO SE ENCUENTRA END

"""
