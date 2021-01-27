import pygame

# Defining colours
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PINK = (255,20,147)
PURPLE = (138,43,226)

pygame.init()

# Set the screen size
size = (1980,1000)
screen = pygame.display.set_mode(size) 

# Title of new window/screen
pygame.display.set_caption("Donkey Kong")

done = False

# CREATE GROUPS for each sprite here

# Create a group of all sprites together
all_sprites_group = pygame.sprite.Group()

# Manages how fast screen refreshes 
clock = pygame.time.Clock()






# MAIN PROGRAM LOOP
# Loop until the user clicks the close button.
while not done:
    # Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    # Game logic should go here
    all_sprites_group.update()
    
    # Screen-clearing code goes here
    
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # Making the screen background black
    screen.fill(BLACK)
    # Draws the background image
    screen.blit(BACKGROUND_IMAGE, [0,0])
    # Draws all the sprites
    all_sprites_group.draw(screen)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    
    # Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()