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
left_score = 0
right_score = 0
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = paddle2_vel = 0

# initialize ball_pos and ball_vel for new bal in middle of table
ball_pos = [WIDTH//2, HEIGHT//2]
ball_vel = [1, 2]

# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global LEFT, RIGHT
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH//2, HEIGHT//2]
    if(direction == LEFT):
        ball_vel[0] = -1
    else:
        ball_vel[0] = 1

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global left_score, right_score  # these are ints
    global ball_pos, ball_vel
    global LEFT, RIGHT
    left_score = 0
    right_score = 0
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = paddle2_vel = 0
    ball_pos = [WIDTH//2, HEIGHT//2]
    ball_vel = [1, 2]

def draw(c):
    global left_score, right_score, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # update ball
    ball_pos[0] += ball_vel[0] 
    ball_pos[1] += ball_vel[1] 
    if(ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH + 1)):  #1 for gutter width
        if(ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT and ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT):
            ball_vel[0] = -(ball_vel[0] + float(ball_vel[0]) / 3)
            
        else:
            #Left Loses, Start ball with direction from right
            right_score += 1
            #call spawn_ball
            spawn_ball(RIGHT)
   
    if(ball_pos[0] >= ((WIDTH - PAD_WIDTH) - (BALL_RADIUS))):
        if(ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT and ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT):
            ball_vel[0] = -(ball_vel[0] + float(ball_vel[0]) / 3)
        else:
            #Right Loses, Start ball with direction from left
            left_score += 1
            #call spawn_ball
            spawn_ball(LEFT)
            
    if(ball_pos[1] <= BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
        
    if(ball_pos[1] >= ((HEIGHT-1)-BALL_RADIUS)):
        ball_vel[1] = -ball_vel[1]
    
    
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos -= paddle1_vel
    paddle2_pos -= paddle2_vel
    
    #avoid paddles going into the boundaries
    if(paddle1_pos <= HALF_PAD_HEIGHT):
        paddle1_pos = HALF_PAD_HEIGHT
    if(paddle1_pos >= HEIGHT - HALF_PAD_HEIGHT):
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
        
    if(paddle2_pos <= HALF_PAD_HEIGHT):
        paddle2_pos = HALF_PAD_HEIGHT
    if(paddle2_pos >= HEIGHT - HALF_PAD_HEIGHT):
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
        
        
    # draw paddles
    c.draw_line([0, paddle1_pos - HALF_PAD_HEIGHT], [0, paddle1_pos + HALF_PAD_HEIGHT], PAD_WIDTH + 2, "White")
    c.draw_line([WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH, paddle2_pos + HALF_PAD_HEIGHT], PAD_WIDTH + 2, "White")
    
    # draw scores
    c.draw_text(str(left_score), [WIDTH/2 - WIDTH*1 / 6, HEIGHT / 4], 40, "White")
    c.draw_text(str(right_score), [WIDTH/2 + WIDTH*1 / 6, HEIGHT / 4], 40, "White")
    
def keydown(key):
    c = 3
    global paddle1_vel, paddle2_vel
    if(key == simplegui.KEY_MAP["w"]):
        paddle1_vel += c
    if(key == simplegui.KEY_MAP["s"]):
        paddle1_vel -= c
    if(key == simplegui.KEY_MAP["up"]):
        paddle2_vel += c
    if(key == simplegui.KEY_MAP["down"]):
        paddle2_vel -= c
    
def keyup(key):
    c = 3
    global paddle1_vel, paddle2_vel
    if(key == simplegui.KEY_MAP["w"]):
        paddle1_vel -= c
    if(key == simplegui.KEY_MAP["s"]):
        paddle1_vel += c
    if(key == simplegui.KEY_MAP["up"]):
        paddle2_vel -= c
    if(key == simplegui.KEY_MAP["down"]):
        paddle2_vel += c
    
def restart():
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart, 100)

# start frame
new_game()
frame.start()
