import numpy as np

EPSILON = 0.0001

class Numero:

    def __init__(self, numeros):
        self.numeros = numeros
        self.usado = False

    def fueUsado(self):
        self.usado = True

def numBitUno(num):
    bitUnos = 0
    while num != 0:
        if num % 2 == 1:
            bitUnos += 1
        num //= 2
    return bitUnos

def diferenciaNum(numeros):
    assert(len(numeros) > 0)

    if len(numeros) == 1:
        return (numeros[0], 0)

    primero, diferenciaPrimero = diferenciaNum(numeros[:len(numeros)//2])
    segundo, diferenciaSegundo = diferenciaNum(numeros[len(numeros)//2:])

    assert(diferenciaPrimero == diferenciaSegundo)

    diferencia = primero ^ segundo
    mascara = ~diferencia
    assert(primero & mascara == segundo & mascara)

    return (primero & mascara, diferenciaPrimero + diferencia)

def reducirDiferencia(numeros):
    if len(numeros) <= 2:
        [primero, segundo] = numeros 
    else: 
        primero = reducirDiferencia(numeros[:len(numeros)//2])
        segundo = reducirDiferencia(numeros[len(numeros)//2:])

    mascara = ~(primero ^ segundo)
    assert(primero & mascara == segundo & mascara)
    return primero & mascara

def diferenciaUnBit(numeros: list[int]):
    if len(numeros) <= 2:
        [numPrevio, numSiguiente] = numeros
    else:
        numPrevio = reducirDiferencia(numeros[:len(numeros)//2])
        numSiguiente = reducirDiferencia(numeros[len(numeros)//2:])

    diferencia = numSiguiente ^ numPrevio
    log2diferencia = np.log2(diferencia) 
    fraccion = log2diferencia - int(log2diferencia)

    return -EPSILON < fraccion and fraccion < EPSILON

def quineMcCluskey(bit: int, f) -> list:
    """
        bit: cantidad de bits que se quiere usar
        f: una funcion que devuelve true si la funcion 
            original es 1 o redundante
    """
    numeros = []
    for _ in range(bit + 1):
        numeros.append([])

    for num in range(2**bit - 1):
        if not f(num):
            continue

        numeros[numBitUno(num)].append(Numero([num]))
    
    parejasPrevias = numeros
    parejasNuevas = []
    parejasNoUsadas = []

    while True:
        agregoNuevaPareja = False

        for i in range(len(parejasPrevias) - 1):
            parejasNuevas.append([])
            previo = parejasPrevias[i]
            siguiente = parejasPrevias[i + 1]

            for numPrevio in previo:
                for numSiguiente in siguiente:
                    if diferenciaNum([*numPrevio.numeros])[1] != diferenciaNum([*numSiguiente.numeros])[1]:
                        continue

                    if not diferenciaUnBit([*numPrevio.numeros, *numSiguiente.numeros]):
                        continue

                    agregoNuevaPareja = True

                    numPrevio.fueUsado()
                    numSiguiente.fueUsado()
                    parejasNuevas[i].append(Numero([*numPrevio.numeros, *numSiguiente.numeros]))

        for nivel in parejasPrevias:
            parejasNoUsadas += list(filter(lambda numero: not numero.usado, nivel))

        if not agregoNuevaPareja:
            break
        
        parejasPrevias = parejasNuevas
        parejasNuevas = []

    parejasFinales = {}
    for pareja in parejasNoUsadas:
        diferencia = diferenciaNum([*pareja.numeros])[1]
        if not diferencia in parejasFinales:
            parejasFinales[diferencia] = pareja

    return parejasFinales.values()
    
#                              0,    1,    2,                   5,   6,    7,    8,     9,   10,                        14
funcionInicial = lambda num: [True, True, True, False, False, True, True, True, True, True, True, False, False, False, True, False][num]

resultado = quineMcCluskey(4, funcionInicial)
for pareja in resultado:
    print(f"{pareja.numeros} - {pareja.usado}")

"""
for i, nivel in enumerate(resultado):
    print(f"Nivel {i}")
    for pareja in nivel:
        print(f"{pareja.numeros} - {pareja.usado}")
"""
