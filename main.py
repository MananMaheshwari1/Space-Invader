import pygame
import random
import math
from pygame import mixer
#initialize the pygame
pygame.init()    #present in every game
#create the screen
screen=pygame.display.set_mode((800,600))

#background
background= pygame.image.load('blue.png')

#bacground music
mixer.music.load('background.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon= pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#player
playerimg= pygame.image.load('player.png')
playerX= 370
playerY= 480
playerX_change=0

#enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change=[]
enemyY_change = []
numofenemies = 6
for i in range(numofenemies):

    enemyimg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

#bullet
bulletimg= pygame.image.load('bullet.png')
bulletX= 0
bulletY= 480
bulletX_change=0
bulletY_change=10
bullet_state = "ready"  #ready- you can't see the bullet on screen and fire- the  bullet is currently moving

#score
score_value=0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf',64)

def showscore(x,y):
    score=font.render("Score :"+ str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))

def player(x,y):
    screen.blit(playerimg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))  

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg,(x+16,y+10))      



def iscollision(enemyX,enemyY,bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance<27:
        return True
    else:
        return False    

# Game Loop
running= True
while running:
    
    # RGB - 0 to 255        
    screen.fill((0 , 0, 0))  
    #background image
    screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            #if keystroke is pressed, check whether left or right
        if event.type == pygame.KEYDOWN:
            #print("A keystroke is pressed")
            if event.key == pygame.K_LEFT:
                playerX_change=-6
                #print("Left arrow is pressed")   
            if event.key == pygame.K_RIGHT:
                #print("Right arrow is pressed")  
                playerX_change=6
            if event.key == pygame.K_SPACE:  
        
                if bullet_state is "ready":
                    bulletsound=mixer.Sound('laser.wav')
                    bulletsound.play()
                    bulletX= playerX  #get the bcurrent X coordinate of the spaceship
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change=0
                #print("Key stroke has been released")

# Checking for boundaries for spaceship so kit doesn't go out of bounds
    playerX += playerX_change   
    
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736
# enemy movement
       
    for i in range(numofenemies):
        #game over
        if enemyY[i]>440:
            for j in range(numofenemies):
                enemyY[j]=2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=4
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]=-4
            enemyY[i]+=enemyY_change[i]
        
        #collision
        collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY) 
        if collision:
            explosionsound=mixer.Sound('explosion.wav')
            explosionsound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            #print(score)
            enemyX[i]= random.randint(0,736)
            enemyY[i]= random.randint(50,150)
        
        enemy(enemyX[i],enemyY[i], i)


    #bullet movement
    if bulletY<=0:
        bulletY= 480
        bullet_state= "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)    
        bulletY -= bulletY_change
  
    
    
    player(playerX,playerY)
    showscore(textX,textY)

    pygame.display.update()     #present in every game
 
