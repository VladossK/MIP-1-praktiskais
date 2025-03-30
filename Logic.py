import random
from collections import defaultdict, deque


class Game():
    def __init__(self):
        """
            Inicializē spēles galvenos laukus.
                - spēles stāvokli (game_state),
                - pašreizējo gājiena kārtu (current_turn) un spēles sākšanas informāciju (max_player),
                - algoritma izvēles karogus (isMinMax, isAlfaBeta),
                - punktu skaitītājus: common_score un bank_score,
                - meklēšanas dziļumu (depth), lēmumu koku (tree) un līmeņus (levels).
        """
        self.game_state = []         # Pašreizējais spēles stāvoklis (skaitļu saraksts)
        self.current_turn = "player"
        self.max_player = "player"


        self.isMinMax = False         # Karogs: izmantot minimax algoritmu
        self.isAlfaBeta = False      # Karogs: izmantot alfa_beta algoritmu
        self.is_maximizing = True    # Spēlētājs, kurš sācis spēli, tiek uzskatīts par maksimizējošo

        self.bank_score = 0          # Bankas punkti (kad summa == 7)
        self.common_score = 0        # Spēlētāja punkti (kad summa <7 vai >7)

        self.length = 15
        self.depth = 3            # Var mainīt meklēšanas dziļumu pēc nepieciešamības
        self.tree = None
        self.levels = {}

    # Izvēlas masīva garumu (no 15 līdz 25)
    def choose_length(self, length):
        self.length = length
        return self.length


    def set_algorithm(self, choice):
        """
        Iestata algoritmu, kuru izmantot, atkarībā no parametra choice.

        Parametri:
            choice (str): "1" – Minimax algoritms, "2" – Alfa-beta algoritms.

        Iestata atbilstošos karogus: self.isMinMax un self.isAlfaBeta.
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
            print("Nepareiza izvēle. Lūdzu, izvēlies \"1\" vai \"2\".")


    # Ģenerē nejaušu skaitļu sarakstu
    def generate_numbers(self, length):
        """
        Ģenerē nejaušu skaitļu (no 1 līdz 9) sarakstu ar norādīto garumu (no 15 līdz 25)    .
        Output piemērs:
            [3, 7, 1, 9, 4, 5, 2, 8, 6, 1, 3, 7, 4, 2, 9]
        """
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
          "score": vārdnīcu {"common_score": ..., "bank_score": ...},
          "children": apakšmezglu sarakstu.
        """
        if score is None:
            score = {"common_score": self.common_score, "bank_score": self.bank_score}
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

            # Logic rules:
            if pair_sum > 7:
                current_state.insert(i, 1)
                new_score["common_score"] += 1
            elif pair_sum < 7:
                current_state.insert(i, 3)
                new_score["common_score"] -= 1
            else:  # pair_sum == 7
                current_state.insert(i, 2)
                new_score["bank_score"] += 1

            child_tree = self.generate_decision_tree(current_state, depth - 1, new_score)
            node["children"].append(child_tree)

        return node


    def split_tree_by_levels(self, tree):
        """
            Sadala koku pa līmeņiem, izmantojot BFS (platuma meklēšanu).
            Atgriež vārdnīcu, kur atslēga ir līmeņa numurs, un vērtība ir mezglu saraksts.
        """
        levels = defaultdict(list)
        # Iniciējam rindu ar saknes mezglu un līmeni 0
        queue = deque([(tree, 0)])

        # Kamēr rinda nav tukša, apstrādājam katru mezglu
        while queue:
            node, depth = queue.popleft()
            levels[depth].append(node)
            # Pievienojam visus bērnu mezglus ar palielinātu līmeni
            for child in node.get("children", []):
                queue.append((child, depth + 1))

        # Atgriežam vārdnīcu kā parastu
        return dict(levels)

    def terminal_eval(self, score):
        """
        Terminālā stāvokļa novērtējums.
        Ja gan common_score, gan bank_score ir pāra skaitļi, atgriež +1 (uzvara spēlētājam, kurš sācis).
        Ja gan common_score, gan bank_score ir nepāra skaitļi, atgriež -1 (uzvara otram spēlētājam).
        Citos gadījumos atgriež 0 (neizšķirts).
        """
        if (score["common_score"] % 2 == 0) and (score["bank_score"] % 2 == 0):
            return 1
        elif (score["common_score"] % 2 == 1) and (score["bank_score"] % 2 == 1):
            return -1
        else:
            return 0

    # Heuristiskā novērtēšanas funkcija ne termināliem stāvokļiem
    def heuristic_eval(self, node):
        common_score = node["score"]["common_score"]
        bank_score = node["score"]["bank_score"]

        eval_score = common_score * 20

        # Ясно различаем четность обоих счетчиков
        if common_score % 2 == 0:
            eval_score += 15
        else:
            eval_score -= 15

        if bank_score % 2 == 0:
            eval_score += 10
        else:
            eval_score -= 10

        # Особое внимание финальным позициям: >???
        if len(node["state"]) == 1:
            if common_score % 2 == 0 and bank_score % 2 == 0:
                eval_score += 200  # Победа – очень много
            elif common_score % 2 == 1 and bank_score % 2 == 1:
                eval_score -= 200  # Поражение – очень плохо
            else:
                eval_score += 50  # Ничья лучше, чем просто проигрыш

        return eval_score

    # Minimax algoritma rekurzīvā ieviešana
    def minimax(self, node, depth, is_maximizing):
        # Только если состояние реально терминальное (1 число), вызываем terminal_eval
        if len(node["state"]) == 1:
            return self.terminal_eval(node["score"])

        # Если глубина исчерпана, используем heuristic_eval (никогда terminal_eval!)
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



    # Izvēlas labāko gājienu, izmantojot minimax vai alfa-beta algoritmu
    def choose_move(self):
        current_depth = self.get_dynamic_depth()
        self.tree = self.generate_decision_tree(self.game_state, current_depth)

        best_move = None
        best_child = None

        # Ключевое исправление: компьютер максимизатор, если он начал игру
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
            # Для GUI
            self.last_computer_move = f"Dators izveleja gājenu {best_move}: stavoklis {self.game_state} (value: {best_value})"
            print(f"\nLabākais gājiens: {best_move} (vērtība: {best_value})")
            print(f"Stāvoklis pēc gājiena: {self.game_state}")
            print(f"Kopējais rezultāts: {self.common_score}, Banka: {self.bank_score}\n")
            return best_child
        else:
            print("Nav pieejamu gājienu.")
            return None


    # Spēlētāja gājiena ieviešanas vieta
    #Gruti realizēt GUI (DELETE NAKOTNE)
    def player_move(self):
        """
            Spēlētāja gājiens:
            - Parāda pašreizējo stāvokli ar indeksiem (skaitīšana sākas no 1).
            - Pieprasa ievadīt pāra sākuma indeksu.
            - Veic gājienu pēc noteikumiem un atjaunina stāvokli, common_score un bank_score.
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
            self.common_score += 1
        elif pair_sum < 7:
            new_val = 3
            self.common_score -= 1
        else:  # pair_sum == 7
            new_val = 2
            self.bank_score += 1

        current_state.insert(i, new_val)
        self.game_state = current_state
        print("Tavs gājiens veiksmīgs!")
        print("Jaunais stāvoklis:", self.game_state)
        print("Player Score:", self.common_score, "Bank Score:", self.bank_score)

    def computer_move(self):
        # Ja lietotājs sāk spēli (self.is_maximizing ir True), tad datora loma ir minimizējoša.
        # Tāpēc izsaucam choose_move ar is_max_turn = False.
        self.choose_move()

    def get_dynamic_depth(self):
        """
            Nosaka dinamiski dziļumu, balstoties uz pašreizējo spēles stāvokli.
            Ja skaitļu skaits ir liels, atgriež mazāku dziļumu, bet, ja mazs – lielāku.
            Funkcija atjauno self.depth un atgriež to.
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

    # GRUTI REALIZET GUI (DELETE NAKOTNE)
    def reset_game(self, restart=True):
        """
        Atiestata visus spēles rādītājus un piedāvā sākt jaunu spēli.
        Šī funkcija:
          - Notīra pašreizējo spēles stāvokli (game_state),
          - Atiestata spēlētāja un bankas punktus uz 0,
          - Notīra lēmumu koku (tree) un līmeņus (levels),
          - Piedāvā lietotājam izvēlēties, vai sākt jaunu spēli.

        Atgriež:
          True, ja lietotājs izvēlas sākt jaunu spēli, pretējā gadījumā False.
        """
        self.game_state = []
        self.common_score = 0
        self.bank_score = 0
        self.tree = None
        self.levels = {}
        return restart





























