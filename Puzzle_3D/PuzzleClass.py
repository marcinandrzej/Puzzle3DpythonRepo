import random

from OpenGL.GL import *

from CubeClass import CubeClass

class PuzzleClass():

    def __init__(self, offset, texture, sound):

        self.offset = offset

        self.active = [0, 0]

        self.y_rotation = 0
        self.x_rotation = 0

        self.end_sound = sound
        self.texture = texture

        self.game = []
        for rows in range(5):
            self.game.append([])
            for cols in range(5):
                self.game[rows].append(CubeClass(rows, cols, self.offset))

        self.shuffle()

    def shuffle(self):
        randi = random.randrange(20, 30)
        for i in range(randi):
            rand_x = random.randrange(5)
            rand_y = random.randrange(5)

            self.active[0] = rand_x
            self.active[1] = rand_y

            self.bigRotationRight()

        for rows in range(5):
            for cols in range(5):
                self.game[rows][cols].deactivate()
                rand_r = random.randrange(1, 3)
                for j in range(rand_r):
                    self.game[rows][cols].rotateLeft()

        self.active = [0, 0]
        self.game[0][0].activate()
        self.game[0][1].activateNeighbour()
        self.game[1][0].activateNeighbour()
        self.game[1][1].activateNeighbour()

    def checkWin(self):
        win = True
        for rows in range(5):
            for cols in range(5):
                if self.game[rows][cols].id_row != rows or\
                                self.game[rows][cols].id_col != cols or\
                                self.game[rows][cols].rotation != 0:
                    win = False

        if win == True:
            self.end_sound.play()
        return win

    def bigRotationRight(self):
        def bigRotationRightMacro(row, col):
            self.game[row][col].push(0, self.offset)
            self.game[row - 1][col].push(self.offset, 0)
            self.game[row - 1][col + 1].push(0, -self.offset)
            self.game[row][col + 1].push(-self.offset, 0)

            temp = self.game[row][col]
            self.game[row][col] = self.game[row][col + 1]
            self.game[row][col + 1] = self.game[row - 1][col + 1]
            self.game[row - 1][col + 1] = self.game[row - 1][col]
            self.game[row - 1][col] = temp

        if self.active[0] > 0 and self.active[1] < 4:
            x = self.active[0]
            y = self.active[1]

            bigRotationRightMacro(x, y)

            self.game[self.active[0]][self.active[1]].activate()
            self.game[self.active[0]][self.active[1] + 1].activateNeighbour()
            self.game[self.active[0] - 1][self.active[1]].activateNeighbour()
            self.game[self.active[0] - 1][self.active[1] + 1].activateNeighbour()
        elif self.active[0] == 0 and self.active[1] < 4:
            x = self.active[0] + 1
            y = self.active[1]

            bigRotationRightMacro(x, y)

            self.game[self.active[0]][self.active[1]].activate()
            self.game[self.active[0]][self.active[1] + 1].activateNeighbour()
            self.game[self.active[0] + 1][self.active[1]].activateNeighbour()
            self.game[self.active[0] + 1][self.active[1] + 1].activateNeighbour()
        elif self.active[0] > 0 and self.active[1] == 4:
            x = self.active[0]
            y = self.active[1] - 1

            bigRotationRightMacro(x, y)

            self.game[self.active[0]][self.active[1]].activate()
            self.game[self.active[0]][self.active[1] - 1].activateNeighbour()
            self.game[self.active[0] - 1][self.active[1] - 1].activateNeighbour()
            self.game[self.active[0] - 1][self.active[1]].activateNeighbour()
        elif self.active[0] == 0 and self.active[1] == 4:
            y = self.active[1] - 1
            x = self.active[0] + 1

            bigRotationRightMacro(x, y)

            self.game[self.active[0]][self.active[1]].activate()
            self.game[self.active[0]][self.active[1] - 1].activateNeighbour()
            self.game[self.active[0] + 1][self.active[1] - 1].activateNeighbour()
            self.game[self.active[0] + 1][self.active[1]].activateNeighbour()

    def smallRotationLeft(self):
        self.game[self.active[0]][self.active[1]].rotateLeft()

    def smallRotationRight(self):
        self.game[self.active[0]][self.active[1]].rotateRight()

    def moveUp(self):
        if self.active[0] > 0:
            self.game[self.active[0]][self.active[1]].deactivate()
            self.active[0] -= 1
            self.game[self.active[0]][self.active[1]].activate()
            if self.active[0] == 0:
                self.game[self.active[0] + 1][self.active[1]].activateNeighbour()
            elif self.active[0] != 0 and self.active[1] < 4:
                self.game[self.active[0] + 1][self.active[1] + 1].deactivate()

                self.game[self.active[0] - 1][self.active[1]].activateNeighbour()
                self.game[self.active[0] - 1][self.active[1] + 1].activateNeighbour()
            elif self.active[0] != 0 and self.active[1] == 4:
                self.game[self.active[0] + 1][self.active[1] - 1].deactivate()

                self.game[self.active[0] - 1][self.active[1]].activateNeighbour()
                self.game[self.active[0] - 1][self.active[1] - 1].activateNeighbour()

    def moveDown(self):
        if self.active[0] < 4:
            self.game[self.active[0]][self.active[1]].deactivate()
            self.active[0] += 1
            self.game[self.active[0]][self.active[1]].activate()
            if self.active[0] != 1 and self.active[1] < 4:
                self.game[self.active[0] - 2][self.active[1] + 1].deactivate()
                self.game[self.active[0] - 2][self.active[1]].deactivate()

                self.game[self.active[0]][self.active[1] + 1].activateNeighbour()
                self.game[self.active[0] - 1][self.active[1]].activateNeighbour()
            elif self.active[0] == 1:
                self.game[self.active[0] - 1][self.active[1]].activateNeighbour()
            elif self.active[0] != 1 and self.active[1] == 4:
                self.game[self.active[0] - 2][self.active[1] - 1].deactivate()
                self.game[self.active[0] - 2][self.active[1]].deactivate()

                self.game[self.active[0]][self.active[1] - 1].activateNeighbour()
                self.game[self.active[0] - 1][self.active[1]].activateNeighbour()

    def moveRight(self):
        if self.active[1] < 4:
            self.game[self.active[0]][self.active[1]].deactivate()
            self.active[1] += 1
            self.game[self.active[0]][self.active[1]].activate()
            if self.active[0] != 0 and self.active[1] != 4:
                self.game[self.active[0] - 1][self.active[1] - 1].deactivate()

                self.game[self.active[0]][self.active[1] + 1].activateNeighbour()
                self.game[self.active[0] - 1][self.active[1] + 1].activateNeighbour()
            elif self.active[0] == 0 and self.active[1] != 4:
                self.game[self.active[0]][self.active[1] - 1].deactivate()
                self.game[self.active[0] + 1][self.active[1] - 1].deactivate()

                self.game[self.active[0]][self.active[1] + 1].activateNeighbour()
                self.game[self.active[0] + 1][self.active[1] + 1].activateNeighbour()
            elif self.active[1] == 4:
                self.game[self.active[0]][self.active[1] - 1].activateNeighbour()

    def moveLeft(self):
        if self.active[1] > 0:
            self.game[self.active[0]][self.active[1]].deactivate()
            self.active[1] -= 1
            self.game[self.active[0]][self.active[1]].activate()
        if self.active[0] != 0 and self.active[1] < 3:
            self.game[self.active[0] - 1][self.active[1] + 2].deactivate()
            self.game[self.active[0]][self.active[1] + 2].deactivate()

            self.game[self.active[0]][self.active[1] + 1].activateNeighbour()
            self.game[self.active[0] - 1][self.active[1]].activateNeighbour()
        elif self.active[0] == 0 and self.active[1] < 3:
            self.game[self.active[0] + 1][self.active[1] + 2].deactivate()
            self.game[self.active[0]][self.active[1] + 2].deactivate()

            self.game[self.active[0]][self.active[1] + 1].activateNeighbour()
            self.game[self.active[0] + 1][self.active[1]].activateNeighbour()
        elif self.active[1] == 3:
            self.game[self.active[0]][self.active[1] + 1].activateNeighbour()

    def draw(self, x_change, y_change):

        if (self.x_rotation + x_change) <= 30 and (self.x_rotation + x_change) >= -30:
            self.x_rotation = self.x_rotation + x_change
        elif (self.x_rotation + x_change) > 30:
            self.x_rotation = 30
        else:
            self.x_rotation = -30

        if (self.y_rotation + y_change) <= 30 and (self.y_rotation + y_change) >= -30:
            self.y_rotation = self.y_rotation + y_change
        elif (self.y_rotation + y_change) > 30:
            self.y_rotation = 30
        else:
            self.y_rotation = -30

        glPushMatrix()
        glRotatef(self.x_rotation, 1, 0, 0)
        glRotatef(self.y_rotation, 0, 1, 0)

        for row in range(5):
            for col in range(5):
                self.game[row][col].draw(self.texture)
        glPopMatrix()