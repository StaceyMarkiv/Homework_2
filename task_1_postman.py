import math
from itertools import permutations


def distance(point1, point2):
    # вычисляем расстояние между точками
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    dist_length = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return dist_length


def route_length(route, print_route=False):
    # вычисляем общую длину маршрута
    route_len = 0
    for j in range(len(route)-1):
        distance_between_points = distance(route[j], route[j+1])
        route_len += distance_between_points
        if print_route:
            print('-> ', route[j+1], [route_len], sep='', end=' ')
    return route_len


start = (0,2)
addresses = [(2,5), (5,2), (6,6), (8,3)]
# addresses = [(2,5), (5,2), (6,6), (8,3), (7,3), (3,1), (5,8), (2,4), (7,1)]

routes = list(permutations(addresses))

# вычисляем длины всех возможных маршрутов
routes_lengths = []
for route in routes:
    full_route = (start, *route, start)
    length = route_length(full_route)
    routes_lengths.append(length)

# находим самый оптимальный по длине маршрут
res_length = min(routes_lengths)

# определяем, какому маршруту соответствует эта длина
res_length_ind = routes_lengths.index(res_length)
res_route = routes[res_length_ind]

res_full_route = (start, *res_route, start)

print('Route details:')
print(res_full_route[0], end=' ')  # выводим стартовую точку
route_length(res_full_route, print_route=True)  # выводим все остальные точки
