from Logic import Game
from pprint import pprint


if __name__ == '__main__':
    game = Game()
    length = game.choose_length(15)
    num_list = game.generate_numbers(length)

    tree = game.generate_decision_tree(num_list, depth=2)
    levels = game.split_tree_by_levels(tree)


    print(game.num_list)
    print(game.tree)
    print(levels)