# game.py
class ConnectFour:
    def __init__(self):
        # Создаем доску 6x7, нумерация с 1
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.current_player = 1  # Игрок начинает (X)
        self.game_over = False
        self.winner = None

    def print_board(self):
        """Вывод текущего состояния доски"""
        print("  1   2   3   4   5   6   7")
        print(" ----------------------------")
        for row in self.board:
            print("|", end=" ")
            for cell in row:
                if cell == 0:
                    print("•", end=" | ")  # Нейтральная точка
                elif cell == 1:
                    print("\033[91m●\033[0m", end=" | ")  # Красная фишка
                else:
                    print("\033[94m●\033[0m", end=" | ")  # Синяя фишка
            print("\n ----------------------------")

    def is_valid_move(self, column):
        """Проверка возможности хода в указанный столбец"""
        # Колонки нумеруются с 1 до 7
        if column < 1 or column > 7:
            return False
        return self.board[0][column-1] == 0

    def make_move(self, column):
        """Совершение хода в указанный столбец"""
        # Проверяем корректность хода
        if not self.is_valid_move(column):
            return False

        # Находим первую свободную позицию снизу вверх
        for row in range(5, -1, -1):
            if self.board[row][column-1] == 0:
                self.board[row][column-1] = self.current_player
                break

        # Проверяем победу
        if self.check_win():
            self.game_over = True
            self.winner = self.current_player

        # Меняем игрока
        self.current_player = 3 - self.current_player  # Переключение между 1 и 2
        return True

    def check_win(self):
        """Проверка победы"""
        # Проверка по горизонтали
        for row in range(6):
            for col in range(4):
                if (self.board[row][col] == self.board[row][col+1] == 
                    self.board[row][col+2] == self.board[row][col+3] != 0):
                    return True

        # Проверка по вертикали
        for row in range(3):
            for col in range(7):
                if (self.board[row][col] == self.board[row+1][col] == 
                    self.board[row+2][col] == self.board[row+3][col] != 0):
                    return True

        # Проверка по диагонали (вправо вниз)
        for row in range(3):
            for col in range(4):
                if (self.board[row][col] == self.board[row+1][col+1] == 
                    self.board[row+2][col+2] == self.board[row+3][col+3] != 0):
                    return True

        # Проверка по диагонали (влево вниз)
        for row in range(3):
            for col in range(3, 7):
                if (self.board[row][col] == self.board[row+1][col-1] == 
                    self.board[row+2][col-2] == self.board[row+3][col-3] != 0):
                    return True

        return False

    def is_board_full(self):
        """Проверка заполненности доски"""
        return all(cell != 0 for row in self.board for cell in row)
