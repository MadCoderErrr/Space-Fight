#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pygame, sys, random
from pygame.locals import *
from pygame import mixer

pygame.init()

WINDOWWIDTH  = 800 # Width of the screen
WINDOWHEIGHT = 550 # Height of the screen
FPS          = 60
WHITE        = (255, 255, 255)
BULLETSPRITE = pygame.sprite.Group()
UFOSPRITE    = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    """
    This is the class for the player and the other functions for the program.
    """
    def __init__(self, DISPLAYSURF):
        pygame.sprite.Sprite.__init__(self)
        self.PLAYER      = pygame.image.load('SpaceRocket.png').convert_alpha() #SpaceShip by dawnydawny from Pixabay
        self.XPLAYER     = WINDOWWIDTH / 2
        self.YPLAYER     = WINDOWHEIGHT - 50
        self.FONT        = pygame.font.Font('freesansbold.ttf', 15)
        self.PBOX        = self.PLAYER.get_rect()
        self.PBOX.center = (self.XPLAYER, self.YPLAYER)
        self.DISPLAYSURF = DISPLAYSURF
        self.color       = WHITE
        
    def makePLAYER(self):
        self.DISPLAYSURF.blit(self.PLAYER, self.PBOX)
        
    def spaceMessage(self, message, x, y):
        self.message = message
        self.mesg    = self.FONT.render(self.message, True, self.color)
        self.MBOX    = self.mesg.get_rect()
        self.MBOX.x  = (x)
        self.MBOX.y  = (y)
        self.DISPLAYSURF.blit(self.mesg, self.MBOX)
        
    def showScore(self, score):
        self.score = score
        self.x     = 50
        self.y     = WINDOWHEIGHT - 500
        self.spaceMessage("SCORE: %s" % score, self.x, self.y)
        
    def terminate(self):
        pygame.quit()
        sys.exit()
        
        
class UFO(pygame.sprite.Sprite):
    """
    This is the class for the UFO.
    """
    def __init__(self, XUFO, YUFO):
        pygame.sprite.Sprite.__init__(self, UFOSPRITE)
        self.XUFO        = XUFO
        self.YUFO        = WINDOWHEIGHT - 570
        self.UFO         = pygame.image.load('SpaceUFO.png').convert_alpha() #Image by Mostafa Elturkey from Pixabay
        self.UBOX        = self.UFO.get_rect()
        self.UBOX.center = (self.XUFO, self.YUFO)
        
    def makeUFO(self, DISPLAYSURF):
        self.DISPLAYSURF = DISPLAYSURF
        self.DISPLAYSURF.blit(self.UFO, self.UBOX)
        
        
class Bullet(pygame.sprite.Sprite):
    """
    This is the class for bullets.
    """
    def __init__(self, bulletx, bullety):
        pygame.sprite.Sprite.__init__(self, BULLETSPRITE)
        self.bulletx        = bulletx
        self.bullety        = bullety
        self.SpaceBulletIMG = pygame.image.load("SpaceBulletIMG.png").convert_alpha() #Image by Clker-Free-Vector-Images from Pixabay
        self.BBOX           = self.SpaceBulletIMG.get_rect()
        self.BBOX.center    = (self.bulletx, self.bullety)
        
    def makeBullet(self, DISPLAYSURF):
        self.DISPLAYSURF = DISPLAYSURF
        self.DISPLAYSURF.blit(self.SpaceBulletIMG, self.BBOX)
        
        
SpaceUFO    = []
SpaceBullet = []
def runGame(Player):
    global FPSCLOCK, BACKGROUNDIMG, DISPLAYSURF, SpaceUFO
    
    DISPLAYSURF   = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BACKGROUNDIMG = pygame.image.load('SpaceBackground.jpg') # Image by Free-Photos from Pixabay 
    FPSCLOCK      = pygame.time.Clock()
    PPlayer        = Player(DISPLAYSURF)
    SpaceKill     = 0
    SCORE         = 0
    BulletSound   = mixer.Sound('BulletSound.wav') # From https://www.freesoundeffects.com/
    GAMEOVER      = False
    pygame.display.set_caption('Space Fight by MadCoderErrr')
    mixer.music.load('SpaceSound.mp3') # Music: https://www.bensound.com
    mixer.music.play(-1)
    
    if SpaceKill > 0:
        SpaceKill += 1
    if SpaceKill > 10:
        SpaceKill = 0
    
    while True:
        DISPLAYSURF.blit(BACKGROUNDIMG, [0, 0])
        PPlayer.spaceMessage('You need to protect the Earth from invaders. A score of -25 means that you lose.', 25, WINDOWHEIGHT - 540)
        PPlayer.spaceMessage('If a UFO bumps into you, you will lose 5 points.', 25, WINDOWHEIGHT - 520)
        while GAMEOVER:
            DISPLAYSURF.blit(BACKGROUNDIMG, [0, 0])
            PPlayer.spaceMessage('YOU LOSE. A score of -25 is an indication that you lose. Press p to play again or q to quit.', 50, WINDOWHEIGHT - 500)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        PPlayer.terminate()
                    if event.key == K_p:
                        GAMEOVER = False
                        runGame(Player)
                if event.type == QUIT:
                    PPlayer.terminate()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                PPlayer.terminate()
            if event.type == KEYDOWN:
                if event.key == K_SPACE and SpaceKill < 10:
                    if len(SpaceBullet) < 10:
                        SpaceBullet.append(Bullet(PPlayer.XPLAYER, PPlayer.YPLAYER))
                    SpaceKill = 1
                    for bullet in SpaceBullet:
                        bullet.BBOX.center = (bullet.bulletx, bullet.bullety)
                        BULLETSPRITE.add(bullet)
                    BulletSound.play()
            for ufo in SpaceUFO.copy():
                if ufo.UBOX.colliderect(PPlayer.PBOX):
                    SCORE -= 5
                    
        for i in range(len(SpaceUFO), 5):
            x, y   = random.randrange(FPS, WINDOWWIDTH - FPS), WINDOWHEIGHT -570
            newUFO = UFO(x, y)
            if not any(ufo for ufo in SpaceUFO if ufo.UBOX.colliderect(newUFO.UBOX)):
                SpaceUFO.append(newUFO)
                print('making new aliens')
            
        for ufo in SpaceUFO.copy():
            ufo.makeUFO(DISPLAYSURF)
            ufo.YUFO += 60 / FPS
            ufo.UBOX.center = (ufo.XUFO, ufo.YUFO)
            
        for ufo in SpaceUFO:
            if ufo.YUFO >= WINDOWHEIGHT:
                SpaceUFO.pop(SpaceUFO.index(ufo))
                print('Alien is gone')
                
        for bullet in SpaceBullet.copy():
            #DISPLAYSURF.blit(bullet.SpaceBulletIMG, [bullet.bulletx, bullet.bullety])
            bullet.makeBullet(DISPLAYSURF)
            if bullet.bullety > 0:
                bullet.bullety -= round(240 / (FPS * 2))
                bullet.BBOX.center = (bullet.bulletx, bullet.bullety)
            if bullet.bullety <= 0:
                bullet.BBOX.center = (bullet.bulletx, bullet.bullety)
                SpaceBullet.pop(SpaceBullet.index(bullet))
                print('Bullet is now gone!')
            continue
            
        if event.type == KEYDOWN:
            if event.key == K_LEFT and not PPlayer.XPLAYER <= 10:
                PPlayer.XPLAYER -= (FPS / 3)
                PPlayer.PBOX.center = (PPlayer.XPLAYER, PPlayer.YPLAYER)
            if event.key == K_RIGHT and PPlayer.XPLAYER < WINDOWWIDTH - (FPS / 10):
                PPlayer.XPLAYER += (FPS / 3)
                PPlayer.PBOX.center = (PPlayer.XPLAYER, PPlayer.YPLAYER)
        
                
        if SpaceBullet:
            for bullet in SpaceBullet.copy():
                for ufo in SpaceUFO.copy():
                    if ufo.UBOX.colliderect(bullet.BBOX):
                        SpaceUFO.pop(SpaceUFO.index(ufo))
                        SpaceBullet.pop(SpaceBullet.index(bullet))
                        print('hit')
                        SCORE += 1
                        break
                        
        if SCORE <= -25:
            GAMEOVER = True
                
        PPlayer.showScore(SCORE)
        PPlayer.makePLAYER()
        FPSCLOCK.tick(FPS)
        pygame.display.flip()
        pygame.display.update()
        
if __name__ == '__main__':
    runGame(Player)

