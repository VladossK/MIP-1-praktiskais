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
        self.depth = 3            # Var mainīt meklēšanas dziļumu pēc nepieciešamības
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
        if (score["player_score"] % 2 == 0) and (score["bank_score"] % 2 == 0):
            return 1
        elif (score["player_score"] % 2 == 1) and (score["bank_score"] % 2 == 1):
            return -1
        else:
            return 0


    # Heuristiskā novērtēšanas funkcija ne termināliem stāvokļiem
    def heuristic_eval(self, node):
        # Piemēram, var novērtēt kā player_score - bank_score
        return node["score"]["player_score"] - node["score"]["bank_score"]

    # Minimax algoritma rekurzīvā ieviešana
    def minimax(self, node, depth, is_maximizing):
        """
        Rekurzīva minimax algoritma ieviešana.
        Ja stāvoklis ir termināls (atlicis viens skaitlis), atgriež novērtējumu (1, -1 vai 0).
        Ja dziļuma robeža sasniegta (depth <= 0) vai nav bērnu, atgriežam heuristisko vērtību.
        """
        # Termināls stāvoklis: atlicis viens skaitlis
        if len(node["state"]) == 1:
            return self.terminal_eval(node["score"])
        # Ja bērnu nav, atgriežam heuristisko vērtību (drošības pārbaude)
        if not node["children"]:
            return self.heuristic_eval(node)
        # Ja dziļuma robeža sasniegta vai kļuvusi negatīva, atgriežam heuristisko vērtību
        if depth <= 0:
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
    def choose_move(self, is_max_turn=None):
        """
        Ģenerē lēmumu koku pašreizējam stāvoklim, izmantojot dinamiski noteikto dziļumu,
        un pēc tam izvēlas labāko gājienu, balstoties uz spēlētāja lomu, kuru norāda is_max_turn.
        Ja is_max_turn ir True, tiek meklēts gājiens ar maksimālo vērtību;
        pretējā gadījumā – gājiens ar minimālo vērtību.
        Pēc labākā gājiena izvēles atjaunina spēles stāvokli:
          game_state, player_score un bank_score.
        """
        # Ja parametrs netiek norādīts, lieto sākotnējo lomu
        if is_max_turn is None:
            is_max_turn = self.is_maximizing

        dynamic_depth = self.get_dynamic_depth()
        self.tree = self.generate_decision_tree(self.game_state, dynamic_depth)

        best_move = None
        best_child = None

        if is_max_turn:
            best_value = float("-inf")
            for idx, child in enumerate(self.tree["children"]):
                # Nākamajā kārtā pretinieks būs minimizējošais
                move_value = self.minimax(child, self.depth - 1, False)
                print(f"Gājiens {idx}: Stāvoklis {child['state']}, Score {child['score']}, Vērtība {move_value}")
                if move_value > best_value:
                    best_value = move_value
                    best_move = idx
                    best_child = child
        else:
            best_value = float("inf")
            for idx, child in enumerate(self.tree["children"]):
                # Nākamajā kārtā pretinieks būs maksimizējošais
                move_value = self.minimax(child, self.depth - 1, True)
                print(f"Gājiens {idx}: Stāvoklis {child['state']}, Score {child['score']}, Vērtība {move_value}")
                if move_value < best_value:
                    best_value = move_value
                    best_move = idx
                    best_child = child

        if best_child is not None:
            # Atjaunina spēles stāvokli pēc datora gājiena
            self.game_state = best_child["state"]
            self.player_score = best_child["score"]["player_score"]
            self.bank_score = best_child["score"]["bank_score"]
            print(f"Labākais gājiens: {best_move} ar vērtību {best_value}")
            print(
                f"Jaunais stāvoklis: {self.game_state}, Player Score: {self.player_score}, Bank Score: {self.bank_score}")
            return best_child
        else:
            print("Nav pieejamu gājienu.")
            return None


    # Spēlētāja gājiena ieviešanas vieta
    def player_move(self):
        """
            Spēlētāja gājiens:
            - Parāda pašreizējo stāvokli ar indeksiem (skaitīšana sākas no 1).
            - Pieprasa ievadīt pāra sākuma indeksu.
            - Veic gājienu pēc noteikumiem un atjaunina stāvokli, player_score un bank_score.
        """
        if len(self.game_state) <= 1:
            print("Spēle jau ir beigusies.")
            return

        # Parāda pašreizējo stāvokli ar indeksiem
        print("Pašreizējais stāvoklis:")
        for i, num in enumerate(self.game_state, start=1):
            print(f"{i}: {num}", end="  ")
        print("\nIzvēlies pāra sākuma indeksu (no 1 līdz {})".format(len(self.game_state) - 1))

        valid = False
        while not valid:
            try:
                idx = int(input("Ievadi indeksu: "))
                if 1 <= idx <= len(self.game_state) - 1:
                    valid = True
                else:
                    print("Nepareizs indeks. Mēģini vēlreiz.")
            except ValueError:
                print("Lūdzu, ievadi veselu skaitli.")

        # Pārvēršam ievadīto indeksu par nulles bāzes indeksu
        i = idx - 1
        current_state = self.game_state.copy()
        # Noņem divus blakus esošus skaitļus
        x = current_state.pop(i)
        y = current_state.pop(i)
        pair_sum = x + y

        # Piemēro gājiena noteikumus un atjaunina punktu vērtības
        if pair_sum > 7:
            new_val = 1
            self.player_score += 1
        elif pair_sum < 7:
            new_val = 3
            self.player_score -= 1
        else:  # pair_sum == 7
            new_val = 2
            self.bank_score += 1

        current_state.insert(i, new_val)
        self.game_state = current_state
        print("Tavs gājiens veiksmīgs!")
        print("Jaunais stāvoklis:", self.game_state)
        print("Player Score:", self.player_score, "Bank Score:", self.bank_score)

    def computer_move(self):
        # Ja lietotājs sāk spēli (self.is_maximizing ir True), tad datora loma ir minimizējoša.
        # Tāpēc izsaucam choose_move ar is_max_turn = False.
        self.choose_move(is_max_turn=not self.is_maximizing)

    def get_dynamic_depth(self):
        """
            Nosaka dinamiski dziļumu, balstoties uz pašreizējo spēles stāvokli.
            Ja skaitļu skaits ir liels, atgriež mazāku dziļumu, bet, ja mazs – lielāku.
            Funkcija atjauno self.depth un atgriež to.
            """
        n = len(self.game_state)
        if n <= 9:
            self.depth = n - 1  # Maksimālā dziļuma vērtība, pilna meklēšana
        elif n <= 15:
            self.depth = 5
        elif n <= 20:
            self.depth = 4
        else:
            self.depth = 3
        return self.depth







