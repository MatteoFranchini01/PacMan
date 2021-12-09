import Sliterlinkv3 as s
import unittest


class ControlWinTest(unittest.TestCase):

    def test_incroci_win(self):
        """"
        verifica la funzione che controlla le linee attorno ai +,
        in particolare verifica la vittoria della partita
        """
        lista_win = []
        game = s.Slitherlink()
        with open("game_win_5x5.txt") as w:
            for line in w:
                board_w = line.strip("\n")
                lista_win += board_w
        game._board = lista_win
        self.assertTrue(game.control_plus() == True)

    def test_incroci_lose(self):
        """
        verifica la funziona che controlla le linee attorno ai +,
        in particolare verifica la non vittoria e quindi la
        continuazione della partita
        """

        lista_l = []
        game = s.Slitherlink()
        with open("game_nowin_5x5.txt") as l:
            for line in l:
                board_l = line.strip("\n")
                lista_l += board_l
        game._board = lista_l
        self.assertTrue(game.control_plus() == False)

    def test_num_loose(self):
        """
        verifica i vincoli numerici, controllando se vi è il
        giusto numero di linee intorno a tutti i numeri della matrice,
        questo test in particolare controlla la non vittoria della partita
        e quindi indirettamente la non comparsa del messaggio di vittoria
        """
        game = s.Slitherlink()
        lista = []
        with open("game_5x5.txt") as g:
            for line in g:
                board = line.strip("\n")
                lista += board
        game._board = lista
        game.play_at(3, 0)
        self.assertTrue(game.finished() == False)

    def test_num_win(self):
        """
        verifica i vincoli numerici, controllando se vi è il
        giusto numero di linee intorno a tutti i numeri della matrice,
        questo test in particolare controlla la vittoria della partita
        """
        game = s.Slitherlink()
        lista = []
        with open("game_half_win_num_5x5.txt") as g:
            for line in g:
                board = line.strip("\n")
                lista += board
        game._board = lista
        game.play_at(7, 10)
        self.assertTrue(game.finished() == True)

    def test_anello_win(self):
        """
        verifica il fatto che la partita sia vinta se e solo se viene
        completato un singolo anello, per fare questo viene simulata
        un'intera partita partendo dalla board bianca ed inserendo tutte
        le linee necessarie
        """
        game = s.Slitherlink()
        lista = []
        with open("game_5x5.txt") as g:
            for line in g:
                board = line.strip("\n")
                lista += board
        game._board = lista
        lista_win = [(1, 10), (3, 10), (0, 9), (4, 9),
                 (0, 7), (1, 6), (2, 5), (1, 4), (0, 3), (1, 2),
                 (2, 1), (4, 1), (4, 5), (5, 6), (5, 4), (5, 8),
                 (6, 9), (7, 10), (9, 10), (10, 9), (9, 8), (8, 7),
                 (7, 6), (9, 4), (7, 4), (10, 3), (10, 1), (9, 0),
                 (8, 1), (7, 2), (5, 2), (3, 0)]
        for i in lista_win:
            x, y = i
            game.play_at(x, y)
            with self.subTest("Controllo vittoria partita"):
                if i != (3, 0):
                    self.assertTrue(game.finished() == False)
                else:
                    self.assertTrue(game.finished() == True)
            with self.subTest("Controllo del loop"):
                if i != (3, 0):
                    self.assertTrue(game.control_loop() == False)
                else:
                    self.assertTrue(game.control_loop() == True)

    def test_anello_lose(self):
        """
        verifica il fatto che la partita sia vinta se e solo se viene
        completato un singolo anello, per fare questo viene simulata
        un'intera partita partendo dalla board bianca ed inserendo tutte
        le linee necessarie tranne una per verificare che la partita rimanga
        aperta e che non risulti vinta
        """
        game = s.Slitherlink()
        lista = []
        with open("game_5x5.txt") as g:
            for line in g:
                board = line.strip("\n")
                lista += board
        game._board = lista
        lista_not_win = [(1, 10), (3, 10), (0, 9), (4, 9),
                     (0, 7), (1, 6), (2, 5), (1, 4), (0, 3), (1, 2),
                     (2, 1), (4, 1), (4, 5), (5, 6), (5, 4), (5, 8),
                     (6, 9), (7, 10), (9, 10), (10, 9), (9, 8), (8, 7),
                     (7, 6), (9, 4), (7, 4), (10, 3), (10, 1), (9, 0),
                     (8, 1), (7, 2), (5, 2)]
        for i in lista_not_win:
            x, y = i
            game.play_at(x, y)
            with self.subTest("Controllo vittoria partita"):
                self.assertTrue(game.finished() == False)

            with self.subTest("Controllo dei loop"):
                self.assertTrue(game.control_loop() == False)


class ControlAutoTest(unittest.TestCase):

    def test_incrocio_click(self):
        """
        verifica il corretto autocompletamento, ovvero il posizionamento
        delle "x" nelle caselle vuote quando intorno al "+" ci sono
        già due linee, dopo aver cliccato su un incorcio "+"
        """
        game = s.Slitherlink()
        lista = []
        with open("game_win_5x5.txt") as g:
            for line in g:
                board = line.strip("\n")
                lista += board
        game._board = lista
        game.auto(4, 2)
        self.assertTrue(game.value_at(3, 2) == "x" and game.value_at(4, 3) == "x")

    def test_numero_click_x(self):
        """
        Verifica il corretto autocompletamento, inserimento di tutte "x" attorno
        ad un numero che ha già n linee, dopo aver cliccato su un numero
        """

        game = s.Slitherlink()
        lista = []

        with open("game_win_5x5.txt") as g:
            for line in g:
                board = line.strip("\n")
                lista += board
        game._board = lista
        with self.subTest("controllo sul numero 2"):
            game.auto(3, 9)
            self.assertTrue(game.value_at(3, 8) == "x" and game.value_at(2, 9) == "x")

        with self.subTest("Controllo sul numero 0"):
            game.auto(3, 3)
            self.assertTrue(game.value_at(3, 4) == "x" and game.value_at(3, 2) == "x" and game.value_at(2, 3) == "x" and game.value_at(4, 3) == "x")

        with self.subTest("Controllo sul numero 3"):
            game.auto(3, 1)
            self.assertTrue(game.value_at(3, 2) == "x")

    def test_numero_click_linea(self):
        """
        Verifica il corretto autocompletamento quando l'utente clicca sul numero
        quando ho n caselle libere attorno al numero e mancano n linee. L'automatismo
        deve completare le caselle vuote con delle linee
        """
        game = s.Slitherlink()
        lista = []
        COLS = 11
        r = [0, 1, 2]
        with open("game_5x5.txt") as g:
            for line in g:
                board = line.strip("\n")
                lista += board
        game._board = lista
        for i in r:
            game._board[9 * COLS + 6] = " "
            game._board[8 * COLS + 7] = " "
            game._board[10 * COLS + 7] = " "
            game._board[9 * COLS + 8] = " "

            if i == 0:
                with self.subTest("Possibilità 1"):
                    game.play_at(7, 10)
                    game._board[9 * COLS + 6] = "x"
                    game._board[8 * COLS + 7] = "x"
                    game.auto(7, 9)
                    self.assertTrue(game.value_at(8, 9) == "|")

            elif i == 1:
                with self.subTest("Possibilità 2"):
                    game.play_at(7, 10)
                    game._board[9 * COLS + 8] = "x"
                    game._board[8 * COLS + 7] = "x"
                    game.auto(7, 9)
                    self.assertTrue(game.value_at(6, 9) == "|")

            elif i == 2:
                with self.subTest("Possibilità 3"):
                    game.play_at(7, 10)
                    game._board[9 * COLS + 8] = "x"
                    game._board[9 * COLS + 6] = "x"
                    game.auto(7, 9)
                    self.assertTrue(game.value_at(7, 8) == "-")


