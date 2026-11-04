from typing import Any, Optional
from copy import copy

class List(list):
    __CRITERION_FUNCTION = {}
    
    def add_criterion(self, criterion_key: str, criterion_function) -> None:
        self.__CRITERION_FUNCTION[criterion_key] = criterion_function
    
    def search(self, search_value: Any, criterion: str = None) -> Optional[int]:
        self.sort_by_criterion(key_criterion=criterion)
        search_criterion = self.__CRITERION_FUNCTION.get(criterion)

        start = 0
        end = len(self) -1
        middle = (start + end) // 2

        while start <= end:
            if search_criterion is None and not isinstance(self[0], (bool, int, float, str)):
                print('no se pudo determinar criterio de busqueda')
                return None

            value = search_criterion(self[middle]) if search_criterion else self[middle]

            if value == search_value:
                return middle
            elif value < search_value:
                start = middle + 1
            else:
                end = middle -1
            
            middle = (start + end) // 2
    
    def delete_value(self, value, criterion=None) -> Optional[Any]:
        index = self.search(value, criterion)
        return self.pop(index) if index is not None else None

    def sort_by_criterion(self, key_criterion=None) -> None:
        sort_criterion = self.__CRITERION_FUNCTION.get(key_criterion)

        if sort_criterion:
            self.sort(key=sort_criterion)
        elif self and isinstance(self[0], (bool, int, float, str)):
            self.sort()
        else:
            print('no se puede ordenar la lista no se como se debe ordenar')

class Queue:
    def __init__(self):
        self.__elements = []

    def arrive(self, value: Any) -> None: 
        self.__elements.append(value)

    def attention(self) -> Any:
        return self.__elements.pop(0)

    def size(self) -> int:
        return len(self.__elements)

class Stack:
    def __init__(self):
        self.__elements = []

    def push(self, value: Any) -> None:
        self.__elements.append(value)

    def pop(self) -> Any:
        return self.__elements.pop()
        
    def size(self) -> int:
        return len(self.__elements)

class HeapMin():
    def __init__(self):
        self.elements = []

    def add_element(self, value: Any) -> None:
        self.elements.append(value)
        self.float(self.size()-1)

    def delete_element(self) -> Any:
        self.elements[0], self.elements[-1] = self.elements[-1], self.elements[0]
        value = self.elements.pop()
        self.sink(0)
        return value

    def size(self) -> int:
        return len(self.elements)

    def float(self, index) -> None:
        while index > 0 and self.elements[index] < self.elements[(index -1) // 2]:
            father = (index -1) // 2
            self.elements[index], self.elements[father] = self.elements[father], self.elements[index]
            index = father

    def sink(self, index) -> None:
        left = (index * 2) + 1
        control = True
        while control and left < self.size():
            right =  (index * 2) + 2
            min = left
            if right < self.size():
                min = min if self.elements[min] < self.elements[right] else right

            if self.elements[index] > self.elements[min]:
                self.elements[index], self.elements[min] = self.elements[min], self.elements[index]
                index = min
                left = (index * 2) + 1
            else:
                control = False

    def arrive(self, value, priority) -> None:
        self.add_element([priority, value])

    def search(self, value):
        for index, element in enumerate(self.elements):
            if element[1][0] == value:
                return index

    def attention(self) -> Any:
        result = None
        if self.size() > 0:
            result = self.delete_element()
        return result

    def change_priority(self, index, new_priority):
        if index < len(self.elements):
            previous_priority = self.elements[index][0]
            self.elements[index][0] = new_priority
            if new_priority > previous_priority:
                self.sink(index)
            elif new_priority < previous_priority:
                self.float(index)

class Graph(List):
    class _nodeVertex():
        def __init__(self, value, other_values=None):
            self.value = value
            self.other_values = other_values
            self.edges = List()
            self.visited = False

            def _sort_by_destination(item):
                return item.destination

            self.edges.add_criterion('destination', _sort_by_destination)

        def __str__(self):
            return f"{self.value}"

    class _nodeEdge():
        def __init__(self, weight, destination):
            self.weight = weight
            self.destination = destination

    def __init__(self, is_dir=True):
        self.is_dir = is_dir

        def sort_by_value(item):
            return item.value
        self.add_criterion('value', sort_by_value)

    def add_vertex(self, value: Any, other_values: Any = None) -> None:
        node_vertex = self._nodeVertex(value, other_values)
        self.append(node_vertex)

    def add_edge(self, weight: Any, origin: Any, destination: Any) -> None:
        pos_origin = self.search(origin, 'value')
        if pos_origin is None:
            return

        pos_destination = self.search(destination, 'value')
        if pos_destination is None:
            return

        node_edge = self._nodeEdge(weight, destination)
        self[pos_origin].edges.append(node_edge)

        if origin != destination and not self.is_dir:
            node_edge = self._nodeEdge(weight, origin)
            self[pos_destination].edges.append(node_edge)

    def delete_edge(self, origin, destination) -> Optional[Any]:
        pos_origin = self.search(origin, 'value')
        if pos_origin is None:
            return

        result  = self[pos_origin].edges.delete_value(destination, 'destination')

        if not self.is_dir:
            pos_destination = self.search(destination, 'value')
            if pos_destination is not None:
                self[pos_destination].edges.delete_value(origin, 'destination')
        return result

    def deep_show(self, origin) -> None:
        def _deep_show(origin) -> None:
            pos_origin = self.search(origin, 'value')
            if pos_origin is not None:
                visited = self[pos_origin].visited
                if not visited:
                    self[pos_origin].visited = True
                    print(self[pos_origin].value)
                    edges = self[pos_origin].edges
                    for edge in edges:
                        _deep_show(edge.destination)

        for vertex in self:
            vertex.visited = False
        _deep_show(origin)

    def amplitude_show(self, origin) -> None:
        for vertex in self:
            vertex.visited = False
    
        pending_queue = Queue()
        pos_origin = self.search(origin, 'value')
        if pos_origin is not None:
            visited = self[pos_origin].visited
            if not visited:
                pending_queue.arrive(self[pos_origin])
                while pending_queue.size() > 0:
                    vertex = pending_queue.attention()
                    if not vertex.visited:
                        vertex.visited = True
                        print(vertex.value)
                        edges = vertex.edges
                        for edge in edges:
                            pos_next_vertex = self.search(edge.destination, 'value')
                            pending_queue.arrive(self[pos_next_vertex])

    def dijkstra(self, origin):
        from math import inf
        no_visited = HeapMin()
        path = Stack()
        
        for vertex in self:
            distance = 0 if vertex.value == origin else inf
            no_visited.arrive([vertex.value, vertex, None], distance)

        while no_visited.size() > 0:
            vertex = no_visited.attention()
            costo_nodo_actual = vertex[0]
            path.push([vertex[1][0], costo_nodo_actual, vertex[1][2]])
            edges = vertex[1][1].edges
            for edge in edges:
                pos = no_visited.search(edge.destination)
                if pos is not None:
                    if costo_nodo_actual + edge.weight < no_visited.elements[pos][0]:
                        no_visited.elements[pos][1][2] = vertex[1][0]
                        no_visited.change_priority(pos, costo_nodo_actual + edge.weight)
        return path                    

    def kruskal(self, origin_vertex):
        def search_in_forest(forest, value):
            for index, tree in enumerate(forest):
                if value in tree:
                    return index
                
        forest = []
        edges = HeapMin()
        for vertex in self:
            forest.append(vertex.value)
            for edge in vertex.edges:
                edges.arrive([vertex.value, edge.destination], edge.weight)
        
        while len(forest) > 1 and edges.size() > 0:
            edge = edges.attention()
            origin = search_in_forest(forest, edge[1][0])
            destination = search_in_forest(forest, edge[1][1])
            if origin is not None and destination is not None:
                if origin != destination:
                    if origin > destination:
                        vertex_origin = forest.pop(origin)
                        vertex_destination = forest.pop(destination)
                    else:
                        vertex_destination = forest.pop(destination)
                        vertex_origin = forest.pop(origin)

                    if '-' not in vertex_origin and '-' not in vertex_destination:
                        forest.append(f'{vertex_origin}-{vertex_destination}-{edge[0]}')
                    elif '-' not in vertex_destination:
                        forest.append(vertex_origin+';'+f'{edge[1][0]}-{vertex_destination}-{edge[0]}')
                    elif '-' not in vertex_origin:
                        forest.append(vertex_destination+';'+f'{vertex_origin}-{edge[1][1]}-{edge[0]}')
                    else:
                        forest.append(vertex_origin+';'+vertex_destination+';'+f'{edge[1][0]}-{edge[1][1]}-{edge[0]}')
        
        from_vertex = search_in_forest(forest, origin_vertex)
        return forest[from_vertex] if from_vertex is not None else forest

    def exist_path(self, origin, destination):
        def __exist_path(graph, origin, destination):
            result = False
            vertex_pos = graph.search(origin, 'value')
            if vertex_pos is not None:
                if not graph[vertex_pos].visited:
                    graph[vertex_pos].visited = True
                    if graph[vertex_pos].value == destination:
                        return True
                    else:
                        for edge in graph[vertex_pos].edges:
                            destination_edge_pos = graph.search(edge.destination, 'value')
                            if not graph[destination_edge_pos].visited:
                                result = __exist_path(graph, graph[destination_edge_pos].value, destination)
                                if result:
                                    break
            return result

        for vertex in self:
            vertex.visited = False

        result = __exist_path(self, origin, destination)
        return result