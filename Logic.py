import random
from collections import deque


class Game():
    def __init__(self):
        # Galvenie spēles lauki
        self.num_list = []
        self.choose_num = 0

        self.isMinMax = False
        self.isAlfaBeta = False
        self.is_maximizing = False

        self.bank_score = 0  # par summu == 7
        self.points = 0  # par summu < 7 vai > 7

        self.minimax = False
        self.is_maximizing = False

        self.isOdd = False
        self.isEven = False

        self.length = 15
        self.depth = 0
        self.tree = None
        self.levels = {}

# Izvēlamies masīva garumu (starp 15 un 25)
    def choose_length(self, length):
        self.length = length
        return self.length

    # Izvēlamies dziļumu algoritmam
    def choose_depth(self, depth):
        self.depth = depth
        return self.depth

    # Ģenerējam nejaušu skaitļu masīvu
    def generate_numbers(self, length):
        if not (15 <= length <= 25):
            raise ValueError("Length must be between 15-25")
        self.num_list = [random.randint(1, 9) for _ in range(length)]
        return self.num_list

    # Ģenerējam lēmumu koku (pēc jūsu loģikas)
    def generate_decision_tree(self, num_list, depth):
        """
            Ģenerē lēmumu koku, balstoties uz skaitļu sarakstu un dziļumu.

            Parametri:
                num_list (list): Skaitļu saraksts, no kura veido koku.
                depth (int): Koka dziļums.

            Atgriež:
                dict: Koka struktūra ar atslēgām "state" un "children".
            """
        if depth == 0:
            return {
                "state": num_list,
                "children": []
            }

        tree = {
            "state": num_list.copy(),
            "children": []
        }

        for i in range(len(num_list) - 1):
            current_list = num_list.copy()
            x, y = current_list[i], current_list[i + 1]
            pair_sum = x + y

            # Dzēšam izvēlētos divus skaitļus
            del current_list[i]
            del current_list[i]

            # Pārveidojam atkarībā no summas
            if pair_sum > 7:
                current_list.insert(i, 1)
            elif pair_sum < 7:
                current_list.insert(i, 3)
            else:  # pair_sum == 7
                current_list.insert(i, 2)

            child_tree = self.generate_decision_tree(current_list, depth - 1)
            tree["children"].append(child_tree)

        self.tree = tree
        return tree

    def split_tree_by_levels(self, tree):
        """
            Sadalīt koku pa līmeņiem.

            Parametri:
                tree (dict): Koka saknes mezgls ar atslēgām "state" un "children".

            Atgriež:
                levels (list): Saraksts, kur katrs elements ir saraksts ar mezgliem attiecīgajā līmenī.
            """
        levels = []
        current_level = [tree]  # Начинаем с корневого узла

        while current_level:
            levels.append(current_level)
            next_level = []
            for node in current_level:
                next_level.extend(node.get("children", []))
            current_level = next_level

        return levels


# Koka optimizācija (kopīgu apakškoku sapludināšana)
    def optimize_tree_hnf(self, root):
        pass

    # Minimax metodes sagatave (lai varētu izmantot, ja isMinMax = True)
    def minimax(self, node, depth, is_maximizing):
        """
        Šeit var ieviest minimax loģiku:
        1. Ja dziļums ir 0 vai gala stāvoklis, atgriežam novērtējuma funkciju.
        2. Ja is_maximizing (mēģinām maksimizēt):
           - Izejam cauri katram bērnam
           - Aprēķinām minimax bērnam (depth - 1, False)
           - Izvēlamies maksimālo rezultātu
        3. Pretējā gadījumā (minimizētājs):
           - Izejam cauri katram bērnam
           - Aprēķinām minimax bērnam (depth - 1, True)
           - Izvēlamies minimālo rezultātu
        """
        pass

    # Alfa-Beta metodes iezīme
    def alfa_beta(self, node, depth, alpha, beta, is_maximizing):
        """
        Alfa-Beta algoritma loģika:
        1. Ja dziļums = 0 vai sasniegts gala stāvoklis, atgriežam novērtējuma vērtību.
        2. Ja is_maximizing:
           - Iniciējam value = -∞
           - Izejam cauri bērniem:
             -- value = max(value, alfa_beta(bērns, depth-1, alpha, beta, False))
             -- alpha = max(alpha, value)
             -- ja beta <= alpha, pārtraucam (break) -> atgriežam value
        3. Ja minimizējošais spēlētājs:
           - Iniciējam value = +∞
           - Izejam cauri bērniem:
             -- value = min(value, alfa_beta(bērns, depth-1, alpha, beta, True))
             -- beta = min(beta, value)
             -- ja beta <= alpha, pārtraucam (break) -> atgriežam value
        4. Atgriežam value
        """
        pass

    # Labākā gājiena izvēle
    def choose_move(self):
        """
        Loģikas soļi, izmantojot minētos algoritmus:
        1. Pārbaudām, vai isMinMax = True -> izmantojam minimax
        2. Ja isAlfaBeta = True -> izmantojam alfa_beta
        3. Apstrādājam rezultātu, atlasām labāko gājienu
        4. Atgriežam (vai tieši izpildām) labāko kustību, kas ietekmēs num_list
        """
        # Piemērs ar komentāriem:
        # if self.isMinMax:
        #     # Izsaucam minimax uz šī brīža koka saknes
        #     # Rezultātā iegūstam labāko iespējamo gājienu saskaņā ar minimax
        #     pass
        #
        # if self.isAlfaBeta:
        #     # Izsaucam alfa_beta ar atbilstošiem parametriem
        #     # Rezultātā iegūstam labāko gājienu, ņemot vērā alfa-beta atgriežamo vērtību
        #     pass
        #
        # Gājiena izvēle (kuru pāri no masīva ņemt) balstās uz novērtējumu,
        # ko atgriež viens no augšējiem algoritmiem.
        pass

    # Spēlētāja gājiens (pagaidu sagatave)
    def player_move(self):
        # Loģika:
        # 1. Izvēlēties divus blakus esošus skaitļus
        # 2. Saskaitīt tos, aizstāt atbilstoši noteikumiem
        # 3. Atjaunināt bank_score un points
        # 4. Pārbaudīt, vai nav palicis tikai viens elements
        pass

    # Datora gājiens (pagaidu sagatave)
    def computer_move(self):
        # 1. Ja isMinMax vai isAlfaBeta, izmantojam choose_move(), lai noteiktu labāko pāri
        # 2. Pielietojam tās pašas aizstāšanas un bank_score/points atjaunošanas darbības
        # 3. Pārbaudām, vai nav palicis tikai viens elements
        pass












