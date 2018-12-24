import pygame
from pygame.locals import *

import random

from OpenGL.GL import *
from OpenGL.GLU import *

from PuzzleClass import PuzzleClass

class GameClass():

    def __init__(self, window_w, window_h, images, sounds):

        #INIT PYGAME AND OPENGL
        pygame.init()
        self.display = (window_w, window_h)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Puzzle 3D!")
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)

        #LOAD TEXTURES
        self.images = images
        self.textures = glGenTextures(len(images))
        for i in range(len(images)):
            SelectSurface = pygame.image.load(images[i]).convert()
            SelectData = pygame.image.tostring(SelectSurface, "RGBX", 1)

            glBindTexture(GL_TEXTURE_2D, self.textures[i])
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, SelectSurface.get_width(), SelectSurface.get_height(), 0,
                         GL_RGBA, GL_UNSIGNED_BYTE, SelectData)

        #LOAD SOUNDS
        self.sound_end = pygame.mixer.Sound(sounds[0])
        self.sound_move = pygame.mixer.Sound(sounds[1])

        self.x_change = 0
        self.y_change = 0

        self.win = False

        self.current_image = random.randrange(len(self.images))
        self.puzzle = PuzzleClass(2.0, self.textures[self.current_image], self.sound_end)

    def eventLoopProces(self):
        for event in pygame.event.get():
            #GAME EXIT
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                #GAME RESET
                if event.key == pygame.K_m:
                    temp = self.current_image
                    while temp == self.current_image:
                        self.current_image = random.randrange(len(self.images))
                    self.puzzle = PuzzleClass(2.0, self.textures[self.current_image], self.sound_end)
                    self.win = False
                if event.key == pygame.K_n:
                    self.puzzle.shuffle()
                    self.win = False
                #CAMERA MOVEMENT
                if event.key == pygame.K_UP:
                    self.x_change = -2
                if event.key == pygame.K_DOWN:
                    self.x_change = 2
                if event.key == pygame.K_RIGHT:
                    self.y_change = -2
                if event.key == pygame.K_LEFT:
                    self.y_change = 2
                #CUBE ROTATION
                if event.key == pygame.K_e  and self.win == False:
                    self.puzzle.smallRotationLeft()
                    self.sound_move.play()
                if event.key == pygame.K_q and self.win == False:
                    self.puzzle.smallRotationRight()
                    self.sound_move.play()
                #FIELD ACTIVATION
                if event.key == pygame.K_w:
                    self.puzzle.moveUp()
                if event.key == pygame.K_s:
                    self.puzzle.moveDown()
                if event.key == pygame.K_d:
                    self.puzzle.moveRight()
                if event.key == pygame.K_a:
                    self.puzzle.moveLeft()
                # BIG ROTATION
                if event.key == pygame.K_r and self.win == False:
                    self.puzzle.bigRotationRight()
                    self.sound_move.play()
            # CAMERA MOVEMENT
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.x_change = 0
                if event.key == pygame.K_DOWN:
                    self.x_change = 0
                if event.key == pygame.K_RIGHT:
                    self.y_change = 0
                if event.key == pygame.K_LEFT:
                    self.y_change = 0

    def checkWinCondition(self):
        if self.win == False:
            self.win = self.puzzle.checkWin()

    def drawGame(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 50.0)
        glTranslate(0.0, 0.0, -20.0)

        self.puzzle.draw(self.x_change, self.y_change)

        pygame.display.flip()

