import math, pygame
from typing import List, Tuple

from shapely.geometry import LineString, Polygon
from shapely import intersection

def euclidean_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

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

def line_intersects_polygon(line, polygon) -> bool:
    (x1, y1), (x2, y2) = line
    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]
        if line_segments_intersect((x1, y1), (x2, y2), p1, p2):
            return True
    return False

def line_segments_intersect(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float], p4: Tuple[float, float]) -> bool:
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    def ccw(A, B, C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

# We asume there is at most one blocking obstacle, and we have to consider walking polygon
def calculate_path(start_pos, end_pos, forb_pols):
    for polygon_coords in forb_pols:
        line = LineString([start_pos, end_pos])
        polygon = Polygon(polygon_coords)
        int_points = intersection(line, polygon).coords
        if not int_points:
            continue
        px1, py1 = int_points[0]
        px2, py2 = int_points[1]
        i = point_near_polygon(px1, py1, polygon_coords, umbral=3)
        j = point_near_polygon(px2, py2, polygon_coords, umbral=3)
        res = polygon_coords[i+1:j+1] if i < j else polygon_coords[i:j:-1]
        return [start_pos,int_points[0]] + res + [int_points[1],end_pos]
    return [start_pos,end_pos]