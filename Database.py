import pandas as pd
from PatronesGEP import generar_patrones
from math import factorial

"""
partidosJugados: [numero partido, equipo, local, puntos, fecha, equipo]


"""

def open_excel(name, page):
    """
    :param name: nombre del archivo a abrir
    :param page: nombre de la pagina de interes
    :return: lista por filas de pagina de excel
    """
    file = pd.ExcelFile(name)
    file = file.parse(page)
    column = []
    for key in file.keys():
        lista = []
        for i in range(len(file[key])):
            lista.append(str(file[key][i]).rstrip().replace("\xa0", " "))
        column.append(lista)
    lista = list(zip(*column))
    return lista


def conjuntoPuntos(equiposDB, Rina):
    """

    """
    puntosInicio = {x[2]: int(x[3]) for x in equiposDB}
    puntosMax = {}
    puntosMin = {}
    resultadoPartidos = {}
    for equipo in equipos:
        ucwin = 0
        ucdraw = 0
        for partidos in list(Rina[equipo].keys())[0:15]:
            if Rina[equipo][partidos][3] == 1:
                ucwin += 1
            elif Rina[equipo][partidos][1] == 1:
                ucdraw += 1
        uclost = 15 - ucwin - ucdraw
        uct = {(x + 16): puntosInicio[equipo] + ((x + 1) * 3) if x < ucwin else puntosInicio[equipo] + (ucwin * 3) + (
                x + 1 - ucwin) if x < ucwin + ucdraw else puntosInicio[equipo] + ucwin * 3 + ucdraw for x in range(15)}
        ucl = {(x + 16): puntosInicio[equipo] if x < uclost else puntosInicio[equipo] + + (
                x + 1 - uclost) if x < uclost + ucdraw else puntosInicio[equipo] + (
                    x + 1 - uclost - ucdraw) * 3 + ucdraw
               for x in range(15)}
        puntosMax[equipo] = uct
        puntosMin[equipo] = ucl
        resultados = {"win": ucwin, "draw": ucdraw, "loss": uclost}
        resultadoPartidos.update({equipo: resultados})

    puntos = {
    equipo: {fecha + 16: [x for x in range(puntosMin[equipo][fecha + 16], puntosMax[equipo][fecha + 16] + 1)] for fecha
             in range(15)} for equipo in equipos}
    # Rina = {line[0]: {puntos: 1 if puntos == puntos else 0} for puntos in [0, 1, 3] for line in equiposDB}

    puntosvalidos = []
    for i in equipos:
        for j in range(15):
            j = j + 16
            for k in range(90):
                if k in puntos[i][j]:
                    puntosvalidos.append((i, k, j))

    return puntosInicio, resultadoPartidos


equiposDB = open_excel("datos/Datos.xlsx", 0)
partidosDB = open_excel("datos/Datos.xlsx", 1)

def partidos_jugados(partidosDB):
    """Creando diccionario Partidos para facilidad de manejo
    primero creamos listPos que indica la posicion en donde el empieza una nueva fecha de partidos en el excel
    Luego partidosJ es un diccionario que para cada fecha contiene sus partidos
    Luego recorro cada uno de estos partidos y creo partidosJugados que contiene [numero partido, equipo, local, puntos, fecha, equipo]
    """
    pos = 0
    listPos = []
    for i in partidosDB:
        if i[0] != "nan":
            listPos.append(pos)
        pos += 1
    dif = []
    partidosJ = {partidosDB[i][0]: partidosDB[i + 1: i + 9] for i in listPos}  # {fecha: [partidos]}
    indice = 0
    partidosJugados = []
    for key in partidosJ.keys():
        newList = []
        for fecha in partidosJ[key]:
            if (119 - indice) < 0:
                break
            resultado = fecha[4].split(" : ")
            if int(resultado[0]) < int(resultado[1]):
                puntos = [0, 3]
            elif int(resultado[0]) > int(resultado[1]):
                puntos = [3, 0]
            else:
                puntos = [1, 1]
            newList.extend([[119 - indice, fecha[2], "Local", puntos[0], key, fecha[3]],
                            [119 - indice, fecha[3], "Visita", puntos[1], key, fecha[2]]])
            indice += 1

        partidosJugados.extend(newList)
    return partidosJugados


partidosJugados = partidos_jugados(partidosDB)

equipos = [equipo[2] for equipo in equiposDB]  #Lista que contiene los equipos


"""
Definiendo variable Eit, toma 1 si equipo "i" tiene "t" puntos.
 para esto tMax es maximo puntaje
"""
Eit = {equipo[2]: {i: 1 if i == int(equipo[3]) else 0 for i in range(84)} for equipo in equiposDB}

"""
variable Rina 1 si cantida de puntos que gana equipo "i" 
jugando partido "n" es igual a "a"
"""
Rina = {}
for equipo in equipos:
    Rina[equipo] = {}

for partido in partidosJugados:
    # partidosJugados = [numero partido, equipo, local, puntos, fecha, equipo]
    Rina[partido[1]].update({partido[0]: {}})

for partido in partidosJugados:
    for puntos in [0, 1, 3]:
        Rina[partido[1]][partido[0]].update({puntos: 1 if partido[3] == puntos else 0})

"""
Nijn 1 si equipo i juega contra equipo j partido n
"""
Nijn = {x: {} for x in equipos}
for equipo in equipos:
    Nijn[equipo] = {x: {i: 0 for i in range(120)} for x in equipos if x != equipo}

contador = 0
for partido in partidosJugados:
    Nijn[partido[1]][partido[5]][partido[0]] = 1
    if contador == 239:
        break
    contador += 1

"""
ELin EVin 1 su equipo i es "L" o "V" en partido n
"""
ELin = {x: {} for x in equipos}
EVin = {x: {} for x in equipos}
for i in equipos:
    for z in range(120):
        EVin[i].update({z: 0})
        ELin[i].update({z: 0})

contador = 0
for i in partidosJugados:
    # print(i)
    ELin[i[1]].update({i[0]: 1 if i[2] == "Local" else 0})
    EVin[i[1]].update({i[0]: 1 if i[2] == "Visita" else 0})
    if contador == 239:
        break
    contador += 1

"""
Wis Toma 1 si a equipo i se le puede asignar patron s
"""
W = open_excel("datos/Generador de Patrones.xlsm", "W")
Wis = {x: {} for x in equipos}
for i in W:
    Wis[i[1]].update({int(i[3]): int(i[5])})

"""
Lfs Toma 1 si patron s indica que partido esde local en fecha s
"""
patrones = open_excel("datos/Generador de Patrones.xlsm", "Patrones")
Lsf = {x + 1: {} for x in range(1440)}
for i in range(1440):
    Lsf[i + 1].update({x + 16: int(patrones[i][x]) for x in range(15)})

"Vf funcion de valor por fecha"
Vf = {x + 1: x * 2 for x in range(30)}

"""
Bift
"""
Bift = {x: {} for x in equipos}
for x in equipos:
    for i in range(15):
        Bift[x].update({i + 16: {}})
for x in equiposDB:
    for fecha in range(15):
        for puntos in range(84):
            Bift[x[2]][fecha + 16].update({puntos: 1 if int(x[3]) + (fecha + 1) * 3 >= puntos else 0})

puntosInicio, resultadoPartidos = conjuntoPuntos(equiposDB, Rina)

"""
Aif
"""
Aif = {equipo: {fecha + 16: 1 if puntosInicio[equipo] + 3 * (15 - fecha) > 34 + (fecha * 3) else 0 for fecha in range(15)} for equipo in equipos}

"""
Dif
"""
Dif = {equipo: {fecha + 16: 1 if puntosInicio[equipo] + (3 * fecha) < 9 + (15 - fecha) * 3 else 0 for fecha in range(15)} for equipo in equipos}

resultadosPosibles = {x: [] for x in equipos}

result = [[x["win"], x["draw"], x["loss"]] for x in resultadoPartidos.values()]
repetidos = []
contador = 0
for i in result:
    if result.count(i) == 2:
        repetidos.append((result.index(i), contador))
    contador += 1
print(repetidos)
contador = 0
contador2 = 1
indexi = []
megalist = []
for i in equipos:
    win = resultadoPartidos[i]["win"]
    draw = resultadoPartidos[i]["draw"]
    loss = resultadoPartidos[i]["loss"]
    if contador not in [8, 11, 15]:
        if contador == 0:
            indexi.append(int(factorial(15)/(factorial(win)*factorial(draw)*factorial(loss))))
            megalist.append([0, int((factorial(15) / (factorial(win) * factorial(draw) * factorial(loss))))])
        else:
            indexi.append(int((factorial(15) / (factorial(win) * factorial(draw) * factorial(loss))) + indexi[contador - contador2]))
            megalist.append([int(indexi[contador - contador2]), int((factorial(15) / (factorial(win) * factorial(draw) * factorial(loss))) + indexi[contador - contador2])])
        resultados = list(map(lambda x: "".join(x), generar_patrones(win, draw, loss)))
        resultadosPosibles[i] = resultados
        contador2 = 1
    elif contador == 8:
        indexi.append(indexi[6])
        megalist.append(megalist[6])
        contador2 = 2
    elif contador == 11:
        indexi.append(indexi[0])
        megalist.append(megalist[0])
        contador2 = 2
    else:
        indexi.append(indexi[4])
        megalist.append(megalist[4])
    contador += 1


RP = list(z for x in resultadosPosibles.values() for z in x)

largo = len(RP)
RPfg = {x + 16: {z: int(RP[z][x]) for z in range(largo)} for x in range(15)}


Rin = {}
for i in equipos:
    Rin[i] = {}

for x in partidosJugados:
     #[numero partido, equipo, local, puntos, fecha, equipo]
    Rin[x[1]].update({x[0]: int(x[3])})

VGig = {equipos[x]: {z: 1 if megalist[x][0] <= z < megalist[x][1] else 0 for z in range(largo)} for x in range(16)}
print(puntosInicio)

dictPosiblesG = {}
for i in range(16):
    dictPosiblesG.update({equipos[i]: [x for x in range(megalist[i][0], megalist[i][1])]})
print(dictPosiblesG["UC"][0], dictPosiblesG["UC"][-1])

listasuprema = []
for i in range(16):
    for z in range(megalist[i][1] + 1):
        if z >= megalist[i][0] and z < megalist[i][1]:
            listasuprema.append((equipos[i], z))
print(megalist[0][0], megalist[0][1])

Tigf = {numerog: {fecha + 16: int(sum(RPfg[fecha2 + 16][numerog] for fecha2 in range(fecha + 1)))
                           for fecha in range(15)} for numerog in range(largo)}
