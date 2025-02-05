import math
import re

def decimal_a_binario(decimal):
    """Convierte un número decimal a su representación binaria de 1 byte."""
    binario = format(decimal, '08b')  # Formatea a 8 bits (1 byte)
    return binario

def binario_a_hexadecimal(binario):
    """Convierte un número binario a su representación hexadecimal."""
    decimal = int(binario, 2)  # Convierte binario a decimal
    hexadecimal = format(decimal, '02X')  # Formatea a 2 dígitos hexadecimales (1 bytes)
    return hexadecimal

def hexadecimal_a_decimal(hexadecimal):
    """Convierte un número hexadecimal a su representación decimal."""
    decimal = int(hexadecimal, 16)  # Convierte hexadecimal a decimal
    return decimal

def decimal_a_hexadecimal(decimal):
    """Convierte un número decimal a su representación hexadecimal con ancho fijo de 4 caracteres."""
    if decimal < 0:
        raise ValueError("El número debe ser no negativo.")
    hexadecimal = hex(decimal)[2:].upper()  # Convertir a hexadecimal y quitar el prefijo '0x'
    return hexadecimal.zfill(4)  # Asegurar que el resultado tenga 4 caracteres, rellenando con ceros a la izquierda

def convertir_tamano(decimal):
    """Convierte un número decimal a su representación hexadecimal con ancho fijo de 4 caracteres."""
    if decimal < 0:
        raise ValueError("El número debe ser no negativo.")
    hexadecimal = hex(decimal)[2:].upper()  # Convertir a hexadecimal y quitar el prefijo '0x'
    return hexadecimal.zfill(2)

def compl(x):
	x=str(x)
	z=x[::-1]
	sum=0
	y=0
	for i in z:
		y+= 1
		if i=="0":
			sum+= 2**(y-1)
	sum= -(sum+1)
	return sum

def cz(hexa):
	j=0
	sumah=hex(int("0",16))
	while j<len(hexa)-1:
		bit=hexa[j]+hexa[j+1]
		sumah=hex(int(bit,16)+int(sumah,16))
		j=j+2
	n=int(sumah,16)
	bStr=""
	while n>0:
		bStr=str(n%2)+bStr
		n=n>>1
	res=bStr
	y=compl(res)
	fin=hex(y)
	return (fin[-2:].upper())

def buscar_d(input_string):
    # Expresión regular para encontrar la forma (XX + d)
    pattern = r'\((.*?) \+ (\d+)\)'

    # Variable para guardar el último valor extraído
    valor_d = None

    # Función lambda para reemplazar el patrón encontrado y guardar el valor de d
    def process_match(match):
        nonlocal valor_d
        # Extraer el valor de d
        d_value = match.group(2)
        # Guardar el valor de d en la variable
        valor_d = int(d_value)
        # Retornar el reemplazo de d por 'd'
        return f'({match.group(1)} + d)'

    # Usar re.sub con la función process_match
    result = re.sub(pattern, process_match, input_string)

    # Retornar la cadena procesada y el último valor extraído
    return result, valor_d


