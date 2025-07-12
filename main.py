import shapely
from matplotlib import pyplot as plt
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection
from typing import Union


def plot_polygon(geom: Union[Polygon, MultiPolygon],
                 ax=None,
                 facecolor: str = 'skyblue',
                 edgecolor: str = 'black',
                 alpha: float = 0.7) -> None:

    if ax is None:
        _, ax = plt.subplots()

    # Обработка MultiPolygon
    if geom.geom_type == 'MultiPolygon':
        for poly in geom.geoms:
            x, y = poly.exterior.xy
            ax.fill(x, y, alpha=alpha, fc=facecolor, ec=edgecolor)
    # Обработка Polygon
    elif geom.geom_type == 'Polygon':
        x, y = geom.exterior.xy
        ax.fill(x, y, alpha=alpha, fc=facecolor, ec=edgecolor)
    else:
        raise ValueError("Поддерживаются только Polygon и MultiPolygon")

    ax.set_aspect('equal')
    plt.show()

p1 = Polygon([(0,0), (0,1), (1,0), (0,0)])
p2 = Polygon([(1,1), (1,2), (2,1), (1,1)])
# p2 = Polygon([(1,1), (1,4), (2,2), (4,1), (1,1)]) - контрпример для convexhull
# p2 = Polygon([(1,1), (1,4), (4,1), (2,2), (1,1)]) - контрпример для concavehull
m = MultiPolygon([p1, p2])
# пробуем все функции
plot_polygon(p1.union())
"""
plot_polygon(shapely.union(p1, p2))
plot_polygon(shapely.coverage_union(p1, p2))
plot_polygon(shapely.unary_union([p1,p2]))
plot_polygon(shapely.convex_hull(m))
plot_polygon(shapely.concave_hull(m))
plot_polygon(shapely.disjoint_subset_union(p1, p2))
plot_polygon(shapely.build_area(GeometryCollection([p1, p2])))
plot_polygon(MultiPolygon(shapely.voronoi_polygons(m)))
"""
