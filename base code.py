import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Clase del carro

class Carro:
    def __init__(self, v):
        self.v = int(v)

# Distancia al otro carrito
#Calcula cuantas celdas hay libres hasta el siguiente carro adelante
# usando condiciones periódicas como tal, ya que imaginen que la carretera es un circuito

def contar_distancia(i, carretera):
    L = len(carretera)
    d = 0

    for step in range(1, L):
        j = (i + step) % L
        if carretera[j] is None:
            d += 1
        else:
            break

    return d


# REGLAS NAGEL- etc etc nombre raro
# Segu el paper estas 4 reglas se aplican a TODOS los carros en paralelo
#1) Aceleración: si puede, aumenta velocidad
# 2) Frenado: evita choques
# 3) Aleatorización: imita tipo errores humanos
# 4) Movimiento: el carro avanza v celdas


def actualizar(carretera, v_max, p=0.5):
    L = len(carretera)
    nueva = [None] * L

    for i, c in enumerate(carretera):

        if c is None:
            continue
# si no hay carro, no hacemos nada
        v = c.v
        d = contar_distancia(i, carretera)

        # 1. aceleración
        if v < v_max and d > v:
            v += 1

        # 2. frenado (evita choques
        if d <= v:
            v = d

        # 3. aleatorización (como q smula errores humanos

        if random.random() < p and v > 0:
            v -= 1

        c.v = v

        # 4. movimiento
        j = (i + v) % L

        if nueva[j] is None:
            nueva[j] = c
        else:
            #  si hay choque, el carro se queda
            nueva[i] = c

    return nueva



# densidad


def calcular_densidad(carretera):
    return sum(c is not None for c in carretera) / len(carretera)


#Mide  cuántos carros cruzan el punto medio del sistema
# en cada instante

def flujo_sistema(carretera):
    L = len(carretera)
    punto = L // 2

    flujo = 0

    for i, c in enumerate(carretera):
        if c is not None:
          # si el carro cruza el punto en este paso
            if i <= punto < (i + c.v) % L:
                flujo += 1

    return flujo

# Simulacion del diagrama fundamental (df)
# Relación entre densidad  y flujo

def simular_rho(rho, L=1000, v_max=5):

    carretera = [None] * L
 # colocamos N autos aleatoriamente según densidad
    N = int(rho * L)
    posiciones = np.random.choice(range(L), size=N, replace=False)

    for p in posiciones:
        carretera[p] = Carro(np.random.randint(0, v_max + 1))

    flujo_total = 0
    mediciones = 0

    for t in range(5000):
        carretera = actualizar(carretera, v_max)

        # relajación
        if t > 2000:
          # dejamos el sistema estabilizarse primero
            flujo_total += flujo_sistema(carretera)
            mediciones += 1

    return flujo_total / max(mediciones, 1)


# CASO v_max = 1 , es como un caso especial digamos
#se usa  para validar teoría que dice que  q = ρ(1 - ρ)

def simular_vm1(rho, L=1000):

    carretera = [None] * L
    N = int(rho * L)

    posiciones = np.random.choice(range(L), size=N, replace=False)

    for p in posiciones:
        carretera[p] = Carro(np.random.randint(0, 2))

    flujo = 0

    for t in range(2000):
        carretera = actualizar(carretera, v_max=1)
        flujo += flujo_sistema(carretera)

    return flujo / 2000


# densidad barrido


v_max = 5
rho_values = np.linspace(0.02, 0.3, 10)

results = []

for rho in rho_values:
    results.append(simular_rho(rho))



# grafica df


plt.figure()
plt.plot(rho_values, results, marker='o')
plt.xlabel("Densidad ρ")
plt.ylabel("Flujo q")
plt.title("Diagrama Fundamental (Nagel-Schreckenberg)")
plt.grid()
plt.show()


# =====================================================
#  v_max = 1 (q = ρ(1-ρ))


rho_test = np.linspace(0.05, 0.95, 10)
q_test = [simular_vm1(r) for r in rho_test]

plt.figure()
plt.plot(rho_test, q_test, marker='o', label="Simulación v=1")
plt.plot(rho_test, rho_test*(1-rho_test), "--", label="Teoría ρ(1-ρ)")
plt.legend()
plt.title("Validación caso v_max = 1")
plt.xlabel("ρ")
plt.ylabel("q")
plt.grid()
plt.show()



# Animacion
#Visualización en tiempo real del movimiento de autos


L = 1000
carretera = [None] * L

rho = 0.08
N = int(rho * L)

posiciones = np.random.choice(range(L), size=N, replace=False)

for p in posiciones:
    carretera[p] = Carro(np.random.randint(0, v_max + 1))


fig, ax = plt.subplots(figsize=(10, 2))
ax.set_xlim(0, L)
ax.set_ylim(-1, 1)
ax.set_title("Modelo de tráfico (NaSch)")
ax.get_yaxis().set_visible(False)
ax.axhline(0, color='gray', lw=4)

grafica, = ax.plot([], [], 'bo', markersize=4)


def init():
    grafica.set_data([], [])
    return grafica,


def animar(frame):
    global carretera

    carretera = actualizar(carretera, v_max)

    x = [i for i, c in enumerate(carretera) if c is not None]
    y = [0] * len(x)

    grafica.set_data(x, y)

    return grafica,


ani = animation.FuncAnimation(
    fig, animar, frames=100, init_func=init, blit=True, interval=120)

plt.show()