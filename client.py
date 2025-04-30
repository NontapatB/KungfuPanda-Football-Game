import pygame
import pygame_menu
from pygame.locals import *

pygame.init()

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '1000,200'

import threading

# ----------------------- Function to create thread -----------------

def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

#------------------------ Connect to server  ------------------------------

import socket
HOST = '127.0.0.1'
PORT = 4710
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
server.connect((HOST,PORT))


#------------------------- Recieve data from server --------------------------------

def recieve_data():
    global player_x1,player_y1,ball_x,ball_y,score_player1,score_player2
    while True:
        data = server.recv(1024).decode()
        data = data.split('-')
        player_x1, player_y1 = float(data[0]), float(data[1])
        if data[2] != '':                                   # To fix bug 
            ball_x, ball_y = float(data[2]), float(data[3])
            score_player1,score_player2 = data[4], data[5]

#------------------------ Another thread doing about server ------------------------------

create_thread(recieve_data)

#------------------------- Create a display of game ---------------------------------

gameSize = (g_width,g_height) = (800,600)
surface = pygame.display.set_mode(gameSize)
pygame.display.set_caption("Po Soccer")

clock = pygame.time.Clock() 

#------------------------ Declare values before recieve from client ----------------

player_x1, player_y1 = 50, 490                        # Declare position of player 1 before recieve position from server
ball_x, ball_y = g_width/2,g_height/2     # Declare position of ball before recieve position from server
ballSize = 60         
score_player1,score_player2 = '0','0'   # Declare score before recieve position from server

#-------------------------------------Animation-------------------------------------
walkRight = [pygame.image.load('image2/R2P.png'), pygame.image.load('image2/R3P.png'), pygame.image.load('image2/R5P.png'),pygame.image.load('image2/R2P.png'), pygame.image.load('image2/R3P.png'), pygame.image.load('image2/R5P.png'),pygame.image.load('image2/R2P.png'), pygame.image.load('image2/R3P.png'), pygame.image.load('image2/R5P.png')]
stand1 = [pygame.image.load('image2/R2P.png'), pygame.image.load('image2/R3P.png'), pygame.image.load('image2/R5P.png'),pygame.image.load('image2/R2P.png'), pygame.image.load('image2/R3P.png'), pygame.image.load('image2/R5P.png'),pygame.image.load('image2/R2P.png'), pygame.image.load('image2/R3P.png'), pygame.image.load('image2/R5P.png')]
walkLeft = [pygame.image.load('image2/L1P.png'), pygame.image.load('image2/L2P.png'), pygame.image.load('image2/L3P.png'), pygame.image.load('image2/L5P.png'), pygame.image.load('image2/L1P.png'), pygame.image.load('image2/L2P.png'), pygame.image.load('image2/L3P.png'), pygame.image.load('image2/L3P.png'), pygame.image.load('image2/L5P.png')]
stand2 = [pygame.image.load('image2/L1P.png'), pygame.image.load('image2/L2P.png'), pygame.image.load('image2/L3P.png'), pygame.image.load('image2/L5P.png'), pygame.image.load('image2/L1P.png'), pygame.image.load('image2/L2P.png'), pygame.image.load('image2/L3P.png'), pygame.image.load('image2/L3P.png'), pygame.image.load('image2/L5P.png')]

left = False
right = False
walkCount = 0
stand = 0

def redrawGameWindow():
    global walkCount
    global stand

    if walkCount + 1 >= 27:
        walkCount = 0
    elif left:
        surface.blit(walkLeft[walkCount//3], (player_x2,player_y2))
        surface.blit(walkRight[walkCount//3], (player_x1,player_y1))
        walkCount += 1
    elif right:
        surface.blit(walkLeft[walkCount//3], (player_x2,player_y2))
        surface.blit(walkRight[walkCount//3], (player_x1,player_y1))
        walkCount +=1
    else:
        if stand +1 >= 27:
            stand = 0
        surface.blit(stand1[stand//3], (player_x1,player_y1))
        surface.blit(stand2[stand//3], (player_x2,player_y2))
        stand += 1
    pygame.display.update()

#----------------------------------- Main -------------------------------------------
def start_the_game():
    running = True
    global stand
    global left
    global right
    global walkCount
    left = False
    right = False
    global player_x2
    global player_y2
    player_x2, player_y2 = 675, 490   # Initial position of player 2

    # Detail of player 
    move = 20               # Speed of player 
    jump = False            # To check player jumping?
    jump_count = 10         # State of jumping
    grav = 0.5              # Gravity

    # Import background in to game
    surface = pygame.display.set_mode(gameSize)
    bg = pygame.image.load(os.path.join('image2','bg_panda2.jpg'))

    # Import image of player, ball
    img_ball = pygame.image.load('image2/ball.png')

    #------------------- Game when create server and client connected --------------
    while running:
        
        # -------------- Condtion before get into the game ------------
        keyspressed = pygame.key.get_pressed()
        for event in pygame.event.get():            # User did something 
            if event.type == pygame.QUIT:           # If user clicked exit
                running = False                     # End the loop


        # ------------------ Make a shape of player --------S

        # --------------------- Making a ball -----------------------------
        ball = Rect(ball_x,ball_y,ballSize,ballSize)

        # ---------------------- Input background ----------
        surface.blit(bg, (0, 0))


        # -------------- Pressing the ESC Key to quit the game --------
        if keyspressed[ord("\x1b")]:
                running = False        


        # ------- Moving player ----------
        if keyspressed[ord("a")]:                   # Pressing A to move left
            player_x2 -= move
            left = True
            right = False
        if keyspressed[ord("d")]:
            right = True
            left = False                   # Pressing D to move right
            if player_x2 >= player_x1-67 and player_y1 == player_y2 and player_x2 <= player_x1-67:
                player_x2 = player_x1 - 67
            else:
                player_x2 += move
        else:
            right = False
            left = False

        if not(jump):                               # Pressing W or Spacebar to jump
            if keyspressed[ord("w")] \
            or keyspressed[ord(" ")]:
                jump = True                         # If jump = True we will calculate Gravity
        else:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                player_y2 = player_y2 - (jump_count**2)* grav * neg
                jump_count -= 1
            else:
                jump = False
                jump_count = 10
    
        if player_x2 >= player_x1-67 and player_y1 == player_y2 and player_x2 <= player_x1-67:
            print(player_x1)
            print(player_x2)
            player_x2=player_x1-67
        if player_x2 < player_x1+67 and player_y1 == player_y2 and player_x2 > player_x1:
            player_x2 = player_x1+67
        if player_x2 >= player_x1-67 and player_y2 > player_y1 and player_x2 <= player_x1-67:
            player_x2 =player_x1-67
        

        #---------------- Detect player won't out of bound --------------
        if player_y2 < 0: 
            player_y2 = 0
        if player_y2 >= surface.get_height()-110: 
            player_y2 = surface.get_height()-110
        if player_x2 < 0: 
            player_x2 = 0
        if player_x2 >= surface.get_width()-67: 
            player_x2 = surface.get_width()-67
        
    


        # ------------------------ Display Objective --------------------------
        surface.blit(img_ball,ball.topleft)       # Display ball as Pokeball 
        

        # ------------------------ Display score ------------------------------
        font = pygame.font.Font(os.path.join('image2', 'GenericMobileSystem.ttf'), 50)
        text_score_player1 = font.render(score_player1, False, (255, 0, 0))
        text_score_player2 = font.render(score_player2, False, (255, 0, 0))      
        surface.blit(text_score_player1, (180,60))
        surface.blit(text_score_player2, (620,60))


        # ------------------------ Send data to server ------------------------
        send_data = '{}-{}'.format(player_x2, player_y2).encode()       # Use format string to enable encode function
        server.send(send_data)

        redrawGameWindow()
        clock.tick(30)                                  # Run the game at 30 frames per second  
        
#------------------------ Menu before enter to the game --------------------------
menu_widgth, menu_height = 400, 250
mytheme = pygame_menu.themes.THEME_SOLARIZED.copy()
mytheme.title_background_color=(230, 242, 255)
menu = pygame_menu.Menu('Po Soccer',menu_widgth,menu_height ,theme = mytheme)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(surface)