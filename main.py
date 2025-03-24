from Logic import Game
from pprint import pprint


if __name__ == '__main__':
    game = Game()
    length = game.choose_length(15)
    num_list = game.generate_numbers(length)

    tree = game.generate_decision_tree(num_list, depth=3)
    levels = game.split_tree_by_levels(tree)

    for level_index, level in enumerate(levels):
        print(f"Līmenis {level_index}:")
        for node in level:
            print(f"  Stāvoklis: {node['state']}")