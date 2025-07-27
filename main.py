from matplotlib import pyplot as plt
from intersection import find_intersection
import union
import convex_hull
import polygon
from math import sqrt

def poly_builder(l: list) -> polygon.Polygon:
    return polygon.Polygon(polygon.Outline(l), [])

import test_util.plot_poly as plt

def union_n(input: list):

    polygons = [poly_builder(elem) for elem in input]
    f = 1
    
    while f == 1:
        A = None
        B = None
        f = 0
        for x in polygons:
            for y in polygons:
                if x == y:
                    continue
                if find_intersection(x, y):
                    f = 1
                    A = x
                    B = y
                    break
            if f == 1:
                break
        if A == None or B == None:
            continue
        polygons.remove(A)
        polygons.remove(B)
        polygons.append(union.union(A, B))

    if len(polygons) == 1:
        return polygons[0]
    cur = convex_hull.build_convex_hull(polygons[0], polygons[1])
    for i in range(2, len(polygons)):
        cur = convex_hull.build_convex_hull(cur, polygons[i])
    return cur


if __name__ == "__main__":

    p1 = [(0,0), (0, 1), (1, 1)]
    p2 = [(0.9,0.5), (0.5, 1.5), (1.5, 1.5)]
    p3 = [(1.5,1), (1, 2), (2, 2)]
    p4 = [(10, 10), (10, 11), (11, 11)]

    lis = [p1, p2, p3, p4]
    plt.plot_polygon([poly_builder(x) for x in lis])

    plt.plot_polygon(union_n(lis))


#def union_two(p1: polygon.Polygon, p2: polygon.Polygon):
#
#    if find_intersection(p1, p2):
#        return union.union(p1, p2)
#    else:
#        return convex_hull.build_convex_hull(p1, p2)



