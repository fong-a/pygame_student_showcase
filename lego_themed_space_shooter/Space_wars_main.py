#
#   Space wars by Sam Hildebrandt
#   v : 0.01
#   1st April 2022
#

import pgzrun
import random
from countdowntimer import CountdownTimer
from high_score import load_high_score, save_high_score
from dad import draw_laser

# =================
# ==  Constants  ==
# =================

# World cordinates
WORLD_WIDTH = 2560 
WORLD_HEIGHT = 1600

# Screen / Window size
WIDTH = 1200
HEIGHT = 800

# Game states
WELCOME = 0
LEVEL1 = 1
LEVEL2 = 2
LEVEL_CHASE = 3
GAME_OVER = 4
CONTROLS = 5
INFORMATION = 6 

# Welcome screen backgrounds
welcome_backgrounds = {WELCOME     : 'menu_background_1',
                       INFORMATION : 'menu_background_information',
                       CONTROLS    : 'menu_background_controls'}

# Music setup
music_list = {WELCOME     : 'welcome',
              LEVEL1      : 'level1',
              LEVEL2      : 'level2',
              LEVEL_CHASE : 'level3',
              GAME_OVER   : 'game_over',
              CONTROLS    : 'welcome',
              INFORMATION : 'welcome'}

# =================
# ==  Variables  ==
# =================

# Sound on / off
sound_on = True

# Debug mode - enable shortcuts to levels
debug = False 

# Score variables
score = 0
score_to_continue = 0
high_score = load_high_score()

# Game complete
game_complete = False

# Laser  variables
fire_laser = False
laser_step = 0
laser_max_power = 150
laser_power = laser_max_power

# Veiw window position (in world cordinates)
window = {'x' : 400,
          'y' : 400}

# Cross hairs 
cross_hairs = {'x'     : window['x'] + (WIDTH/2),
               'y'     : window['y'] + (HEIGHT/2),
               'actor' : Actor('cross_hairs')}

# Game over actor
game_over = Actor('game_over', center = (WIDTH/2, HEIGHT/2))

# Well done actor
well_done = Actor('well_done', center = (WIDTH/2, HEIGHT/2))

# Background animation for chase level
chase_backgrounds = ["chase_background" + str(x+1) for x in range(10)]  # Make a list of file names for the background animation
chase_background_step = 0

# List of current eneimies and power ups and explosions and pop ups
enemies = []
power_ups = []
explosions = []
pop_ups = []

# Current game state
current_state = -1 

# Level timer
level_timer = CountdownTimer()

# Message object
message = {'text' : '',
           'step' : 0,
           'colour' : (255, 255, 0)}

# =========================
# ==  General functions  ==
# =========================

# Cheack sound on
def check_sound():
    if not sound_on and music.is_playing(''):
        music.stop()
    elif sound_on and not music.is_playing(''):
        music.play(music_list[current_state])

# Play a sound if sound is enabled
def play_sound(s):
    if sound_on:
        s.play()

# Key press event (called automatically once any time a key is pressed)
def on_key_down(key):
    global fire_laser
    global laser_power
    global sound_on
    if current_state >= LEVEL1 and current_state < GAME_OVER:
      if key == keys.SPACE and laser_power > 50:
        fire_laser = True
        play_sound(sounds.laser)
        laser_power -= 50
        
    if keyboard.m:
        sound_on = not sound_on

# Check keyboard (called from update() )
def check_keyboard():
    
    if keyboard.left:
        cross_hairs['x'] -= 7
        if cross_hairs['x'] < 0:
            cross_hairs['x'] = 0
          
    elif keyboard.right:
        cross_hairs['x'] += 7
        if cross_hairs['x'] > WORLD_WIDTH -1:
            cross_hairs['x'] = WORLD_WIDTH -1
        if current_state == LEVEL_CHASE and cross_hairs['x'] > WIDTH:
            cross_hairs['x'] = WIDTH
      
    if keyboard.up:
        cross_hairs['y'] -= 7
        if cross_hairs['y'] < 0:
            cross_hairs['y'] = 0
        
    elif keyboard.down:
        cross_hairs['y'] += 7
        if cross_hairs['y'] > WORLD_HEIGHT -1:
            cross_hairs['y'] = WORLD_HEIGHT -1
        if current_state == LEVEL_CHASE and cross_hairs['y'] > HEIGHT:
            cross_hairs['y'] = HEIGHT

    if current_state >= LEVEL1 and current_state < LEVEL_CHASE:
      if keyboard.a:
          if window['x'] > 20:
              window['x']-= 20
              cross_hairs['x'] -= 20
            
      elif keyboard.d:
          if window['x'] < WORLD_WIDTH - WIDTH - 20:
              window['x']+= 20
              cross_hairs['x'] += 20
            
      if keyboard.w:
          if window['y'] > 20:
              window['y']-= 20
              cross_hairs['y'] -= 20
            
      if keyboard.s:
          if window['y'] < WORLD_HEIGHT - HEIGHT - 20:
              window['y']+= 20
              cross_hairs['y'] += 20
            
    if current_state == WELCOME:
      if keyboard.i:
          set_state(INFORMATION)
          
      if keyboard.c:
          set_state(CONTROLS)
      
      if keyboard.p:
        set_state(LEVEL1)
        
      if keyboard.e:
          exit() 
        
    if keyboard.b and (current_state == INFORMATION or current_state == CONTROLS):
        set_state(WELCOME)
        
    # Debug mode
    if debug:
      if keyboard.k_1:
        set_state(LEVEL1)
        
      if keyboard.k_2:
        set_state(LEVEL2)
        
      if keyboard.k_3:
        set_state(LEVEL_CHASE)
        
      if keyboard.k_0:
        set_state(GAME_OVER)
        
# ==================
# ==   Enemies    ==
# ==================

# Create big fighter
def create_big_fighters(n):
    for i in range(n):    
      actors = ['lego_big_fighter_right', 'lego_big_fighter_left'] 
      dir = random.randint(0,1)
      f = {'type'    : 'big_fighter',
           'actor'   : Actor(actors[dir]),
           'x'       : random.randint(0, WORLD_WIDTH),
           'y'       : random.randint(30, WORLD_HEIGHT - 30),
           'speed_x' : random.randint(1,4),
           'dir'     : dir,
           'score'   : 10}
      enemies.append(f)     

# Create blue fighter
def create_blue_fighters(n):
    for i in range(n):
      actors = ['lego_fighter_right', 'lego_fighter_left'] 
      dir = random.randint(0,1)
      f = {'type'    : 'blue_fighter',
           'actor'   : Actor(actors[dir]),
           'x'       : random.randint(0, WORLD_WIDTH),
           'y'       : random.randint(30, WORLD_HEIGHT - 30),
           'speed_x' : random.randint(2,5),
           'speed_y' : 0,
           'dir'     : dir,
           'score'   : 15}
      enemies.append(f)
    
# Create red fighter
def create_red_fighters(n):
    for i in range(n):    
      actors = ['lego_red_fighter_right', 'lego_red_fighter_left'] 
      dir = random.randint(0,1)
      y = random.randint(30, WORLD_HEIGHT - 30)
      f = {'type'    : 'red_fighter',
           'actor'   : Actor(actors[dir]),
           'x'       : random.randint(0, WORLD_WIDTH),
           'y'       : y,
           'speed_x' : random.randint(3,7),
           'speed_y' : 0,
           'new_y_timer'   : 0, # Counter for new position
           'new_y'   : y,
           'dir'     : dir,
           'score'   : 20}
      enemies.append(f) 
      
# Create chase fighter
def create_chase_fighters(n):
    for i in range(n):    
      f = {'type'    : 'chase',
           'actor'   : Actor('chase_fighter'),
           'x'       : random.randint(200, WIDTH - 200),
           'y'       : -100,
           'speed_x' : 0,
           'speed_y' : 0,
           'new_x'   : 0,
           'new_y'   : 0,
           'new_pos_timer'   : 0, # Counter for new position
           'score'   : 50}
      enemies.append(f)
 
# Update chase fighter
def update_chase_fighter(e):
    
    if e != enemies[0]:  # If not first enemy, do not update 
      return
     
    # Check if its time to choose new location
    e['new_pos_timer'] -= 1  # Decrement the new position timer
    
    if e['new_pos_timer'] <= 0:  #If timer has timed out, choose new position
        e['new_x'] = random.randint(200, WIDTH - 200)
        e['new_y'] = random.randint(100, HEIGHT - 100)
        e['new_pos_timer'] = random.randint(30,50)
    
    # Update enemy speed retive to distance to new position
    desired_speed_x = (e['new_x'] - e['x']) * 0.1
    if e['speed_x'] < desired_speed_x:
        e['speed_x'] += 1
    elif e['speed_x'] > desired_speed_x:
        e['speed_x'] -= 1
    
    desired_speed_y = (e['new_y'] - e['y']) * 0.1
    if e['speed_y'] < desired_speed_y:
        e['speed_y'] += 1
    elif e['speed_y'] > desired_speed_y:
        e['speed_y'] -= 1
    
    # Limit the speeds 
    if e['speed_x'] > 20:
        e['speed_x'] = 20
    elif e['speed_x'] < -20:
        e['speed_x'] = -20
        
    if e['speed_y'] > 10:
        e['speed_y'] = 10
    elif e['speed_y'] < -10:
        e['speed_y'] = -10

    # Apply the speed
    e['x'] += e['speed_x']
    e['y'] += e['speed_y']
    
    # Apply angle relaitve to x speed
    e['actor'].angle = -e['speed_x'] * 2
    
# Check for enemies hit by laser
def check_enemy_hit():
    global score
    for e in enemies:
        if e['actor'].collidepoint(cross_hairs['actor'].center):
            create_explosion(cross_hairs['x'], cross_hairs['y'])
            display_pop_up("+" + str(e['score']), 0, cross_hairs['actor'].x, cross_hairs['actor'].y - 50)
            score += e['score']
            play_sound(sounds.explosion)
            enemies.remove(e)    

# Update any enemy 
def update_enemy(e): 
    if e['type'] == 'chase':
        update_chase_fighter(e)
        
    else:  # All other enemies handled below    
    
      # Do motion in x direction
      if e['dir'] == 0:                   # If direction = Left
          e['x'] += e['speed_x']
          if e['x'] > WORLD_WIDTH + 50:
              e['x'] = -50
              e['y'] = random.randint(30, WORLD_HEIGHT - 30)
      else:
          e['x'] -= e['speed_x']
          if e['x'] < -50:                # If direction = Right
              e['x'] = WORLD_WIDTH + 50
              e['y'] = random.randint(30, WORLD_HEIGHT - 30)
    
      # Do motion in y direction for enemies that have a new_y value
      if 'new_y' in e:  
          if e['new_y_timer'] > 0:          # Decrement timer
              e['new_y_timer'] -= 1
          else:                             # Time to pick a new y value
              e['new_y_timer'] = random.randint(500,1500)
              e['new_y'] = random.randint(20,HEIGHT - 20)
              e['speed_y'] = random.randint(1,4)
              if e['new_y'] < e['y']:
                e['speed_y'] *= -1
            
          e['y'] += e['speed_y']             # update the y value acording to the speed
        
          # If going down and reached new_y OR going up and reached new_y
          if (e['speed_y'] > 0 and e['y'] > e['new_y']) or (e['speed_y'] < 0 and e['y'] < e['new_y']):    
              e['y'] = e['new_y']
              e['speed_y'] = 0               # Stop vertical movment
        
          # Calculate desired angle for actor relative to its vertical speed
          desired_angle = e['speed_y'] * 5
          if e['dir'] == 0:                  # If travelling left 
              desired_angle *= -1            # Invert the angle 
        
          # Update the actors angle 
          if e['actor'].angle < desired_angle:
              e['actor'].angle += 1
          elif e['actor'].angle > desired_angle:
              e['actor'].angle -= 1
                  
    # Update actor positions for ALL enemies
    e['actor'].x = e['x'] - window['x']
    e['actor'].y = e['y'] - window['y']
    
# ==================
# ==  Power Ups   ==
# ==================
  
# Extra time power up
def create_time_power_ups(n):
    for i in range(n):
        p = {'type'    : 'time',
             'actor'   : Actor('clock'),
             'x'       : random.randint(30, WORLD_WIDTH - 30),
             'y'       : random.randint(30, WORLD_HEIGHT - 30),
             'time'    : 10,
             'step'    : 0,
             'visible' : False}
        power_ups.append(p)
        
# Extra laser power up
def create_laser_power_ups(n):
    for i in range(n):
        p = {'type'    : 'power',
             'actor'   : Actor('battery'),
             'x'       : random.randint(30, WORLD_WIDTH - 30),
             'y'       : random.randint(30, WORLD_HEIGHT - 30),
             'power'   : 50,
             'step'    : 0,
             'visible' : False}
        power_ups.append(p)

# Check for power up hit by laser
def check_power_up_hit():
   global laser_max_power
   for p in power_ups:
        if p['actor'].collidepoint(cross_hairs['actor'].center) and p['visible']:
            if p['type'] == 'time':
              play_sound(sounds.extra_time)
              level_timer.extend(p['time'])
            elif p['type'] == 'power':
              play_sound(sounds.laser_power_up)
              laser_max_power += p['power']
            power_ups.remove(p)

# Update power up position
def update_power_up(p):
    p['actor'].x = p['x'] - window['x']
    p['actor'].y = p['y'] - window['y']
    if p['step'] > 0:
        p['step'] -= 1
    else:
       p['step'] = random.randint(500,1000)
       p['x'] = random.randint(30, WORLD_WIDTH - 30)
       p['y'] = random.randint(30, WORLD_HEIGHT - 30)
    
    p['visible'] = p['step'] < 300
    
    # Wiggle by changing actor angle
    if p['visible']:
        a = (p['step'] % 20 - 10) * 2
        if (p['step'] % 40) >= 20:
            a *= -1 
        p['actor'].angle = a
      
# ==================
# ==  Explosions  ==
# ==================

# Create explosion
def create_explosion(x,y):
        ex = {'actor'   : Actor('explosion1'),
              'images'  : [ 'explosion' + str(i+1) for i in range(11)],
              'x'       : x,
              'y'       : y,
              'step'    : 0}
        explosions.append(ex)
    
# Update explosion 
def update_explosion(ex):
    ex['actor'].x = ex['x'] - window['x']
    ex['actor'].y = ex['y'] - window['y']
    if ex['step'] < len(ex['images']):
        ex['actor'].image = ex['images'][ex['step']]
        ex['step'] += 1
    else:
        explosions.remove(ex)

# ===============
# ==  Pop ups  ==
# ===============

# Display pop up
def display_pop_up(text,duration,x,y):
    p = {'text' : text,
         'step' : duration * 60 + 30,  # Number of updates + 30 fade out
         'x'    : x,
         'y'    : y}
    pop_ups.append(p)

# Update pop up
def update_pop_up(p):
    if p['step'] > 1:
        p['step'] -= 1
        p['y'] -= 1
    else:
        pop_ups.remove(p)
        
# Draw pop up
def draw_pop_up(p):
    alpha = 1
    if p['step'] <30:
      alpha = p['step'] / 30
        
    screen.draw.text(p['text'], center = (p['x'], p['y']), color = (255,255,0), fontsize=40, alpha = alpha)
        
# ==============
# ==  Message ==
# ==============

# Display message
def display_message(mesg,duration):
    message['text'] = mesg
    message['step'] = duration * 60 + 100 # Number of updates + 100 for fade out
    
# Update message
def update_message():
    if message['step'] > 0:
        message['step'] -= 1
    
# Draw message
def draw_message():
    if message['step'] > 100:
        screen.draw.text(message['text'], center = (WIDTH / 2 , HEIGHT / 2 - 100), color = message['colour'], fontsize=70)
    elif message['step'] > 0:
        screen.draw.text(message['text'], center = (WIDTH / 2 , HEIGHT / 2 - 100), color = message['colour'], fontsize=70, alpha = message['step'] / 100)
        
# =========================
# ==  Laser Power Level  ==
# =========================

# Update laser power
def update_laser_power():
    global laser_power
    
    if laser_power < laser_max_power:
        laser_power += 0.5

# Draw power level
def draw_laser_power():
    
    # Set location of bar graph bottom left
    blx = WIDTH - 50
    bly = HEIGHT - 50
    
    # Calculate bar heights
    max_bar_height = laser_max_power
    bar_height = max_bar_height * (laser_power / laser_max_power)
    
    # Create rectangles
    max_bar = Rect((blx, bly - max_bar_height), (20, max_bar_height))
    bar = Rect((blx, bly - bar_height), (20, bar_height))
    
    # Calculate bar colour relative to power level
    green = 255 * (laser_power / laser_max_power)
    red = 255 - green
    
    # Draw bar graph
    screen.draw.filled_rect(max_bar, (0, 0, 0))  # Black background
    screen.draw.filled_rect(bar, (red, green, 0))  # Colored bar graph
    screen.draw.rect(max_bar, (255, 255, 255))  # White frame
    screen.draw.text('Power', (WIDTH - 70,HEIGHT - 35), color=(255,255,255), fontsize=30)  # Power label

# ===============================
# ==  Main game state control  ==
# ===============================

# Set a new game state
def set_state(state):
    global current_state
    global score
    global score_to_continue
    global high_score
    
    enemies.clear()
    power_ups.clear()
    explosions.clear()
    pop_ups.clear()
    game_complete = False
    if state == LEVEL1:  # Level 1
        create_blue_fighters(10)
        create_big_fighters(15)
        create_time_power_ups(5)
        create_laser_power_ups(2)
        level_timer.set(30)
        score = 0
        score_to_continue = 150
        
    elif state == LEVEL2:  # Level 2
        create_blue_fighters(15)
        create_red_fighters(10)
        create_time_power_ups(5)
        create_laser_power_ups(2)
        level_timer.set(30)
        score_to_continue = score + 200
        play_sound(sounds.level_up)
        
    elif state == LEVEL_CHASE:  # Level 3
        window['x'] = 0
        window['y'] = 0
        cross_hairs['x'] = WIDTH / 2
        cross_hairs['y'] = HEIGHT / 2
        create_chase_fighters(10)
        level_timer.set(60)
        score_to_continue = score + 250
        play_sound(sounds.level_up)

    
    elif state == GAME_OVER:  # Game over
        level_timer.set(5)
        if score > high_score:
            high_score = score
            save_high_score(high_score)
    
    # Play music for each level
    if music_list[state] != '' and sound_on:
        music.stop()
        music.set_volume(0.3)
        if state == GAME_OVER:
            music.play(music_list[state])
    current_state = state
    
    # Display the level
    display_message(f'Level {current_state}', 2)
    
# Check for end of level
def check_for_end_level():
    global game_complete
    
    if current_state >= LEVEL1 and current_state < GAME_OVER: # currently in game mode
        if len(enemies) == 0 or level_timer.is_time_up():     # no enemies left or time is up
            if score >= score_to_continue:                    # score is good enough to continue
                set_state(current_state + 1)                  # go to next level
                game_complete = (current_state == GAME_OVER)  # just completed the last level
            else:
                set_state(GAME_OVER)                          # else game is over
                    
    elif current_state == GAME_OVER:
        if level_timer.is_time_up():
          set_state(WELCOME)

# ========================
# == Laser firing code  ==
# ========================
        
# Check laser
def check_laser():
    global fire_laser
    global laser_step
    
    if fire_laser:
        laser_step += 1
        if laser_step > 7:
            check_enemy_hit()
            check_power_up_hit()
            laser_step = 0
            fire_laser = False
            
# Draw laser
def draw_lasers():
    if laser_step > 0:
        draw_laser(screen,(100, HEIGHT), cross_hairs['actor'].center, laser_step)
        draw_laser(screen,(WIDTH - 100, HEIGHT), cross_hairs['actor'].center, laser_step)
        
# Update cross hairs position        
def update_cross_hairs():
    cross_hairs['actor'].x = cross_hairs['x'] - window['x']
    cross_hairs['actor'].y = cross_hairs['y'] - window['y']
     

# ============================
# ==  Main update function  ==
# ============================

def update():
    
    global current_state
    global chase_background_step
    
    # Check keyboard
    check_keyboard()
    
    # Check sound is on or off
    check_sound()
    
    # Check for end of level
    check_for_end_level()
    
    
    # Window limit
    if cross_hairs['x'] < window['x']:
        window['x'] = cross_hairs['x']
    
    if cross_hairs['x'] > window['x'] + WIDTH:
        window['x'] = cross_hairs['x'] - WIDTH
        
    if cross_hairs['y'] < window['y']:
        window['y'] = cross_hairs['y']
    
    if cross_hairs['y'] > window['y'] + HEIGHT:
        window['y'] = cross_hairs['y'] - HEIGHT

     # Check for laser
    check_laser()
    
    # Update game objects
    for e in enemies:
        update_enemy(e)
        
    for p in power_ups:
        update_power_up(p)
        
    for p in pop_ups:
        update_pop_up(p)
        
    for ex in explosions:
        update_explosion(ex)
    
    # Update cross hairs
    update_cross_hairs()
    
    # Update laser power
    update_laser_power()
    
    # Update message
    update_message()
    
    # Chase level background animation
    if current_state == LEVEL_CHASE:
        chase_background_step += 1
        if chase_background_step >= len(chase_backgrounds)*2:
            chase_background_step = 0

# =========================
# == Main draw function  ==
# =========================

def draw():
    
    global score        
    
    # Weclome screens
    if current_state == WELCOME or current_state == INFORMATION or current_state == CONTROLS:
        screen.blit(welcome_backgrounds[current_state], (0,0))
        screen.draw.text('High score: ' + str(high_score), (30, HEIGHT-50), color=(255,255,0), fontsize=50)
    
    # Game over window
    elif current_state == GAME_OVER:
        if game_complete:
            well_done.draw()
        else:
            game_over.draw()
        screen.draw.text('Your score: ' + str(score), center = (WIDTH/2,HEIGHT/2 + 20), color=(255,255,255), fontsize=50)
        screen.draw.text('High score: ' + str(high_score), center = (WIDTH/2,HEIGHT/2+ 80), color=(255,255,255), fontsize=50)
        
    else:  # Current state is a game level
      if current_state == LEVEL_CHASE:  
          screen.blit(chase_backgrounds[ chase_background_step//2], (-window['x'],-window['y']))  # Level chase background
      else:  
          if current_state == LEVEL1:  
              screen.blit('background_1',(-window['x'],-window['y']))  # Level 1 background
          elif current_state == LEVEL2:
              screen.blit('background_2',(-window['x'],-window['y']))  # Level 2 background
      
      for e in enemies:
          e['actor'].draw()  # Draw enemies
          
      for p in power_ups:
          if p['visible']:
              p['actor'].draw()  # Draw power ups
          
      for ex in explosions:
          ex['actor'].draw()  # Draw explosions
          
      for p in pop_ups:
          draw_pop_up(p)  # Draw pop_ups
    
      # Draw laser
      draw_lasers()
      
      # Draw cross hairs
      cross_hairs['actor'].draw()
      
      # Draw score
      screen.draw.text('Score: ' + str(score), (15,10), color=(255,255,255), fontsize=30)
      
      # Draw level timer
      screen.draw.text('Mission Time: ' + level_timer.as_string(), (WIDTH - 200, 10), color=(0,255,0), fontsize=30)
      
      # Draw laser power level 
      draw_laser_power()
      
      # Draw messages
      draw_message()
    
# Main program starts here    
set_state(WELCOME)

pgzrun.go() # Must be last line