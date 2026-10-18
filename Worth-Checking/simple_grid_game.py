import random
import readchar

print('\n\nThis is a grid game.\nUse WASD to move.\nTo win you must first collect Treasure then Exit.\nPress q to quit')
input('Press Enter to Start')

class GridGame:
    def __init__(self):
        self.grid = [[] for i in range(10)]                          #grid initialising
        for i in range(10):
            for j in range(10):
                if i == 0 or i == 9:
                    self.grid[i].append(' # ')
                else:
                    if j == 0 or j == 9: self.grid[i].append(' # ')
                    else: self.grid[i].append(' . ')

        self.e = f"{'\033[91m'} E {'\033[0m'}"
        self.k = f"{'\033[94m'} K {'\033[0m'}"
        self.t = f"{'\033[93m'} T {'\033[0m'}"
        self.p = f"{'\033[97m'} P {'\033[0m'}"

        self.treasure = 'F'
        self.key = 'F'

        self.wall = 0
        self.t_check = 0
        self.score = 0
        self.e_check = 0

        self.x = 1
        self.y = 1

        self.wa = []

    def initialising(self):

        for i in range(20):
            o = [0,1]
            k = random.choice(o)
            if k == 1:
                x = random.randint(1, 8)
                y = random.randint(1, 8)
                self.wa.append((y , x))
                self.grid[y][x] = ' # '

        self.grid[random.randint(1,8)][random.randint(1,8)] = self.k
        self.grid[random.randint(1, 8)][random.randint(1, 8)] = self.t

        o1 = [0,9]
        o2 = [1,8]
        self.grid[random.choice(o2)][random.choice(o1)] = self.e
        self.grid[1][1] = self.p

    def printing(self):
        print("\033[2J\033[H", end="")
        print()
        for row in self.grid:
            print(''.join(row))
        print('\n')
        print('Key Acquired: ',self.key)
        print('Treasure Looted: ',self.treasure)

    def collision(self):
        block = self.grid[self.y][self.x]

        if block == ' # ':
            self.wall = 1
        elif block == self.k:
            self.key = 'T'
        elif block == self.t:
            if self.key == 'T': self.treasure = 'T'
            else: self.t_check = 1
        elif block == self.e:
            if self.treasure == 'T':
                self.e_check = 1
            else: self.e_check = -1

    def movement(self):

        def w():                                            ############################################################
            self.grid[self.y][self.x] = self.p
            self.grid[self.y + 1][self.x] = ' . '

        def a():                                            ############################################################
            self.grid[self.y][self.x] = self.p
            self.grid[self.y][self.x + 1] = ' . '

        def s():                                            ############################################################
            self.grid[self.y][self.x] = self.p
            self.grid[self.y - 1][self.x ] = ' . '

        def d():                                            ############################################################
                self.grid[self.y][self.x] = self.p
                self.grid[self.y][self.x - 1] = ' . '

        while True:

            key = readchar.readkey().lower()

            if key == 'w':                                              ################################################
                self.y -= 1
                self.collision()

                if self.wall == 0 and self.t_check == 0 and self.e_check != -1: w()
                else: self.y += 1

            elif key == 'a':                                            ################################################
                self.x -= 1
                self.collision()

                if self.wall==0 and self.t_check == 0 and self.e_check != -1: a()
                else: self.x += 1

            elif key == 's':                                            ################################################
                self.y += 1
                self.collision()

                if self.wall == 0 and self.t_check == 0 and self.e_check != -1: s()
                else: self.y -= 1

            elif key == 'd':                                            ################################################
                self.x+=1
                self.collision()

                if self.wall == 0 and self.t_check == 0 and self.e_check != -1: d()
                else: self.x -= 1

            elif key == 'q':                                            ################################################
                print('\nGame Over')
                break

            if self.e_check == 1:                                       #-----------------------------------------------
                self.grid[self.y][self.x] = self.p
                self.printing()
                print('Game Over')
                break

            self.printing()

            self.wall = 0
            self.t_check = 0
            self.e_check = 0

    def run(self):
        self.initialising()
        self.printing()
        self.movement()

GridGame().run()
