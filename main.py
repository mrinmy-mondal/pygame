import pygame
import random
import math

##initialize pygame
pygame.init()
##set height and width
screen = pygame.display.set_mode((800, 600))
#title and icon
pygame.display.set_caption("SPACE-INVADER")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
running = True;
from pygame import mixer
#player
playerimg = pygame.image.load('player.png')
playerx = 370
playery = 480
playerx_change = 0
def player():
    screen.blit(playerimg, (playerx, playery))##draw the player
#
#score text
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx= 10
texty= 10
def show_score():
    score_s = font.render("Score : " + str(score), True, (255,255,255))
    screen.blit(score_s, (textx,texty))
#enemy
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0, 750))
    enemyy.append(random.randint(0, 150))
    enemyx_change.append(4)
    enemyy_change.append(40)


#background
background = pygame.image.load('background.jpg')
#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)
#bullet
bulletimg = pygame.image.load('bullet.png')
buttetx = 0 
bullety = 480
bulletxc=0
bulletyc=40
bullet_state = "ready"
def game_over_text():
    fontgo = pygame.font.Font('freesansbold.ttf', 64)
    gotxt = fontgo.render("GAME OVER", True, (255,255,255))
    screen.blit(gotxt, (200,400))
def isCollision(enx,eny,bulx,buly):
    distance = math.sqrt(math.pow(enx-bulx,2) + math.pow(eny-buly,2))
    if distance < 27:
        return True
    else:
        return False
#ready = bullet not visible but ready
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x,y))
while running:#game loop
    screen.fill((255,255,255))#change screen color
    #background image
    screen.blit(background, (0,0))
    for event in pygame.event.get():#search through alll events
        if event.type == pygame.QUIT:
            running = False
        #check keystrock
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -4
            if event.key == pygame.K_RIGHT:
                playerx_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    buttetx = playerx
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    fire_bullet(playerx, playery)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerx_change = 0
            if event.key == pygame.K_RIGHT:
                playerx_change = 0
        
    if((playerx+playerx_change <736) and (playerx+playerx_change > 36)):
        playerx += playerx_change
    player()#draw player for each framer
    for i in range(num_of_enemies):
        if enemyy[i] > 470:
                  for j in range(num_of_enemies):
                      enemyy[j] = 2000
                  game_over_text()
                  break
        if(enemyx[i]+enemyx_change[i] >736):
           enemyx_change[i] = -4
           enemyy_change[i] = 40
        elif(enemyx[i]+enemyx_change[i] < 36):
            enemyx_change[i] = 4
            enemyy_change[i] = 40
        collision = isCollision(enemyx[i],enemyy[i],buttetx,bullety)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullety = 480
            bullet_state = "ready"
            score+=1
            enemyx[i] = random.randint(0, 750)
            enemyy[i] = random.randint(0, 150)
            print(score)

        
    if bullety < 0:
        bullety = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(buttetx,bullety)
        bullety -= bulletyc
    #collision
        
    
    for i in range(num_of_enemies):
        enemyx[i]+=enemyx_change[i]
        enemyy[i]+=enemyy_change[i]
    for i in range(num_of_enemies):
        enemyy_change[i] = 0
        screen.blit(enemyimg[i], (enemyx[i], enemyy[i]))
    show_score()
    pygame.display.update()###important
