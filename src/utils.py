import math, pygame

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

def reverse_path(original_list, sublist):
    # Get the indices of the start and end of the sublist in the original list
    start_index = original_list.index(sublist[0])
    end_index = original_list.index(sublist[-1])
    # Create the reverse path outside of the sublist
    reverse_path = []
    # Check if the sublist goes forward or backward
    if (start_index < end_index) or (start_index == len(original_list) - 1 and end_index == 0):
        # The sublist is in forward order, go backwards in the list
        i = (start_index - 1) % len(original_list)
        while i != end_index:
            reverse_path.append(original_list[i])
            i = (i - 1) % len(original_list)
    else:
        # The sublist is in reverse order, go forwards in the list
        i = (start_index + 1) % len(original_list)
        while i != end_index:
            reverse_path.append(original_list[i])
            i = (i + 1) % len(original_list)
    return reverse_path

def euclidean_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def total_length(points):
    total = 0
    for i in range(len(points) - 1):
        total += euclidean_distance(points[i], points[i + 1])
    return total

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

def line_intersection(p1, p2, p3, p4):
    x1,y1 = p1
    x2,y2 = p2
    x3,y3 = p3
    x4,y4 = p4
    denom = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
    if denom == 0: # parallel
        return None
    ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denom
    if ua < 0 or ua > 1: # out of range
        return None
    ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denom
    if ub < 0 or ub > 1: # out of range
        return None
    x = x1 + ua * (x2-x1)
    y = y1 + ua * (y2-y1)
    return (x,y)

def line_intersects_poly(line, polygon):
    ii = []
    l1, l2 = line
    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]
        if line_intersection(l1, l2, p1, p2):
            ii.append(i)
    return ii

# TODO: This needs A LOT of improvement
def calculate_path(start_pos, end_pos, forb_pols):
    intersected_polygon = None
    for polygon_coords in forb_pols:
        ii = line_intersects_poly((start_pos, end_pos), polygon_coords)
        if len(ii) == 0:
            continue
        if intersected_polygon:
            return None
        # int_points = [polygon_coords[ii[0]],polygon_coords[ii[-1]]]
        intersected_polygon = (ii[0], ii[1], polygon_coords)
    if intersected_polygon:
        (p0, p1, polygon_coords) = intersected_polygon
        reverse = euclidean_distance(start_pos, polygon_coords[p0]) < \
                  euclidean_distance(start_pos, polygon_coords[p1])
        res = polygon_coords[p0:p1] if reverse else polygon_coords[p1:p0:-1]
        path1 = [start_pos] + res + [end_pos]
        path2 = [start_pos] + reverse_path(polygon_coords,res) + [end_pos]
        if total_length(path1) > total_length(path2):
            return path2
        else:
            return path1
    return [start_pos,end_pos]