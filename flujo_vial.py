import numpy as np
import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Carro:
	def __init__(self, velocidad):
		self.v = int(velocidad)

def evento():
	n = (random.random() < 0.5)
	return n
		
def contar_distancia(celda, carretera):
	distancia = 0
	n = len(carretera)
	
	for espacio in range(1,n):
		siguiente = (celda + espacio) % n
		
		if carretera[siguiente] == 0:
			distancia += 1
		else:
			break
	
	return distancia
	
def actualizar(carretera, v_max):
	n = len(carretera)
	
	carros = []
	
	for i, celda in enumerate(carretera):
		if celda != 0:
			carros.append((i,celda))
	
	for i, celda in carros:
		distancia = contar_distancia(i, carretera)
			
		if (celda.v < v_max) and (distancia > celda.v):
			celda.v += 1
			
		if (distancia <= celda.v):
			celda.v = distancia
				
		if evento() and (celda.v > 0):
			celda.v -= 1
			
	nueva_carretera = [0] * n
		
	for i, celda in carros:
		indice_nuevo = (i + celda.v) % n
		nueva_carretera[indice_nuevo] = celda
		
	return nueva_carretera
			
	
carretera = [0] * 1000

dt = 1.0
t_final = 10000
tiempos = []

intervalo_snapshot = 1
snapshots = []

v = [0, 1, 2, 3, 4, 5]
v_max = int(v[-1])

#cantidad_carros = 100

#posiciones = random.sample(range(len(carretera)), cantidad_carros)

#for posicion in posiciones:
	#carretera[posicion] = Carro(velocidad=random.randint(v[0], v[-1]))

t0 = time.perf_counter()

for n in range(int(t_final/dt) + 1):
	
	if carretera[0] == 0:
		carretera[0] = Carro(velocidad=0)
	
	for m in range(len(carretera)-6,len(carretera)):
		if carretera[m] != 0:
			carretera[m] = 0
	
	if n % intervalo_snapshot == 0:
		
		posiciones = []
		
		for celda in carretera:
			if celda != 0:
				posiciones.append(1)
			else:
				posiciones.append(0)
			
		snapshots.append(np.copy(posiciones))
		tiempos.append(n*dt)
	
	carretera = actualizar(carretera, v_max)
	
t1 = time.perf_counter()
	
for i, snap in enumerate(snapshots):
	print(i, np.sum(snap))

print(t1-t0)

fig, ax = plt.subplots(figsize=(10,2))

linea = ax.imshow(
	[snapshots[0]],
	cmap="viridis",
	aspect="auto",
	interpolation="nearest",
	vmin=0,
	vmax=1
	)

ax.set_xlabel("posicion")
ax.set_yticks([])
ax.set_title("Simulacion")

def animar(i):
	linea.set_data([snapshots[i]])
	ax.set_title(tiempos[i])
	return [linea]
	
ani = animation.FuncAnimation(
	fig,
	animar,
	frames=len(snapshots),
	interval=100,
	blit=False
	)

plt.show()

plt.imshow(snapshots, aspect="auto", cmap="viridis")
plt.xlabel("posicion")
plt.ylabel("tiempo")

plt.show()
