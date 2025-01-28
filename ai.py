# ai.py
import math

class ConnectFourAI:
    def __init__(self, game, max_depth=4):
        self.game = game
        self.max_depth = max_depth

    def evaluate_board(self):
        """Оценка текущего состояния доски"""
        # Простая эвристическая оценка
        score = 0
        
        # Центральные столбцы важнее
        center_columns = [self.game.board[r][3] for r in range(6)]
        score += center_columns.count(2) * 3  # За O
        score -= center_columns.count(1) * 3  # Против X

        # Проверка выигрышных линий
        score += self.check_lines(2)  # Линии для O
        score -= self.check_lines(1)  # Линии для X

        return score

    def check_lines(self, player):
        """Подсчет потенциальных выигрышных линий"""
        score = 0
        
        # Горизонтальные линии
        for row in range(6):
            for col in range(4):
                line = self.game.board[row][col:col+4]
                score += self.score_line(line, player)

        # Вертикальные линии
        for col in range(7):
            for row in range(3):
                line = [self.game.board[row+i][col] for i in range(4)]
                score += self.score_line(line, player)

        # Диагональ вправо вниз
        for row in range(3):
            for col in range(4):
                line = [self.game.board[row+i][col+i] for i in range(4)]
                score += self.score_line(line, player)

        # Диагональ влево вниз
        for row in range(3):
            for col in range(3, 7):
                line = [self.game.board[row+i][col-i] for i in range(4)]
                score += self.score_line(line, player)

        return score

    def score_line(self, line, player):
        """Оценка потенциальной линии"""
        opponent = 3 - player
        
        # Подсчет фишек игрока и пустых клеток
        player_count = line.count(player)
        empty_count = line.count(0)
        
        # Различные бонусы и штрафы
        if player_count == 4:
            return 100  # Победная линия
        elif player_count == 3 and empty_count == 1:
            return 5  # Почти победная линия
        elif player_count == 2 and empty_count == 2:
            return 2  # Потенциальная линия
        
        return 0

    def minimax(self, depth, alpha, beta, is_maximizing):
        """Алгоритм минимакс с альфа-бета отсечением"""
        # Проверка на завершение игры или достижение максимальной глубины
        if depth == 0 or self.game.game_over:
            return self.evaluate_board()

        if is_maximizing:
            max_eval = float('-inf')
            for col in range(1, 8):
                if self.game.is_valid_move(col):
                    # Создаем копию доски для симуляции
                    original_board = [row.copy() for row in self.game.board]
                    original_player = self.game.current_player
                    
                    # Делаем ход
                    self.game.make_move(col)
                    
                    # Рекурсивный вызов
                    eval_score = self.minimax(depth-1, alpha, beta, False)
                    max_eval = max(max_eval, eval_score)
                    
                    # Откат хода
                    self.game.board = original_board
                    self.game.current_player = original_player
                    self.game.game_over = False
                    
                    # Альфа-бета отсечение
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
            return max_eval
        
        else:
            min_eval = float('inf')
            for col in range(1, 8):
                if self.game.is_valid_move(col):
                    # Создаем копию доски для симуляции
                    original_board = [row.copy() for row in self.game.board]
                    original_player = self.game.current_player
                    
                    # Делаем ход
                    self.game.make_move(col)
                    
                    # Рекурсивный вызов
                    eval_score = self.minimax(depth-1, alpha, beta, True)
                    min_eval = min(min_eval, eval_score)
                    
                    # Откат хода
                    self.game.board = original_board
                    self.game.current_player = original_player
                    self.game.game_over = False
                    
                    # Альфа-бета отсечение
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
            return min_eval

    def get_best_move(self):
        """Выбор лучшего хода для ИИ"""
        best_score = float('-inf')
        best_move = None
        
        for col in range(1, 8):
            if self.game.is_valid_move(col):
                # Создаем копию доски для симуляции
                original_board = [row.copy() for row in self.game.board]
                original_player = self.game.current_player
                
                # Делаем ход
                self.game.make_move(col)
                
                # Оценка хода
                score = self.minimax(self.max_depth-1, float('-inf'), float('inf'), False)
                
                # Откат хода
                self.game.board = original_board
                self.game.current_player = original_player
                self.game.game_over = False
                
                # Обновляем лучший ход
                if score > best_score:
                    best_score = score
                    best_move = col
        
        return best_move
