#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <omp.h>
#include <random>

// 

// Compilar:
// g++ -O3 -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) -fopenmp funciones.cpp -o flujovial$(python3-config --extension-suffix)

bool evento_cpp(){

	std::random_device rd;
	std::mt19937 gen(rd());
	
	std::uniform_real_distribution<double> distrib(0.0, 1.0);
	
	double numero = distrib(gen);
	
	return numero < 0.5;
}

int contar_distancia_cpp(int celda, std::vector<int>& carretera){

	int distancia = 0;
	
	int n = carretera.size();
	
	for(int espacio = 1; espacio < n; espacio++){
	
		int siguiente = (celda + espacio) % n;
		
		if(carretera[siguiente] == 0){
		
			distancia++;	
		}
		else{
		
			break;
		}
	}
	
	return distancia;
}

















