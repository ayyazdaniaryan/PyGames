
"""
    Implementation of classic arcade game Pong    
    simplegui and other dependencies are contained within
    CodeSkulptor online service (www.codeskulptor.org)

    This code can be accessed and run online via
    http://www.codeskulptor.org/#user13_ufoNmILOWsropyv_0.py
"""

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
top1 = 160
top2 = 160
ball_pos = [WIDTH/2,HEIGHT/2]
paddle1_vel = 0
paddle2_vel = 0 
PAD_VEL = 6
ball_vel = 0
paddle1_pos = [(0,top2),(PAD_WIDTH,top1),(PAD_WIDTH,top1+PAD_HEIGHT),(0,top1+PAD_HEIGHT)]
paddle2_pos = [(WIDTH-PAD_WIDTH,top2),(WIDTH,top2),(WIDTH,top2+PAD_HEIGHT),(WIDTH-PAD_WIDTH,top2+PAD_HEIGHT)]
score_left = 0
score_right = 0

# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel, paddle1_pos, paddle2_pos
    ball_pos = [WIDTH/2,HEIGHT/2]
    paddle1_pos = [(0,top2),(PAD_WIDTH,top1),
                   (PAD_WIDTH,top1+PAD_HEIGHT),
                   (0,top1+PAD_HEIGHT)]
    paddle2_pos = [(WIDTH-PAD_WIDTH,top2),(WIDTH,top2),
                   (WIDTH,top2+PAD_HEIGHT),
                   (WIDTH-PAD_WIDTH,top2+PAD_HEIGHT)]
    dx = random.randrange(120, 240)
    dy = random.randrange(60, 180)
    if right:
        ball_vel = [dx, -dy]
    else:
        ball_vel = [-dx, -dy]
        
def rand_right():
    x = random.randint(0,1)
    if x == 0:
        return False
    else: 
        return True
# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score_left, score_right  # these are ints
    score_left = 0
    score_right = 0
    ball_init(rand_right())

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global ball_pos, ball_vel, top1, top2
    
    ##control how far up/down the paddles can go
    if top1 <= 0:
        top1 =0
    if top1 >= (HEIGHT-PAD_HEIGHT-1):
        top1 = HEIGHT-PAD_HEIGHT-1
    if top2 <= 0: 
        top2 = 0
    if top2 >= (HEIGHT-PAD_HEIGHT-1):
        top2 = HEIGHT-PAD_HEIGHT-1

# update paddle's vertical position, keep paddle on the screen
    top1 += paddle1_vel
    top2 += paddle2_vel
        
    ## update the paddle position vectors
    paddle1_pos = [(0,top1),(PAD_WIDTH,top1),
                   (PAD_WIDTH,top1+PAD_HEIGHT),
                   (0,top1+PAD_HEIGHT)]
    paddle2_pos = [(WIDTH-PAD_WIDTH,top2),(WIDTH,top2),
                   (WIDTH,top2+PAD_HEIGHT),
                   (WIDTH-PAD_WIDTH,top2+PAD_HEIGHT)]
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    c.draw_polygon(paddle1_pos, 1, "White", "White") 
    c.draw_polygon(paddle2_pos, 1, "White", "White")
    
    # update ball
    ball_pos[0] += ball_vel[0]/60
    ball_pos[1] += ball_vel[1]/60
    
    # check collision and scoring
    check_update_coll()
            
    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    c.draw_text("Player 1 uses w/s, Player 2 uses up/down, Esc to reset", 
                (WIDTH/2 + 20,HEIGHT-3), 12, "White")
    c.draw_text(str(score_left), 
                (WIDTH/2 - 30,20), 24, "White")
    c.draw_text(str(score_right), 
                (WIDTH/2 + 20,20), 24, "White")
        
def check_update_coll():
    global ball_pos, ball_vel

    #check left wall
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        #Check if in paddlerange
        if ball_pos[1] >= top1 and ball_pos[1] <= top1+PAD_HEIGHT:
            ball_vel[0] = - 1.1 * ball_vel[0]
        else:
            update_score(1)
            ball_init(True)
    
    #check right wall
    if ball_pos[0] >= (WIDTH -1) - BALL_RADIUS - PAD_WIDTH:
        
        #Check if in paddlerange
        if ball_pos[1] >= top2 and ball_pos[1] <= top2+PAD_HEIGHT:
            ball_vel[0] = - 1.1 * ball_vel[0]
        else:
            update_score(0)
            ball_init(False)
    
    #check top wall
    if ball_pos[1] <= BALL_RADIUS + PAD_WIDTH:
        ball_vel[1] = - ball_vel[1]
    
    #check bottom wall
    if ball_pos[1] >= (HEIGHT-1) - BALL_RADIUS - PAD_WIDTH:
        ball_vel[1] = - ball_vel[1]
        
def update_score(winner):
    global score_left, score_right
    if winner == 0:
        score_left += 1
    elif winner == 1:
        score_right += 1

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= PAD_VEL
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += PAD_VEL
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= PAD_VEL
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += PAD_VEL

    
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel += PAD_VEL
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel -= PAD_VEL
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel += PAD_VEL
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel -= PAD_VEL
    elif key == 27: ##escape
        new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
frame.start()
new_game()
