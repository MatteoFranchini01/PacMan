import g2d
from random import choice
from pacman_map import in_wall

class Actor():
    '''Interface to be implemented by each game character
    '''
    def move(self):
        '''Called by Arena, at the actor's turn
        '''
        raise NotImplementedError('Abstract method')

    def collide(self, other: 'Actor'):
        '''Called by Arena, whenever the `self` actor collides with some
        `other` actor
        '''
        raise NotImplementedError('Abstract method')

    def position(self) -> (int, int):
        '''Return the position of the actor (left-top corner)
        (x, y)
        '''
        raise NotImplementedError('Abstract method')

    def size(self) -> (int, int):
        '''Return the size of the actor
        (w, h)
        '''
        raise NotImplementedError('Abstract method')

    def symbol(self) -> (int, int):
        '''Return the position (x, y) of current sprite, if it is contained in
        a larger image, with other sprites. Otherwise, simply return None
        '''
        raise NotImplementedError('Abstract method')

class Arena():
    '''A generic 2D game, with a given size in pixels and a list of actors
    '''
    def __init__(self, size: (int, int)):
        '''Create an arena, with given dimensions in pixels
        '''
        self._w, self._h = size
        self._count = 0
        self._actors = []

    def add(self, a: Actor):
        '''Register an actor into this arena.
        Actors are blitted in their order of registration
        '''
        if a not in self._actors:
            self._actors.append(a)

    def remove(self, a: Actor):
        '''Cancel an actor from this arena
        '''
        if a in self._actors:
            self._actors.remove(a)

    def move_all(self):
        '''Move all actors (through their own move method).
        After each single move, collisions are checked and eventually
        the `collide` methods of both colliding actors are called
        '''
        actors = list(reversed(self._actors))
        for a in actors:
            pos = a.position()
            a.move()
            if pos != a.position():
                for other in actors:
                    # reversed order, so actors drawn on top of others
                    # (towards the end of the cycle) are checked first
                    if other is not a and self.check_collision(a, other):
                            a.collide(other)
                            other.collide(a)
        self._count += 1

    def check_collision(self, a1: Actor, a2: Actor) -> bool:
        '''Check the two actors (args) for mutual collision (bounding-box
        collision detection). Return True if colliding, False otherwise
        '''
        x1, y1, w1, h1 = a1.position() + a1.size()
        x2, y2, w2, h2 = a2.position() + a2.size()
        return (y2 < y1 + h1 and y1 < y2 + h2
            and x2 < x1 + w1 and x1 < x2 + w2
            and a1 in self._actors and a2 in self._actors)

    def actors(self) -> list:
        '''Return a copy of the list of actors
        '''
        return list(self._actors)

    def size(self) -> (int, int):
        '''Return the size of the arena as a couple: (width, height)
        '''
        return (self._w, self._h)

    def count(self) -> int:
        '''Return the total count of ticks (or frames)
        '''
        return self._count

class Biscuit():
    def size(self) -> (int, int):
        raise NotImplementedError('Abstract method')

    def symbol(self) -> (int, int):
        raise NotImplementedError('Abstract method')

    def position(self) -> (int, int):
        raise NotImplementedError('Abstract method')

    def punteggio(self):
        raise NotImplementedError('Abstract method')

    def collide(self, other: 'Actor'):
        raise NotImplementedError('Abstract method')

class PacMan(Actor):
    def __init__(self, arena, pos, lives):
        self._x, self._y = pos
        self._x_in, self._y_in = 8, 8
        self._w, self._h = 16, 16
        self._speed = 2
        self._dx, self._dy = 0, 0
        self._lives = lives
        self._last_collision = 0
        self._arena = arena
        self._symbol = (16, 0)
        arena.add(self)
        self._power = False

    def move(self):
        arena_w, arena_h = self._arena.size()
        if in_wall(self._x + self._dx, self._y + self._dy) == False:
            self._y += self._dy
            if self._y < 0:
                self._y = 0
            elif self._y > arena_h - self._h:
                self._y = arena_h - self._h

            self._x += self._dx
            if self._x < 0:
                self._x = arena_w
            elif self._x > arena_w:
                self._x = 0

    def control(self, keys):
        u, d, l, r = "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"
        #u, d, l, r = "w", "s", "a", "d"
        dy_old, dx_old = self._dy, self._dx

        if in_wall(self._x + self._dx, self._y + self._dy) == False:
            if self._x % 8 == 0 and self._y % 8 == 0:
                if u in keys:
                    self._dy = -self._speed
                    self._dx = 0
                elif d in keys:
                    self._dy = self._speed
                    self._dx = 0
                elif l in keys:
                    self._dx = -self._speed
                    self._dy = 0
                elif r in keys:
                    self._dx = self._speed
                    self._dy = 0

        else:
            self._dx, self._dy = 0, 0

        if in_wall(self._x + self._dx, self._y + self._dy) == True:
            if self._x % 8 == 0 and self._y % 8 == 0:
                self._dy, self._dx = dy_old, dx_old

    def lives(self) -> int:
        return self._lives

    def collide(self, other):
        if self._arena.count() - self._last_collision < 30:
            return
        self._last_collision = self._arena.count()

        if isinstance(other, Ghost):
            if self._lives != 0:
                self._lives -= 1
                self._x, self._y = self._x_in, self._y_in
                self._dx, self._dy = 0, 0

        elif isinstance(other, Ghost_alt):
            if self._lives != 0:
                self._lives -= 1
                self._x, self._y = self._x_in, self._y_in
                self._dx, self._dy = 0, 0

    def position(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def symbol(self):
        if self._dx > 0:
            self._symbol = (16, 0)

        elif self._dx < 0:
            self._symbol = (16, 16)

        elif self._dy < 0:
            self._symbol = (16, 32)

        elif self._dy > 0:
            self._symbol = (16, 48)

        return self._symbol

class Ghost(Actor):
    def __init__(self, arena, pos, color):
        self._x, self._y = pos
        self._w, self._h = 16, 16
        self._dx, self._dy = 0, 2
        self._arena = arena
        self._color = color #1 =< color =< 4
        arena.add(self)

    def move(self):
        val = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        if in_wall(self._x + self._dx, self._y + self._dy) == True:
            if self._x % 8 == 0 and self._y % 8 == 0:
                val.remove((self._dx, self._dy))
                self._dx, self._dy = choice(val)
        else:
            arena_w, arena_h = self._arena.size()
            self._x = (self._x + self._dx) % arena_w
            self._y = (self._y + self._dy) % arena_h

    def collide(self, other):
        pass

    def position(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def symbol(self):
        if self._dx > 0:
            return 16, (64 + 16 * self._color)

        elif self._dx < 0:
            return 48, (64 + 16 * self._color)

        elif self._dy < 0:
            return 80, (64 + 16 * self._color)

        elif self._dy > 0:
            return 112, (64 + 16 * self._color)

class Ghost_alt(Actor):
    def __init__(self, arena, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 16
        self._dx, self._dy = 0, 0
        self._arena = arena
        self._speed = 2
        arena.add(self)

    def move(self):
        arena_w, arena_h = self._arena.size()
        if in_wall(self._x + self._dx, self._y + self._dy) == False:
            self._y += self._dy
            if self._y < 0:
                self._y = 0
            elif self._y > arena_h - self._h:
                self._y = arena_h - self._h

            self._x += self._dx
            if self._x < 0:
                self._x = 0
            elif self._x > arena_w - self._w:
                self._x = arena_w - self._w

    def control(self, keys):

        u, d, l, r = "w", "s", "a", "d"
        # u, d, l, r = "w", "s", "a", "d"
        dy_old, dx_old = self._dy, self._dx

        if in_wall(self._x + self._dx, self._y + self._dy) == False:
            if self._x % 8 == 0 and self._y % 8 == 0:
                if u in keys:
                    self._dy = -self._speed
                    self._dx = 0
                elif d in keys:
                    self._dy = self._speed
                    self._dx = 0
                elif l in keys:
                    self._dx = -self._speed
                    self._dy = 0
                elif r in keys:
                    self._dx = self._speed
                    self._dy = 0

        else:
            self._dx, self._dy = 0, 0

        if in_wall(self._x + self._dx, self._y + self._dy) == True:
            if self._x % 8 == 0 and self._y % 8 == 0:
                self._dy, self._dx = dy_old, dx_old

    def collide(self, other):
        pass

    def position(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def symbol(self):
        if self._dx > 0:
            return 16, 64
        elif self._dx < 0:
            return 48, 64
        elif self._dy < 0:
            return 80, 64
        elif self._dy > 0:
            return 112, 64
        else:
            return 16, 64

class BisPic(Biscuit):
    def __init__(self, arena, gioco, pos):
        self._arena = arena
        self._gioco = gioco
        self._x, self._y = pos
        self._W, self._H = 4, 4
        self._COST = 8
        arena.add(self)
        self._score = 0

    def size(self):
        return self._W, self._H

    def symbol(self):
        return 32 + 4, 88 + 4

    def number(self):
        return 32, 30

    def position(self):
        return (self._y - 2) * self._COST, self._x * self._COST

    def collide(self, other):
        if isinstance(other, PacMan):
            self._arena.remove(self)
            self._gioco.add_score(100)

    def move(self):
        pass

class BisGr(Biscuit):
    def __init__(self, arena, gioco, pos):
        self._arena = arena
        self._gioco = gioco
        self._x, self._y = pos
        self._W, self._H = 16, 16
        self._COST = 8
        arena.add(self)
        self._score = 0

    def size(self):
        return self._W, self._H

    def symbol(self):
        return 176,48

    def position(self):
        return (self._y - 2.7) * self._COST, (self._x - 1) * self._COST

    def collide(self, other):
        if isinstance(other, PacMan):
            self._arena.remove(self)
            self._gioco.add_score(200)

    def move(self):
        pass

class PacManGame:
    def __init__(self, level: str, alternative: str):
        self._level = level
        self._alternative = alternative
        self._arena = Arena((232, 280)) #Arena 232, 256. Arena con spazio 232, 280
        self._score = 0
        with open("Board.txt") as board:
            b = board.readlines()
            for i in range(32):
                for x in range(30):
                    if b[i][x] == "-":
                        BisPic(self._arena, self, (i, x))
                    elif b[i][x] == "+":
                        BisGr(self._arena, self, (i, x))
        if self._alternative == "1":
            if self._level == "e":
                self._hero = PacMan(self._arena, (8, 8), 5)
                self._ghost = Ghost(self._arena, (88, 88), 0)
                self._ghost = Ghost(self._arena, (88, 88), 1)

            elif self._level == "m":
                self._hero = PacMan(self._arena, (8, 8), 3)
                self._ghost = Ghost(self._arena, (88, 88), 0)
                self._ghost = Ghost(self._arena, (88, 88), 1)
                self._ghost = Ghost(self._arena, (88, 88), 2)

            elif self._level == "h":
                self._hero = PacMan(self._arena, (8, 8), 2)
                self._ghost = Ghost(self._arena, (88, 88), 0)
                self._ghost = Ghost(self._arena, (88, 88), 1)
                self._ghost = Ghost(self._arena, (88, 88), 2)
                self._ghost = Ghost(self._arena, (88, 88), 3)

        elif self._alternative == "2":
            self._hero = PacMan(self._arena, (8, 8), 3)
            self._ghost_alt = Ghost_alt(self._arena, (88, 88))

    def arena(self) -> Arena:
        return self._arena

    def hero(self) -> PacMan:
        return self._hero

    def ghost_alt(self) -> Ghost_alt:
        return self._ghost_alt

    def add_score(self, x: int):
        self._score += x

    def score(self):
        return self._score

    def game_over(self) -> bool:
        if self._hero.lives() <= 0:
            return True

    def game_won(self) -> bool:
        if self._score == 24800:
            return True

class PacManGui:
    def __init__(self, boolean: bool, level: str, alternative: str):
        self._level, self._alternative = level, alternative
        self._bool = boolean
        self._welcome = self._bool
        if self._welcome == False:
            self._game = PacManGame(self._level, self._alternative)
            g2d.init_canvas(self._game.arena().size())
            self._sprites = g2d.load_image("pac-man.png")
            g2d.main_loop(self.tick)
        else:
            self.tick()

    def tick(self):
        if self._welcome == True:
            self._alternative = g2d.prompt("Benvenuto, scegli il numero di giocatori (1 o 2): ")
            if self._alternative == "1":
                self._level = g2d.prompt("Inserire il livello di difficoltà a cui si intende giocare.\nInserire E, M, H per scegliere il livello")
                if self._level == "e":
                    g2d.alert("Hai a disposizione 3 vite e nella mappa compariranno 2 fantasmi")
                elif self._level == "m":
                    g2d.alert("Hai a disposizione 3 vite e nella mappa compariranno 3 fantasmi")
                elif self._level == "h":
                    g2d.alert("Hai selezionato il livello più difficile, hai a disposizione 2 vite e compariranno 4 fantasmi")
                else:
                    g2d.alert("Valore Errato")
                    self.tick()
                g2d.alert("Lo scopo del gioco è mangiare tutti i biscotti senza essere colpiti dai fantasmi")
            elif self._alternative == "2":
                g2d.alert("PacMan viene controllato tramite le frecce\n\nIl fantasma tramite i tasti \nw, a, s, d")
                g2d.alert("Il giocatore (PacMan) dovrà mangiare tutti i biscotti senza essere colpito dal giocatore (Fantasma)")
            else:
                g2d.alert("Valore Errato")
                self.tick()
            self._welcome = False
            PacManGui(self._welcome, self._level, self._alternative)

        elif self._welcome == False:
            self._game.hero().control(g2d.current_keys())
            if self._alternative == "2":
                self._game.ghost_alt().control(g2d.current_keys())
            arena = self._game.arena()
            arena.move_all()  # Game logic
            g2d.clear_canvas()
            g2d.draw_image("pac-man-bg.png", (0, 0))
            for a in arena.actors():
                if a.symbol() != None:
                    g2d.draw_image_clip(self._sprites, a.symbol(), a.size(), a.position())
                else:
                    g2d.fill_rect(a.position(), a.size())
            g2d.set_color((255, 255, 255))
            g2d.draw_text_centered("Lives: " + str(self._game.hero().lives()), (50, 265), 20)
            g2d.draw_text_centered("Score: " + str(self._game.score()), (175, 265), 20)

            if self._game.game_over():
                 g2d.alert("Game over")
                 g2d.close_canvas()
            elif self._game.game_won():
                 g2d.alert("Game won")
                 g2d.close_canvas()

PacManGui(True, "", "")


