###########################################################################
# Settings
###########################################################################

#import necessary modules
import pygame
import random
from pygame import mixer

#finds local font that matches 'avant garde'
font_name = pygame.font.match_font('avant garde')

#adds images for player and cats
alienImg = pygame.image.load('hank.png')
background = pygame.image.load('sky.jpg')
cat1 = pygame.image.load('cat.png')

#sets the height and width of the screen
screen_width =  800 
screen_height = 600 

#sets screen variable for quicker reference
screen = pygame.display.set_mode([screen_width, screen_height])

#list of sprites - only the cats and not the player
block_list = pygame.sprite.Group()

#list of every sprite - all cats and the player
all_sprites_list = pygame.sprite.Group()

#to manage how fast the screen updates
clock = pygame.time.Clock()

###########################################################################
# Hank & Cats
###########################################################################

#defines the cats[and player - see class player comments] - uses sprite class in pygame to create
class Block(pygame.sprite.Sprite):
    #define attributes needed for cats
    def __init__(self, image, width, height):
        #calls the parent class (Sprite) constructor
        super().__init__()

        #set image for cats
        self.image = cat1

        #create rectangle for cats and updates their positions by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
    
    #resets cats position to top of screen at a random location - either the cats have gone out of range or there has been a collision
    def reset_pos(self):

        #sets range for rec.x and rect.y
        self.rect.y = random.randrange(-200, -30)
        self.rect.x = random.randrange(0, screen_width)

    #updates screen display with each frame
    def update(self):

        #move cats down 2 pixels
        self.rect.y += 2

        #if cats are too far down, reset to top of screen
        if self.rect.y > 610:
            self.reset_pos()

#defines the player - uses block class as a foundation to work from but overrides the 'update' function with a movement function to follow mouse
class Player(Block):
    #sets how player updates itself
    def update(self):

        #gets the current mouse position and returns it as a list of 2 numbers (x,y)
        pos = pygame.mouse.get_pos()

        #uses(x,y) from above and sets the player to the mouse location
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        #set image for player
        self.image = alienImg

###########################################################################
# Game Set Up
###########################################################################

#initialize pygame
pygame.init()

#sets name of game in pygame window
pygame.display.set_caption('Hank the Hero')

#sets attributes of player i,e self, width, height
player = Player(alienImg, 20, 15)

#adds the player to the all_sprites_list only
all_sprites_list.add(player)

#sets number of cats on the screen
for i in range(20):
    #sets attributes of cats i.e self, width, height
    block = Block(cat1, 20, 15)

    #sets a random location for the cats
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)

    #adds the cats to both lists
    block_list.add(block)
    all_sprites_list.add(block)

#push screen to display
screen.blit(background, (0,0))

###########################################################################
# Music
###########################################################################

#adds background music
mixer.music.load('Blazer_Rail.mp3')
#loops music
mixer.music.play(-1)

###########################################################################
# Score Counter
###########################################################################

#defines how to draw text to use for score counter
def draw_text(surf, text, size, x, y):
    #sets font type and size
    font = pygame.font.Font(font_name, size)
    #sets text, anti-aliased and colour
    text_surface = font.render(text, True, (0, 0, 0))
    #creates text box
    text_rect = text_surface.get_rect()
    #sets position of text box
    text_rect.midtop = (x , y)
    #push to screen display
    surf.blit(text_surface, text_rect)

###########################################################################
# Game Intro Page
###########################################################################

#sets game intro
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
    #if player presses the x in the top right of the pygame window or quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit
            if event.type == pygame.KEYDOWN:
                #if player presses C stop intro and run game loop
                if event.key == pygame.K_c:
                    intro = False
                #if player presses Q quit pygame window
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit
        #sets background
        screen.blit(background, (0,0))
        #sets text
        draw_text(screen, "Hank the Hero needs you!", 50, 400, 100)
        draw_text(screen, "Control the spaceship with your mouse to save as many kittens as possible!", 25, 400, 200)
        draw_text(screen, "Press C to start or Q to quit", 25, 400, 300)
        #updates screen display
        pygame.display.update()

###########################################################################
# Game Mechanics
###########################################################################

def game_loop():
    #starts score at 0
    score = 0

    #main game loop
    running = True
    while running:
        #for each pygame event
        for event in pygame.event.get():
            #if player presses the x in the top right of the pygame window, quit the game and print final score to terminal
            if event.type == pygame.QUIT:
                print("Final Score: " + str(score))
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print("Final Score: " + str(score))
                    running = False
                if event.key == pygame.K_ESCAPE:
                    print("Final Score: " + str(score))
                    running = False
        #clear the screen
        screen.blit(background, (0,0))

        #calls update() method on every sprite in the list
        all_sprites_list.update()

        #see if the player has collided with anything (collected any cats) and create list of collisions
        blocks_hit_list = pygame.sprite.spritecollide(player, block_list, False)

        #check the list of collisions
        for block in blocks_hit_list:
            #check the list of collisions and update the score
            score += 1
            #print(score)

            #reset cats to the top of the screen to fall again
            block.reset_pos()

        #draw all the sprites (cats and player)
        all_sprites_list.draw(screen)

        #show score counter in pygame window
        draw_text(screen, "Kittens Saved", 25, 70, 480)
        draw_text(screen, str(score), 40, 65, 525)

        #limit to 80 frames per second
        clock.tick(60)

        #update screen display
        pygame.display.flip()

    #close pygame
    pygame.quit()

game_intro()
game_loop()