import convex_hull
import union
import polygon
import math
import test_util.plot_poly as plt


def poly_builder(l: list) -> polygon.Polygon:
    return polygon.Polygon(polygon.Outline(l), [])


def generate_regular_polygon(n, r, x, y, start_angle=0):
    """
    Генерирует вершины правильного n-угольника, вписанного в круг радиуса r.

    Параметры:
    n (int): Количество сторон многоугольника
    r (float): Радиус описанной окружности
    x (float): X-координата центра
    y (float): Y-координата центра
    start_angle (float): Начальный угол в радианах (по умолчанию 0)

    Возвращает:
    list: Список вершин многоугольника в порядке обхода по часовой стрелке
    """
    vertices = []
    # Шаг угла между вершинами (в радианах)
    angle_step = 2 * math.pi / n

    for i in range(n):
        # Угол для текущей вершины (по часовой стрелке)
        angle = start_angle - i * angle_step
        # Вычисление координат вершины
        vertex_x = x + r * math.cos(angle)
        vertex_y = y + r * math.sin(angle)
        vertices.append((vertex_x, vertex_y))

    return vertices


def test1s_disj(n):
    """
    Большие пилы, тест по количество зубцов - n.

    ----

    **Отчет:** адекватно и быстро работает на значенияз порядка 100000, большие значения вызывают
    численные ошибки, поэтому выпуклая оболочка не строится корректно, а ее постобработка уходит в бесконечный
    цикл, вероятно всего из-за некорректной структуры оболочки

    **Проблема:** неустойчивость в численным ошибкам, в случае большого количества близких углов

    **Решение:** использование численно устойчивых методов для сортировки по углам, не считать углы (их триг функции)

    ----

    """
    A = [(0, 0)]
    B = [(3, 0)]
    for i in range(1, n + 1):
        A.append((1, 2 * i - 1))
        A.append((0, 2 * i))
    A.append((2, 2 * n))
    A.append((2, 0))

    for i in range(1, n + 1):
        B.append((4, 2 * i - 1))
        B.append((3, 2 * i))
    B.append((5, 2 * n))
    B.append((5, 0))

    return poly_builder(A), poly_builder(B)


def test2s_disj(n):
    """
    Большие правильные многоугольники, в разных центральных точках
    """
    return (poly_builder(generate_regular_polygon(n, 140, 0, 0)),
            poly_builder(generate_regular_polygon(n, 140, 300, 300)))


def test1s_inter(n):
    """
    По классике правильные многоугольники
    """
    return (poly_builder(generate_regular_polygon(n, 140, 50, 0)),
            poly_builder(generate_regular_polygon(n, 140, 100.2, 100.2)))


sample = list(test1s_inter(1000))
plt.plot_polygon(sample)
plt.plot_polygon(union.union(sample[0], sample[1]))
