import polygon
import test_util.plot_poly as plt
import convex_hull as hull
import union


def poly_builder(l: list) -> polygon.Polygon:
    return polygon.Polygon(polygon.Outline(l), [])


def test1_disj():
    """
    Обычные квадраты, ничего такого
    """
    A = [(0, 0), (0, 1), (1, 1), (1, 0)]
    B = [(2, 2), (2, 3), (3, 3), (3, 2)]
    return poly_builder(A), poly_builder(B)


def test2_disj():
    """
    Сделаем все точки коллениарными, хотя бы попарно
    """
    A = [(0, 0), (0, 1), (1, 0)]
    B = [(2, 0), (0, 2), (0, 3), (3, 0)]
    return poly_builder(A), poly_builder(B)


def test3_disj():
    """
    Теперь будем делать что-то с выпуклостью, пока что базовый тест
    """
    A = [(1, 1), (0, 1), (2, 2), (1, 0)]
    B = [(3, 3), (4, 5), (4, 4), (5, 4)]
    return poly_builder(A), poly_builder(B)


def test4_disj():
    """
    Будем смотреть на то, что будет при сильно вогнутых фигурах
    """
    A = [(-3, 0), (-2, 1), (-2, 2), (-1, 3), (-3, 4), (3, 4), (1, 3), (2, 2), (2, 1), (3, 0)]
    B = [(-3, 5), (-2, 6), (-2, 7), (-1, 8), (-3, 9), (3, 9), (1, 8), (2, 7), (2, 6), (3, 5)]
    return poly_builder(A), poly_builder(B)


def test5_disj():
    """
    Множество точек, в котором будет крайне много самых левых точек, также тут имеем фигуру, которая частично покрыта
    другой
    """
    A = [(0, 0), (0, 1), (3, 4), (0, 7), (0, 8), (4, 4)]
    B = [(0, 2), (0, 3), (1, 4), (0, 5), (0, 6), (2, 4)]
    return poly_builder(A), poly_builder(B)


def test6_disj():
    """
    Пусть один многоугольник полностью окружает другой (это нереально сделать без дырки, но у меня есть
    очень интересная идея на этот счет
    """
    A = [(0, 0), (0, 2), (1, 2), (1, 1), (4, 1), (4, 6), (1, 6), (1, 5), (0, 5), (0, 7), (5, 7), (5, 0)]
    B = [(1, -2), (-2, -2), (-2, 9), (1, 9), (1, 8), (-1, 8), (-1, 4), (3, 4), (3, 3), (-1, 3), (-1, -1), (1, -1)]
    return poly_builder(A), poly_builder(B)


def test7_disj():
    """
    Последний тест, который писал я как живой человек, тут будут пилы
    """
    A = [(0, 0), (1, 1), (0, 2), (1, 3), (0, 4), (1, 5), (3, 5), (2, 4), (3, 3), (2, 2), (3, 1), (2, 0)]
    B = [(0, 0)]
    return poly_builder(A), poly_builder(B)


def test1_inter():
    """
    Проверяем функции глеба, пока что они крайне пососно сделаны, поэтому рыдаем.
    Начнем с квадратиков.
    """
    A = [(0, 0), (0, 2), (2, 2), (2, 0)]
    B = [(1, 1), (1, 3), (3, 3), (3, 1)]
    return poly_builder(A), poly_builder(B)


def test2_inter():
    """
    Делаем так, чтобы была дырка после объединения
    """
    A = [(1, 0), (1, 7), (4, 7), (4, 6), (2, 6), (2, 1), (4, 1), (4, 0)]
    B = [(0, 2), (0, 3), (3, 3), (3, 4), (0, 4), (0, 5), (4, 5), (4, 2)]
    return poly_builder(A), poly_builder(B)


def test3_inter():
    """
    Сделаем много прямо дырочек всяких
    """
    A = [(3, 0), (3, 3), (0, 3), (0, 4), (3, 4), (3, 7), (4, 7), (4, 4), (7, 4), (7, 3), (4, 3), (4, 0)]
    B = [(1, 1), (1, 6), (5, 6), (5, 5), (2, 5), (2, 2), (5, 2), (5, 5), (6, 5), (6, 1)]
    return poly_builder(A), poly_builder(B)


test = list(test2_inter())
plt.plot_polygon(test, None, True)
plt.plot_polygon(union.union(test[0], test[1]))
