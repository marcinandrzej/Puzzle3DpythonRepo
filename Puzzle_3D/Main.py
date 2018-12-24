from GameClass import GameClass

WINDOW_W = 800
WINDOW_H = 600
IMAGES = ('IMAGES\\SHIBA.png', 'IMAGES\\PUG.png', 'IMAGES\\NEKO.png',
          'IMAGES\\LUDI.png', 'IMAGES\\JANUSZ.png','IMAGES\\GIN.png')
SOUNDS = ('SOUNDS\\congratulations.ogg', 'SOUNDS\\sfx_sounds_button11.wav')


def main():

    game = GameClass(WINDOW_W, WINDOW_H, IMAGES, SOUNDS)

    while True:
        game.eventLoopProces()

        game.checkWinCondition()

        game.drawGame()


if __name__ == '__main__': main()

