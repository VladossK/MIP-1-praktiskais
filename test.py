from Logic import Game

# Testējam spēli

game = Game()
game.choose_length(25)
initial_numbers = game.generate_numbers(game.length)
print("Sākotnējais stāvoklis:", initial_numbers)
game.game_state = initial_numbers.copy()


first = game.choose_first_move()
if game.is_maximizing:
    game.current_turn = "player"
else:
    game.current_turn = "computer"


    # Spēles galvenā cilpa
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
print(game.depth)