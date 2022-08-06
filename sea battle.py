import random

#ships_on_board_ai = []
#ships_on_board_player = []
#occupied_dots_player = []
player_wins = []
ai_wins = []
player_moves = []
ai_moves = []
ships_obj = []
diagonal_plus = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
SIZE = 6
attempt = 0


class FaultyShipsPlacement(Exception):
    pass


class MissShotbyAi(Exception):
    def __str__(self):
        print("")
        return "Ваш оппонент промазал!"


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

        self.ships = []
        self.occupied_dots = []

    # Генерация случайной доски. Цикл расстановки кораблей на доске
    def place_ships(self, ship):
        try:
            while ai.num_ships > 0:
                global attempt
                dot = 0
                self.ships = []
                while ship.length != dot:
                    attempt += 1
                    if attempt < 200:
                        x = random.randint(1, SIZE)
                        y = random.randint(1, SIZE)
                        for num in range(self.length):
                            if self.direction == 0:
                                y_co = y + num
                                x_co = x
                            elif self.direction == 1:
                                x_co = x + num
                                y_co = y
                            if ((x_co, y_co) in self.occupied_dots) or (x_co > 6) or (y_co > 6):
                                self.ships.clear()
                                dot = 0
                                break
                            else:
                                self.ships.append((x_co, y_co))
                                print(self.ships)
                                dot += 1
                    else:
                        raise FaultyShipsPlacement

                for dots in ship.dots:
                    self.occupied_dots.append(dots)
                ships_obj.append(ship)
                ai.num_ships -= 1
                self.contour(0, ship)
            return board

        except FaultyShipsPlacement:
            self.occupied_dots.clear()
            ships_obj.clear()
            attempt = 0
            return False

    @property
    def dots(self):
        return self.ships

    # Делает контур вокруг кораблей, чтобы невозможно было поставить корабль в соседнюю ячейку
    def contour(self, num, ship):
        if num == 0:
            for dots in ship.dots:
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        dot = ((dots[0] + x), (dots[1] + y))
                        if (dot not in self.occupied_dots) and (1 <= dot[0] <= 6) and (1 <= dot[1] <= 6):
                            self.occupied_dots.append(dot)

        elif num == 2:
            for dots in ship.dots_p:
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        dot = ((dots[0] + x), (dots[1] + y))
                        if (dot not in ai_moves) and (1 <= dot[0] <= 6) and (1 <= dot[1] <= 6):
                            ai_moves.append(dot)

        elif num == 3:
            for dots in ship.dots:
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        dot = ((dots[0] + x), (dots[1] + y))
                        if (dot not in player_moves) and (1 <= dot[0] <= 6) and (1 <= dot[1] <= 6):
                            player_moves.append(dot)

    def place_ships_user(self, ship):
        while player.num_ships > 0:
            board.show_board()
            count = 0
            self.player_ships = []
            while self.length != count:
                try:
                    print("")
                    player_ship = input(f"Cпускаем на воду корабль длиной {self.length} клетки(а):  ")
                    wrong_coordinates(player_ship)
                    player_ship = tuple(map(int, player_ship.split()))

                    if not out_of_board(player_ship[0], player_ship[1]):
                        raise DotsAreWrong
                    elif player_ship in self.occupied_dots:
                        raise YouCantPlaceShipHere

                    self.player_ships.append(player_ship)
                    self.ships.append(player_ship)
                    board.show_board()
                    count += 1
                except WrongDots as e:
                    print(e)

            ships_obj.append(ship)
            player.num_ships -= 1
            self.contour(0, 0)
        return board

    @property
    def dots_p(self):
        return self.player_ships


class Player:
    def __init__(self, flag_, num_ships):
        self.flag_ = flag_
        self.num_ships = num_ships

    def player_move(self):
        if ai.num_ships == 0:
            self.end("pl")
        while True:
            try:
                print("")
                print("Ваш ход")
                board.show_board_ai()
                player_move = input("Сначала введите значение по горизонтали, а затем через пробел (!) по вертикали:  ")
                wrong_coordinates(player_move)
                player_move = tuple(map(int, player_move.split()))

                if not out_of_board(player_move[0], player_move[1]):
                    raise DotsAreWrong
                elif player_move in player_moves:
                    raise TheSameMoveAgain
                break
            except WrongDots as e:
                print(e)

        for ship in ships_obj:
            if player_move in ship.dots:
                ship.life -= 1
                if ship.life >= 1:
                    print("Вы попали! Продолжайте разгром!")
                elif ship.life == 0:
                    print("Вражеский корабль потоплен!")
                    ai.num_ships -= 1
                    Ships.contour(3, ship)
                player_wins.append(player_move)
                move = 1
                return move
            else:
                continue
        print("Вы промахнулись!")
        player_moves.append(player_move)
        move = 0
        return move

    def ai_move(self):
        if player.num_ships == 0:
            self.end("ai")
        try:
            x_co, y_co = self.check_ai_move()
            move = self.check_ai_win(x_co, y_co)

            if move == 2:
                print("")
                print("Ход компьютера")
                while True:
                    x_co = random.randint(x_co - 1, x_co + 1)
                    y_co = random.randint(y_co - 1, y_co + 1)
                    if ((x_co, y_co) not in ai_moves) and out_of_board(x_co, y_co):
                        break
                    else:
                        continue
                move = self.check_ai_win(x_co, y_co)
            elif move == 0:
                return move

            if move == 2:
                steps = 0
                print("")
                print("Ход компьютера")
                while steps < 10:
                    if (x_co, y_co + 1) in ai_wins:
                        y_co = random.choice([y_co + 2, y_co - 1])
                    elif (x_co, y_co - 1) in ai_wins:
                        y_co = random.choice([y_co - 2, y_co + 1])
                    elif (x_co + 1, y_co) in ai_wins:
                        x_co = random.choice([x_co + 2, x_co - 1])
                    elif (x_co - 1, y_co) in ai_wins:
                        x_co = random.choice([x_co - 2, x_co + 1])
                    if ((x_co, y_co) not in ai_moves) and out_of_board(x_co, y_co):
                        break
                    else:
                        steps += 1
                        continue
                move = self.check_ai_win(x_co, y_co)
                return move
            elif move == 0:
                return move

        except MissShotbyAi as e:
            print(e)
            board.show_board()
            move = 1
            return move

    def check_ai_move(self):
        print("")
        print("Ход компьютера")
        while True:
            x_co = random.randint(1, 6)
            y_co = random.randint(1, 6)
            if (x_co, y_co) not in ai_moves:
                return x_co, y_co
            else:
                continue

    def check_ai_win(self, x_co, y_co):
        move = 1
        for ship in ships_obj:
            if (x_co, y_co) in ship.dots_p:
                ship.life -= 1
                ai_wins.append((x_co, y_co))
                ai_moves.append((x_co, y_co))
                self.diagonal_shots(x_co, y_co)
                if ship.life >= 1:
                    print("")
                    print("Компьютер попал в ваш корабль! Пахнет жаренным.")
                    move = 2
                elif ship.life == 0:
                    print("")
                    print("Кажется, ваша флотилия уменьшилась на один корабль! RIP")
                    player.num_ships -= 1
                    Ships.contour(2, ship)
                    move = 0
                board.show_board()
                return move
            else:
                continue
        if move == 1:
            ai_moves.append((x_co, y_co))
            raise MissShotbyAi

    def diagonal_shots(self, x_co, y_co):
        for i in diagonal_plus:
            if ((x_co + i[0], y_co + i[1]) not in ai_moves) and 1 <= x_co + i[0] <= 6 and 1 <= y_co + i[1] <= 6:
                ai_moves.append((x_co + i[0], y_co + i[1]))

    def end(self, winner):
        if winner == "pl":
            print("")
            print("Поздравляем! Победа за вами. Все вражеские корабли потоплены!")
            board.show_board_ai()
            return False
        else:
            print("")
            print("Поздравляем компьютер! Победа. Дааа, деньки человечества сочтены.")
            board.show_board()
            return False


ai = Player(2, 7)
player = Player(1, 7)


class Board:
    def __init__(self, SIZE, board_show):
        self.board_show = board_show
        self.size = SIZE

    # Добавить корабль на доску
    def show_board(self):
        print("")
        print("   | 1 | 2 | 3 | 4 | 5 | 6 |")
        print("____________________________")
        print(ai_moves)
        for dots in ai_moves:
            self.board_show[dots[0]-1][dots[1]-1] = "."

        #for dots in ship.dots_p:
            self.board_show[dots[0]-1][dots[1]-1] = "■"

        for dots in ai_wins:
            self.board_show[dots[0]-1][dots[1]-1] = "V"

        for i, list_ in enumerate(self.board_show):
            print(f"{i+1}  | {' | '.join(list_)} |")
            print("____________________________")


    def show_board_ai(self):
        print("")
        print("   | 1 | 2 | 3 | 4 | 5 | 6 |")
        print("____________________________")
        for dots in player_moves:
            self.board_show[dots[0]-1][dots[1]-1] = "."

        #for dots in ship.dots:
            self.board_show[dots[0]-1][dots[1]-1] = "■"

        for dots in player_wins:
            self.board_show[dots[0]-1][dots[1]-1] = "V"

        for i, list_ in enumerate(self.board_show):
            print(f"{i + 1}  | {' | '.join(list_)} |")
            print("____________________________")


board = Board(SIZE, [["O"] * SIZE for _ in range(1, SIZE + 1)])


class Game:
    def __init__(self):
        self.ships_length = [3, 2, 2, 1, 1, 1, 1]

    #Приветствие пользователя
    def greet(self):
        print("")
        print("Добро пожаловать в игру 'Морской бой'!")
        print("")
        print("Перед вами игровая доска.")
        print("Расставьте ваши корабли:")
        print("■ ■ ■  - 1 шт.")
        print("■ ■ - 2 шт.")
        print("■ - 4 шт.")
        print("Помните, что нельзя размещать корабли вплотную друг к другу.")
        print("Вводите координаты корабля через пробел, например, x y.")

    def get_ships_ai(self):
        board_ai = None
        for length in self.ships_length:
            print(length)
            ship = Ships(length, random.randint(0, 1), length)
            board_ai = ship.place_ships(ship)
            print(board_ai)
        if not board_ai:
            return True
        else:
            return board_ai

    def player_choice(self):
        while True:
            choice = input("Хотите ли вы сами расставить корабли на доске? Если да, введите P. Мы всё сделаем за вас, если укажите A:  ")
            if choice == "P":
                return 1
            elif choice == "A":
                return 2
            else:
                print("Ошибка при вводе!")
                continue

    def get_ships_pl(self):
        board_user = None
        choice = self.player_choice()
        for length in self.ships_length:
            ship = Ships(length, random.randint(0, 1), length)
            if choice == 1:
                board_user = ship.place_ships_user(ship)
            elif choice == 2:
                board_user = ship.place_ships(ship)
                if not board_user:
                    return True
                else:
                    return board_user
        return board_user

    # Определяем того, кто первый ходит
    def first_move(self):
        print("")
        print("Теперь давайте определим очередность хода.")
        print("")
        print(
            f"Какое число выбираете: 1 или 2?\nПри совпадении выбранного вами числа и выпавшего, первыми будете ходить вы. Так что постарайтесь.")

        player_choice = int(input("Ваш выбор: "))
        random_choice = random.randrange(1, 3)

        print("")
        print(f"На кубике выпало: {random_choice}")

        if player_choice == random_choice:
            print("Первый ход за вами. Да победит светлая сторона силы!")
            move = 1
        else:
            print("И всё-таки первым будет ходить компьютер. Тёмная сторона силы заполучила шанс.")
            move = 0
        return move

    # Игровой цикл
    def game(self):
        self.greet()
        g.get_ships_ai()
        while True:
            g.get_ships_pl()
        move = self.first_move()
        while True:
            if move == 1:
                player.player_move()
            elif move == 0:
                ai.ai_move()


g = Game()
g.game()


