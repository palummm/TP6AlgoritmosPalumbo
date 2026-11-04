from typing import Any, Optional
from Estructuras import List, Queue, Stack, HeapMin, Graph

def extraer_camino_dijkstra(grafo, origen, destino):
    if not grafo.exist_path(origen, destino):
        return float('inf'), []
    
    paths = grafo.dijkstra(origen)
    destino_actual = destino
    peso_total = None
    camino_completo = []

    while paths.size() > 0:
        value = paths.pop()
        if value[0] == destino_actual:
            if peso_total is None:
                peso_total = value[1]
            camino_completo.append(value[0])
            destino_actual = value[2]
            
    camino_completo.reverse()
    return peso_total, camino_completo

casa = Graph(is_dir=False)

ambientes = [
    'Cocina', 'Comedor', 'Cochera', 'Quincho', 
    'Baño 1', 'Baño 2', 'Habitación 1', 'Habitación 2', 
    'Sala de estar', 'Terraza', 'Patio'
]

for ambiente in ambientes:
    casa.add_vertex(ambiente)

distancias = [ 
    (3, 'Comedor', 'Cocina'),
    (2, 'Comedor', 'Baño 1'),
    (4, 'Comedor', 'Sala de estar'),
    (5, 'Comedor', 'Habitación 1'),
    (6, 'Comedor', 'Patio'),

    (10, 'Patio', 'Quincho'),
    (4, 'Patio', 'Terraza'),
    (8, 'Patio', 'Cochera'),
    (3, 'Patio', 'Baño 2'),

    (2, 'Cocina', 'Sala de estar'),
    (5, 'Cocina', 'Cochera'),
    
    (3, 'Baño 1', 'Habitación 1'),
    (3, 'Baño 1', 'Habitación 2'),
    
    (5, 'Sala de estar', 'Terraza'),
    (6, 'Sala de estar', 'Habitación 2'),
    
    (4, 'Habitación 1', 'Habitación 2'),
    
    (5, 'Habitación 2', 'Baño 2'),
    
    (6, 'Quincho', 'Terraza'),
    (2, 'Quincho', 'Baño 2'),
    
    (7, 'Terraza', 'Cochera')
]

for peso, origen, destino in distancias:
    casa.add_edge(peso, origen, destino)

print("arbol de expansion minima")
min_tree = casa.kruskal('Comedor') 

metros_totales_cable = 0

print("Conexiones a realizar:")
for edge in min_tree.split(';'):
    if edge:
        origen, destino, peso = edge.split('-')
        metros_totales_cable += int(peso)
        print(f" Conectar {origen} con {destino} -> {peso} metros")

print(f"\n>> Total de cable necesario para toda la casa: {metros_totales_cable} metros.\n")

print("camino mas corto")
origen_cable = 'Habitación 1'
destino_cable = 'Sala de estar'
costo_red, camino_red = extraer_camino_dijkstra(casa, origen_cable, destino_cable)
print(f"Ruta optima desde {origen_cable} hasta {destino_cable}:")
print(" -> ".join(camino_red))
print(f"\n>> Se necesitan {costo_red} metros de cable de red.")