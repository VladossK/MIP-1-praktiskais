from Logic import Game

game = Game()
game.choose_length(15)
game.set_algorithm(2)
game.current_turn = "computer"
game.max_player = "computer"


while True:
    initial_numbers = game.generate_numbers(game.length)
    print("Sākotnējais stāvoklis:", initial_numbers)
    game.game_state = initial_numbers.copy()

    while len(game.game_state) > 1:
        if game.current_turn == "player":
            print("\nSpēlētāja gājiens:")
            game.player_move()
            game.current_turn = "computer"
        else:
            print("\nDatora gājiens:")
            game.computer_move()
            game.current_turn = "player"

    print("\nSpēle beigusies!")
    print("Galīgais stāvoklis:", game.game_state)
    print("Player Score:", game.player_score, "Bank Score:", game.bank_score)
    print("Dziļums:", game.depth)

    if not game.reset_game():
        break