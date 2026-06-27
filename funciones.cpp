#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <vector>
#include <omp.h>
#include <random>

// Compilar:
// g++ -O3 -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) -fopenmp funciones.cpp -o trafico$(python3-config --extension-suffix)

namespace py = pybind11;

int v(int velocidad){

	int vel = velocidad - 1;
	return vel;
}

int contar_distancia_cpp(int celda, int* carretera, int n){

	int distancia = 0;
	
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

int actualizar(py::array_t<int> carretera_py, int v_max, double p, int medicion, int hilos){

	py::buffer_info carretera_b = carretera_py.request();
	int* carretera = static_cast<int*>(carretera_b.ptr);
	
	int n = carretera_py.size();
	
	std::vector<std::pair<int, int>> carros;
	
	for (int i = 0; i < n; i++){
		if (carretera[i] != 0){
		
			carros.push_back({i, carretera[i]});
		}
	}
	
	#pragma omp parallel num_threads(hilos)
	{
		std::random_device rd;
		int tid = omp_get_thread_num();
	
		std::mt19937 gen(rd() + tid);
		std::uniform_real_distribution<double> distrib(0.0, 1.0);
	
	
		#pragma omp for
		for (std::pair<int, int>& carro : carros){
		
			int i = carro.first;
			int velocidad = v(carro.second);
	
			int distancia = contar_distancia_cpp(i, carretera, n);
		
			if ((velocidad < v(v_max)) && (distancia > velocidad)){
			
				velocidad++;
			}
		
			if (distancia <= velocidad){
		
				velocidad = distancia;
			}
		
			if ((distrib(gen) < p) && (velocidad > 0)){
		
				velocidad--;
			}
		
			carro.second = velocidad + 1;
		}
	}
	
	std::vector<int> nueva_carretera(n, 0);
	int flujo_instantaneo = 0;
	
	for (std::pair<int, int>& carro : carros){
	
		int i = carro.first;
		int velocidad = v(carro.second);
		
		int nuevo_indice = (i + velocidad) % n;
		
		if (velocidad > 0){
			for (int espacio = 1; espacio <= velocidad; espacio++){
			
				int posicion = (i + espacio) % n;
				
				if (posicion == medicion){
					
					flujo_instantaneo++;
				}
			}
		}
		
		nueva_carretera[nuevo_indice] = carro.second;
	}
	
	for (int i = 0; i < n; i++){
	
		carretera[i] = nueva_carretera[i];
	}
	
	
	return flujo_instantaneo;	
}

PYBIND11_MODULE(trafico, m){
	
	m.doc() = "Actualización de datos de carros en flujo vial.";
	
	m.def("actualizar", &actualizar, "Actualizar la carretera y el flujo instantaneo.");
}
















