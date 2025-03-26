from Logic import Game

# Testējam spēli

game = Game()
game.choose_length(15)
initial_numbers = game.generate_numbers(game.length)
print("Sākotnējais stāvoklis:", initial_numbers)
game.game_state = initial_numbers.copy()

    # Spēles galvenā cilpa
while len(game.game_state) > 1:
    print("\nSpēlētāja gājiens:")
    game.player_move()
    if len(game.game_state) == 1:
        break
    print("\nDatora gājiens:")
    game.computer_move()

print("\nSpēle beigusies!")
print("Galīgais stāvoklis:", game.game_state)
print("Player Score:", game.player_score, "Bank Score:", game.bank_score)
print(game.depth)