import pygame
import pygame_menu
from pygame.locals import *
import socket
import threading
import os

pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = '200,200'

def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

HOST = '127.0.0.1'
PORT = 4710
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print("waiting for connection...")
conn, addr = server.accept()
print('Client connected by ', str(addr))

#------------------------- Recieve data from client --------------------------------

def recieve_data():
    global player_x2
    global player_y2                                 # Global player_x2, player_y2 to change position of player 2
    while True:
        data = conn.recv(1024).decode()
        data = data.split('-')
        player_x2, player_y2 = float(data[0]), float(data[1])  # Change value of position player 2

#------------------------ Another thread doing about server ------------------------------

create_thread(recieve_data)

#------------------------- Create a display of game ---------------------------------

size_game = (g_width,g_height) = (800,600)
surface = pygame.display.set_mode(size_game)
pygame.display.set_caption("Po Soccer") 
clock = pygame.time.Clock()

walkRight = [pygame.image.load('image2/R2P.png'), pygame.image.load('image2/R3P.png'), pygame.image.load('image2/R5P.png'),pygame.image.load('image2/R2P.png'), pygame.image.load('image2/R3P.png'), pygame.image.load('image2/R5P.png'),pygame.image.load('image2/R2P.png'), pygame.image.load('image2/R3P.png'), pygame.image.load('image2/R5P.png')]
walkLeft = [pygame.image.load('image2/L1P.png'), pygame.image.load('image2/L2P.png'), pygame.image.load('image2/L3P.png'), pygame.image.load('image2/L5P.png'), pygame.image.load('image2/L1P.png'), pygame.image.load('image2/L2P.png'), pygame.image.load('image2/L3P.png'), pygame.image.load('image2/L3P.png'), pygame.image.load('image2/L5P.png')]
stand1 = [pygame.image.load('image2/R2P.png'), pygame.image.load('image2/R3P.png'), pygame.image.load('image2/R5P.png'),pygame.image.load('image2/R2P.png'), pygame.image.load('image2/R3P.png'), pygame.image.load('image2/R5P.png'),pygame.image.load('image2/R2P.png'), pygame.image.load('image2/R3P.png'), pygame.image.load('image2/R5P.png')]
stand2 = [pygame.image.load('image2/L1P.png'), pygame.image.load('image2/L2P.png'), pygame.image.load('image2/L3P.png'), pygame.image.load('image2/L5P.png'), pygame.image.load('image2/L1P.png'), pygame.image.load('image2/L2P.png'), pygame.image.load('image2/L3P.png'), pygame.image.load('image2/L3P.png'), pygame.image.load('image2/L5P.png')]

left = False
right = False
walkCount = 0
stand = 0

#------------------------ Declare values before recieve from client ----------------
global player_x1, player_y1
player_x2, player_y2 = 675, 490           # Declare position of player 2 before recieve position from client


#----------------------------------- Main -------------------------------------------
def redrawGameWindow():
    global walkCount
    global stand

    if walkCount + 1 >= 27:
        walkCount = 0
    elif left:
        surface.blit(walkRight[walkCount//3], (player_x1,player_y1))
        surface.blit(walkLeft[walkCount//3], (player_x2,player_y2))
        walkCount += 1
    elif right:
        surface.blit(walkRight[walkCount//3], (player_x1,player_y1))
        surface.blit(walkLeft[walkCount//3], (player_x2,player_y2))
        walkCount +=1
    else:
        if stand +1 >= 27:
            stand = 0
        surface.blit(stand1[stand//3], (player_x1,player_y1))
        surface.blit(stand2[stand//3], (player_x2,player_y2))
        stand += 1
    pygame.display.update()
    

def start_the_game():
    global stand
    global left
    global right
    global walkCount
    left = False
    right = False
    running = True
    global player_x1
    global player_y1
    player_x1, player_y1 = 50, 490  # Initial position of player 1

    # Detail of player 
    move = 25               # Speed of player 
    jump = False            # To check player jumping?
    jump_count = 10         # State of jumping
    grav = 0.5              # Gravity

    # Import background in to game
    surface = pygame.display.set_mode(size_game)
    bg = pygame.image.load(os.path.join('image2','bg_panda2.jpg'))
    
    ball=pygame.image.load('image2/ball.png')
    ballrect=ball.get_rect()
    ballrect=ballrect.move(g_width/2,g_height/2)

    # Detail of ball
    ballSize = 60         
    x = 5                   # Initial speed of ball in x, x > 0 go right,x < 0 go left
    y = 0                   # Initial speed of ball in y, y > 0 go down, y < 0 go up
    reaction_x = 1          # Reaction when ball bouncing
    friction_x = 0.1
    gravball = 0.5
    pos_x,pos_y  = (g_width/2,g_height/2)  # Initial position of ball
    
    score_player1 = 0       # Initial score of player 1
    score_player2 = 0       # Initial score of player 2


    #------------------- Game when create server and client connected --------------
    while running:
        # -------------- Condtion before get into the game ------------
        keyspressed = pygame.key.get_pressed()
        for event in pygame.event.get():            # User did something 
            if event.type == pygame.QUIT:           # If user clicked exit
                running = False                     # End the loop


        # ------------------ Make a shape of player --------
        player1 = Rect(player_x1, player_y1, 67, 74)
        player2 = Rect(player_x2, player_y2, 67, 74)


        # ---------------------- Display background ----------
        surface.blit(bg, (0, 0))


        # -------------- Pressing the ESC Key to quit the game --------
        if keyspressed[ord("\x1b")]:
                running = False             

        if keyspressed[ord("a")]:                   # Pressing A to move left
            player_x1 -= move
            left = True
            right = False 
            player1=player1.move(-move,0)
            if (player1.left<0):
                player1.left=0
        elif keyspressed[ord("d")]:                   # Pressing D to move right
            player_x1 += move
            right = True
            left = False
            player1=player1.move(move,0)
            if(player1.right>g_width):
                player1.right=g_width
        else :
            right = False
            left = False
            
        if not(jump):                               # Pressing W or Spacebar to jump
            if keyspressed[ord("w")] \
            or keyspressed[ord(" ")]:
                jump = True                         # If jump = True we will calculate Gravity
        else:
            if jump_count >= -10:                   # Calculate projectile
                neg = 1
                if jump_count < 0:
                    neg = -1
                player_y1 = player_y1 - (jump_count**2)* grav * neg
                player1[1]= player_y1
                jump_count -= 1
            else:
                jump = False
                jump_count = 10


        #---------------- Detect player won't out of bound --------------
        if player_y1 < 0:                                  # If player1 go to highest 
            player_y1 = 0
        if player_y1 >= surface.get_height()-110:          # If player1 going to lowest 
            player_y1 = surface.get_height()-110
        if player_x1 < 0:                                  # If player1 going to leftest
            player_x1 = 0
        if player_x1 >= surface.get_width()-67:           # If player1 going to rightest
            player_x1 = surface.get_width()-67  
             
             
        
        if player1.colliderect(player2):
            if player1.bottom>=player2.top and \
            player1.bottom<=player2.bottom and \
            player1.right>=player2.left and \
            player1.left<=player2.right :
                offsetplayer = player1.center[0] - player2.center[0]
                print(offsetplayer)
                if offsetplayer>0:
                    player_x1 = player_x2+67
                else:
                    player_x1=player_x2-67




        # --------------------- Making a ball -----------------------------
        if score_player1 != "Win!" and score_player1 != "Lose!":
            ballrect=ballrect.move(x,y)
            
            pos_x += x                              # Make the ball moving in x
            pos_y += y                              # Make the ball moving in y

            if pos_y < 0:                                   # If the ball hit the top frame
                y = -y
                
            if pos_x + ballSize > g_width or \
            pos_x < 0:                                   # If the ball hit the left or right wall
                x = -(x*reaction_x)

            if pos_y + ballSize > 560 and y > 0:                                   
                y  = -y
            if pos_y + ballSize > 560 and pos_y + ballSize < 562 and x > 0:
                x -=friction_x
                pos_y = 560 - ballSize
                y += gravball
            if pos_y + ballSize > 560 and pos_y + ballSize < 562 and x < 0 :
                x +=friction_x
                pos_y = 560 - ballSize
                y += gravball
            if pos_y + ballSize > 560 and pos_y + ballSize < 562 and  x == 0 :
                pos_y = 560 - ballSize
                y += gravball
            if pos_y + ballSize != 560 :
                y += gravball
            if pos_y + ballSize == 560: 
                if x < -1:
                    x += friction_x
                if x > 1:
                    x -= friction_x
                if -1 <= x <= 1 :
                    x = 0 

        # --------------------- Ball hit the player floor ------------------------
        # when the player 2 win, the ball will release in player 2 side
        if 300 <= pos_y <= 560-ballSize and \
           pos_x < 0:     
            
            # Reset detail of the ball and release  the ball in player 2 side
            x, y = -5, 0                
            reaction_x = 1              
            pos_x, pos_y = (g_width/2,g_height/2)
            ballrect=ball.get_rect()
            ballrect=ballrect.move(g_width/2,g_height/2) 
            
            # Plus score to player 2 
            score_player2 += 1

            # If score player 2 = 10 ; stop ball 
            if score_player2 == 5:
                x, y = 0, 0
                gravball = 0
                score_player2 = "Win!"
                score_player1 = "Lose!"
            print("Player1 lose")
        
        # when the player 1 win, the ball will release in player 1 side
        if 300 <= pos_y <= 560-ballSize and \
           pos_x + ballSize >= g_width :     

            # Reset detail of the ball and release the ball in player 1 side
            x, y = 5, 0
            reaction_x = 1
            pos_x, pos_y = (g_width/2,g_height/2)
            ballrect=ball.get_rect()
            ballrect=ballrect.move(g_width/2,g_height/2)

            # Plus score to player 1
            score_player1 += 1
            if score_player1 == 5:
                x, y = 0, 0
                gravball = 0
                score_player1 = "Win!"
                score_player2 = "Lose!"
            print("Player2 lose")
        

        # ---------------- Ball hit player ------------------
        
        if ballrect.bottom>=player1.top and \
            ballrect.bottom<=player1.bottom and \
            ballrect.right>=player1.left and \
            ballrect.left<=player1.right :
            if y > 0:
                y = -y-grav
            offset= ballrect.center[0] - player1.center[0]
            if offset>0:
                if offset>30:
                    x=20
                elif offset>23:
                    x=15
                elif offset>17:
                    x=10
            else:
                if offset<-30:
                    x=-20
                elif offset<-23:
                    x=-15
                elif offset<-17:
                    x=-10
        if ballrect.bottom>=player2.top and \
            ballrect.bottom<=player2.bottom and \
            ballrect.right>=player2.left and \
            ballrect.left<=player2.right :
            if y > 0:
                y = -y-grav
            offset= ballrect.center[0] - player2.center[0]
            if offset>0:
                if offset>30:
                    x=15
                elif offset>23:
                    x=10
                elif offset>17:
                    x=5
            else:
                if offset<-30:
                    x=-15
                elif offset<-23:
                    x=-10
                elif offset<-17:
                    x=-5

        # ------------------------ Display Objective --------------------------
        surface.blit(ball, ballrect)
        
        y += grav                                 # When display the ball at first frame
                                                  # then increase speed by gravity


        # ------------------------ Display score ------------------------------
        font = pygame.font.Font(os.path.join('image2', 'GenericMobileSystem.ttf'), 50)
        text_score_player1 = font.render(str(score_player1), False, (255, 0, 0))
        text_score_player2 = font.render(str(score_player2), False, (255, 0, 0))      
        surface.blit(text_score_player1, (180,60))
        surface.blit(text_score_player2, (620,60))
        


        # ------------------------ Send data to client ------------------------

        send_data = '{}-{}-{}-{}-{}-{}'.format(player_x1, player_y1, pos_x, pos_y, score_player1, score_player2).encode()       # Use format string to enable encode function
        conn.send(send_data)

        redrawGameWindow()
        clock.tick(30)                             # Run the game at 30 frames per second  
        

#------------------------ Menu before enter to the game --------------------------
menu_widgth, menu_height = 400, 250
mytheme = pygame_menu.themes.THEME_SOLARIZED.copy()
mytheme.title_background_color=(230, 242, 255)
menu = pygame_menu.Menu('Po Soccer',menu_widgth,menu_height ,theme = mytheme)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(surface)