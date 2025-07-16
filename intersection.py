import polygon
from union import next_non_intersection, find_lines_intersection

def find_intersection(p1: polygon.Polygon, p2: polygon.Polygon):
    current1 = p1.c.root
    current2 = p2.c.root

    # Цикл по всем ребрам двух полигонов
    while (True):
        while (True):

            next1 = next_non_intersection(current1)
            next2 = next_non_intersection(current2)

            intersection = find_lines_intersection(current1, next1, current2, next2)

            # check intersection
            if (intersection[1] > 0 and intersection[1] < 1
                    and intersection[2] > 0 and intersection[2] < 1):
                    return True
        
            current2 = next_non_intersection(current2)

            if current2 != p2.c.root:
                continue
            else:
                 break

        current1 = next_non_intersection(current1)

        if current1 != p1.c.root:
            continue
        else:
            break

    return False