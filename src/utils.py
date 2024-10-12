import math, heapq, pygame, time
from shapely.geometry import LineString, Polygon

# Returns new (image, rect)
def rescale_to_rect(img, rect=None, size=130):
    if not rect:
        rect = pygame.Rect(0,0,size,size)
    image_width, image_height = img.get_size()
    if image_width > size or image_height > size:
        scale_w = rect.width / image_width
        scale_h = rect.height / image_height
        scale = min(scale_w, scale_h)  # Elegir la escala más pequeña para mantener la relación de aspecto
        # Calcular el nuevo tamaño de la imagen
        new_size = (int(image_width * scale), int(image_height * scale))
        # Redimensionar la imagen
        img = pygame.transform.scale(img, new_size)
    return img, img.get_rect(center=rect.center)

#-------------------------

def euclidean_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def distance_point_line(x, y, p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    n = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
    d = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
    return n/d

def point_near_polygon(px, py, polygon, umbral=10):
    n = len(polygon)
    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        if distance_point_line(px, py, p1, p2) <= umbral:
            return i
    return None

def point_inside_polygon(point, polygon):
    x, y = point
    inside = False
    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]
        if (p1[1] > y) != (p2[1] > y) and (x < (p2[0] - p1[0]) * (y - p1[1]) / (p2[1] - p1[1]) + p1[0]):
            inside = not inside
    return inside

# PATH GENERATION

def line_inside_polygon(l, p):
    line = LineString(l)
    polygon = Polygon(p)
    if line.intersects(polygon):
        intersection = line.intersection(polygon)
        if not polygon.boundary.contains(intersection):
            return True
    return False

def line_outside_polygon(l, p):
    line = LineString(l)
    polygon = Polygon(p)
    if line.intersects(polygon):
        intersection = line.intersection(polygon)
        outside_part = line.difference(intersection)
        if not outside_part.is_empty:
            return True
    return False

def is_valid_line(l, wa, fas):
    for poly in wa:
        if line_outside_polygon(l,poly):
            return False
    for poly in fas:
        if line_inside_polygon(l, poly):
            return False
    return True

def add_point_to_graph(graph,point,wa,fas):
    graph[point] = {}
    for p in graph:
        if is_valid_line((point, p), wa, fas):
            distance = euclidean_distance(point, p)
            graph[point][p] = distance
            graph[p][point] = distance
    return graph

def create_walkable_graph(wa, fas):
    graph = {}
    for poly in wa+fas:
        for p in poly:
            graph = add_point_to_graph(graph,tuple(p),wa,fas)
    return graph

def calculate_path(start_pos, end_pos, graph, wa, fas):
    graph = add_point_to_graph(graph,start_pos,wa,fas)
    graph = add_point_to_graph(graph, end_pos, wa, fas)
    # Dijkstra
    queue = [(0, start_pos)]
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start_pos] = 0
    shortest_path = {vertex: None for vertex in graph}
    while queue:
        current_distance, current_vertex = heapq.heappop(queue)
        # If the popped vertex is the end point, we're done
        if current_vertex == end_pos:
            break
        if current_distance > distances[current_vertex]:
            continue
        # Explore neighbors
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
                shortest_path[neighbor] = current_vertex

    # If we never reached the 'end' node, return None (no path found)
    if distances[end_pos] == float('infinity'):
        return None
    # Reconstruct the shortest path
    path = []
    while end_pos is not None:
        path.append(end_pos)
        end_pos = shortest_path[end_pos]
    path.reverse()
    return path