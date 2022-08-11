import random

SIZE = 6
N = 7
ships_length = [3, 2, 2, 1, 1, 1, 1]


class FaultyShipsPlacement(Exception):
    pass


class MissShotbyAi(Exception):
    def __str__(self):
        print("")
        return "Мимо!"


class WrongDots(Exception):
    pass


class CorrectDotsWeNeed(WrongDots):
    def __str__(self):
        return "Вы ввели что-то совсем неправильное. Апгрейд внимательности запущен!"


class DotsAreWrong(WrongDots):
    def __str__(self):
        return "У вас сбился глазомер! Обратите внимание на размеры поля."


class YouCantPlaceShipHere(WrongDots):
    def __str__(self):
        return "В эти координаты нельзя ставить корабль!"


class TheSameMoveAgain(WrongDots):
    def __str__(self):
        return "Вы уже стреляли по этим координатам!"


def out_of_board(x_co, y_co):
    return 1 <= x_co <= 6 and 1 <= y_co <= 6


def wrong_coordinates(coor):
    if len(coor) == 3 and coor[0].isdigit() and coor[-1].isdigit() and (not coor[1].isdigit()):
        pass
    else:
        raise CorrectDotsWeNeed


class Ships:
    def __init__(self, length, direction, life):
        self.length = length
        self.direction = direction
        self.life = life

        self.ship_dots = []

    # Точки для каждого корабля на доске
    def dots(self):
        x_co, y_co = 0, 0
        self.ship_dots = []
        x = random.randint(1, SIZE)
        y = random.randint(1, SIZE)
        for num in range(self.length):
            if self.direction == 0:
                y_co = y + num
                x_co = x
            elif self.direction == 1:
                x_co = x + num
                y_co = y
            self.ship_dots.append((x_co, y_co))
        return self.ship_dots

    @property
    def dots_pr(self):
        return self.ship_dots

    def dots_pl(self, dots):
        self.ship_dots = []
        for d in dots:
            self.ship_dots.append(d)
        return self.ship_dots


class Board:
    def __init__(self, SIZE):
        self.size = SIZE

        self.board_face = [["O"] * SIZE for _ in range(1, SIZE + 1)]
        self.diagonal_plus = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
        self.ships = []
        self.occupied_dots = []
        self.ships_obj = []
        self.num_ships = 0
        self.ai_wins = []

    # Генерация случайной доски. Цикл расстановки кораблей на доске
    def place_ships(self, ship):
        attempt = 0
        while True:
            try:
                if attempt < 200:
                    attempt += 1
                    self.ships = ship.dots()
                    for dot in self.ships:
                        if ((dot[0], dot[1]) in self.occupied_dots) or (dot[0] > SIZE) or (dot[1] > SIZE):
                            raise FaultyShipsPlacement
                    for dot in self.ships:
                        self.board_face[dot[0] - 1][dot[1] - 1] = "■"
                        self.occupied_dots.append(dot)
                    self.ships_obj.append(ship)
                    self.contour(self.ships)
                    return False

                else:
                    self.clear()
                    return False

            except FaultyShipsPlacement:
                pass

    # Расстановка кораблей игроком в ручном режиме
    def place_ships_pl(self, board):
        #board = Board(SIZE)
        self.clear()
        for length in ships_length:
            count = 0
            self.ships = []
            ship = Ships(length, random.randint(0, 1), length)
            while length != count:
                try:
                    print("")
                    print("Получается так хорошо, что нужно всё переделать? Введите S ниже.")
                    player_ship = input(f"Cпускаем на воду корабль длиной {length} клетки(а):  ")
                    if player_ship == "S":
                        return False
                    wrong_coordinates(player_ship)
                    player_ship = tuple(map(int, player_ship.split()))

                    if not out_of_board(player_ship[0], player_ship[1]):
                        raise DotsAreWrong
                    elif player_ship in board.occupied_dots:
                        raise YouCantPlaceShipHere
                    elif player_ship in self.occupied_dots:
                        raise CorrectDotsWeNeed

                    self.ships.append(player_ship)
                    self.occupied_dots.append(player_ship)
                    self.board_face[player_ship[0] - 1][player_ship[1] - 1] = "■"
                    self.show_board("ai")
                    count += 1

                except WrongDots as e:
                    print(e)

            self.ships = ship.dots_pl(self.ships)
            self.ships_obj.append(ship)
            self.contour(self.ships)
        self.occupied_dots = []
        return board

    # Делает контур вокруг кораблей, чтобы невозможно было поставить корабль в соседнюю ячейку и
    # для исключения точек вокруг подбитых кораблей
    def contour(self, ship):
        for dots in ship:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    dot = ((dots[0] + x), (dots[1] + y))
                    if (dot not in self.occupied_dots) and (1 <= dot[0] <= 6) and (1 <= dot[1] <= 6):
                        self.occupied_dots.append(dot)

    # Отображение игровой доски
    def show_board(self, show):
        str_ = "\n"
        str_ += "   | 1 | 2 | 3 | 4 | 5 | 6 | \n"
        str_ += "____________________________ \n"

        for i, list_ in enumerate(self.board_face):
            str_ += f"{i + 1}  | {' | '.join(list_)} | \n"
            str_ += "____________________________ \n"

        if show == "pl":
            str_ = str_.replace("■", "O")

        print(str_)

    # Чистка доски для создания доски другого игрока
    def clear(self):
        self.ships_obj = []
        self.occupied_dots = []
        self.board_face = [["O"] * SIZE for _ in range(1, SIZE + 1)]

    # Проверка выстрелов на попадание
    def check_win(self, dots, flag_):
        try:
            move = 1
            for ship in self.ships_obj:
                if dots in ship.dots_pr:
                    ship.life -= 1
                    self.occupied_dots.append(dots)
                    if flag_ > 1:
                        self.diagonal_shots(dots)
                    self.board_face[dots[0] - 1][dots[1] - 1] = "V"
                    if ship.life >= 1:
                        if flag_ == 1:
                            print("")
                            print("Вы попали! Продолжайте разгром!")
                        elif flag_ > 1:
                            print("")
                            print("Компьютер попал в ваш корабль! Пахнет жаренным.")
                            self.ai_wins.append(dots)
                            if len(ship.dots_pr) == 3 and ship.life == 1:
                                move = 4
                            else:
                                move = 3
                    elif ship.life == 0:
                        if flag_ == 1:
                            print("")
                            print("Вражеский корабль потоплен!")
                        elif flag_ > 1:
                            print("")
                            print("Кажется, ваша флотилия уменьшилась на один корабль! RIP")
                            self.ai_wins.append(dots)
                            move = 2
                        self.num_ships += 1
                        self.contour(ship.dots_pr)
                        for shots in self.occupied_dots:
                            if self.board_face[shots[0] - 1][shots[1] - 1] == "V":
                                pass
                            else:
                                self.board_face[shots[0] - 1][shots[1] - 1] = "."
                    return move, dots[0], dots[1]
                else:
                    continue
            self.occupied_dots.append(dots)
            self.board_face[dots[0] - 1][dots[1] - 1] = "."
            raise MissShotbyAi

        except MissShotbyAi as e:
            print(e)
            return 0, 0, 0

    # Функция для ai. При попадании в корабль игрока заносит все точки по диагонали
    # в список уже сделанных ходов, чтобы ai туда уже не стрелял
    def diagonal_shots(self, dots):
        for i in self.diagonal_plus:
            if ((dots[0] + i[0], dots[1] + i[1]) not in self.occupied_dots) and 1 <= dots[0] + i[0] <= 6 and 1 <= dots[1] + i[1] <= 6:
                self.occupied_dots.append((dots[0] + i[0], dots[1] + i[1]))

    # Ход ai. Определение случайных координат выстрела
    def ai_move(self):
        while True:
            x_co = random.randint(1, 6)
            y_co = random.randint(1, 6)
            if (x_co, y_co) not in self.occupied_dots:
                return x_co, y_co
            else:
                continue

    # Ход ai. При попадании в корабль игрока, в случае, если корабль игрока занимает больше одной
    # клетки, делается выстрел в ближайшую клетку, а не просто наобум
    def ai_move_continue(self, x, y):
            while True:
                x_co = random.randint(x - 1, x + 1)
                y_co = random.randint(y - 1, y + 1)
                if ((x_co, y_co) not in self.occupied_dots) and out_of_board(x_co, y_co):
                    return x_co, y_co
                else:
                    continue

    # Ход ai. Продолжение предыдущего хода. Попытка подбить корабль из трех ячеек.
    def ai_move_continue2(self, x, y):
        steps = 0
        x_co, y_co = 0, 0
        while steps < 10:
            if (x, y + 1) in self.ai_wins:
                y_co = random.choice([y + 2, y - 1])
                x_co = x
            elif (x, y - 1) in self.ai_wins:
                y_co = random.choice([y - 2, y + 1])
                x_co = x
            elif (x + 1, y) in self.ai_wins:
                x_co = random.choice([x + 2, x - 1])
                y_co = y
            elif (x - 1, y) in self.ai_wins:
                x_co = random.choice([x - 2, x + 1])
                y_co = y
            elif (x, y + 2) in self.ai_wins:
                y_co = y + 1
                x_co = x
            elif (x, y - 2) in self.ai_wins:
                y_co = y - 1
                x_co = x
            elif (x + 2, y) in self.ai_wins:
                y_co = y
                x_co = x + 1
            elif (x - 2, y) in self.ai_wins:
                y_co = y
                x_co = x - 1
            if ((x_co, y_co) not in self.occupied_dots) and out_of_board(x_co, y_co):
                break
            else:
                steps += 1
                continue
        return x_co, y_co


class Player:
    def __init__(self, board_ai, board_pl):
        self.board_ai = board_ai
        self.board_pl = board_pl

    # Ход игрока. Запрос координат и их проверка
    def player_move(self, made_shots):
        while True:
            try:
                print("")
                player_move = input("Сначала введите значение по горизонтали, а затем через пробел (!) по вертикали:  ")
                wrong_coordinates(player_move)
                player_move = tuple(map(int, player_move.split()))

                if not out_of_board(player_move[0], player_move[1]):
                    raise DotsAreWrong
                elif player_move in made_shots:
                    raise TheSameMoveAgain

                return player_move

            except WrongDots as e:
                print(e)


class Game:
    def __init__(self):
        self.greet = self.greet()

        board_ai = self.get_boards()
        board_pl = self.board_for_pl()

        self.ai = Player(board_ai, board_pl)
        self.pl = Player(board_ai, board_pl)

    #Приветствие пользователя
    def greet(self):
        print("")
        print("Добро пожаловать в игру 'Морской бой'!")
        print("Перед вами игровая доска.")
        print("")
        print("   | 1 | 2 | 3 | 4 | 5 | 6 | ")
        print("____________________________ ")
        greet_board = [["O"]*6 for _ in range(1, 7)]
        for i, list_ in enumerate(greet_board):
            print(f"{i + 1}  | {' | '.join(list_)} | ")
            print("____________________________ ")
        print("")
        print("Расставьте ваши корабли:")
        print("■ ■ ■  - 1 шт.")
        print("■ ■ - 2 шт.")
        print("■ - 4 шт.")
        print("")
        print("Помните, что нельзя размещать их вплотную друг к другу.")
        print("Вводите координаты корабля через пробел, например, x y.")

    # Определяем того, кто первый ходит
    def first_move(self):
        print("")
        print("Теперь давайте определим очередность хода.")
        print("")
        print(
            f"Какое число выбираете: 1 или 2?\nПри совпадении выбранного вами числа и выпавшего, первыми будете ходить вы. Так что постарайтесь.")

        while True:
            random_choice = None
            player_choice = input("Ваш выбор: ")
            if player_choice == "1" or player_choice == "2":
                random_choice = random.randrange(1, 3)
                print("")
                print(f"На кубике выпало: {random_choice}")
                break
            else:
                print("Такого варианта нет. Введите либо 1, либо 2.")
                continue

        if int(player_choice) == random_choice:
            print("Первый ход за вами. Да победит светлая сторона силы!")
            move = 1
        else:
            print("И всё-таки первым будет ходить компьютер. Тёмная сторона силы заполучила шанс.")
            move = 2
        return move

    # Создание игровых досок
    def get_boards(self):
        while True:
            try:
                board = Board(SIZE)
                board.clear()
                i = len(board.ships_obj)
                for length in ships_length[i:]:
                    ship = Ships(length, random.randint(0, 1), length)
                    board.place_ships(ship)
                if len(board.ships_obj) == N:
                    board.occupied_dots = []
                    return board
                else:
                    pass

            except FaultyShipsPlacement:
                pass

    # Выбор игрока: использовать автоматическую генерацию доски или расставить корабли самому
    def board_for_pl(self):
        while True:
            print("")
            choice = input("Хотите ли вы сами расставить корабли на доске? Если да - введите P. Мы всё сделаем за вас, если укажите A:  ")
            if choice == "P":
                while True:
                    board = Board(SIZE)
                    board = board.place_ships_pl(board)
                    if not board:
                        pass
                    else:
                        break
            elif choice == "A":
                board = self.get_boards()
            else:
                print("Ошибка при вводе!")
                continue
            return board

    # Игровой цикл
    def game(self):
        move = self.first_move()
        x, y = 0, 0
        while True:
            if self.pl.board_ai.num_ships == N:
                print("")
                print("Поздравляем! Победа за вами. Все вражеские корабли потоплены!")
                self.pl.board_ai.show_board("ai")
                return False
            elif self.ai.board_pl.num_ships == N:
                print("")
                print("Поздравляем компьютер! Победа. Дааа, деньки человечества сочтены.")
                self.ai.board_pl.show_board("ai")
                return False
            if move == 1:
                print("-" * 28)
                print("Ваш ход")
                print("Доска соперника")
                self.pl.board_ai.show_board("pl")
                dots = self.pl.player_move(self.pl.board_ai.occupied_dots)
                print("")
                print(f"Ход игрока: {dots}")
                move, x, y = self.pl.board_ai.check_win(dots, move)
                if not move:
                    move = 2
                    continue
            elif move == 2:
                print("-" * 28)
                print("Ход соперника")
                print("Ваша доска")
                self.ai.board_pl.show_board("ai")
                dots = self.ai.board_pl.ai_move()
                print("")
                print(f"Ход игрока: {dots}")
                move, x, y = self.ai.board_pl.check_win(dots, move)
                if not move:
                    move = 1
                    continue
            elif move == 3 or move == 4:
                print("-" * 28)
                print("Ход соперника")
                print("Ваша доска")
                self.ai.board_pl.show_board("ai")
                if move == 3:
                    dots = self.ai.board_pl.ai_move_continue(x, y)
                else:
                    dots = self.ai.board_pl.ai_move_continue2(x, y)
                print("")
                print(f"Ход игрока: {dots}")
                move, x, y = self.ai.board_pl.check_win(dots, move)
                if not move:
                    move = 1



g = Game()
g.game()
