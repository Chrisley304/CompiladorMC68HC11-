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
    # filename = "prueba.asm" # NOTA: debe de estar dentro de la carpeta "ProgramasEjemplo"
    filename = "Profe.ASC" # NOTA: debe de estar dentro de la carpeta "ProgramasEjemplo"
    lineas = getPrograma(filename)
    
    Variables = {}  # {'variable/constante' : direcciónDememoria}
    Etiquetas = {}  # {'etiqueta' : direcciónDememoria}
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
                    linea["compilado"] = "\t\t\t"
                    break

                elif linea["contenido"][0] == 'fcb':
                    linea["compilado"] = "\t\t\t"

                # Directiva ORG, comienza el contador de memoria
                elif linea["contenido"][0] == 'org':
                    Cont_memoria = ConvertHex(linea["contenido"][1][1:])
                    linea["compilado"] = "\t\t" + getHexString(Cont_memoria)
                    # Cont_memoria = hex(int('0x' + linea["contenido"][2][1:], 16))
                
                
                else: # se envia al precompilador
                    try:
                        Cont_memoria = Precompilado(linea, Mnemonicos, Variables,Etiquetas,Cont_memoria)
                    except Exception as e:
                        print("Linea con error (pre): {}".format(linea))
                        print(e)
                        return
            # No tiene espacio
            else:
                if (linea["contenido"][0] in Mnemonicos) or (linea["contenido"][0] == 'org' or linea["contenido"][0] == 'end' or linea["contenido"][0] == 'fcb'):
                    linea["compilado"] = "ERROR 009"
                else:
                    # Se trata de una etiqueta [0,etiqueta]
                    if(len(linea["contenido"]) == 1):
                        # Se pasa a compilar para almacenar en el dict. Variables el lugar
                        # Guardar como etiqueta
                        Etiquetas[linea["contenido"][0]] = Cont_memoria
                        linea["compilado"] = getHexString(Cont_memoria) + "\t"
                    
                    # Se declara una variable o constante
                    elif linea["contenido"][1] == "equ":
                        Variables[linea["contenido"][0]] = ConvertHex(linea["contenido"][2][1:])
                        linea["compilado"] = getHexString(Variables[linea["contenido"][0]]) + "\t"
                    
                    else: #Puede ser una etiqueta con mnemonico
                        
                        if linea["contenido"][1] in Mnemonicos:
                            Etiquetas[linea["contenido"][0]] = Cont_memoria
                            Cont_memoria = Precompilado(linea, Mnemonicos, Variables,Etiquetas,Cont_memoria)

                        # Directiva END, dejar de compilar 
                        elif linea["contenido"][1] == 'end':
                            flagDeEnd = True
                            Etiquetas[linea["contenido"][0]] = Cont_memoria
                            linea["compilado"] = getHexString(Cont_memoria) + "\t"
                            break

                        elif linea["contenido"][1] == 'fcb':
                            Etiquetas[linea["contenido"][0]] = Cont_memoria
                            linea["compilado"] = getHexString(Cont_memoria) + "\t"

                        # Directiva ORG, comienza el contador de memoria
                        elif linea["contenido"][1] == 'org':
                            Cont_memoria = ConvertHex(linea["contenido"][2][1:])
                            linea["compilado"] = "\t\t" + getHexString(Cont_memoria)
                            Etiquetas[linea["contenido"][0]] = Cont_memoria
                            # Cont_memoria = hex(int('0x' + linea["contenido"][2][1:], 16))

                        else:
                            linea["compilado"] = "ERROR 011"

        else:
            linea["compilado"] = "\t\t"


    # Post compilado: (2da vuelta)
    # NOTAS: Directiva FCB, no hace nada el compilador, END TERMINA DE COMPILAR, ORG Inicia cont. memoria (inicia el programa)
    for linea in lineas_formateadas:
        try:
            if linea["compilado"] == None and len(linea["contenido"]) !=0:
                PostCompilado(linea,Mnemonicos,Etiquetas,Variables)   
        except Exception as e:
            print("Linea con error (post): {}".format(linea))
            print(e)
            return

    if not flagDeEnd:
        # Error no hay END
        lineas_formateadas.append({"compilado":"ERROR 010"})
        lineas.append("")
    
    # Escritura del archivo .LST
    try:
        EscrituraLST(lineas_formateadas,lineas,filename)
        print("El archivo .LST se genero correctamente.")
    except:
        print("Error al generar el archivo .LST")
    
    try:
        EscrituraHTML(lineas_formateadas,lineas,filename)
        print("El archivo HTML se genero correctamente.")
    except:
        print("Error al generar el archivo HTML")

    try:
        EscrituraS19(lineas_formateadas,filename)
        print("El archivo S19 se genero correctamente.")
    except:
        print("Error al generar el archivo S19")


Main()


""" 
    TODO:
    
    Instrucciones especiales:
    Casos de 3: 
    - BRCLR (3 operandos)
    - BRSET (3 operandos)
        ej. 15,#12 Etiqueta
            [DIR,INDXoY de 8 bits][IMM] [Etiqueta] <- La etiqueta se calcula como relativa
            15,x,#12 Etiqueta
            15,y,#12 Etiqueta
    
    Casos de 2:
    - BCLR (2 operandos)
    - BSET (2 operandos)
        ej. 15,#12 
            15,x,#12 
            15,y,#12


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
    
    Errores nuestros:
    011 SINTAXIS INCORRECTA
    012 INSTRUCCIÓN CON EXCESO DE OPERANDO(S)

"""
