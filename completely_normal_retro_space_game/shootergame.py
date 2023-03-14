#####################################################################################################################################
#                                                                                                                                   #
#                                                                                                                                   #
#                                                            A Game By Oliver Healey                                                #
#                                                             9IST Assessment Task 1                                                #
#                                            (Not owned by Mr Fong no matter how much he claims it is)                              #
#                                                                                                                                   #
#                                                                                                                                   #
#####################################################################################################################################

import pgzrun
import random
import math
import time


### VARIABLE AND CONSTANT PREPARATION ###

music.play('ending') #yes, my start screen music is called "ending"

game_state = 0 #0 = start menu, 1 = main game, 2 = game over, 3 = boss battle, 4 = loading animation, 5 = boss explosion, 42 = win

wave = 0
score = 0
health = 3
new_wave_score = 10
high_score = 0

grid = []
glitched = False

back_red = 0
back_green = 0
back_blue = 0

small_x = 0
small_y = 0

stars = []

glitchers = []
bossbullets = []
missiles = []
command_activate = False
shoot = False
bossHealth = 3
bossInvunerable = 0
won = bool(False)

invunerable = 0

kaboom = []
kaboom_dur = []

singleColour = ['red', 'green', 'blue', 'black']

enemy1Move = False
enemy2Move = False
enemy3Move = False
enemy4Move = False
enemyDir = 1
enemyLoop = 0

WIDTH = 800
HEIGHT = 600

bullet_dir = 35
bullets = []
bullet_delay = 0

rayX = 0
rayY = 0

boss_wave = 2

enemyBullets = []

healthColour = [0, 0, 0]

gameLoops = 0

gameOverTransition = 12

secret_settings = False

#### ACTORS ####

screenRed = [0, 139, 0]
screenGreen = [0, 172, 0]
screenBlue =[0, 15, 100]
mainRed = [255, 0, 255]
mainGreen = [255, 0, 255]
mainBlue = [255, 0, 255]

start = Actor('start_front1', center = (400,300))

load_full = Actor('loading_full', center = (400,300))

load_half = Actor('loading_half', center = (400,300))

player = Actor('spaceship1-1')
player.x = 370
player.y = 550 

collectable = Actor('gem1')
collectable.x = random.randint(15, 785)
collectable.y = -70

new_wave_gem = Actor('gem2')
new_wave_gem.x = random.randint(20, 780)
new_wave_gem.y = -70

gemCount = 0
levelUpActivate = False # prepare new_wave_gem

enemy1 = Actor('enemy1-1')
enemy1.x = random.randint(20, 780)
enemy1.y = -70

enemy2 = Actor('enemy1-2')
enemy2.x = random.randint(150, 780)
enemy2.y = -70

enemy3 = Actor('enemy2-3')
enemy3.x = random.randint(150, 780)
enemy3.y = -70

enemy4 = Actor('enemy3-4')
enemy4.x = random.randint(150, 780)
enemy4.y = -70

ray = Actor('ray')
ray.x = 0
ray.y = 0

boss = Actor('finalboss')
boss.x = 400
boss.y = -128

command_gem = Actor('command_gem')
command_gem.y = -70
command_gem.x = random.randint(150, 780)

### WAVE CHANGE SCRIPTS ###

def changePlayer(level): # change player look but keep the x and y pos and angle
    global player
    x = player.x
    y = player.y
    angle = player.angle
    if level == 0:
        player = Actor('spaceship1-1')
    elif level == 1:
        player = Actor('spaceship2-1')
    elif level == 2:
        player = Actor('spaceship3-1')
    player.x = x
    player.y = y
    player.angle = angle


def changeEnemy(level): # change enemy look but keep the x and y pos and angle
    global enemy1
    global enemy2
    global enemy3
    global enemy4
    x = enemy1.x
    y = enemy1.y
    angle = enemy1.angle
    if level == 0:
        enemy1 = Actor('enemy1-1')
    elif level == 1:
        enemy1 = Actor('enemy2-1')
    elif level == 2:
        enemy1 = Actor('enemy3-1')
    enemy1.x = x
    enemy1.y = y
    enemy1.angle = angle
    x = enemy2.x
    y = enemy2.y
    angle = enemy2.angle
    if level == 0:
        enemy2 = Actor('enemy1-2')
    elif level == 1:
        enemy2 = Actor('enemy2-2')
    elif level == 2:
        enemy2 = Actor('enemy3-2')
    enemy2.x = x
    enemy2.y = y
    enemy2.angle = angle
    x = enemy3.x
    y = enemy3.y
    angle = enemy3.angle
    if level == 0:
        enemy3 = Actor('enemy2-3')
    elif level == 1:
        enemy3 = Actor('enemy2-3')
    elif level == 2:
        enemy3 = Actor('enemy3-3')
    enemy3.x = x
    enemy3.y = y
    enemy3.angle = angle
    x = enemy4.x
    y = enemy4.y
    angle = enemy4.angle
    if level == 0:
        enemy4 = Actor('enemy3-4')
    elif level == 1:
        enemy4 = Actor('enemy3-4')
    elif level == 2:
        enemy4 = Actor('enemy3-4')
    enemy4.x = x
    enemy4.y = y
    enemy4.angle = angle
    


def changeCollectable(level): # change collectable look but keep the x and y pos
    global collectable
    global new_wave_gem
    x = collectable.x
    y = collectable.y
    if level == 0:
        collectable = Actor('gem1')
    elif level == 1:
        collectable = Actor('gem2')
    elif level == 2:
        collectable = Actor('gem3')
    collectable.x = x
    collectable.y = y
    x = new_wave_gem.x
    y = new_wave_gem.y
    if level == 0:
        new_wave_gem = Actor('gem2')
    if level == 1:
        new_wave_gem = Actor('gem3')
    elif level == 2:
        new_wave_gem = Actor('command_gem')
    new_wave_gem.x = x
    new_wave_gem.y = y


### MAIN SCRIPT ###

changePlayer(wave)
changeEnemy(wave)
changeCollectable(wave) #confirm wave is correct before start (for testing purposes mainly)

def update_game():
    global score
    global invunerable
    global health
    global wave
    global rayX
    global rayY
    global gemCount
    global levelUpActivate
    global new_wave_score
    global enemy1Move
    global enemy2Move
    global enemy4Move
    global bullet_delay
    global enemyDir
    global enemyLoop
    global bullet_dir
    global game_state
    global gameLoops
    global gameOver
    global enemyBullets
    global enemy3Move
    global colour
    global stars
    global kaboom
    global kaboom_dur
    global bullets
    global secret_settings
    
    if secret_settings == True:
        if keyboard.q:
            levelUpActivate = True
        if keyboard.e:
            score += 10
    
    for i in range(len(kaboom_dur)-1):
        kaboom_dur[i] += 1
        if kaboom_dur[i] > 15:
            if len(kaboom_dur)-1 > i:
                kaboom_dur.remove(kaboom_dur[i])
            if len(kaboom)-1 > i:
                kaboom.remove(kaboom[i])
    
    for boom in kaboom:
        boom.y += 3
        if boom.y >= 610:
            if boom in kaboom:
                kaboom.remove(boom)
    
    if keyboard.a:
        player.y = player.y - (5* math.cos(math.radians(player.angle + 90)))
        player.x = player. x - (5* math.sin(math.radians(player.angle + 90))) #fancy math
    if player.x < -64:
        player.x = 864
    if keyboard.d:
        player.y = player.y - (5* math.cos(math.radians(player.angle - 90)))
        player.x = player. x - (5* math.sin(math.radians(player.angle - 90))) #fancy math
    if player.x > 864:
        player.x = -64
    if wave > 0:
        if keyboard.w or keyboard.up:
            player.y = player.y - (5* math.cos(math.radians(player.angle)))
            player.x = player. x - (5* math.sin(math.radians(player.angle))) # also fancy math
        
        if keyboard.s or keyboard.down:
            
            player.y = player.y + (5* math.cos(math.radians(player.angle)))
            player.x = player. x + (5* math.sin(math.radians(player.angle))) #fancy math but backwards
    
    if wave == 2: #raycast
        ray.x = player.x
        ray.y = player.y
        ray.angle = player.angle
        repeat = 0
        while (ray.colliderect(enemy1) or ray.colliderect(enemy2) or ray.colliderect(enemy3) or ray.colliderect(enemy4) or ray.x <= 0 or ray.y <= 0 or ray.x >= 800 or ray.y >= 600 or repeat > 100) == False:
            ray.y = ray.y - (5* math.cos(math.radians(player.angle)))
            ray.x = ray. x - (5* math.sin(math.radians(player.angle)))
        ray.y = ray.y - (60* math.cos(math.radians(player.angle)))
        ray.x = ray. x - (60* math.sin(math.radians(player.angle)))
        rayY = ray.y
        rayX = ray.x
    
    if player.y >= 600:
        player.y = 600
    if player.y <= 0:
        player.y = 0
    if wave > 1:
        if keyboard.right:
            player.angle -= 3
        if keyboard.left:
            player.angle += 3
    else:
        if keyboard.right:
            player.x += 5
        if keyboard.left:
            player.x -= 5
    if collectable.colliderect(player):#collecting collectable
        if wave == 0:
           sounds.sfx_sounds_impact3.play() 
        elif wave == 1:
            sounds.sfx_sounds_powerup18.play()
        elif wave == 2:
            sounds.sfx_sound_neutral10.play()
        gemCount += 1
        collectable.y = 0
        collectable.x = random.randint(15, 785)
        score += 10
        if gemCount % new_wave_score == 0:
            levelUpActivate = True
    
    if keyboard.space and bullet_delay == 0:#shootingd 
        if wave == 0:
            sounds.sfx_weapon_singleshot5.play()
            bullet_delay = 30
            bullet = Actor('bullet1')
            bullets.append(bullet)
        elif wave == 1:
            sounds.sfx_weapon_singleshot6.play()
            bullet_delay = 10
            bullet = Actor('bullet2')
            bullets.append(bullet)
        elif wave == 2:
            sounds.sfx_movement_portal4.play()
            bullet_delay = 20
            bullet = Actor('bullet3')
            bullets.append(bullet)
        if wave == 1:
            bullet.x = player.x + bullet_dir
            bullet.y = player.y
            bullet.angle = player.angle
            if bullet_dir == 35:
                bullet_dir = -35
            else:
                bullet_dir = 35
        else:
            bullet.x = player.x
            bullet.y = player.y
            bullet.angle = player.angle
    if bullet_delay > 0:
        bullet_delay -= 1
    
    for bullet in bullets:#bullet moving/destroying, enemy destroying (with boom)
        bullet.y = bullet.y - (10* math.cos(math.radians(bullet.angle)))
        bullet.x = bullet. x - (10* math.sin(math.radians(bullet.angle)))
        if bullet in bullets:
            if bullet.y < -64:
                bullets.remove(bullet)
            if bullet.y > 664:
                bullets.remove(bullet)
            if bullet.x < -64:
                bullets.remove(bullet)
            if bullet.x > 864:
                bullets.remove(bullet)
    
    for bullet in bullets: 
        if bullet.colliderect(enemy1):
            if wave == 0:
                sounds.door.play()
            elif wave == 1:
                sounds.sfx_exp_medium5.play()
            elif wave == 2:
                sounds.sfx_exp_medium1.play()
                boom = Actor('explosion')
                boom.x = enemy1.x
                boom.y = enemy1.y
                boom.angle = random.randint(0,359)
                kaboom.append(boom)
                kaboom_dur.append(0)
            if bullet in bullets:
                bullets.remove(bullet)
            enemy1Move = False
            enemy1.x = random.randint(20, 780)
            enemy1.y = -70
            score += 20
            
    
        if bullet.colliderect(enemy2):
            if wave == 0:
                sounds.door.play()
            elif wave == 1:
                sounds.sfx_exp_medium5.play()
            elif wave == 2:
                sounds.sfx_wpn_cannon5.play()
                boom = Actor('explosion')
                boom.x = enemy2.x
                boom.y = enemy2.y
                boom.angle = random.randint(0,359)
                kaboom.append(boom)
                kaboom_dur.append(0)
            if bullet in bullets:
                bullets.remove(bullet)
            enemy2Move = False
            enemy2.x = random.randint(20, 780)
            enemy2.y = -70
            score += 20
            
        if bullet.colliderect(enemy3):
            if wave == 0:
                sounds.door.play()
            elif wave == 1:
                sounds.sfx_exp_medium5.play()
            elif wave == 2:
                sounds.sfx_wpn_cannon5.play()
                boom = Actor('explosion')
                boom.x = enemy3.x
                boom.y = enemy3.y
                boom.angle = random.randint(0,359)
                kaboom.append(boom)
                kaboom_dur.append(0)
            if bullet in bullets:
                bullets.remove(bullet)
            enemy3Move = False
            enemy3.x = random.randint(20, 780)
            enemy3.y = -70
            score += 30
        
        if bullet.colliderect(enemy4):
            if wave == 0:
                sounds.door.play()
            elif wave == 1:
                sounds.sfx_exp_medium5.play()
            elif wave == 2:
                sounds.sfx_wpn_cannon5.play()
                boom = Actor('explosion')
                boom.x = enemy4.x
                boom.y = enemy4.y
                boom.angle = random.randint(0,359)
                kaboom.append(boom)
                kaboom_dur.append(0)
            if bullet in bullets:
                bullets.remove(bullet)
            enemy4Move = False
            enemy4.x = random.randint(20, 780)
            enemy4.y = -70
            score += 30
            
    for enemyBullet in enemyBullets:   #damage/death #1- enemy bullets
        if enemyBullet.colliderect(player):
            if wave == 0:
                sounds.sfx_sounds_error3.play()
            elif wave == 1:
                sounds.sfx_sounds_damage1.play()
            elif wave == 2:
                sounds.sfx_sounds_damage3.play()
            enemyBullets.remove(enemyBullet)
            invunerable = 60
            health -= 1
            if health <= 0:
                music.stop()
                sounds.sfx_sound_shutdown1.play()
                draw()
                enemy3Move = False
                gameLoops = 0
                gameOver = Actor('game_over1')
                gameOver.x = 400
                gameOver.y = 300
                game_state = 2
    
    if invunerable > 0: #double-damage invunerability
        if (enemy1.colliderect(player) or enemy2.colliderect(player) or enemy3.colliderect(player) or enemy4.colliderect(player)) == False:
            invunerable -= 1
    
    
    #damage/death #2- enemies
    if (enemy1.colliderect(player) or enemy2.colliderect(player) or enemy3.colliderect(player) or enemy4.colliderect(player)) and gameLoops > 30 and invunerable == 0:
        if wave == 0:
            sounds.sfx_sounds_error3.play()
        elif wave == 1:
            sounds.sfx_sounds_damage1.play()
        elif wave == 2:
            sounds.sfx_sounds_damage3.play()
        if enemy1.colliderect(player):
            enemy1.x = random.randint(20, 780)
            enemy1.y = -70
        elif enemy2.colliderect(player):
            enemy2.x = random.randint(20, 780)
            enemy2.y = -70
        elif enemy3.colliderect(player):
            enemy3x = random.randint(20, 780)
            enemy3.y = -70
        elif enemy4.colliderect(player):
            enemy4.x = random.randint(20, 780)
            enemy4.y = -70
        
        invunerable = 60
        health -= 1
        if health <= 0:
            music.stop()
            sounds.sfx_sound_shutdown1.play()
            draw()
            gameLoops = 0
            gameOver = Actor('game_over1')
            gameOver.x = 400
            gameOver.y = 300
            game_state = 2
      
    
    if wave == 2:#make stars in level 2
        if random.randint(1,10) == 1:
            star = Actor('star'+str(random.randint(1,5)))
            star.y = 0
            star.x = random.randint(10,790)
            stars.append(star)
    
    for star in stars:#move stars
        star.y += 3
        if star.y > 600:
            stars.remove(star)
    
    collectable.y += 4
    if levelUpActivate == True:#level up gem movement
        new_wave_gem.y += 6
        if new_wave_gem.y > 600:
            levelUpActivate = False
            new_wave_gem.y = -70
            new_wave_gem.x = random.randint(80, 720)
    
    if new_wave_gem.colliderect(player): #level up
        if wave == 0:
            sounds.sfx_coin_cluster6.play()
        elif wave == 1:
            sounds.sfx_coin_cluster8.play()
        elif wave == 2:
            sounds.sfx_sounds_negative2.play()
        levelUpActivate = False
        new_wave_score *= 3
        new_wave_gem.y = -70
        new_wave_gem.x = random.randint(80, 720)
        if wave < 2:
            wave += 1
            if wave == 1:
                health = 4
                music.play('retrogame_wave2')
            elif wave == 2:
                health = 5
                music.play('title')
            changePlayer(wave)
            changeCollectable(wave)
            changeEnemy(wave)
        else:
            music.play('boss music')
            colour = ['red1', 'green1', 'blue1', 'black1', 'black1', 'black1']
            wave = 500
            bullets = []
            game_state = 3
    
    
    
    if collectable.y > 600:#reset collectable
        collectable.y = 0
        collectable.x = random.randint(15, 785)
    
    #start to move enemy
    if random.randint(1, 1000) > 980 - (wave * 10):
        enemy1Move = True
    
    if random.randint(1, 2000) > 1980 - (wave * 10):
        enemy2Move = True
    
    if wave > 0:
        if random.randint(1, 2000) > 1975:
            enemy3Move = True
    
    if wave > 1 and enemy4.y < 0:
        if random.randint(1, 2000) > 1985:
            enemy4Move = True
            enemy4.angle = enemy4.angle_to(player) + 90
      
    #enemy movement
    if enemy1Move == True:
        enemy1.y += 5
        if enemy1.y > 700:
            enemy1Move = False
            enemy1.x = random.randint(20, 780)
            enemy1.y = -70
    
    if enemy2Move == True:
        if enemyDir == 1:
            enemy2.y += 5
            enemyLoop += 2
        elif enemyDir == 2:
            enemy2.x += 5
            enemyLoop += 1
        elif enemyDir == 3:
            enemy2.y += 5
            enemyLoop += 2
        else:
            enemy2.x -= 5
            enemyLoop += 1
        
        if enemyLoop == 40:
            enemyDir += 1
            enemyLoop = 0
            if enemyDir == 5:
                enemyDir = 1
        if enemy2.y > 700:
            enemy2Move = False
            enemy2.x = random.randint(150, 780)
            enemy2.y = -70
    
    if enemy3Move == True:
        enemy3.y += 5
        if gameLoops % 60 == 0:
            if wave == 1:
                enemyBullet = Actor('enemy_bullet2') 
                sounds.sfx_sounds_impact5.play()
            elif wave == 2:
                enemyBullet = Actor('enemy_bullet3')
                sounds.sfx_sound_nagger2.play()
            enemyBullets.append(enemyBullet)
            enemyBullet.x = enemy3.x
            enemyBullet.y = enemy3.y
        if enemy3.y > 700:
            enemy3Move = False
            enemy3.x = random.randint(20, 780)
            enemy3.y = -70
    for enemyBullet in enemyBullets:
        enemyBullet.y += 10
        if enemyBullet.y > 600:
            enemyBullets.remove(enemyBullet)
    
    if enemy4Move == True:
        enemy4.y = enemy4.y + (5* math.cos(math.radians(enemy4.angle)))
        enemy4.x = enemy4.x + (5* math.sin(math.radians(enemy4.angle)))
        if enemy4.y > 700:
            enemy4Move = False
            enemy4.x = random.randint(20, 780)
            enemy4.y = -70

def update_gameover():
    global wave
    global health
    global score
    global bullets
    global bullet_delay
    global bullet_dir
    global enemyLoop
    global enemyDir
    global enemy1Move
    global enemy2Move
    global enemy3Move
    global enemy4Move
    global new_wave_score
    global game_state
    global gameLoops
    global gameOverTransition
    global gameOver
    global enemyBullets
    global rayX
    global rayY
    global levelUpActivate
    global grid
    if gameOverTransition == 10:
        gameOver = Actor('game_over2-1')
        gameOver.x = 400
        gameOver.y = 300
        gameOverTransition = 11
    elif gameOverTransition == 20:
        gameOver = Actor('game_over3-2')
        gameOver.x = 400
        gameOver.y = 300
        gameOverTransition = 21
    elif gameOverTransition == 30:
        gameOver = Actor('game_over1-3')
        gameOver.x = 400
        gameOver.y = 300
        gameOverTransition = 31
    elif gameOverTransition == 11:
        gameOver = Actor('game_over2')
        gameOver.x = 400
        gameOver.y = 300
        gameOverTransition = 22
    elif gameOverTransition == 21:
        gameOver = Actor('game_over3')
        gameOver.x = 400
        gameOver.y = 300
        gameOverTransition = 32
    elif gameOverTransition == 31:
        gameOver = Actor('game_over1')
        gameOver.x = 400
        gameOver.y = 300
        gameOverTransition = 12
    
    elif random.randint(0,10000) > 9750:
        rng = random.randint(1,5)
        if rng == 1:
            sounds.sfx_sounds_error3.play()
        elif rng == 2:
            sounds.sfx_sounds_error5.play()
        elif rng == 3:
            sounds.sfx_sounds_error6.play()
        elif rng == 4:
            sounds.sfx_sounds_error11.play()
        elif rng == 5:
            sounds.sfx_sounds_error12.play()
        if gameOverTransition == 12:
            gameOver = Actor('game_over1-2')
            gameOver.x = 400
            gameOver.y = 300
            gameOverTransition = 10
            draw()
        if gameOverTransition == 22:
            gameOver = Actor('game_over2-3')
            gameOver.x = 400
            gameOver.y = 300
            gameOverTransition = 20
            draw()
        if gameOverTransition == 32:
            gameOver = Actor('game_over3-1')
            gameOver.x = 400
            gameOver.y = 300
            gameOverTransition = 30
            draw()
    
    if gameLoops > 60:
        if keyboard.space:
            music.play('ending')
            grid = []
            game_state = 0

def update_start():
    global start
    global won
    global high_score
    global score
    if score > high_score:
        high_score = score
    if keyboard.escape:
        exit()
    if won == True:
        start = Actor('start_front1-1', center = (400,300))
    else:
        start = Actor('start_front1', center = (400,300))


def create_glitch():
    global grid
    global game_state
    global length
    global colour
    global wave
    global health
    global score
    global bullets
    global bullet_delay
    global bullet_dir
    global enemyLoop
    global enemyDir
    global enemy1Move
    global enemy2Move
    global enemy3Move
    global enemy4Move
    global new_wave_score
    global game_state
    global gameLoops
    global gameOverTransition
    global gameOver
    global enemyBullets
    global rayX
    global rayY
    global levelUpActivate
    global grid
    global colour
    global singleColour
    global gameLoops
    global game_state
    global gameOver
    global boss_wave
    global invunerable
    global missiles
    global command_activate
    global shoot
    global bullets
    changePlayer(wave)
    glitch_width = 105
    glitch_height = 90
    grid = []
    for x in range(glitch_height):
        row = []
        for e in range(glitch_width):
            glitch = Actor('glitch_'+colour[random.randint(0,len(colour)-1)])
            row.append(glitch)
            glitch.x = e*12
            glitch.y = x*12
            
        grid.append(row)
    
    
def animate_load():
    global rect_x
    global rect_y
    global back_y
    global back_x
    global rel_rect_x
    global rel_rect_y
    global rel_back_x
    global rel_back_y
    global invunerable
    if rect_x <= 750 and not keyboard.s:
        rect_x += 150
        rel_rect_x -= 150
        clock.schedule_unique(animate_load, 0.1)
    elif rect_y <= 550 and not keyboard.s:
        rect_y += 40
        rel_rect_y -= 40
        rect_x = 40
        rel_rect_x = 720
        clock.schedule_unique(animate_load, 0.1)
    else:
        if back_x <= 750 and not keyboard.s:
            back_x += 150
            rel_back_x -= 150
            clock.schedule_unique(animate_load,0.1)
        elif back_y <= 550 and not keyboard.s:
            back_y += 40
            rel_back_y -= 40
            back_x = 40
            rel_back_x = 720
            clock.schedule_unique(animate_load, 0.1)
        else:
            sounds.zxspectrum_tape2.stop()
            sounds.sfx_menu_select4.play()
            invunerable = 60
            start_game()

def start_game():
    global grid
    global game_state
    global length
    global colour
    global wave
    global health
    global score
    global bullets
    global bullet_delay
    global bullet_dir
    global enemyLoop
    global enemyDir
    global enemy1Move
    global enemy2Move
    global enemy3Move
    global enemy4Move
    global new_wave_score
    global game_state
    global gameLoops
    global gameOverTransition
    global gameOver
    global enemyBullets
    global rayX
    global rayY
    global levelUpActivate
    global grid
    global colour
    global singleColour
    global gameLoops
    global game_state
    global gameOver
    global boss_wave
    global invunerable
    global missiles
    global command_activate
    global shoot
    global bullets
    global boss
    global stars
    global kaboom
    global bossHealth
    global gemCount
    global back_red
    global back_green
    global back_blue
    gemCount = 0
    back_red = 0
    back_green = 0
    back_blue = 0
    stars = []
    kaboom = []
    boss = Actor('finalboss')
    bossHealth = 3
    boss.y = -128
    boss.x = 400
    bossbullets = []
    missiles = []
    enemyBullets = []
    boss_wave = 2
    enemy1.x = random.randint(20, 780)
    enemy1.y = -70
    enemy2.x = random.randint(150, 780)
    enemy2.y = -70
    enemy3.x = random.randint(150, 780)
    enemy3.y = -70
    enemy4.x = random.randint(150, 780)
    enemy4.y = -70
    wave = 0
    score = 0
    health = 3
    new_wave_score = 10
    enemy1Move = False
    enemy2Move = False
    enemy3Move = False
    enemy4Move = False
    levelUpActivate = False
    rayX = 0
    rayY = 0
    enemyDir = 1
    enemyLoop = 0
    bullet_dir = 35
    bullets = []
    bullet_delay = 0
    new_wave_gem.x = random.randint(20, 780)
    new_wave_gem.y = -70
    player.x = 370
    player.y = 550
    player.angle = 0
    collectable.x = random.randint(15, 785)
    collectable.y = -70
    gameLoops = 0
    changePlayer(0)
    changeCollectable(0)
    changeEnemy(0)
    game_state = 2
    
def update_boss():
    global bossHealth
    global grid
    global colour
    global singleColour
    global gameLoops
    global game_state
    global gameOver
    global boss_wave
    global invunerable
    global missiles
    global command_activate
    global shoot
    global bullets
    global bossInvunerable
    global won
    global boss
    global particles
    glitch_width = 105
    glitch_height = 90
    grid = []
    
    if boss.y < 50:
        boss.y += 1
        gameLoops = 0
    else:
        if gameLoops < 600:
            if boss.x != player.x:
                if boss.x > player.x:
                    if boss.x - player.x > 2:
                        boss.x -= 2
                else:
                    if player.x - boss.x > 2:
                        boss.x += 2
            if gameLoops % 60 == 0:
                sounds.sfx_wpn_punch1.play()
                bossbullet = Actor('boss_bullet')
                bossbullet.x = boss.x
                bossbullet.y = boss.y
                bossbullets.append(bossbullet)
        elif gameLoops > 600 and gameLoops < 1200:
            if boss.x != player.x:
                if boss.x > player.x:
                    if boss.x - player.x > 4:
                        boss.x -= 4
                else:
                    if player.x - boss.x > 4:
                        boss.x += 4
            if gameLoops % 10 == 0:
                sounds.sfx_wpn_punch2.play()
                bossbullet = Actor('boss_bullet')
                bossbullet.x = boss.x
                bossbullet.y = boss.y
                bossbullets.append(bossbullet)
        elif gameLoops > 1200:
            if boss.x != 400:
                if boss.x > 400:
                    if boss.x - 400 > 2:
                        boss.x -= 2
                else:
                    if 400 - boss.x > 2:
                        boss.x += 2
            if gameLoops % 50 == 0:
                missileLocations = [800 - 800/6 * (i+1) for i in range(5)]
                for i in range(random.randint(1,3)):
                    sounds.sfx_wpn_missilelaunch.play()
                    missile = Actor('enemy_missile')
                    missile.y = 0
                    rng = random.randint(0,len(missileLocations)-1)
                    missile.x = missileLocations[rng]
                    missileLocations.remove(missileLocations[rng])
                    missiles.append(missile)
    
    if boss_wave < 2: #fix angle and y-pos when player level becomes low
        if player.angle % 360 != 0:
            if player.angle % 360 > 180:
                player.angle += 1
            else:
                player.angle -= 1
        if boss_wave < 1:
            if player.y > 550:
                player.y -= 1
            elif player.y < 550:
                player.y += 1
    
    if bossInvunerable > 0:
         bossInvunerable -= 1
    
    for bullet in bullets:
        if bullet.colliderect(boss) : #kill/damage the boss
            if bossInvunerable == 0:
                bossHealth -= 1
                if bossHealth <= 0:
                    sounds.sfx_sounds_fanfare1.play()
                    x = boss.x
                    y = boss.y
                    boss = Actor('trophy')
                    boss.y = y
                    boss.x = x
                    particles = []
                    for i in range(45):
                        particle = Actor('explode_particle')
                        particle.y = boss.y
                        particle.x = boss.x
                        particles.append(particle)
                    won = True
                    gameLoops = 0
                    game_state = 5
                else:
                    sounds.sfx_exp_medium7.play()
                    bossInvunerable = 60
            bullets.remove(bullet)
    
    for x in range(glitch_height):#create small background "glitches"
        row = []
        for e in range(glitch_width):
            if random.randint(1,50) == 3:
                glitch = Actor('glitch_'+colour[random.randint(0,len(colour)-1)])
                row.append(glitch)
                glitch.x = e*12
                glitch.y = x*12
        grid.append(row)
    
    for missile in missiles: #kaboom
        missile.y += 7
        if missile.colliderect(player) and invunerable <= 0:
            boss_wave -= 1
            if boss_wave < 0:
                gameLoops = 0
                gameOver = Actor('game_over1')
                gameOver.x = 400
                gameOver.y = 300
                game_state = 2
            else:
                invunerable = 60
                changePlayer(boss_wave)
    
    if random.randint(1,1000) > 898: #create large background "glitches"
        glitcher = Actor('glitch_'+singleColour[random.randint(0,3)])
        glitcher.x = random.randint(0,800)
        glitcher.y = random.randint(0,400)
        glitchers.append(glitcher)
        if len(glitchers) > 4:
            glitchers.remove(glitchers[0])
    
    
    #movement
    
    if keyboard.a:
        player.y = player.y - (5* math.cos(math.radians(player.angle + 90)))
        player.x = player. x - (5* math.sin(math.radians(player.angle + 90))) #fancy math
    if player.x < -64:
        player.x = 864
    if keyboard.d:
        player.y = player.y - (5* math.cos(math.radians(player.angle - 90)))
        player.x = player. x - (5* math.sin(math.radians(player.angle - 90))) #fancy math
    if player.x > 864:
        player.x = -64
    if boss_wave > 0:
        if keyboard.w or keyboard.up:
            player.y = player.y - (5* math.cos(math.radians(player.angle)))
            player.x = player. x - (5* math.sin(math.radians(player.angle))) # also fancy math
        
        if keyboard.s or keyboard.down:
            
            player.y = player.y + (5* math.cos(math.radians(player.angle)))
            player.x = player. x + (5* math.sin(math.radians(player.angle))) #fancy math but backwards
    if player.y > 600:
        player.y = 600
    if player.y < 0:
        player.y = 0
    
    if boss_wave > 1: 
        if keyboard.right:
            player.angle -= 3
        if keyboard.left:
            player.angle += 3
    else:
        if keyboard.right:
            player.x += 5
        if keyboard.left:
            player.x -= 5
    
    if command_activate == True: #move gem
        command_gem.y += 4
        if command_gem.y > 600:
            command_gem.y = -70
            command_activate = False
    
    if command_gem.colliderect(player): #detect gem collision
        shoot = True
        command_gem.y = -70
        command_gem.x = random.randint(150, 780)
        command_activate = False
    
    if keyboard.space and shoot == True: #shooting 5 bullets in a row if gem is collected (each bullet is either a 1, 0 or frog)
        sounds.sfx_sound_neutral5.play()
        codes = ["0","1","frog"]
        for i in range(5):
            bullet = Actor("matrix_"+codes[random.randint(0,2)]+"-1-1")
            bullets.append(bullet)
            bullet.x = player.x
            bullet.y = player.y
            bullet.angle = player.angle
            for bullet in bullets:
                bullet.y = bullet.y - (32* math.cos(math.radians(bullet.angle)))
                bullet.x = bullet. x - (32* math.sin(math.radians(bullet.angle)))
                if bullet in bullets:
                    if bullet.y < 0:
                        bullets.remove(bullet)
                    if bullet.y > 600:
                        bullets.remove(bullet)
                    if bullet.x < 0:
                        bullets.remove(bullet)
                    if bullet.x > 800:
                        bullets.remove(bullet)
            shoot = False
    
    for bullet in bullets:
        bullet.y = bullet.y - (10* math.cos(math.radians(bullet.angle)))
        bullet.x = bullet. x - (10* math.sin(math.radians(bullet.angle)))
        if bullet in bullets:
            if bullet.y < 0:
                bullets.remove(bullet)
            if bullet.y > 600:
                bullets.remove(bullet)
            if bullet.x < 0:
                bullets.remove(bullet)
            if bullet.x > 800:
                bullets.remove(bullet)
            
    
    for bossbullet in bossbullets: # control boss bullet movement/collisionsa
        bossbullet.y += 5
        bossbullet.angle = random.randint(0,359)
        if bossbullet.y > 600:
            bossbullets.remove(bossbullet)
        if bossbullet.colliderect(player) and invunerable <= 0:
            boss_wave -= 1
            if boss_wave < 0:
                gameLoops = 0
                gameOver = Actor('game_over1')
                gameOver.x = 400
                gameOver.y = 300
                game_state = 2
            else:
                invunerable = 60
                changePlayer(boss_wave)
    
    if gameLoops > 1800:
        gameLoops = 0
        command_activate = True
    if invunerable > 0:
        invunerable -= 1
    
    
def on_mouse_down(pos):
    global rect_x
    global rect_y
    global back_x
    global back_y
    global rel_rect_x
    global rel_rect_y
    global rel_back_x
    global rel_back_y
    global game_state
    global glitched
    global length
    global colour
    if game_state == 0:
        if pos[0] > 270 and pos[0] < 520 and pos[1] > 320 and pos[1] < 400:       
            music.stop()
            game_state = 4
            rect_x = 40
            rect_y = 40
            rel_rect_x = 720
            rel_rect_y = 500
            back_x = 40
            back_y = 40
            rel_back_x = 720
            rel_back_y = 500
            sounds.zxspectrum_tape2.play()
            colour = ['red1', 'green1', 'blue1', 'black1', 'black1']
            create_glitch()
            animate_load()
            
def update_boom(): #make boss go boom
    global gameLoops
    global particles
    global gameLoops
    global game_state
    i = 0
    for particle in particles:
        particle.y = particle.y - (10* math.cos(math.radians(i*8)))
        particle.x = particle.x - (10* math.sin(math.radians(i*8)))
        i += 1
    if gameLoops >= 30:
        time.sleep(0.2)
        game_state = 42

def update_win():
    global boss
    global game_state
    global grid
    if player.angle % 360 != 0:
        if player.angle % 360 > 180:
            player.angle += 1
        else:
            player.angle -= 1
    if player.x != 400:
        if player.x > 400:
            player.x -= 1
        elif player.x < 400:
            player.x += 1
    if player.y != 550:
        if player.y > 550:
            player.y -= 1
        elif player.y < 550:
            player.y += 1
    if boss.x != 400:
        if boss.x > 400:
            boss.x -= 1
        elif boss.x < 400:
            boss.x += 1
    if boss.y != 300:
        if boss.y > 300:
            boss.y -= 1
        elif boss.y < 300:
            boss.y += 1
    if keyboard.space:
        music.play('ending')
        grid = []
        game_state = 0

def on_mouse_move(pos):
    global game_state
    global small_x
    global small_y
    if game_state == 0:
        small_x = (pos[0]-400)/50
        small_y = (pos[1]-300)/50

def update(): #main game loop, 60x a second (if i don't lag out thonny with 1000's of actors)
    global gameLoops
    global secret_settings
    if game_state == 0:
        update_start()
    elif game_state == 1:
        update_game()
    elif game_state == 2:
        update_gameover()
    elif game_state == 3:
        update_boss()
    elif game_state == 42:
        update_win()
    elif game_state == 5:
        update_boom()
    gameLoops += 1
    if keyboard.lshift and keyboard.rshift and keyboard.e:
        secret_settings = True


def draw():
    global back_red
    global back_green
    global back_blue
    if game_state == 0:
        if len(grid) > 0:
            for i in grid:
                for glitch in i:
                    glitch.draw()
        else:
            screen.blit('start_back',(small_x,small_y))
            start.draw()
            screen.draw.text('High Score:' + str(high_score), (15,10), color=(255,255,255), fontname= 'pressstart2p', fontsize=15)
        
    elif game_state == 1 or game_state == 2:
        if wave < 3:
            screen.fill((back_red,back_green,back_blue))
            if back_red != screenRed[wave]:
                if back_red > screenRed[wave]:
                    back_red -= 1
                else:
                    back_red += 1
            if back_green != screenGreen[wave]:
                if back_green > screenGreen[wave]:
                    back_green -= 1
                else:
                    back_green += 1
            if back_blue != screenBlue[wave]:
                if back_blue > screenBlue[wave]:
                    back_blue -= 1
                else:
                    back_blue += 1
        else:
            screen.fill((100+random.randint(1,10),100+random.randint(1,10),100+random.randint(1,10)))
            for i in grid:
                for glitch in i:
                    glitch.draw()
            for glitcher in glitchers:
                glitcher.draw()
            boss.draw()
            for bossbullet in bossbullets:
                bossbullet.draw()
        for star in stars:
            star.draw()
        for bullet in bullets:
            bullet.draw()
        for enemyBullet in enemyBullets:
            enemyBullet.draw()
        for boom in kaboom:
            boom.draw()
        if wave < 3:
            enemy3.draw()
        if wave == 2 and keyboard.lshift:
            ray.draw()
            screen.draw.line((player.x,player.y),(rayX,rayY),(255,0,0))
            screen.draw.line((player.x+1,player.y+1),(rayX+1,rayY+1),(255,0,0))
            screen.draw.line((player.x-1,player.y-1),(rayX-1,rayY-1),(255,0,0))
        if invunerable > 0:
            if invunerable % 4 == 0:
                player.draw()
        else:
            player.draw()
        collectable.draw()
        new_wave_gem.draw()
        if wave < 3:
            enemy1.draw()
            enemy2.draw()
            enemy4.draw()
        if wave < 3:
            screen.draw.text('Score:' + str(score), (15,10), color=(mainRed[wave],mainGreen[wave],mainBlue[wave]), fontname= 'pressstart2p', fontsize=15)
        if wave == 0:
            screen.draw.text('Lives:' + str(health), (15,30), color=(mainRed[wave],mainGreen[wave],mainBlue[wave]), fontname= 'pressstart2p', fontsize=15)
        elif wave == 1:
            screen.draw.text('Health', (15,30), color=(mainRed[wave],mainGreen[wave],mainBlue[wave]), fontname= 'pressstart2p', fontsize=20)
            screen.draw.filled_rect(Rect((140,27),(190,30)), (48, 98, 48))
            screen.draw.filled_rect(Rect((145,32),(((health / 4)*180),20)), (139, 172, 15))
        elif wave == 2:
            healthColour = [0, 0, 0]
            if health == 5:
                healthColour[1] = 255
            elif health == 4:
                healthColour[0] = 100
                healthColour[1] = 255
            elif health == 3:
                healthColour[0] = 255
                healthColour[1] = 255
            elif health == 2:
                healthColour[0] = 255
                healthColour[1] = 100
            else:
                healthColour[0] = 255
            
            screen.draw.text('Health', (15,30), color=(mainRed[wave],mainGreen[wave],mainBlue[wave]), fontname= 'pressstart2p', fontsize=20)
            screen.draw.filled_rect(Rect((140,27),(190,30)), (0, 0, 0))
            screen.draw.filled_rect(Rect((145,32),(((health / 5)*180),20)), (healthColour[0], healthColour[1], healthColour[2]))    
        if game_state == 2:
            gameOver.draw()
    elif game_state == 3:
        if random.randint(0,3) == 3:
            screen.fill((100+random.randint(1,10),100+random.randint(1,10),100+random.randint(1,10)))
        for i in grid:
            for glitch in i:
                glitch.draw()
        for glitcher in glitchers:
            glitcher.draw()
        for bossbullet in bossbullets:
            bossbullet.draw()
        for missile in missiles:
            missile.draw()
        for bullet in bullets:
            bullet.draw()
        if invunerable > 0:
            if invunerable % 4 == 0:
                player.draw()
        else:
            player.draw()
        if bossInvunerable > 0:
            if bossInvunerable % 4 == 0:
                boss.draw()
        else:
            boss.draw()
        for bullet in bullets:
            bullet.draw()
        command_gem.draw()
    elif game_state == 42:
        screen.blit('start_back',(0,0))
        screen.draw.text('Congratulations- You Won!', (150,30), color=(255,255,255), fontname= 'patuaone-regular', fontsize=40)
        screen.draw.text('Press Space to Re-Install Virus and Play Again!', (175,75), color=(255,255,255), fontname= 'patuaone-regular', fontsize=20)
        boss.draw()
        player.draw()
    elif game_state == 4:
        BOX_FRONT = Rect((rect_x,rect_y),(rel_rect_x,rel_rect_y))
        BOX_FRONTY = Rect((40,rect_y+40),(720,rel_rect_y))
        BOX_BACK = Rect((back_x,back_y),(rel_back_x,rel_back_y))
        BOX_BACKY = Rect((40,back_y+40),(720,rel_back_y))
        screen.fill((0,0,0))
        if len(grid) > 0:
            for i in grid:
                for glitch in i:
                    glitch.draw()
        screen.draw.filled_rect(Rect((30,30),(740,560)), (255,255,255))
        load_full.draw()
        screen.draw.filled_rect(BOX_BACK,(255, 255, 255))
        screen.draw.filled_rect(BOX_BACKY,(255, 255, 255))
        load_half.draw()
        screen.draw.filled_rect(BOX_FRONT,(255, 255, 255))
        screen.draw.filled_rect(BOX_FRONTY,(255, 255, 255))
    elif game_state == 5:
        screen.fill((0,0,gameLoops*2))
        boss.draw()
        player.draw()
        for particle in particles:
            particle.draw()

pgzrun.go()
#