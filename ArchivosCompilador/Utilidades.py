# Devuelve una string sin el 0x de Python y añadiendo 0's para que tenga el formato del profesor.
def getHexStringInt(number: int):
    hex_dec = str(hex(number))
    hex_str = hex_dec.replace('0x', '')
    if len(hex_str) == 3 or len(hex_str) == 1:
        hex_str = '0' + hex_str
    return hex_str.upper()

# Sobrecarga de la funcion para admitir de igual forma tipo de variable hex puro de Python

# Devuelve una string sin el 0x de Python y añadiendo 0's para que tenga el formato del profesor.

def getHexString(number: hex):
    hex_str = str(number).replace('0x', '')
    if len(hex_str) == 3 or len(hex_str) == 1:
        hex_str = '0' + hex_str
    return hex_str.upper()

#Suma 2 hex

def SumHex(A: hex, B: int):
    sum_hex = int(A, 16)
    sum_hex = sum_hex + B
    return hex(sum_hex)

#Verifica si un salto es válido

def CheckHex(etiqueta: hex, origen: hex, flag: bool):
    # Salto hacia atras, si es menor a 127 regresa falso
    if(flag):
        res_int = int(etiqueta, 16)
        origen_int = int(origen, 16)    
        return True if (res_int - (origen_int + 1)) > -128 else False
    
    # Salto hacia adelante, si es mayor a 128 regresa falso
    else:
        res_int = int(etiqueta, 16)
        origen_int = int(origen, 16)    
        return True if (res_int - origen_int) < 129 else False


def CheckSalto(etiqueta: hex, origen: hex):
    # Salto hacia atras, si es menor a 127 regresa falso

    True if int(origen,16) > int(etiqueta,16) else False

#Resta 2 hex


def ResHex(etiqueta: hex, origen: hex):
    res_hex = int(etiqueta, 16)
    origen_int = int(origen, 16)
    res_hex = res_hex - origen_int
    # Convierte el numero negativo a hexadecimal de 8 bits
    return hex(res_hex & (2**8-1) )

#Devuelve el hex en str ingresado en hex()


def ConvertHex(hexa: str):
    return hex(int('0x' + hexa, 16))

#Pone en minúsculas las palabras
# Regresa una linea con la siguiente estructura:
# linea = {espacio: True/False, contenido: [...], compilado = None/[cadena compilada] , }
def formater(line):
    formatedLine = {}
    if (line[0] == ' ' or line[0] == '\t'):  # Si tiene espacio coloca True
        formatedLine["espacio"] = True
    else:
        formatedLine["espacio"] = False

    formatedLine["contenido"] = []

    for word in line.split():
        if(word.startswith('*')):  # Es un comentario
            break
        formatedLine["contenido"].append(word.lower())

    formatedLine["compilado"] = None
    formatedLine["localidad"] = None
    formatedLine["OPCODE"] = ""
    formatedLine["operando"] = ""
    return formatedLine


def Convert_to_HTML(cont,direccion,OPCODE,operando,original):
    salida = "<p>{}: {} (<span style=\"color: red;\">{}</span><span style=\"color: blue;\">{}</span>):{}</p>".format(cont,direccion,OPCODE,operando,original)
    return salida


def Divide_str(l):

    for i in range(0, len(l), 2): 
        yield l[i:i + 2]