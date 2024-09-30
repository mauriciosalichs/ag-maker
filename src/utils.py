import math, pygame
from typing import List, Tuple


# Returns new (image, rect)
def rescale_to_rect(img, rect):
    image_width, image_height = img.get_size()
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

def point_inside_polygon(point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
    x, y = point
    inside = False
    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]
        if (p1[1] > y) != (p2[1] > y) and (x < (p2[0] - p1[0]) * (y - p1[1]) / (p2[1] - p1[1]) + p1[0]):
            inside = not inside
    return inside

def line_intersects_polygon(line: Tuple[Tuple[float, float], Tuple[float, float]], polygon: List[Tuple[float, float]]) -> bool:
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

def find_nearest_valid_point(current: Tuple[float, float], target: Tuple[float, float], forbidden: List[List[Tuple[float, float]]], step: float) -> Tuple[float, float]:
    angle = math.atan2(target[1] - current[1], target[0] - current[0])
    for i in range(36):  # Check 36 directions around the current point
        test_angle = angle + i * math.pi / 18  # 20 degrees increment
        new_x = current[0] + step * math.cos(test_angle)
        new_y = current[1] + step * math.sin(test_angle)
        new_point = (new_x, new_y)
        if not any(line_intersects_polygon((current, new_point), poly) for poly in forbidden):
            return new_point
    return current  # If no valid point found, return the current point

def generate_path(start_pos: Tuple[float, float], end_pos: Tuple[float, float], polygon: List[Tuple[float, float]], forbidden: List[List[Tuple[float, float]]]) -> List[Tuple[float, float]]:
    if not point_inside_polygon(start_pos, polygon) or not point_inside_polygon(end_pos, polygon):
        raise ValueError("Start or end position is not inside the polygon.")

    path = [start_pos]
    current_pos = start_pos
    step = 100  # Step size for each iteration
    max_iterations = 1000  # Prevent infinite loops

    for _ in range(max_iterations):
        if math.dist(current_pos, end_pos) < step:
            path.append(end_pos)
            break

        next_pos = find_nearest_valid_point(current_pos, end_pos, forbidden, step)

        if next_pos == current_pos:
            step /= 2  # If stuck, reduce step size
            if step < 0.1:  # If step size becomes too small, we're truly stuck
                break
            continue
        next_pos = [int(n) for n in next_pos]
        path.append(next_pos)
        current_pos = next_pos
    return path

