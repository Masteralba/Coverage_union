from polygon import *

'''
todo:
В данный момент не работает сценарий, в котором одна фигура поглощена другой, с этим что-то надо делать, но не
сейчас
Также на данный момент численные ошибки играют большую роль
'''


class HullPoint:

    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.c = c
        self.angle = None

    def __str__(self):
        return f"{self.x} {self.y} {self.angle}"


def point_cmp(a: HullPoint, b: HullPoint) -> HullPoint:
    if a is None:
        return b
    if b is None:
        return a

    if a.x < b.x:
        return a
    if a.x > b.x:
        return b

    if a.y < b.y:
        return a
    return b


def build_point_list(A: Polygon, id: int, storage: list[HullPoint]) -> HullPoint:
    selected = None
    cur = A.c.root
    f = 0
    while cur != A.c.root or f == 0:
        cur_p = HullPoint(cur.x, cur.y, id)
        storage.append(cur_p)
        selected = point_cmp(selected, cur_p)
        cur = cur.next
        f = 1

    return selected


def compute_angles(storage: list[HullPoint], selected: HullPoint):
    for x in storage:
        d = ((selected.x - x.x) ** 2 + (selected.y - x.y) ** 2) ** 0.5
        if d == 0:
            continue
        x.angle = (x.y - selected.y) / d


def orientation(a, b, c):
    val = (a.x * (b.y - c.y)) + \
          (b.x * (c.y - a.y)) + \
          (c.x * (a.y - b.y))
    if val < 0:
        return -1  # Clockwise
    elif val > 0:
        return 1  # Counter-clockwise
    return 0  # Collinear


def build_convex_hull(A: Polygon, B: Polygon) -> Polygon | None:
    """
    Строим и обрабатываем выпуклую оболочку двух многоугольников, пока что существует проблема:
    если выпуклая оболочка не содержит точек второго многоугольника, то результат алгоритма
    гарантированно оказывается неверным!!!
    :param A: Первый многоугольник
    :param B: Второй многоугольник
    :return:
    """
    storage = []
    selected = point_cmp(build_point_list(A, 0, storage), build_point_list(B, 1, storage))
    storage.remove(selected)
    compute_angles(storage, selected)
    storage = sorted(storage, key=lambda p: (
        p.angle,
        -((p.x - selected.x) ** 2 + (p.y - selected.y) ** 2)
    ),
                     reverse=True)
    hull = [selected]
    for x in storage:
        while len(hull) > 1 and orientation(x, hull[-1], hull[-2]) != 1:
            hull.pop(-1)
        hull.append(x)
    print([str(x) for x in hull])
    return Polygon(Outline(poly_walk(A, B, hull)), [])


def find_point(A: Polygon, point: HullPoint) -> Node | None:
    f = 1
    cur = A.c.root
    while cur != A.c.root or f == 1:
        if cur.x == point.x and cur.y == point.y:
            return cur

        cur = cur.next
        f = 0
    return None


def poly_walk(A: Polygon, B: Polygon, hull: list[HullPoint]) -> list:
    selected = hull[0]
    sel_node = find_point(A, selected)

    if sel_node is None:
        sel_node = find_point(B, selected)

    point_list = []
    f = 1
    i = 0
    while i != 0 or f == 1:
        point_list.append((hull[i].x, hull[i].y))

        if hull[(i + 1) % len(hull)].c != hull[i].c:
            i += 1
            i %= len(hull)
            sel_node = find_point(A, hull[i])
            if sel_node is None:
                sel_node = find_point(B, hull[i])
        else:
            sel_node = sel_node.next
            while sel_node.x != hull[(i + 1) % len(hull)].x or sel_node.y != hull[(i + 1) % len(hull)].y:
                point_list.append((sel_node.x, sel_node.y))
                sel_node = sel_node.next
            i += 1
            i %= len(hull)

        f = 0
    return point_list
