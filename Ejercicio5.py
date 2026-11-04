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
red = Graph(is_dir=False)

nodos_info = [
    ('Red Hat', 'notebook'), ('Debian', 'notebook'), ('Arch', 'notebook'),
    ('Ubuntu', 'pc'), ('Mint', 'pc'), ('Manjaro', 'pc'), 
    ('Parrot', 'pc'), ('Fedora', 'pc'),
    ('Guaraní', 'servidor'), ('MongoDB', 'servidor'),
    ('Impresora', 'impresora'),
    ('Router 1', 'router'), ('Router 2', 'router'), ('Router 3', 'router'),
    ('Switch 1', 'switch'), ('Switch 2', 'switch')
]

for nombre, tipo in nodos_info:
    red.add_vertex(nombre, tipo)

aristas_info = [
    (25, 'Red Hat', 'Router 2'), (9, 'Guaraní', 'Router 2'),
    (37, 'Router 2', 'Router 1'), (50, 'Router 2', 'Router 3'),
    (43, 'Router 1', 'Router 3'), (29, 'Router 1', 'Switch 1'),
    (61, 'Router 3', 'Switch 2'),
    (17, 'Switch 1', 'Debian'), (18, 'Switch 1', 'Ubuntu'),
    (22, 'Switch 1', 'Impresora'), (80, 'Switch 1', 'Mint'),
    (40, 'Switch 2', 'Manjaro'), (12, 'Switch 2', 'Parrot'),
    (5, 'Switch 2', 'MongoDB'), (56, 'Switch 2', 'Arch'),
    (3, 'Switch 2', 'Fedora')
]

for peso, origen, destino in aristas_info:
    red.add_edge(peso, origen, destino)

print("Barridos en Profundidad y Amplitud")
notebooks = ['Red Hat', 'Debian', 'Arch']
for nb in notebooks:
    print(f"\n> barrido en profundidad desde {nb}:")
    red.deep_show(nb)
    print(f"\n> barrido en amplitud desde {nb}:")
    red.amplitude_show(nb)

print("Camino mas corto hacia la Impresora")
origenes_impresion = ['Manjaro', 'Red Hat', 'Fedora']
for pc in origenes_impresion:
    costo, camino = extraer_camino_dijkstra(red, pc, 'Impresora')
    print(f"Desde {pc} a Impresora: {' -> '.join(camino)} (Costo: {costo})")

print("arbol de expansion minima")
min_tree = red.kruskal('Router 1')
print("Bosque resultante:")
for edge in min_tree.split(';'):
    print(edge)

print("PC con camino mas corto a Guarani")
pcs = ['Ubuntu', 'Mint', 'Manjaro', 'Parrot', 'Fedora']
mejor_pc = None
min_costo = float('inf')

for pc in pcs:
    costo, camino = extraer_camino_dijkstra(red, pc, 'Guaraní')
    if costo < min_costo:
        min_costo = costo
        mejor_pc = pc
print(f"La pc con el camino mas corto a Guarani es '{mejor_pc}' con un costo de {min_costo}")

print("Computadora de Switch 1 mas cercana a MongoDB")
comps_sw1 = ['Debian', 'Ubuntu', 'Mint']
mejor_comp_sw1 = None
min_costo_sw1 = float('inf')

for comp in comps_sw1:
    costo, camino = extraer_camino_dijkstra(red, comp, 'MongoDB')
    if costo < min_costo_sw1:
        min_costo_sw1 = costo
        mejor_comp_sw1 = comp
print(f"La computadora del Switch 1 mas cercana a MongoDB es '{mejor_comp_sw1}' con un costo de {min_costo_sw1}.")

print("Cambio de impresora a Router 2 y ejecutar punto B")
red.delete_edge('Switch 1', 'impresora')
red.add_edge(22, 'Router 2', 'impresora') 

for nb in notebooks:
    print(f"\n> nuevo barrido en profundidad desde {nb}:")
    red.deep_show(nb)
    print(f"\n> nuevo barrido en amplitud desde {nb}:")
    red.amplitude_show(nb)