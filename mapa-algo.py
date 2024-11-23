import numpy as np

EPSILON = 0.0001

def numBitUno(num):
    bitUnos = 0
    while num != 0:
        if num % 2 == 1:
            bitUnos += 1
        num //= 2
    return bitUnos

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

def quineMcCluskey(bit, f):
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

        numeros[numBitUno(num)].append(num)
    
    parejas = []
    for i in range(len(numeros) - 1):
        parejas.append([])
        previo = numeros[i]
        siguiente = numeros[i + 1]

        for numPrevio in previo:
            for numSiguiente in siguiente:
                if not diferenciaUnBit([numPrevio, numSiguiente]):
                    continue
                    
                parejas[i].append((numPrevio, numSiguiente))

    return parejas
    
#                              0,    1,    2,                   5,   6,    7,    8,     9,   10,                        14
funcionInicial = lambda num: [True, True, True, False, False, True, True, True, True, True, True, False, False, False, True, False][num]

print(quineMcCluskey(4, funcionInicial))
