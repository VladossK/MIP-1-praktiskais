import random


class Game():

    def __init__(self):
        self.num_list = []
        self.choose_num = 0
        self.isMinMax = False
        self.isAlfaBeta = False
        self.bank_score = 0
        self.score = 0
        self.isOdd = False
        self.isEven = False
        self.length = 15
        self.depth = 0
        self.tree = None


    def choose_length(self, length):
        self.length = length
        return self.length

    def choose_depth(self, depth):
        self.depth = depth
        return self.depth

    def generate_numbers(self, length):
        if not ( 15 <= length <= 25):
            raise ValueError("Length must be between 15 and 25")
        self.num_list = [random.randint(1, 9) for _ in range(length)]
        return self.num_list


    def generate_decision_tree(self, num_list, depth, index=1):
        if depth == 0:
            return {
                "index": index,
                "state": num_list,
                "bank_score": self.bank_score,
                "children": []
            }

        tree = {
            "index": index,
            "state": num_list.copy(),
            "bank_score": self.bank_score,
            "children": []
        }

        for i in range(len(num_list) - 1):
            current_list = num_list.copy()
            x, y = current_list[i], current_list[i + 1]
            pair_sum = x + y
            del current_list[i]
            del current_list[i]

            if pair_sum > 7:
                current_list.insert(i, 1)
            elif pair_sum < 7:
                current_list.insert(i, 3)
            else:  # pair_sum == 7
                current_list.insert(i, 2)
                self.bank_score += 1

            index += 1
            child_tree = self.generate_decision_tree(current_list, depth - 1, index)
            tree["children"].append(child_tree)

        self.tree = tree
        return tree














