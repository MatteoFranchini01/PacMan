import pacman
import unittest

class PacManGameTest(unittest.TestCase):

    def test_game_won_1pl(self):
        '''Controllo la gestione della vittoria della partita in caso
        di giocatore singolo'''

        test_value = (("e", "1"), ("m", "1"), ("h", "1"))
        for i in test_value:
            par_1, par_2 = i
            game = pacman.PacManGame(par_1, par_2)
            game._score = 24800
            self.assertTrue(game.game_won() == True)

    def test_game_won_2pl(self):
        '''Controllo la gestione della vittoria della partita in caso
        di due giocatori'''

        game = pacman.PacManGame("", "2")
        game._score = 24800
        self.assertTrue(game.game_won() == True)

    def test_game_over(self):
        '''Controllo la gestione della sconfitta'''

        game = pacman.PacManGame("e", "1")
        pac = game.hero()
        pac._lives = 0
        self.assertTrue(game.game_over() == True)
        pac._lives = 1
        self.assertFalse(game.game_over() == True)


class PacManTest(unittest.TestCase):

    def test_symbol(self):
        '''Controllo l'immagine di pacman in caso di movimento verso destra'''
        arena = pacman.Arena((232, 280))
        pac = pacman.PacMan(arena, (8, 8), 3)
        pac._dx, pac._dy = 5, 0
        self.assertTrue(pac._symbol == (16, 0))

    def test_control(self):
        ''' Partendo dall'angolo può muoversi
        a destra e in basso, mentre non potrà muoversi verso l'alto o
        a sinistra '''
        arena = pacman.Arena((232, 280))
        pac = pacman.PacMan(arena, (8, 8), 3)
        pac.control("ArrowDown")
        self.assertTrue(pac._dx == 0 and pac._dy == pac._speed)
        pac.control("ArrowRight")
        self.assertTrue(pac._dx == pac._speed and pac._dy == 0)
        pac.control("ArrowLeft")
        self.assertFalse(pac._dx == -pac._speed and pac._dy == 0)
        pac.control("ArrowUp")
        self.assertFalse(pac._dx == 0 and pac._dy == -pac._speed)


if __name__ == "__main__":
    unittest.main()
