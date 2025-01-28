1
# main.py
from game import ConnectFour
from ai import ConnectFourAI

def main():
    game = ConnectFour()
    ai = ConnectFourAI(game)

    print("Добро пожаловать в игру 4 в ряд!")
    print("Вы играете за \033[91m●\033[0m, компьютер играет за \033[94m●\033[0m.")
    
    while not game.game_over and not game.is_board_full():
        # Ход игрока
        game.print_board()
        
        while True:
            try:
                move = int(input("Ваш ход (введите номер столбца 1-7): "))
                if game.is_valid_move(move):
                    game.make_move(move)
                    break
                else:
                    print("Некорректный ход. Попробуйте снова.")
            except ValueError:
                print("Пожалуйста, введите число от 1 до 7.")
        
        # Проверка победы игрока
        if game.game_over:
            game.print_board()
            print("Поздравляю! Вы победили!")
            break
        
        # Ход ИИ
        ai_move = ai.get_best_move()
        print(f"Компьютер выбрал столбец: {ai_move}")
        game.make_move(ai_move)
        
        # Проверка победы ИИ
        if game.game_over:
            game.print_board()
            print("Компьютер победил!")
            break
        
        # Проверка ничьей
        if game.is_board_full():
            game.print_board()
            print("Ничья!")
            break

if __name__ == "__main__":
    main()
