"""
April 26, 2014
Kaili Liu
"""
# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [300, 200]
ball_vel = [5,-5]
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0



# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    if direction == RIGHT:       
        ball_vel[0] = - (random.randrange(120, 240))/60
        ball_vel[1] = - (random.randrange(60, 180))/60
      
    
    if direction == LEFT:
        ball_vel[0] = (random.randrange(120, 240))/60
        ball_vel[1] = - (random.randrange(60, 180))/60


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos  # these are numbers
    global score1, score2  # these are integers
    ball_pos = [300, 200]
    paddle1_pos = 200
    paddle2_pos = 200
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(LEFT)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
 
        
    # draw mid line 
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    
    #draw gutters
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    
    #collide and reflect off of bottom of canvas
    if ball_pos[1] >= (HEIGHT-1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    #collide and reflect off of top of canvas
    if ball_pos[1] <= BALL_RADIUS:
       ball_vel[1] = - ball_vel[1]   
                          
    #collide and reflect off of left gutter
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if 40 >= abs(paddle1_pos - ball_pos[1]):
            ball_vel[0] = - 1.1 * ball_vel[0]
           
        
        else:
            score2 += 1
            ball_pos = [300, 200]
            spawn_ball(LEFT)        
            
    #collide and reflect off of right gutter
    if ball_pos[0] >= (WIDTH - 1) - BALL_RADIUS - PAD_WIDTH:
        if 40 >= abs(paddle2_pos - ball_pos[1]):
            ball_vel[0] = - 1.1 *ball_vel[0]
        
        
        else:
            score1 += 1
            ball_pos = [300, 200]
            spawn_ball(RIGHT)
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, 'Aqua', 'Aqua')
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    
    
    if paddle1_pos <= 40: 
        paddle1_pos = 40
        paddle1_vel = 0
    if paddle1_pos >= 360:
        paddle1_pos = 360
        paddle1_vel = 0
    if paddle2_pos <= 40:
        paddle2_pos = 40
        paddle2_vel = 0
    if paddle2_pos >= 360:
        paddle2_pos = 360
        paddle2_vel = 0
            
            
    # draw paddles
    canvas.draw_polygon([(0, paddle1_pos - 40), (PAD_WIDTH - 1, paddle1_pos - 40), (PAD_WIDTH - 1, paddle1_pos + 40), (0, paddle1_pos + 40)], 1, 'Silver', 'SILVER')
    canvas.draw_polygon([(WIDTH - PAD_WIDTH + 1, paddle2_pos - 40), (WIDTH, paddle2_pos - 40), (WIDTH, paddle2_pos + 40), (WIDTH - PAD_WIDTH + 1, paddle2_pos + 40)], 1, 'Silver', 'SILVER')

    
    # draw scores
    canvas.draw_text(str(score1), (230, 30), 36, 'White')
    canvas.draw_text(str(score2), (350, 30), 36, 'White')
    
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
           paddle1_vel = 0
    if key == simplegui.KEY_MAP['s']:
           paddle1_vel = 0
    if key == simplegui.KEY_MAP['up']:
           paddle2_vel = 0
    if key == simplegui.KEY_MAP['down']:            
           paddle2_vel = 0   
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
           paddle1_vel = -5
    if key == simplegui.KEY_MAP['s']:
           paddle1_vel = 5
    if key == simplegui.KEY_MAP['up']:
           paddle2_vel = -5
    if key == simplegui.KEY_MAP['down']:            
           paddle2_vel = 5

  

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
restart_button = frame.add_button('Restart', new_game, 75)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
