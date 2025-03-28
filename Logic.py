import random
from collections import defaultdict, deque


class Game():
    def __init__(self):
        # Galvenie spēles lauki
        self.game_state = []         # Pašreizējais spēles stāvoklis (skaitļu saraksts)
        self.choose_num = 0

        self.isMinMax = False         # Karogs: izmantot minimax algoritmu
        self.isAlfaBeta = False      # Karogs: izmantot alfa_beta algoritmu
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

    def choose_first_move(self):
        """
        Funkcija, kas ļauj izvēlēties, kurš sāks spēli.

        Ievadi:
          1 – ja vēlies sākt pats (spēlētājs kļūst par maksimizējošo),
          2 – ja datora gājiens sāk (dators kļūst par maksimizējošo).

        Funkcija iestata mainīgo self.is_maximizing atbilstoši izvēlei un atgriež izvēlēto vērtību.
        """
        valid = False
        choice = None
        while not valid:
            try:
                user_input = input("Kurš sāk spēli? Ievadi 1 (spēlētājs) vai 2 (dators): ")
                choice = int(user_input)
                if choice == 1 or choice == 2:
                    valid = True
                else:
                    print("Lūdzu, ievadi 1 vai 2.")
            except ValueError:
                print("Lūdzu, ievadi veselu skaitli (1 vai 2).")

        if choice == 1:
            # Spēlētājs sāk, tad viņš ir maksimizējošais
            self.is_maximizing = True
            print("Spēlētājs sāks spēli.")
        else:
            # Dators sāk, tad datoram ir maksimizējošā loma
            self.is_maximizing = False
            print("Dators sāks spēli.")

        return choice

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

            # Logic rules:
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
            Rekurzīva minimax algoritma ieviešana (bez maiņas starp maximizēšanu un minimizēšanu).
            Ja spēlētājs, kurš sāk (maksimizējošais), veic gājienus, tad visos rekursīvās izsaukumos tiek
            izmantota tā pati loma (True), tātad tiek vienmēr maksimizēta vērtība.
            Ja loma ir minimizējoša, tad vienmēr tiek izmantota False.

            Ja stāvoklis ir termināls (atlicis viens skaitlis), atgriež novērtējumu, izmantojot terminal_eval.
            Ja dziļuma robeža sasniegta (depth <= 0) vai bērnu nav, atgriež heuristisko vērtību.
            """
        # Termināls stāvoklis: atlicis viens skaitlis
        if len(node["state"]) == 1:
            return self.terminal_eval(node["score"])
        if not node["children"] or depth <= 0:
            return self.heuristic_eval(node)

        if is_maximizing:
            best_value = float("-inf")
            for child in node["children"]:
                # Nodarbojamies ar tādu pašu lomu (neatsaucoties uz pretinieku)
                value = self.minimax(child, depth - 1, True)
                best_value = max(best_value, value)
            return best_value
        else:
            best_value = float("inf")
            for child in node["children"]:
                value = self.minimax(child, depth - 1, False)
                best_value = min(best_value, value)
            return best_value


    # Alfa-beta algoritma ieviešana
    def alfa_beta(self, node, depth, alpha, beta, is_maximizing):
        """
            Alfa-beta algoritma rekurzīva ieviešana.
            Ja stāvoklis ir termināls (atlicis viens skaitlis), atgriež novērtējumu (1, -1 vai 0).
            Ja dziļuma robeža sasniegta (depth <= 0) vai bērnu nav, atgriež heuristisko vērtību.
            Maksimizējošajam spēlētājam tiek meklēta maksimālā vērtība,
            minimizējošajam – minimālā vērtība, izmantojot alfa-beta apgriezšanas tehnoloģiju.
            """
        # Terminālais stāvoklis: atlicis viens skaitlis
        if len(node["state"]) == 1:
            return self.terminal_eval(node["score"])

        # Ja bērnu nav, atgriežam heuristisko vērtību (drošības pārbaude)
        if not node["children"]:
            return self.heuristic_eval(node)

        # Ja dziļuma robeža sasniegta vai kļuvusi negatīva, atgriežam heuristisko vērtību
        if depth <= 0:
            return self.heuristic_eval(node)

        # Maksimizējošā loma: meklējam maksimālo vērtību
        if is_maximizing:
            value = float("-inf")
            for child in node["children"]:
                # Rekursīvi izsaucam alfa_beta ar minimizējošu nākamo gājienu
                value = max(value, self.alfa_beta(child, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                # Ja beta ir mazāks vai vienāds ar alfa, pārtraucam gājienu (cut-off)
                if beta <= alpha:
                    break
            return value
        else:
            # Minimējošā loma: meklējam minimālo vērtību
            value = float("inf")
            for child in node["children"]:
                # Rekurzīvi izsaucam alfa_beta ar maksimizējošu nākamo gājienu
                value = min(value, self.alfa_beta(child, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                # Ja beta ir mazāks vai vienāds ar alfa, pārtraucam gājienu (cut-off)
                if beta <= alpha:
                    break
            return value

    # Izvēlas labāko gājienu, izmantojot minimax vai alfa-beta algoritmu
    def choose_move(self):
        """
            Ģenerē lēmumu koku pašreizējam stāvoklim, izmantojot dinamiski noteikto dziļumu,
            un pēc tam izvēlas labāko gājienu, izmantojot izvēlēto algoritmu – minimax vai alfa-beta.

            Saskaņā ar spēles noteikumiem:
              - Ja cilvēks sāk spēli (self.is_maximizing == True), tad cilvēks ir maksimizators,
                un datoram jāizvēlas gājiens kā minimizētājam.
              - Ja dators sāk spēli (self.is_maximizing == False), tad dators ir maksimizators.

            Pēc labākā gājiena izvēles atjaunina spēles stāvokli: game_state, player_score un bank_score.
            """
        # Atjaunina dziļumu, izmantojot dinamiski noteikto dziļumu
        current_depth = self.get_dynamic_depth()
        self.tree = self.generate_decision_tree(self.game_state, current_depth)

        best_move = None
        best_child = None
        best_value = None

        if self.isMinMax:
            # Ja cilvēks sāk, tad dators spēlē kā minimizētājs.
            if self.is_maximizing:
                best_value = float("inf")
                for idx, child in enumerate(self.tree["children"]):
                    # Nākamajā kārtā dators spēlē kā minimizētājs (parametr False)
                    move_value = self.minimax(child, current_depth - 1, False)
                    print(f"Gājiens {idx}: Stāvoklis {child['state']}, Score {child['score']}, Vērtība {move_value}")
                    if move_value < best_value:
                        best_value = move_value
                        best_move = idx
                        best_child = child
            # Ja dators sāk, tad dators spēlē kā maksimizētājs.
            else:
                best_value = float("-inf")
                for idx, child in enumerate(self.tree["children"]):
                    # Nākamajā kārtā dators spēlē kā maksimizētājs (parametr True)
                    move_value = self.minimax(child, current_depth - 1, True)
                    print(f"Gājiens {idx}: Stāvoklis {child['state']}, Score {child['score']}, Vērtība {move_value}")
                    if move_value > best_value:
                        best_value = move_value
                        best_move = idx
                        best_child = child
        elif self.isAlfaBeta:
            if self.is_maximizing:
                best_value = float("inf")
                for idx, child in enumerate(self.tree["children"]):
                    move_value = self.alfa_beta(child, current_depth - 1, float("-inf"), float("inf"), False)
                    print(f"Gājiens {idx}: Stāvoklis {child['state']}, Score {child['score']}, Vērtība {move_value}")
                    if move_value < best_value:
                        best_value = move_value
                        best_move = idx
                        best_child = child
            else:
                best_value = float("-inf")
                for idx, child in enumerate(self.tree["children"]):
                    move_value = self.alfa_beta(child, current_depth - 1, float("-inf"), float("inf"), True)
                    print(f"Gājiens {idx}: Stāvoklis {child['state']}, Score {child['score']}, Vērtība {move_value}")
                    if move_value > best_value:
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
        self.choose_move()

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

    def reset_game(self):
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
        self.player_score = 0
        self.bank_score = 0
        self.tree = None
        self.levels = {}

        restart = input("Vai vēlaties sākt jaunu spēli? (jā/nē): ")
        if restart.lower() in ["jā", "ja", "y", "yes"]:
            return True
        else:
            return False







