import multiprocessing
import random

semaforo = None
porta_nova: int = 0
porta_saida: int = 0
ultrapassou: int = 0
ultrapassou_pedra: int = 0
portas: int = [0] * 4

def init(sa, nv, s, u, up, p):
    global porta_saida
    global porta_nova
    global semaforo
    global ultrapassou
    global ultrapassou_pedra
    global portas
    porta_saida = sa
    porta_nova = nv
    semaforo = s
    ultrapassou = u
    ultrapassou_pedra = up
    portas = p

def corredor(cavaleiro, velocidade):
    global semaforo
    global ultrapassou
    percorrido: int = 0
    tocha: bool = False

    while percorrido < 500:
        percorrido = percorrido + velocidade

    with semaforo:
        if ultrapassou.value != 1:
            ultrapassou.value = 1
            velocidade = velocidade + 2
            tocha = True

    if tocha:
        p_porta(cavaleiro, velocidade, percorrido)
    else:
        pedra(cavaleiro, velocidade, percorrido)

def pedra(cavaleiro, velocidade, percorrido):
    global semaforo
    global ultrapassou_pedra

    while percorrido < 1500:
        percorrido = percorrido + velocidade

    with semaforo:
        if ultrapassou_pedra.value != 1:
            ultrapassou_pedra.value = 1
            velocidade = velocidade + 2
    p_porta(cavaleiro, velocidade, percorrido)

def p_porta(cavaleiro, velocidade, percorrido):
    global semaforo
    global porta_saida
    global porta_nova
    global portas

    while percorrido < 2000:
        percorrido = percorrido + velocidade

    with semaforo:
        porta_nova.value = random.randint(1,4)

        while porta_nova.value in portas:
            porta_nova.value = random.randint(1,4)

        for i in range(4):
            if portas[i] == 0:
                portas[i] = porta_nova.value
                break
        if porta_saida.value == porta_nova.value:
            print ('O cavaleiro', cavaleiro, 'foi o único que conseguiu sair')

def main():
    sem = None
    saida: int = 0
    nova: int = 0
    passagem: int = 0
    pedra: int = 0
    porta: int = [0] * 4

    saida = multiprocessing.Value('i', random.randint(1,4))
    nova = multiprocessing.Value('i', 0)
    passagem = multiprocessing.Value('i', 0)
    pedra = multiprocessing.Value('i', 0)
    porta = multiprocessing.Array('i', porta)

    params: int = [(0,0)] * 4
    velocidades: int = [0] * 4

    for i in range(4):
        velocidades[i] = random.randint(2,4)
        params[i] = ((i+1), velocidades[i])

    with multiprocessing.Manager() as manager:
        sem = manager.Semaphore(1)
        with multiprocessing.Pool(processes=4, initializer=init, initargs=(saida, nova, sem, passagem, pedra, porta)) as pool:
            pool.starmap(corredor, params)

if __name__ == '__main__':
    main()