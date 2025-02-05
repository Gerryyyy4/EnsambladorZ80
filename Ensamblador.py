from tkinter import Tk, filedialog
import diccionario
import convertir
import re
import os

CL = 0
CO = ""
COHEX = ""
CLHEX = 0
tSimbolos = {}
tamano_programa = 0


patronh = r'\((\w+)H\)'

patron = r'(^\w+\s+)(\w+)(,\s+)(\d{2,4})$'

patronjp = r'\b(JP\s+)(\w+)\b'

patrond = re.compile(r'(\w+)\s+(\w+),\s*\((\w+)\s*\+\s*(\d+)\)')

patronjpcc = r'\bJP\s+(\w+),\s+(\w+)\b'

patronhh = r'(\b\w+\s+\w+,\s+)([0-9A-Fa-f]+)H\b'

# Crear una instancia de Tkinter y ocultar la ventana principal
root = Tk()
root.withdraw()

# Abrir el cuadro de diálogo para seleccionar un archivo
archivo_path = filedialog.askopenfilename(filetypes=[("Archivos ASM", "*.asm")])

# Obtener el nombre del archivo de la ruta completa
nombre_archivo_completo = os.path.basename(archivo_path)
    
# Separar el nombre del archivo de su extensión
nombre_archivo, _ = os.path.splitext(nombre_archivo_completo)

nombre_archivo_hex = f"{nombre_archivo}.hex"
nombre_archivo_lst = f"{nombre_archivo}.lst"

# Cerrar la instancia de Tkinter
root.destroy()

def primera_pasada():
    global CL

    with open(archivo_path, "r") as archivo:
        
        # Itera sobre cada línea del archivo
        for linea in archivo:
            #Quitando los comentarios del codigo
            lineasc = linea.split(';')[0].strip()
            # Divide la línea en palabras
            nem = lineasc.split()
            if len(nem) != 0: 
                #Si encuentra la directiva ORG inicia el CL en la direccion dada
                if "ORG" in nem:
                    #Extrae la direccion de la linea de codigo
                    direccion_hexadecimal = nem[1]
                    CL = int(direccion_hexadecimal[:-1], 16)  # Elimina el último carácter 'H' y convierte de hexadecimal a decimal
                    continue
                #Si encuentra END termina el bucle
                if "END" in lineasc:
                    break    

                #Para cualquier instruccion JP
                if "JP" in nem:
                    direccionsalto = nem[len(nem)-1]
                    inst = lineasc.replace(direccionsalto, "NN")
                    CL = CL + diccionario.t_nemonicos[inst][0]
                    print("Para cualquier instruccion JP")
                    print(lineasc)
                    continue

                #Para cualquier instruccion JR
                if "JR" in nem:
                    etiqueta = nem[len(nem)-1]
                    inst = lineasc.replace(etiqueta, "DIS")
                    CL = CL + diccionario.t_nemonicos[inst][0]
                    print("Para cualquier instruccion JR")
                    print(lineasc)
                    continue

                else:
                    n = nem[0]
                    #Si encuentra un ':' significa que encontro una etiqueta
                    if ':' in n:
                        #Si la etiqueta no se encuentra en la tabla de simbolos la guarda junto con su valor
                        if n[:-1] not in tSimbolos:
                            #Elimina los ':' para guardar la etiqueta sin ellos
                            inst = n[:-1]
                            #Guarda la etiqueta en la tabla de simbolos y el valor del CL en hexadecimal
                            tSimbolos[inst] = convertir.decimal_a_hexadecimal(CL)
                            continue
                        else:
                            print(n," Ya se encuentra definida")
                            break 
                        

                    #Para cualquier instruccion sin variables   
                    if lineasc in diccionario.t_nemonicos:
                        print("Para cualquier instruccion con registros")
                        print(lineasc)
                        CL = CL + diccionario.t_nemonicos[lineasc][0]
                        continue

                    #Para [Instruccion] dato8bits
                    elif len(nem) == 2 and nem[1] not in diccionario.registros and nem[0] not in ["CPU", "HOF", "ORG"]:
                        inst = lineasc.replace(nem[1], "N")
                        CL = CL + diccionario.t_nemonicos[inst][0]
                        print("Para [Instruccion] dato8bits")
                        print(inst)
                        print(lineasc)
                        continue
                    
                    #Para [Instruccion] (Direccion), [Registro]
                    elif len(nem) > 2 and re.match(patronh, nem[1]):
                        coincidencia = re.match(patronh, nem[1])
                        if coincidencia:
                            # Extraer el valor sin la 'H'
                            inst = re.sub(patronh, '(NN)', lineasc)
                            CL = CL + diccionario.t_nemonicos[inst][0]
                            print("Para [Instruccion] (Direccion), [Registro]")
                            print(lineasc)
                            continue

                    #Para [Instruccion] [Registro], (Direccion)
                    elif len(nem) > 2 and re.match(patronh, nem[2]):
                        coincidencia = re.match(patronh, nem[2])
                        if coincidencia: 
                            inst = re.sub(patronh, '(NN)', lineasc)
                            CL = CL + diccionario.t_nemonicos[inst][0]
                            print("Para [Instruccion] [Registro], (Direccion)")
                            print(lineasc)
                            continue

                    #Para [Instruccion] [Registro], dato 8bits
                    elif re.match(patron, lineasc):
                            coincidencia = re.match(patron, lineasc)
                            if coincidencia:
                                registro = coincidencia.group(2)
                                if registro in diccionario.registros:
                                    # Construir la instrucción genérica para buscar en t_nemonicos
                                    inst = re.sub(patron, rf'\1{registro}\3N', lineasc)
                                    CL = CL + diccionario.t_nemonicos[inst][0]
                                    print("Para [Instruccion] [Registro], dato")
                                    print(lineasc)
                                    continue

                    #Para [Instruccion] [Registro], dato 16bits
                    elif re.match(patronhh, lineasc):
                        coincidencia = re.search(patronhh, lineasc)
                        if coincidencia:
                            # Sustituir la dirección hexadecimal por 'NN'
                            inst = re.sub(patronhh, r'\1NN', lineasc)
                            CL = CL + diccionario.t_nemonicos[inst][0]
                            print("#Para [Instruccion] [Registro], dato 16bits")
                            print(lineasc)
                            continue
                    
                    #Para [Instruccion] [Registro], ([Registro] + d)
                    elif re.match(patrond, lineasc):
                        coincidencia = re.search(patrond, lineasc)
                        if coincidencia:
                            # Extraer los componentes de la instrucción
                            operacion, r1, r2, d = coincidencia.groups()
                            # Reemplazar d por temp en la instrucción
                            inst = f"{operacion} {r1}, ({r2} + d)"
                            CL = CL + diccionario.t_nemonicos[inst][0]
                            print("Para [Instruccion] [Registro], ([Registro] + d)")
                            print(lineasc)
                            continue
                                    
    tamano_programa = CL

def segunda_pasada():
    global COHEX
    global CLHEX
    CL = 0
    with open(archivo_path, "r") as archivo:
        with open(nombre_archivo_lst, "w") as archivolst:
            # Itera sobre cada línea del archivo
            for linea in archivo:
                #Quitando los comentarios del codigo
                lineasc = linea.split(';')[0].strip()
                # Divide la línea en palabras
                nem = lineasc.split()
                if len(nem) == 0:
                    archivolst.write("\n")
                    continue

                else: 
                    if "CPU" in nem:
                        escribir = f"{convertir.decimal_a_hexadecimal(CL)}           {linea}"
                        archivolst.write(escribir)
                        continue

                    if "HOF" in nem:
                        escribir = f"{convertir.decimal_a_hexadecimal(CL)}           {linea}"
                        archivolst.write(escribir)
                        continue

                    #Si encuentra la directiva ORG inicia el CL en la direccion dada
                    if "ORG" in nem:
                        #Extrae la direccion de la linea de codigo
                        direccion_hexadecimal = nem[1]
                        CL = int(direccion_hexadecimal[:-1], 16)  # Elimina el último carácter 'H' y convierte de hexadecimal a decimal
                        CLHEX = CL
                        escribir = f"{convertir.decimal_a_hexadecimal(CL)}           {linea}"
                        archivolst.write(escribir)
                        continue
                        
                    #Si encuentra END termina el bucle
                    if "END" in lineasc:
                        escribir = f"{convertir.decimal_a_hexadecimal(0)}           {linea}"
                        archivolst.write(escribir)
                        for clave, valor in tSimbolos.items():
                            archivolst.write(f"{valor} {clave}             ")
                        break

                    if "JP" in nem:
                        direccionsalto = nem[len(nem)-1]
                        if direccionsalto in tSimbolos:
                            direccion = tSimbolos.get(direccionsalto)
                            inst = lineasc.replace(direccionsalto, "NN")
                            byte1 = direccion[:2]
                            byte2 = direccion[2:]
                            direccion_invertida = byte2 + byte1
                            CO = diccionario.t_nemonicos[inst][1]
                            CO = CO.replace("xxxx", direccion_invertida)
                            COHEX = COHEX + CO
                            escribir = f"{convertir.decimal_a_hexadecimal(CL).zfill(4)} {CO}      {linea}"
                            archivolst.write(escribir)
                            CL = CL + diccionario.t_nemonicos[inst][0]
                            continue

                        else:
                            print(f"Etiqueta {direccionsalto} no definida")
                            break

                    if "JR" in nem:
                        etiqueta = nem[len(nem)-1]
                        if etiqueta in tSimbolos:
                            inst = lineasc.replace(etiqueta, "DIS")
                            CLTEMP = CL
                            CL = CL + diccionario.t_nemonicos[inst][0]
                            CLN = convertir.hexadecimal_a_decimal(tSimbolos.get(etiqueta))
                            CLA = CL
                            x = convertir.decimal_a_hexadecimal(CLN-CLA)
                            CO = diccionario.t_nemonicos[inst][1]
                            CO = CO.replace("xx", x[-2:])
                            COHEX = COHEX + CO
                            escribir = f"{convertir.decimal_a_hexadecimal(CLTEMP).zfill(4)} {CO}      {linea}"
                            archivolst.write(escribir)
                            continue

                        else:
                            print(f"Etiqueta {etiqueta} no definida")
                            break

                    else:
                        n = nem[0]
                        #Si encuentra un ':' significa que encontro una etiqueta
                        if ':' in n:
                            escribir = f"{convertir.decimal_a_hexadecimal(CL)}           {linea}"
                            archivolst.write(escribir)    
                            continue 

                        #Para cualquier instruccion sin variables                           
                        if lineasc in diccionario.t_nemonicos:
                            #print(diccionario.t_nemonicos.get(lineasc))
                            CO = diccionario.t_nemonicos[lineasc][1]
                            COHEX = COHEX + CO
                            escribir = f"{convertir.decimal_a_hexadecimal(CL)} {CO}        {linea}"
                            archivolst.write(escribir)
                            CL = CL + diccionario.t_nemonicos[lineasc][0]
                            continue

                        #Para [Instruccion] dato8bits
                        elif len(nem) == 2 and nem[1] not in diccionario.registros:
                            inst = lineasc.replace(nem[1], "N")
                            CO = diccionario.t_nemonicos[inst][1]
                            CO = CO.replace("xx", nem[1])
                            COHEX = COHEX + CO
                            escribir = f"{convertir.decimal_a_hexadecimal(CL)} {CO}        {linea}"
                            archivolst.write(escribir)
                            CL = CL + diccionario.t_nemonicos[inst][0]
                            continue

                        #Para [Instruccion] (Direccion), [Registro]
                        elif len(nem) > 2 and re.match(patronh, nem[1]):
                            coincidencia = re.match(patronh, nem[1])
                            if coincidencia:
                                # Extraer el valor sin la 'H'
                                valor = coincidencia.group(1)
                                inst = re.sub(patronh, '(NN)', lineasc)
                                byte1 = valor[:2]
                                byte2 = valor[2:]
                                # Invertir los bytes
                                valor_invertido = byte2 + byte1
                                CO = diccionario.t_nemonicos[inst][1]
                                CO = CO.replace("xxxx", valor_invertido)
                                COHEX = COHEX + CO
                                escribir = f"{convertir.decimal_a_hexadecimal(CL).zfill(4)} {CO}      {linea}"
                                archivolst.write(escribir)
                                CL = CL + diccionario.t_nemonicos[inst][0]
                                continue

                        #Para [Instruccion] [Registro], (Direccion)
                        elif len(nem) > 2 and re.match(patronh, nem[2]):
                            coincidencia = re.match(patronh, nem[2])
                            if coincidencia:
                                # Extraer el valor sin la 'H'
                                valor = coincidencia.group(1)
                                inst = re.sub(patronh, '(NN)', lineasc)
                                byte1 = valor[:2]
                                byte2 = valor[2:]
                                # Invertir los bytes
                                valor_invertido = byte2 + byte1
                                CO = diccionario.t_nemonicos[inst][1]
                                CO = CO.replace("xxxx", valor_invertido)
                                COHEX = COHEX + CO
                                escribir = f"{convertir.decimal_a_hexadecimal(CL).zfill(4)} {CO}      {linea}"
                                archivolst.write(escribir)
                                CL = CL + diccionario.t_nemonicos[inst][0]
                                continue

                        #Para [Instruccion] [Registro], dato 8bits
                        elif re.match(patron, lineasc):
                            coincidencia = re.match(patron, lineasc)
                            if coincidencia:
                                instruccion = coincidencia.group(1).strip()
                                registro = coincidencia.group(2)
                                dato = coincidencia.group(4)
                                # Construir la instrucción genérica para buscar en t_nemonicos
                                inst = re.sub(patron, rf'\1{registro}\3N', lineasc)
                                CO = diccionario.t_nemonicos[inst][1]
                                CO = CO.replace("xx", dato)
                                COHEX = COHEX + CO
                                escribir = f"{convertir.decimal_a_hexadecimal(CL).zfill(4)} {CO}      {linea}"
                                archivolst.write(escribir)
                                CL = CL + diccionario.t_nemonicos[inst][0]
                                continue

                        #Para [Instruccion] [Registro], dato 16bits
                        elif re.match(patronhh, lineasc):
                            coincidencia = re.search(patronhh, lineasc)
                            if coincidencia:
                                # Sustituir la dirección hexadecimal por 'NN'
                                inst = re.sub(patronhh, r'\1NN', lineasc)
                                # Extraer el valor de la dirección hexadecimal sin la 'H'
                                valor = coincidencia.group(2)
                                byte1 = valor[:2]
                                byte2 = valor[2:]
                                # Invertir los bytes
                                valor_invertido = byte2 + byte1
                                CO = diccionario.t_nemonicos[inst][1]
                                CO = CO.replace("xxxx", valor_invertido)
                                COHEX = COHEX + CO
                                escribir = f"{convertir.decimal_a_hexadecimal(CL).zfill(4)} {CO}      {linea}"
                                archivolst.write(escribir)
                                CL = CL + diccionario.t_nemonicos[inst][0]
                                continue

                        #Para [Instruccion] [Registro], ([Registro] + d)
                        elif re.match(patrond, lineasc):
                            coincidencia = re.search(patrond, lineasc)
                            if coincidencia:
                                # Extraer los componentes de la instrucción
                                operacion, r1, r2, d = coincidencia.groups()
                                
                                # Crear la variable temp con el valor de d
                                valor = d
                                inst = f"{operacion} {r1}, ({r2} + d)"
                                CO = diccionario.t_nemonicos[inst][1]
                                CO = CO.replace("xx", valor)
                                COHEX = COHEX + CO
                                escribir = f"{convertir.decimal_a_hexadecimal(CL).zfill(4)} {CO}      {linea}"
                                archivolst.write(escribir)
                                CL = CL + diccionario.t_nemonicos[inst][0]
                                continue

def generar_hex():
    with open(nombre_archivo_hex, "w") as archivohex:
        global COHEX
        global CLHEX
        grupos = [COHEX[i:i+32] for i in range(0, len(COHEX), 32)]
        for grupo in grupos:
            tamano_decimal = int(len(grupo)/2)
            tamano = convertir.convertir_tamano(tamano_decimal)
            hexa = f"{tamano}{convertir.decimal_a_hexadecimal(CLHEX)}00{grupo}"
            print(hexa)
            cz = convertir.cz(hexa)
            archivohex.write(f":{tamano}{convertir.decimal_a_hexadecimal(CLHEX)}00{grupo}{cz}\n")
            CLHEX = CLHEX + tamano_decimal
        archivohex.write(":00000001FF")

            
primera_pasada()
segunda_pasada()
print(tSimbolos)
generar_hex()

