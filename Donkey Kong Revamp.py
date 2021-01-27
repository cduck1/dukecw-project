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
size = (1920,1000)
screen = pygame.display.set_mode(size) 

# Title of new window/screen
pygame.display.set_caption("Donkey Kong")

done = False

# Manages how fast screen refreshes 
clock = pygame.time.Clock()

# Game class
class Game(object):
    
    def __init__(self):
        # CREATE GROUPS for each sprite here
        self.player_group = pygame.sprite.Group()
        self.allwall_group = pygame.sprite.Group()   # All wall group is a group including all inner and outer walls
        self.outerwall_group = pygame.sprite.Group()
        self.innerwall_group = pygame.sprite.Group()

        # Create a group of all sprites together
        self.all_sprites_group = pygame.sprite.Group()

        # Setting the gameRunning flag to false
        self.gameRunning = True


    # Method where all the game logic goes
    def runlogic(self):
        self.all_sprites_group.update()

    def display(self, screen):
        # Making the screen background black
        screen.fill(BLACK)

        # Draws all the sprites
        self.all_sprites_group.draw(screen)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Method which closes the game 
    def eventprocess(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False
        
    def levelsetup(self):
        for i in range (0,750):
            # temp_x and temp_y are the temporary values where the wall will be created for that iteration of the for loop, so if there is a 1 at that position, it will be created at a different x and y each time
            # We have an if i == 0 here because we need the walls to start at zero, if it didnt we would start with temp_x = temp_x + 40 and so fourth
            # Add 40 to the x coordinate for the wall when there is a y in the list
            if i == 0:
                temp_x = 0
            else:
                temp_x = temp_x + 40
                
            # Increases the y value (goes down to the next row of walls) once the row is filled (after 25 elements in the list), but dont change it when i = 0
            if i == 0:
                temp_y = 0
            elif i % 30 == 0:
                temp_x = 0
                temp_y = temp_y + 40
                # 1s in the array represent outer walls
            if self.level1[i] == 1:
                self.myOuterWall = outerwall(RED, 40, 40, temp_x, temp_y)
                self.outerwall_group.add(myOuterWall)
                self.allwall_group.add(myOuterWall)
                self.all_sprites_group.add(myOuterWall)
            # 2s in the array represent inner walls
            if self.level1[i] == 2:
                self.myInnerWall = innerwall(RED, 40, 40, temp_x, temp_y)
                self.innerwall_group.add(myInnerWall)
                self.allwall_group.add(myInnerWall)
                self.all_sprites_group.add(myInnerWall)
            # 3s in the array represent the starting position of the player
            if self.level1[i] == 3:
                # Instantiate the player class - colour, width, height, x, y, speed
                self.myPlayer = player(BLUE, 40, 40, 20, 20, temp_x, temp_y)
                # Add the player to a player group and an all sprites group
                self.player_group.add(myPlayer)
                self.all_sprites_group.add(myPlayer)
    # CLASSES
    # Making the player class
    class player(pygame.sprite.Sprite):
        # Define the constructor for the player
        def __init__(self, color, width, height, x_speed, y_speed, x, y):
            # Call the super class (the super class for the player is sprite)
            super().__init__()
            # Set the position of the sprite
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    # Outerwall class
    class outerwall(pygame.sprite.Sprite):
        # Define the constructor for the wall class
        def __init__(self, color, width, height, x, y):
            super().__init__()
            # Create a sprite and fill it with a the image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
    # Innerwall class (basically the construction bars that mario runs along) - inherits everything from the outerwall class
    class innerwall(outerwall):
        pass


# STAYS OUTSIDE OF ANY CLASS
game = Game()

# Main Program Loop
while not done:
    #  Main event loop
    # done = game.eventprocess() means that when the game is exited, eventprocess returns True, making done = True, which exits the game
    done = game.eventprocess()

    # Game logic should go here
    game.runlogic()

    # Draw the screen
    game.display(screen)

    # Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
