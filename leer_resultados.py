import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def limpiar_csv(carpeta="resultados"):
	
	datos = []
	
	for nombre in os.listdir(carpeta):
		if nombre.endswith(".csv"):
		
			ruta = os.path.join(carpeta, nombre)
			
			df = pd.read_csv(ruta)
			
			df = df[df["cantidad_carros"] != "cantidad_carros"]
			
			df["cantidad_carros"] = pd.to_numeric(df["cantidad_carros"])
			df["densidad_real"] = pd.to_numeric(df["densidad_real"])
			df["densidad_aproximada"] = pd.to_numeric(df["densidad_aproximada"])
			df["flujo_promedio"] = pd.to_numeric(df["flujo_promedio"])
            		
			df.to_csv(ruta, index=False)
			
			datos.append(df)
	
	return datos
            		
datos = limpiar_csv()

df = pd.concat(datos, ignore_index=True)
df = df.sort_values("densidad_real")

densidad_real = df["densidad_real"].tolist()
flujo_promedio = df["flujo_promedio"].tolist()

plt.scatter(densidad_real, flujo_promedio)

plt.xlabel("Densidad Real")
plt.ylabel("Flujo Promedio")
plt.show()
