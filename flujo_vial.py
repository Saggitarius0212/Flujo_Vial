import numpy as np
import argparse
import csv
import os
import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import trafico as tf

# Ejecutar como:
# python flujo_vial.py --cantidad_carros [carros deseados] --hilos [hilos usados] --seed [semilla a usar]
#
# Cantidades Default
# --cantidad_carros 100
# --hilos 1
# --seed 12345

# Guardar datos de simulaciones

def guardar_datos(cantidad, densidad_r, densidad_a, flujo_total):
	
	os.makedirs("resultados", exist_ok=True)
	
	ruta = os.path.join("resultados", f"cantidad_carros_{cantidad}.csv")
	
	archivo_existe = os.path.isfile(ruta)
	
	with open(ruta, "a", newline="") as archivo:
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

# Definir velocidad en lista con velocidad real

def velocidad_codificada(velocidad_real):
	
	velocidad_carretera = velocidad_real + 1
	return velocidad_carretera

# Calcular la velocidad promedio de la carretera

def velocidad_promedio(carretera):
	
	velocidad = []

	for carro in carretera:
		if carro != 0:
		
			velocidad.append(carro - 1)
			
	return np.mean(velocidad)

# Datos de simulación simultánea

parser = argparse.ArgumentParser()

parser.add_argument("--cantidad_carros", type=int, default=100)
parser.add_argument("--hilos", type=int, default=1)
parser.add_argument("--seed", type=int, default=12345)

args = parser.parse_args()

cantidad = args.cantidad_carros
hilos = args.hilos
semilla = args.seed

# Ajustar semilla de aleatoriedad

random.seed(semilla)
np.random.seed(semilla)

# Datos de cantidad de Carros

cantidad_carros = cantidad

# Datos de la carretera
				
L = 1000	
carretera = np.zeros(L, dtype=np.int32)

# Validar datos de bash

if (cantidad_carros < 0) or (cantidad_carros > L):
	raise ValueError(f"cantidad_carros debe estar entre 0 y {L}.")
	
if hilos <= 0:
	raise ValueError(f"hilos debe ser mayor a 0.")

# Datos del tiempo

dt = 1.0
t_final = 50*L
t_relajacion = 10*L
tiempos_snapshots = []
tiempos_velocidades = []

# Datos de snapshots

intervalo_snapshot = 1
snapshots = []

# Datos de velocidades

v_max = velocidad_codificada(5)
velocidades = []

# Datos de densidad y flujo

densidad = cantidad_carros / L
densidad_aproximada = 0
flujo_total = 0
T = 3600
medicion = 100
flujo_instantaneo = 0

# Dato de evento aleatorio

p = 0.5

# Definir colormap

colormap = ["black", "red", "orangered", "orange", "yellow", "greenyellow", "lime"]
colormap = ListedColormap(colormap)

# Decidir tipo de flujo (0 = Circular | 1 = Abierto)

tipo_flujo = 0

if (tipo_flujo != 0) and (tipo_flujo != 1):
	raise ValueError("tipo_flujo debe ser 0 o 1")

# Generación de autos de densidad constante (Carretera Circular) tipo_flujo == 0

if tipo_flujo == 0:

	posiciones = random.sample(range(len(carretera)), cantidad_carros)

	for posicion in posiciones:
		carretera[posicion] = velocidad_codificada(0)

t0 = time.perf_counter()

for n in range(int(t_final/dt) + 1):
	
	# Generación de autos de densidad variable (Carretera Abierta) tipo_flujo == 1
	
	if tipo_flujo == 1:
		if carretera[0] == 0:
			carretera[0] = velocidad_codificada(0)
		
		for m in range(len(carretera)-6,len(carretera)):
			if carretera[m] != 0:
				carretera[m] = 0
		
	flujo_instantaneo = tf.actualizar(carretera, v_max, p, medicion, semilla, n, hilos)
				
	if (intervalo_snapshot != 0) and (n > t_relajacion) and (n % intervalo_snapshot == 0):
			
		snapshots.append(carretera.copy())
		tiempos_snapshots.append(n*dt)
		
	if t_relajacion < n <= t_relajacion + T:
		
		velocidades.append(velocidad_promedio(carretera)*20)
		tiempos_velocidades.append(n*dt)
		
		if carretera[medicion] != 0:
			densidad_aproximada += 1
			
		flujo_total += flujo_instantaneo

		
t1 = time.perf_counter()
	
# Depuración de cantidad de carros

for i, snap in enumerate(snapshots):
	print(i, np.count_nonzero(snap))

# Impresión de datos de simulación

print("Semilla: ", semilla)

if tipo_flujo == 0:
	print("Cantidad de carros: ", cantidad_carros)

print("Tiempo: ",t1-t0)

if tipo_flujo == 0:
	print("Densidad Real: ", densidad)

print("Densidad Aproximada: ", densidad_aproximada/T)

print("Flujo Total: ", flujo_total/T)

#guardar_datos(cantidad_carros, densidad, densidad_aproximada/T, flujo_total/T)

if (intervalo_snapshot != 0) and (len(snapshots) > 0):

	fig, ax = plt.subplots(figsize=(10,2))

	linea = ax.imshow(
		[snapshots[0]],
		cmap=colormap,
		aspect="auto",
		interpolation="nearest",
		vmin = 0,
		vmax = v_max
		)

	ax.set_xlabel("posicion")
	ax.set_yticks([])
	ax.set_title("Simulacion")

	def animar(i):
		linea.set_data([snapshots[i]])
		ax.set_title(f"Tiempo: {tiempos_snapshots[i]:.0f} s")
		return [linea]
		
	ani = animation.FuncAnimation(
		fig,
		animar,
		frames=len(snapshots),
		interval=100,
		blit=False
		)

	plt.show()

	plt.imshow(np.array(snapshots[:550]),
			aspect="auto",
			cmap=colormap,
			vmin = 0,
			vmax = v_max
			)
			
	plt.xlabel("Posición")
	plt.ylabel("Tiempo")

	plt.show()

plt.plot(tiempos_velocidades, velocidades)

plt.xlabel("Tiempo")
plt.ylabel("Velocidad")
plt.grid(True)

plt.show()

