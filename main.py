# Начало программы. Приветствие, правила игры
def hello():
    print("Добро пожаловать в игру 'Крестики-Нолики'!")
    print("Игровое поле выглядит следующим образом:")
    print("")
    print("   |  0  |  1  |   2")
    print("----------------------")
    print("0  |  1  |  2  |   3")
    print("----------------------")
    print("1  |  4  |  5  |   6")
    print("----------------------")
    print("2  |  7  |  8  |   9")
    print("----------------------")
    print("")
    print("Ячейки для вашего хода пронумерованы от 1 до 9.")
    print("Что ж, начинаем!")


hello()

# Определение того, кто будет ходить первым
def first_move():
    import random
    print("")
    print("Давайте для начала определим очередность хода.")
    print("")
    print(
        f"Какое число выбираете: 1 или 2?\nПри совпадении выбранного вами числа и выпавшего, первыми будут ходить крестики.")

    player_choice = int(input("Ваш выбор: "))
    random_choice = random.randrange(1, 3)

    print("")
    print(f"На кубике выпало: {random_choice}")

    if player_choice == random_choice:
        print("Первый ход за крестиками.")
        flag_ = 1
    else:
        print("И всё-таки первыми будут ходить нолики.")
        flag_ = 2
    return flag_


dict_field = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9"}

# Проверка хода игрока на правильность ввода
def check_moves():
    while True:
        moves = input("Ваш ход. Напишите номер ячейки:  ")

        if moves.isdigit():
            moves = int(moves)
        else:
            print("")
            print("Вы ввели какую-то бяку, а не число!")
            continue

        if 1 <= moves <= 9:
            pass
        else:
            print("")
            print("Вы ввели неправильный номер ячейки.")
            continue

        if dict_field[moves] != "X" and dict_field[moves] != "O":
            return moves
        else:
            print("")
            print("Вы указали уже занятую ячейку.")
            continue

# Отображение игрового поля и сделанных ходов
def print_field():
        print("\n")
        print(f"   |  0  |  1  |   2")
        print(f"----------------------")
        for i in range(1, 10, 3):
            print(f"{round(i ** 0.5 - 1)}  |  {dict_field[i]}  |  {dict_field[i + 1]}  |   {dict_field[i + 2]}")
            print(f"----------------------")
        print("\n")

# Проверка на выигрыш уже сделанных ходов
def winner():

        win_ = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [7, 5, 3]]

        for comb in win_:
            perfect_comb = []

            for i in comb:
                perfect_comb.append(dict_field[i])

            if perfect_comb == ["X", "X", "X"]:
                print("Поздравляем! Крестики выиграли.")
                return True
            elif perfect_comb == ["O", "O", "O"]:
                print("Поздравляем! Выиграли нолики.")
                return True
        return False

# Основная часть программы. Запуск цикла
flag_ = first_move()
count = 1
while count <= 9:
    print("")
    moves = check_moves()

    if flag_ == 1:
        dict_field[moves] = "X"
        flag_ = 2
    elif flag_ == 2:
        dict_field[moves] = "O"
        flag_ = 1

    print_field()

    if winner():
        break

    if count == 9:
        print("Что ж, свершилась боевая ничья!")
        break

    if flag_ == 1:
         print("")
         print("Сейчас ходят крестики.")
    elif flag_ == 2:
         print("")
         print("Сейчас ходят нолики.")

    count += 1







