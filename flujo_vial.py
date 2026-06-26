import numpy as np
import pandas as pd
import argparse
import csv
import os
import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Guardar datos de simulaciones

def guardar_datos(nombre, cantidad, densidad_r, densidad_a, flujo_total):
	
	archivo_existe = os.path.isfile(nombre)
	
	with open(nombre, "a", newline="") as archivo:
		escritor = csv.writer(archivo)
		
		if not archivo_existe:
			escritor.writerow([
				"cantidad_carros",
				"densidad_real",
				"densidad_aproximada",
				"flujo_promedio"
				])
		
		escritor.writerow([
			cantidad,
			densidad_r,
			densidad_a,
			flujo_total
		])

# Definir objeto Carro

class Carro:
	def __init__(self, velocidad):
		self.v = int(velocidad)

# Definir evento aleatorio

def evento(p):
	n = (random.random() < p)
	return n
	
# Contar espacios vacíos frente a un carro
		
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

# Actualizar Carros
	
def actualizar(carretera, v_max, p, medicion):
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
				
		if evento(p) and (celda.v > 0):
			celda.v -= 1
			
	nueva_carretera = [0] * n
	flujo_instantaneo = 0
		
	for i, celda in carros:
		indice_nuevo = (i + celda.v) % n
		
		if celda.v > 0:
			posiciones_recorridas = [(i + paso) % n for paso in range(1, celda.v + 1)]
			if medicion in posiciones_recorridas:
				flujo_instantaneo += 1
		
		nueva_carretera[indice_nuevo] = celda
		
	return nueva_carretera, flujo_instantaneo

parser = argparse.ArgumentParser()

parser.add_argument("--cantidad_carros", type=int)

args = parser.parse_args()

cantidad = args.cantidad_carros


# Datos de cantidad de Carros

cantidad_carros = cantidad

# Datos de la carretera
				
L = 1000	
carretera = [0] * 1000

# Datos del tiempo

dt = 1.0
t_final = 50*L
t_relajacion = 10 * L
tiempos = []

# Datos de snapshots

intervalo_snapshot = 1
snapshots = []

# Datos de velocidades

v_max = 5
v = list(range(v_max + 1))

# Datos de densidad y flujo

densidad = cantidad_carros / L
densidad_aproximada = 0
flujo_total = 0
T = 1000
medicion = 100

# Dato de evento aleatorio

p = 0.5

# Generación de autos de densidad constante (Carretera Circular)

posiciones = random.sample(range(len(carretera)), cantidad_carros)

for posicion in posiciones:
	carretera[posicion] = Carro(velocidad=0)

t0 = time.perf_counter()

for n in range(int(t_final/dt) + 1):
		
	#if carretera[0] == 0:
		#carretera[0] = Carro(velocidad=0)
		
	#for m in range(len(carretera)-6,len(carretera)):
		#if carretera[m] != 0:
			#carretera[m] = 0
		
	#print(n)
				
	if (n % intervalo_snapshot == 0) and (n > 10*L):
			
		posiciones = []
			
		for celda in carretera:
			if celda != 0:
				posiciones.append(1)
			else:
				posiciones.append(0)
				
		snapshots.append(np.copy(posiciones))
		tiempos.append(n*dt)
		 
	if t_relajacion < n <= t_relajacion + T:
		if carretera[medicion] != 0:
			densidad_aproximada += 1
			
		flujo_total += flujo_instantaneo
			
		
	carretera, flujo_instantaneo = actualizar(carretera, v_max, p, medicion)
		
t1 = time.perf_counter()
		
#for i, snap in enumerate(snapshots):
	#print(i, np.sum(snap))

print("Cantidad de carros: ", cantidad_carros)

print("Tiempo: ",t1-t0)

print("Densidad Real: ", densidad)

print("Densidad Aproximada: ", densidad_aproximada/T)

print("Flujo Total: ", flujo_total/T)

guardar_datos("prueba_5.csv", cantidad_carros, densidad, densidad_aproximada/T, flujo_total/T)

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

plt.imshow(np.array(snapshots[:500]), aspect="auto", cmap="viridis")
plt.xlabel("posicion")
plt.ylabel("tiempo")

plt.show()

#df = pd.read_csv("prueba_4.csv")

#densidad_real = df["densidad_real"].tolist()
#flujo_promedio = df["flujo_promedio"].tolist()

#plt.scatter(densidad_real, flujo_promedio)

#plt.show()


		
	
	
	
	
	


