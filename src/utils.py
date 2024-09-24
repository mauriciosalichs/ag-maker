def is_inside_polygon(position, polygon):
    n = len(polygon)
    inside = False
    px, py = position
    for i in range(n):
        j = (i + 1) % n
        x1, y1 = polygon[i]
        x2, y2 = polygon[j]
        
        if ((y1 > py) != (y2 > py)) and (px < (x2 - x1) * (py - y1) / (y2 - y1) + x1):
            inside = not inside
    return inside
