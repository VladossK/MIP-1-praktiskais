from Logic import Game
from pprint import pprint


if __name__ == '__main__':
    game = Game()
    length = game.choose_length(15)
    num_list = game.generate_numbers(length)
    decision_tree = game.generate_decision_tree(num_list, depth=2)
    pprint(decision_tree)

    #test
    print(game.bank_score)
    print(game.tree)