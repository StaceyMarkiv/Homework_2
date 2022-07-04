import random


def check_empty_points(game_field):
    # выбор всех пустых клеток на поле
    empty = []
    for i in range(10):
        for j in range(10):
            if game_field[i][j] != 'X' and game_field[i][j] != 'O':
                point = i*10 + j
                empty.append(point)
    return empty


def choose_comp_point(empty_points_list):
    # компьютер выбирает случайную точку на поле
    point = random.choice(empty_points_list)
    point_coords = (point // 10, point % 10)
    return point_coords


def add_mark(game_field, point, sign):
    # добавляем отметку на игровое поле
    x = point[0]
    y = point[1]
    game_field[x][y] = sign


def surrounding_points(point_coord):
    # находим координаты точек вокруг введенной точки (против часовой стрелки, начиная с левого верхнего угла)
    point1 = (point_coord[0] - 1, point_coord[1] - 1)
    point2 = (point_coord[0], point_coord[1] - 1)
    point3 = (point_coord[0] + 1, point_coord[1] - 1)
    point4 = (point_coord[0] + 1, point_coord[1])
    point5 = (point_coord[0] + 1, point_coord[1] + 1)
    point6 = (point_coord[0], point_coord[1] + 1)
    point7 = (point_coord[0] - 1, point_coord[1] + 1)
    point8 = (point_coord[0] - 1, point_coord[1])

    points = [point1, point2, point3, point4, point5, point6, point7, point8]
    points_res = [point for point in points if (0 <= point[0] <= 9) and (0 <= point[1] <= 9)]

    return points_res


def filled_points(game_field, surr_points):
    # проверяем наличие заполненных полей вокруг введенной точки
    filled_x = {}
    filled_o = {}
    for i, point in enumerate(surr_points):
        x_coord = point[0]
        y_coord = point[1]
        if game_field[x_coord][y_coord] == 'X':
            filled_x[i] = point
        elif game_field[x_coord][y_coord] == 'O':
            filled_o[i] = point
    return filled_x, filled_o


def filled_points_qty(init_point, surr_point, game_field, sign):
    # проверяем точки в одном ряду с init_point и surr_point
    def counting(ind1, ind2):
        nonlocal init_point
        nonlocal game_field
        nonlocal sign
        count = 0
        for i in range(1, 5):
            new_point = (init_point[0] + ind1 * i, init_point[1] + ind2 * i)
            x = new_point[0]
            y = new_point[1]
            if (0 <= x <= 9) and (0 <= y <= 9):
                if game_field[x][y] == sign:
                    count += 1
                else:
                    break
        return count

    ind1 = surr_point[0] - init_point[0]
    ind2 = surr_point[1] - init_point[1]
    qty_one_side = counting(ind1, ind2)
    qty_another_side = counting(-ind1, -ind2)
    return qty_one_side + qty_another_side + 1


def find_winner(filled_x, filled_o, init_point, game_field, sign):
    win = ''
    filled_dict = {}
    other_sign = ''

    if sign == 'X':
        filled_dict = filled_x
        other_sign = 'O'
    elif sign == 'O':
        filled_dict = filled_o
        other_sign = 'X'

    for key in filled_dict:
        if key in range(4):
            filled_qty = filled_points_qty(init_point, filled_dict[key], game_field, sign)
            if filled_qty >= 5:
                win = other_sign

    return win


field = [['-' for i in range(10)] for j in range(10)]
empty_points = check_empty_points(field)
print(*field, sep='\n')
print('---')

player_choice = random.randint(0, 1)
if player_choice == 0:
    print('Первый ход компьютера')
    sign_comp = 'X'
    sign_hum = 'O'

    # ход компьютера
    comp_point = choose_comp_point(empty_points)
    add_mark(field, comp_point, sign_comp)
    empty_points = check_empty_points(field)
    print(*field, sep='\n')
    print('---')

else:
    print('Первый ход ваш')
    sign_comp = 'O'
    sign_hum = 'X'

winner = ''
while not winner:
    # ход пользователя
    print('Введите координаты точки - два числа от 0 до 9 через пробел: ')
    hum_point = tuple()
    while not hum_point:
        hum_point = tuple(map(int, input().split()))
        if len(hum_point) != 2:
            print('Введите 2 координаты:')
            hum_point = tuple()
        elif (hum_point[0] < 0 or hum_point[0] > 9) or (hum_point[1] < 0 or hum_point[1] > 9):
            print('Неверные координаты, введите другие:')
            hum_point = tuple()
        elif field[hum_point[0]][hum_point[1]] == sign_hum or field[hum_point[0]][hum_point[1]] == sign_comp:
            print('Поле занято, введите другие координаты:')
            hum_point = tuple()

    add_mark(field, hum_point, sign_hum)
    empty_points = check_empty_points(field)

    surround = surrounding_points(hum_point)
    filled_X, filled_O = filled_points(field, surround)
    winner = find_winner(filled_X, filled_O, hum_point, field, sign_hum)
    print(*field, sep='\n')
    print('---')

    if winner:
        break

    # ход компьютера
    comp_point = choose_comp_point(empty_points)
    add_mark(field, comp_point, sign_comp)

    surround = surrounding_points(comp_point)
    filled_X, filled_O = filled_points(field, surround)
    winner = find_winner(filled_X, filled_O, comp_point, field, sign_comp)
    print(*field, sep='\n')
    print('---')

    if winner:
        break

if winner == sign_comp:
    print('Победил компьютер')
elif winner == sign_hum:
    print('Вы победили. Поздравляю!')
