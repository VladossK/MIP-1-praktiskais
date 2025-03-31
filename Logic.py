import random

class Game():
    def __init__(self):
        """
            Inicializē spēles loģiku.
        """
        self.game_state = []
        self.current_turn = "player"
        self.max_player = "player"

        self.isMinMax = False
        self.isAlfaBeta = False
        self.is_maximizing = True

        self.bank_score = 0
        self.common_score = 0

        self.length = 15
        self.depth = 3
        self.tree = None

    def choose_length(self, length):
        self.length = length
        return self.length

    def set_algorithm(self, choice):
        """
            Parametri:
                choice (str): "1" – Minimax algoritms, "2" – Alfa-beta algoritms.
        """
        if choice == 1:
            self.isMinMax = True
            self.isAlfaBeta = False
            print("Izvēlēts Minimax algoritms.")
        elif choice == 2:
            self.isMinMax = False
            self.isAlfaBeta = True
            print("Izvēlēts Alfa-beta algoritms.")
        else:
            print("Wrong choose")

    def generate_numbers(self, length):
        """
            Ģenerē nejaušu skaitļu (no 1 līdz 9) sarakstu ar norādīto garumu (no 15 līdz 25)    .
            Output piemērs:
                [3, 7, 1, 9, 4, 5, 2, 8, 6, 1, 3, 7, 4, 2, 9]
        """
        if not (15 <= length <= 25):
            raise ValueError("Garumam ir jabūt no 15 līdz 25")
        self.game_state = [random.randint(1, 9) for _ in range(length)]
        return self.game_state

    def generate_decision_tree(self, game_state, depth, score=None):
        """
            Ģenerē lēmumu koku, balstoties uz skaitļu sarakstu, dziļumu un pašreizējo punktu vērtību.
            Katrs mezgls satur:
                "state": skaitļu saraksts,
                "score": vārdnīcu {"common_score": ..., "bank_score": ...},
                "children": apakšmezglu sarakstu.
        """
        if score is None:
            score = {"common_score": self.common_score, "bank_score": self.bank_score}
        node = {"state": game_state.copy(), "score": score.copy(), "children": []}

        if depth == 0 or len(game_state) == 1:
            return node

        for i in range(len(game_state) - 1):
            current_state = game_state.copy()
            x = current_state.pop(i)
            y = current_state.pop(i)
            pair_sum = x + y

            new_score = score.copy()

            if pair_sum > 7:
                current_state.insert(i, 1)
                new_score["common_score"] += 1
            elif pair_sum < 7:
                current_state.insert(i, 3)
                new_score["common_score"] -= 1
            else:
                current_state.insert(i, 2)
                new_score["bank_score"] += 1

            child_tree = self.generate_decision_tree(current_state, depth - 1, new_score)
            node["children"].append(child_tree)

        return node


    def terminal_eval(self, score):
        """
            Terminālā stāvokļa novērtējums.
            Ja gan common_score, gan bank_score ir pāra skaitļi, atgriež +1 (uzvara spēlētājam, kurš sācis).
            Ja gan common_score, gan bank_score ir nepāra skaitļi, atgriež -1 (uzvara otram spēlētājam).
            Citos gadījumos atgriež 0 (Draw).
        """
        if (score["common_score"] % 2 == 0) and (score["bank_score"] % 2 == 0):
            return 1
        elif (score["common_score"] % 2 == 1) and (score["bank_score"] % 2 == 1):
            return -1
        else:
            return 0

    def heuristic_eval(self, node):
        """
            Heuristiska novērtēšana mezglam, pamatojoties uz common_score un bank_score vērtībām.
        """
        common_score = node["score"]["common_score"]
        bank_score = node["score"]["bank_score"]

        eval_score = common_score * 20

        if common_score % 2 == 0:
            eval_score += 15
        else:
            eval_score -= 15

        if bank_score % 2 == 0:
            eval_score += 10
        else:
            eval_score -= 10

        return eval_score

    def minimax(self, node, depth, is_maximizing):
        """
            Minimaks algoritma rekursīvā implementācija.

            Parametri:
                node (dict): Pašreizējā lēmumu koka mezgla stāvoklis.
                depth (int): Meklēšanas dziļums.
                is_maximizing (bool): Vai pašreizējais spēlētājs ir maksimizējošais.

            Output:
                int: Novērtējuma vērtība, ko minimaks algoritms aprēķināja.
        """
        if len(node["state"]) == 1:
            return self.terminal_eval(node["score"])

        if depth <= 0 or not node["children"]:
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



    def alfa_beta(self, node, depth, alpha, beta, is_maximizing):
        """
            Alfa-beta algoritma implementācija ar novēršanu, optimizējot minimaks meklēšanu.
            Parametri:
                node (dict): Pašreizējā lēmumu koka mezgla stāvoklis.
                depth (int): Meklēšanas dziļums.
                alpha (float): Alfa vērtība.
                beta (float): Beta vērtība.
                is_maximizing (bool): Vai pašreizējais spēlētājs ir maksimizējošais.
            Output:
                int: Novērtējuma vērtība, ko alfa-beta algoritms aprēķināja.
        """
        if len(node["state"]) == 1:
            return self.terminal_eval(node["score"])

        if depth <= 0 or not node["children"]:
            return self.heuristic_eval(node)

        if is_maximizing:
            value = float("-inf")
            for child in node["children"]:
                value = max(value, self.alfa_beta(child, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value
        else:
            value = float("inf")
            for child in node["children"]:
                value = min(value, self.alfa_beta(child, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value


    def choose_move(self):
        """
            Izvēlas labāko gājienu, izmantojot izvēlēto algoritmu (minimax vai alfa-beta).

            Atjauno spēles stāvokli (game_state), common_score un bank_score,
            un izvada datora izvēlēto gājienu informāciju.

            Output:
                dict: Labākā gājiena lēmumu koka mezgls, ja tas ir atrasts.
        """
        current_depth = self.get_dynamic_depth()
        self.tree = self.generate_decision_tree(self.game_state, current_depth)

        best_move = None
        best_child = None

        is_computer_max = (self.max_player == "computer")

        if self.isMinMax:
            if is_computer_max:
                best_value = float("-inf")
                for idx, child in enumerate(self.tree["children"]):
                    move_value = self.minimax(child, current_depth - 1, False)
                    print(f"Gājiens {idx}: Stāvoklis {child['state']}, Score {child['score']}, Vērtība {move_value}")
                    if move_value > best_value:
                        best_value = move_value
                        best_move = idx
                        best_child = child
            else:
                best_value = float("inf")
                for idx, child in enumerate(self.tree["children"]):
                    move_value = self.minimax(child, current_depth - 1, True)
                    print(f"Gājiens {idx}: Stāvoklis {child['state']}, Score {child['score']}, Vērtība {move_value}")
                    if move_value < best_value:
                        best_value = move_value
                        best_move = idx
                        best_child = child

        elif self.isAlfaBeta:
            if is_computer_max:
                best_value = float("-inf")
                for idx, child in enumerate(self.tree["children"]):
                    move_value = self.alfa_beta(child, current_depth - 1, float("-inf"), float("inf"), False)
                    print(f"Gājiens {idx}: Stāvoklis {child['state']}, Score {child['score']}, Vērtība {move_value}")
                    if move_value > best_value:
                        best_value = move_value
                        best_move = idx
                        best_child = child
            else:
                best_value = float("inf")
                for idx, child in enumerate(self.tree["children"]):
                    move_value = self.alfa_beta(child, current_depth - 1, float("-inf"), float("inf"), True)
                    print(f"Gājiens {idx}: Stāvoklis {child['state']}, Score {child['score']}, Vērtība {move_value}")
                    if move_value < best_value:
                        best_value = move_value
                        best_move = idx
                        best_child = child

        if best_child is not None:
            self.game_state = best_child["state"]
            self.common_score = best_child["score"]["common_score"]
            self.bank_score = best_child["score"]["bank_score"]
            # for GUI
            self.last_computer_move = f"Dators izveleja gājenu {best_move}: stavoklis {self.game_state} (value: {best_value})"
            print(f"\nLabākais gājiens: {best_move} (vērtība: {best_value})")
            print(f"Stāvoklis pēc gājiena: {self.game_state}")
            print(f"Kopējais rezultāts: {self.common_score}, Banka: {self.bank_score}\n")
            return best_child
            return None


    def get_dynamic_depth(self):
        """
            Aprēķina dinamisko meklēšanas dziļumu, balstoties uz pašreizējo masīva garumu.

            Output:
                int: Meklēšanas dziļums.
        """
        n = len(self.game_state)
        if n <= 9:
            self.depth = n - 1
        elif n <= 15:
            self.depth = 5
        elif n <= 20:
            self.depth = 4
        else:
            self.depth = 3
        return self.depth

    def reset_game(self, restart=True):
        """
            Atiestata spēles loģiku uz sākotnējo stāvokli.

            Notīra game_state, common_score, bank_score, lēmumu koku (tree) un citus papildus mainīgos.

            Output:
                bool: restart vērtības.
        """
        self.game_state = []
        self.common_score = 0
        self.bank_score = 0
        self.tree = None
        return restart




























