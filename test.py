from Logic import Game

# Testējam spēli

game = Game()
game.choose_length(15)
initial_numbers = game.generate_numbers(game.length)
print("Sākotnējais stāvoklis:", initial_numbers)
game.game_state = initial_numbers.copy()

# Ģenerē lēmumu koku
decision_tree = game.generate_decision_tree(game.game_state, game.depth)
print("\nLēmumu koks:")
levels = game.split_tree_by_levels(decision_tree)
for level, nodes in levels.items():
    print(f"Līmenis {level}:")
    for node in nodes:
        print("  Stāvoklis:", node["state"], "Score:", node["score"])

# Datora gājiens (izmantojot minimax vai, nākotnē, alfa_beta)
print("\nDatora gājiens (Minimax):")
game.computer_move()