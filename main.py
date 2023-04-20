import random  # for generating random numbers
import sys  # sys.exit to exit the programs
import pygame
import login
from pygame.locals import *  # basic pygame imports



"""
This is the Main file of Flappy bird application created by 
Rajwant Kaur- C0866224
"""

# Global variables declared for games
FPS = 32  # FPS is frames per second
SCREEN_WIDTH = 288  # Screenwidth in pixels
SCREEN_HEIGHT = 512 #screen height in pixels


GROUND_Y = SCREEN_HEIGHT*0.8  #  Constant to set ground of game
GAME_SPRITES = {}  # Global dictionary to store images used in game.
GAME_SOUNDS = {}  # Global dictionary to store sounds effects used in game.
PLAYER = 'FlappyBirdGame/res/images/flappy-player.png'   # Path for the Image of bird player
BACKGROUND = 'FlappyBirdGame/res/images/background.png' # Path for the Image of game background
PIPE = 'FlappyBirdGame/res/images/pipe.png'   # Pips images  are used as obstacles in game

#Main Function of game.
def mainGame():
    score = 0   #Initial score of player is zero.
   
    playerx = int(SCREEN_WIDTH/5)  
    playery = int(SCREEN_WIDTH/2)
    basex = 0

    # create 2 pipes for  blitting on screen
    newpipe1 = getRandomPipe()
    newpipe2 = getRandomPipe()   

    # Upper pipes list
    upperPipes = [
        {
            'x': SCREEN_WIDTH+200, 'y': newpipe1[0]['y']
        },
        {
            'x': SCREEN_WIDTH+200+(SCREEN_WIDTH/2), 'y': newpipe2[0]['y']
        }
    ]
    # Lower pipes list
    lowerPipes = [
        {
            'x': SCREEN_WIDTH+200, 'y': newpipe1[1]['y']
        },
        {
            'x': SCREEN_WIDTH+200+(SCREEN_WIDTH/2), 'y': newpipe2[1]['y']
        }
    ]
    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccV = -8  # velocity while flapping
    playerFlapped = False  # it will be  true when bird is flapping

    while True:
        for event in pygame.event.get():
            #Quit game if these actions are used.
            if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # if user presses up key or space bar,  start the game for them.
            elif event.type == KEYDOWN or (event.type == K_SPACE and event.type == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccV
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()   #play sound as bird is flying.

        # This function will return true if player is crashed.
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)

        # Return player crashed and player score on collision.    
        if crashTest:
            return crashTest,score

        # Check for scores
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2

        # Increase player score if pipe crossed.
        for pipe in upperPipes:
            pipeMidPos = pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos+4:
                score += 1
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery+min(playerVelY, GROUND_Y-playery-playerHeight)

        # Move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when first pipe about to leave
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

       # if pipe is out of screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

      # Screen blits
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))   #Blit background
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],                           #Blit pipes
                        (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],
                        (lowerPipe['x'], lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUND_Y))   #blit base
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))  #blit player

        #Blit  score 
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
            Xoffset = (SCREEN_WIDTH-width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],
                        (Xoffset, SCREEN_HEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)



#check Bird collision
def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUND_Y - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()    #Play Hit sound, if collided
        return True
    for pipe in upperPipes:   #check collision for upper pipes
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight+pipe['y'] and abs(playerx-pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
          GAME_SOUNDS['hit'].play()
          return True
        
    for pipe in lowerPipes:    #check collision for lower pipes
       
        if ((playery +GAME_SPRITES['player'].get_height()>pipe['y']) and abs(playerx-pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
          GAME_SOUNDS['hit'].play()
          return True
        

    # Get random pipes as obstacles   
def getRandomPipe():
    # Generate positions of two pipes
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREEN_HEIGHT/3

    y2 = offset+random.randrange(0, int(300-1.2*offset))
    pipex = SCREEN_WIDTH+20
    y1 = pipeHeight-y2+offset
    pipe = [{'x': pipex, 'y': -y1},  # Upper pipe
            {'x': pipex, 'y': y2}]  # lower pipe
    return pipe



# User will  get this screen after login
def welcomeScreen():
    # Show welcome images
    playerx = int(SCREEN_WIDTH/5)
    playery = int((SCREEN_HEIGHT-GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREEN_WIDTH-GAME_SPRITES['player'].get_width())/2)
    messagey = int(SCREEN_HEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # if user presses up key or space bar,  start the game for them.
            elif event.type == KEYDOWN or (event.type == K_SPACE and event.type == K_UP):
                return
            else:
                #Show welcome image until user press any key.
                SCREEN.blit(GAME_SPRITES['message'], (0, 0))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


# Main function or entry point for game
if __name__ == "__main__":

#This will open login window, and will proceed only if login is success.
 if(login.login_Window()):
   
   while True: 
    pygame.init()  # initialize all pygame's modules
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    FPSCLOCK = pygame.time.Clock()
    print('Flappy Bird By Rajwant Kaur...')
    pygame.display.set_caption('Flappy Bird By Rajwant Kaur')

    #Initalise images
    GAME_SPRITES['numbers'] = (
        pygame.image.load(
            'FlappyBirdGame/res/images/0.png').convert_alpha(),
        pygame.image.load(
            'FlappyBirdGame/res/images/1.png').convert_alpha(),
        pygame.image.load(
            'FlappyBirdGame/res/images/2.png').convert_alpha(),
        pygame.image.load(
            'FlappyBirdGame/res/images/3.png').convert_alpha(),
        pygame.image.load(
            'FlappyBirdGame/res/images/4.png').convert_alpha(),
        pygame.image.load(
            'FlappyBirdGame/res/images/5.png').convert_alpha(),
        pygame.image.load(
            'FlappyBirdGame/res/images/6.png').convert_alpha(),
        pygame.image.load(
            'FlappyBirdGame/res/images/7.png').convert_alpha(),
        pygame.image.load(
            'FlappyBirdGame/res/images/8.png').convert_alpha(),
        pygame.image.load(
            'FlappyBirdGame/res/images/9.png').convert_alpha(),
    )
    GAME_SPRITES['message'] = pygame.image.load(
        'FlappyBirdGame/res/images/Flappy-Bird-welcome.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load(
        'FlappyBirdGame/res/images/base.png').convert_alpha()
    GAME_SPRITES['game-over'] = pygame.image.load(
        'FlappyBirdGame/res/images/game-over.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
                            pygame.image.load(PIPE).convert_alpha()
                            )

    # Game Sounds
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('FlappyBirdGame/res/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('FlappyBirdGame/res/audio/point.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('FlappyBirdGame/res/audio/wing.wav')
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()



    welcomeScreen()  # show welcome screen to user until he press a button
    crashed,score= mainGame()  # main game function
    # Show game over screen if player is collided
    if crashed:
     while True:
        SCREEN.blit(GAME_SPRITES['game-over'], (0, 0))

        font = pygame.font.Font(None, 50)  # Font for game score
        score_text = font.render(f"Score: {score}", True, (50, 168, 82)) #show final score on collision
        #Blit score on game over screen.
        SCREEN.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2,30))
        
        # Call main function after any key press on game over screen.
        for event in pygame.event.get():
          crashed,score=   mainGame()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
 else:
    print("Login is not success or window quit.")