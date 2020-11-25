"""
Main class Game to control all games

"""

from constants import *

import random


class Game():
    highest_score = 0

    def __init__(self):
        self.score = 0
        self.gravity = 0
        self.play = False

        # self.king = King(RESX / 2, RESY + (KING_SIZE / 2), )
        # termporal variable for king
        self.tmp = 0

        # decide a music
        # self.bg_music

        # back ground image managements
        self.imgnum = -1
        self.phase = -1
        self.bg_imgs = []
        for i in range(NUM_BG_IMGS):
            self.bg_imgs.append(
                loadImage(PATH + "/images/bg" + str(i) + ".png"))

        # platform creations
        self.platforms = []
        Game.create_platforms(self)

    def startup(self):
        '''
        Display the startup screen
        '''
        image(loadImage(PATH + "/images/bg0.png"), 0, 0, width, height)
        imageMode(CENTER)
        logo = loadImage(PATH + "/images/logo.png")
        image(logo, width / 2, height * 2 / 5, width * 5 / 6,
              (width * 5 / 6) * logo.height / logo.width)
        imageMode(CORNER)
        fill(255)
        textAlign(CENTER)
        font = createFont("3270SemiNarrow", floor(RESX * 0.03))
        textFont(font)
        text("Click Anywhere to Start", width / 2, height * 3 / 4)
        img = loadImage(PATH + "/images/king0.png")
        image(img, KING_SIZE, RESY - KING_SIZE * 1.5, KING_SIZE * 1.5,
              KING_SIZE * 1.5, 0, 0, img.width, img.height)


    def gameover(self):
        '''
        Display the game over screen
        '''
        image(loadImage(PATH + "/images/bg0.png"), 0, 0, width, height)
        imageMode(CENTER)
        logo = loadImage(PATH + "/images/gameover.png")
        image(logo, width / 2, height * 1 / 5, width * 5 / 6,
              (width * 5 / 6) * logo.height / logo.width)
        imageMode(CORNER)
        fill(255)
        textAlign(CENTER)
        font = createFont("3270SemiNarrow", floor(RESX * 0.04))
        textFont(font)
        text("Your Score", width / 2, height * 2 / 5)
        textSize(floor(RESX * 0.03))
        text(str(self.score), width / 2, height * 3 / 5)
        img = loadImage(PATH + "/images/king7.png")
        image(img, KING_SIZE, RESY - KING_SIZE * 1.5, KING_SIZE * 1.5,
              KING_SIZE * 1.5, 0, 0, img.width, img.height)


    def create_platforms(self):
        '''
        Create a new set of platforms
        '''

        # set distance in relation to the last board
        last_distance = 0
        if self.platforms:
            last_distance = self.platforms.pop().y_position
        distance = JUMP_HIGHET - last_distance

        # append platform instance anonimously
        last_y = 0
        while last_y > JUMP_HIGHET:
            # choose x position of the platform
            # might be too far to jump on
            center_x = random.randint(GAMEX_L, GAMEX_R)

            # choose y position of the platform
            # upper_bound: king should be visible in all sceans
            upper_bound = max([last_y - distance, KING_SIZE])
            # lower_bound: platform should be higher than the last one
            lower_bound = last_y
            center_y = random.randint(upper_bound, lower_bound)

            # instanciate Platform(x, y)
            self.platforms.append(Platform(center_x, center_y))

            # update variables
            last_y = center_y
            distance = JUMP_HEIGHT

    def new_phase(self):
        '''
        Calculate a num of bg_img and the phase
        Return if the bg_img has changed
        '''
        # calculate bg_img to display
        imgnum = self.tmp // RESX

        # show the last img for the exceeded part
        self.imgnum = min([imgnum, NUM_BG_IMGS - 1])
        # calculate a phase
        self.phase = self.imgnum // NUM_PHASE

        # if the bg_img needs to be changed
        if imgnum > self.imgnum:
            return True

        return False

    def display(self):
        '''
        0. game over display
        1. display the background
        2. display side boundry
        3. display platform (call .display())
        4. display life left
        5. display king (call .display())
        '''

        # 0. if the game is over
        if 1 == 1 or not self.king.live:
            self.gameover()
            return


        # 1. display the background
        # check if the bg_img changed
        new_phase = Game.new_phase(self)
        # display back ground image of the current phase(at the very back)
        img = self.bg_imgs[self.imgnum]
        image(img, 0, 0, width, height)

        # 2. displaying side boundries
        bottom = 0
        while bottom < RESY:
            img = loadImage(PATH + "/images/sidebrick0.png")
            # display at the edge of the screen
            image(img, 0, bottom, GAMEX_L, GAMEX_L * img.height / img.width)
            image(img, GAMEX_R, bottom, GAMEX_L,
                  GAMEX_L * img.height / img.width)
            bottom += GAMEX_L * img.height / img.width

        # 3. display platforms
        # create random platforms
        # if new_phase:
        #     Game.create_platforms()
        # for platform in self.platforms:
        #   platform.display()

        # 4. display life left
        yposition = GAMEX_L * 0.5
        # for life in king.life:
        for i in range(3):
            heart = loadImage(PATH + "/images/heart.png")
            image(heart, GAMEX_R + (GAMEX_L * 0.2), yposition, GAMEX_L * 0.6, GAMEX_L * 0.6)
            yposition += GAMEX_L

        # 5. display king (just a imgage for now)
        # self.king.diplay()
        img = loadImage(PATH + "/images/king0.png")
        image(img, 20, RESY - self.tmp %
              RESX, KING_SIZE, KING_SIZE, 0, 0, img.width, img.height)
