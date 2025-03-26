import random
from collections import deque


class Game():
    def __init__(self):
        # Galvenie spēles lauki
        self.game_state = []         # Pašreizējais spēles stāvoklis (skaitļu saraksts)
        self.choose_num = 0

        self.isMinMax = True         # Karogs: izmantot minimax algoritmu
        self.isAlfaBeta = False      # Karogs: izmantot alfa_beta algoritmu (nākotnē)
        self.is_maximizing = True    # Spēlētājs, kurš sācis spēli, tiek uzskatīts par maksimizējošo

        self.bank_score = 0          # Bankas punkti (kad summa == 7)
        self.player_score = 0        # Spēlētāja punkti (kad summa <7 vai >7)

        self.length = 15
        self.depth = 4            # Var mainīt meklēšanas dziļumu pēc nepieciešamības
        self.tree = None
        self.levels = {}

    # Izvēlas masīva garumu (no 15 līdz 25)
    def choose_length(self, length):
        self.length = length
        return self.length

    # Izvēlas algoritma dziļumu
    def choose_depth(self, depth):
        self.depth = depth
        return self.depth

    # Ģenerē nejaušu skaitļu sarakstu
    def generate_numbers(self, length):
        if not (15 <= length <= 25):
            raise ValueError("Garumam jābūt no 15 līdz 25")
        self.game_state = [random.randint(1, 9) for _ in range(length)]
        return self.game_state

    # Ģenerē lēmumu koku, saglabājot stāvokli un punktu vērtības
    def generate_decision_tree(self, game_state, depth, score=None):
        """
        Ģenerē lēmumu koku, balstoties uz skaitļu sarakstu, dziļumu un pašreizējo punktu vērtību.
        Katrs mezgls satur:
          "state": skaitļu saraksts,
          "score": vārdnīcu {"player_score": ..., "bank_score": ...},
          "children": apakšmezglu sarakstu.
        """
        if score is None:
            score = {"player_score": self.player_score, "bank_score": self.bank_score}
        node = {"state": game_state.copy(), "score": score.copy(), "children": []}

        # Terminālais stāvoklis: atlicis viens skaitlis
        if depth == 0 or len(game_state) == 1:
            return node

        # Iterē caur visiem iespējamiem gājieniem (katru blakus esošo skaitļu pāri)
        for i in range(len(game_state) - 1):
            current_state = game_state.copy()
            # Izņem divus blakus esošus skaitļus
            x = current_state.pop(i)
            y = current_state.pop(i)  # pēc pirmā pop otrais elements pārvietojas uz pozīciju i
            pair_sum = x + y

            new_score = score.copy()
            # Piemēro aizstāšanas noteikumus un atjaunina punktu vērtības:
            if pair_sum > 7:
                current_state.insert(i, 1)
                new_score["player_score"] += 1
            elif pair_sum < 7:
                current_state.insert(i, 3)
                new_score["player_score"] -= 1
            else:  # pair_sum == 7
                current_state.insert(i, 2)
                new_score["bank_score"] += 1

            child_tree = self.generate_decision_tree(current_state, depth - 1, new_score)
            node["children"].append(child_tree)

        return node

    def split_tree_by_levels(self, tree):
        """
        Sadala koku pa līmeņiem, saglabājot pilnu informāciju par katru mezglu.
        Atgriež vārdnīcu, kur atslēga ir līmeņa numurs, un vērtība ir mezglu saraksts.
        """
        levels = {}
        def traverse(node, depth):
            if depth not in levels:
                levels[depth] = []
            levels[depth].append(node)
            for child in node.get("children", []):
                traverse(child, depth + 1)
        traverse(tree, 0)
        return levels

    def terminal_eval(self, score):
        """
        Terminālā stāvokļa novērtējums.
        Ja gan player_score, gan bank_score ir pāra skaitļi, atgriež +1 (uzvara spēlētājam, kurš sācis).
        Ja gan player_score, gan bank_score ir nepāra skaitļi, atgriež -1 (uzvara otram spēlētājam).
        Citos gadījumos atgriež 0 (neizšķirts).
        """

    # Heuristiskā novērtēšanas funkcija ne termināliem stāvokļiem
    def heuristic_eval(self, node):
        # Piemēram, var novērtēt kā player_score - bank_score
        return node["score"]["player_score"] - node["score"]["bank_score"]

    # Minimax algoritma rekurzīvā ieviešana
    def minimax(self, node, depth, is_maximizing):
        """
        Rekurzīva minimax algoritma ieviešana.
        Ja stāvoklis ir termināls (atlicis viens skaitlis), atgriež novērtējumu (1, -1 vai 0).
        Ja dziļuma robeža sasniegta (depth == 0), atgriež heuristisko vērtību (šeit 0).
        """
        # Termināls stāvoklis: atlicis viens skaitlis
        if len(node["state"]) == 1:
            return self.terminal_eval(node["score"])
        # Ja dziļuma robeža sasniegta, atgriežam heuristisko vērtību
        if depth == 0:
            return self.heuristic_eval(node)

        if is_maximizing:
            best_value = float("-inf")
            for child in node["children"]:
                value = self.minimax(child, depth - 1, False)
                best_value = max(best_value, value)
            return best_value
        else:
            best_value = float("inf")
            for child in node["children"]:
                value = self.minimax(child, depth - 1, True)
                best_value = min(best_value, value)
            return best_value

    # Alfa-beta algoritma ieviešana (nākotnē)
    def alfa_beta(self, node, depth, alpha, beta, is_maximizing):
        pass

    # Izvēlas labāko gājienu, izmantojot minimax vai alfa-beta algoritmu
    def choose_move(self):
        """
        Ģenerē lēmumu koku pašreizējam stāvoklim,
        tad katram pirmā līmeņa gājienam aprēķina izvēlēto algoritmu vērtību.
        Ja isMinMax ir True, tiek izmantots minimax.
        Ja isAlfaBeta ir True, nākotnē tiks izmantots alfa_beta.
        Pēc labākā gājiena izvēles, atjaunina spēles stāvokli:
          game_state, player_score un bank_score.
        """
        self.tree = self.generate_decision_tree(self.game_state, self.depth)
        best_value = float("-inf")
        best_move = None
        best_child = None

        if self.isMinMax:
            for idx, child in enumerate(self.tree["children"]):
                move_value = self.minimax(child, self.depth - 1, False)
                print(f"Gājiens {idx}: Stāvoklis {child['state']}, Score {child['score']}, Vērtība {move_value}")
                if move_value > best_value:
                    best_value = move_value
                    best_move = idx
                    best_child = child
        elif self.isAlfaBeta:
            # Nākotnē: implementēt alfa_beta algoritmu
            for idx, child in enumerate(self.tree["children"]):
                # move_value = self.alfa_beta(child, self.depth - 1, float("-inf"), float("inf"), False)
                # print(f"Gājiens {idx}: Stāvoklis {child['state']}, Score {child['score']}, Vērtība {move_value}")
                # if move_value > best_value:
                #     best_value = move_value
                #     best_move = idx
                #     best_child = child
                pass

        if best_child is not None:
            # Atjaunina spēles stāvokli pēc datora gājiena
            self.game_state = best_child["state"]
            self.player_score = best_child["score"]["player_score"]
            self.bank_score = best_child["score"]["bank_score"]
            print(f"Labākais gājiens: {best_move} ar vērtību {best_value}")
            print(f"Jaunais stāvoklis: {self.game_state}, Player Score: {self.player_score}, Bank Score: {self.bank_score}")
            return best_child
        else:
            print("Nav pieejamu gājienu.")
            return None

    # Spēlētāja gājiena ieviešanas vieta
    def player_move(self):
        pass

    # Datora gājiens
    def computer_move(self):
        self.choose_move()










