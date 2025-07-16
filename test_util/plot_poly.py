import matplotlib.pyplot as plt
import numpy as np


def plot_polygon(polygons, ax=None, show=True, show_direction=True):
    """
    Визуализирует один или несколько многоугольников с помощью matplotlib.

    Параметры:
    polygons (Polygon или list[Polygon]): Один многоугольник или список многоугольников
    ax (matplotlib.axes.Axes): Оси для отрисовки. Если None, создаются новые.
    show (bool): Показывать график сразу после отрисовки (по умолчанию True)
    show_direction (bool): Показывать направление сегментов стрелками (по умолчанию True)
    """
    if not isinstance(polygons, list):
        polygons = [polygons]

    if ax is None:
        ax = plt.gca()

    # Генерация уникальных цветов для каждого многоугольника
    colors = plt.cm.tab10(np.linspace(0, 1, len(polygons)))

    def collect_points(outline):
        """Собирает точки контура в список кортежей (x, y)."""
        points = []
        if outline is None or outline.root is None:
            return points

        current = outline.root
        while True:
            points.append((current.x, current.y))
            current = current.next
            if current == outline.root or current is None:
                break
        return points

    for i, polygon in enumerate(polygons):
        color = colors[i]

        # Собираем точки внешнего контура
        outer_points = collect_points(polygon.c)

        # Рисуем внешний контур
        if outer_points:
            x_outer = [p[0] for p in outer_points]
            y_outer = [p[1] for p in outer_points]
            x_outer.append(outer_points[0][0])  # Замыкаем контур
            y_outer.append(outer_points[0][1])

            # Отрисовка линий контура
            line, = ax.plot(x_outer, y_outer, '-', color=color, linewidth=2,
                            label=f'Polygon {i + 1} (outer)')

            # Отрисовка стрелок направления
            if show_direction:
                # Рассчитываем положение стрелок (каждый N-ый сегмент)
                arrow_step = max(1, len(outer_points) // 5)
                for j in range(0, len(outer_points), arrow_step):
                    # Начало и конец сегмента
                    x_start, y_start = outer_points[j]
                    next_idx = (j + 1) % len(outer_points)
                    x_end, y_end = outer_points[next_idx]

                    # Пропускаем нулевые сегменты
                    if (x_start, y_start) == (x_end, y_end):
                        continue

                    # Рассчитываем положение стрелки (75% от начала к концу)
                    arrow_pos = 0.75
                    x_arrow = x_start + arrow_pos * (x_end - x_start)
                    y_arrow = y_start + arrow_pos * (y_end - y_start)

                    # Рассчитываем длину сегмента для масштабирования стрелки
                    segment_length = np.sqrt((x_end - x_start) ** 2 + (y_end - y_start) ** 2)
                    arrow_size = min(0.1, segment_length * 0.3)  # Размер стрелки

                    # Рисуем стрелку
                    ax.annotate('',
                                xy=(x_end, y_end),
                                xytext=(x_arrow, y_arrow),
                                arrowprops=dict(arrowstyle='->',
                                                color=color,
                                                lw=1,
                                                shrinkA=0,
                                                shrinkB=0,
                                                mutation_scale=15))

        # Рисуем дырки
        for j, hole in enumerate(polygon.holes):
            hole_points = collect_points(hole)
            if hole_points:
                x_hole = [p[0] for p in hole_points]
                y_hole = [p[1] for p in hole_points]
                x_hole.append(hole_points[0][0])  # Замыкаем контур
                y_hole.append(hole_points[0][1])

                # Отрисовка линий отверстий
                ax.plot(x_hole, y_hole, '--', color=color, linewidth=1.5,
                        label=f'Polygon {i + 1} hole {j + 1}' if j == 0 else "")

                # Отрисовка стрелок направления для отверстий
                if show_direction:
                    arrow_step = max(1, len(hole_points) // 3)
                    for k in range(0, len(hole_points), arrow_step):
                        # Начало и конец сегмента
                        x_start, y_start = hole_points[k]
                        next_idx = (k + 1) % len(hole_points)
                        x_end, y_end = hole_points[next_idx]

                        # Пропускаем нулевые сегменты
                        if (x_start, y_start) == (x_end, y_end):
                            continue

                        # Рассчитываем положение стрелки (75% от начала к концу)
                        arrow_pos = 0.75
                        x_arrow = x_start + arrow_pos * (x_end - x_start)
                        y_arrow = y_start + arrow_pos * (y_end - y_start)

                        # Рассчитываем длину сегмента для масштабирования стрелки
                        segment_length = np.sqrt((x_end - x_start) ** 2 + (y_end - y_start) ** 2)
                        arrow_size = min(0.1, segment_length * 0.3)  # Размер стрелки

                        # Рисуем стрелку
                        ax.annotate('',
                                    xy=(x_end, y_end),
                                    xytext=(x_arrow, y_arrow),
                                    arrowprops=dict(arrowstyle='->',
                                                    color=color,
                                                    lw=1,
                                                    shrinkA=0,
                                                    shrinkB=0,
                                                    mutation_scale=15))

    # Настройки осей
    ax.axis('equal')
    ax.grid(False)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Polygons Visualization')

    # Добавляем легенду, если есть что показывать
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(handles, labels)

    # Автоматическое масштабирование
    ax.autoscale_view()

    if show:
        plt.show()