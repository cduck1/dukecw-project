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

# CLASSES
# Making the player class
class player(pygame.sprite.Sprite):
    # Define the constructor for the player
    def __init__(self, color, width, height, x_speed, y_speed, x, y):
        # Call the super class (the super class for the player is sprite)
        super().__init__()
        # Set the position of the sprite
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Set a speed vector
        self.change_x = 0
        self.change_y = 0
        
    def update(self):
        # PLAYER MOVEMENT
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game.gravity = True # This seemingly extra gravity = true just ensures that when the player moves off the ladder mid way up, they will always fall again
            self.changespeed(-5, 0)
        if keys[pygame.K_RIGHT]:
            game.gravity = True # This seemingly extra gravity = true just ensures that when the player moves off the ladder mid way up, they will always fall again
            self.changespeed(5, 0)
        # Makes it so that player can only go up if he is in contact with the ladder and turns gravity off while the player is on the ladder
        if pygame.sprite.groupcollide(game.player_group, game.ladder_group, False, False):
            if keys[pygame.K_UP]:
                game.gravity = False
                self.changespeed(0, -5)
            else:
                game.gravity = True
        # Makes it so that player can only go down if he is in contact with the ladder and turns gravity off while the player is on the ladder
        if pygame.sprite.groupcollide(game.player_group, game.ladder_group, False, False):
            if keys[pygame.K_DOWN]:
                game.gravity = False
                self.changespeed(0, 5)
            else:
                game.gravity = True


        # GRAVITY - if the player is not colliding with anything, aka he is in the open space, make him fall to the ground (at which point he will be colliding with the ground)
        if game.gravity == True:
            self.changespeed(0,3)

        # Made this code functions because it cleans up the previously cluttered update function significantly
        self.movehorizontal()
        self.movevertical()

        # Resets the speed change to 0 every update so that the speed doesn't accelerate infinitely
        self.change_x = 0
        self.change_y = 0

    # Change the x and y speed of the player
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def movehorizontal(self):
        # Move the player left/right
        self.rect.x += self.change_x
        # Did we HIT A WALL while moving left/right
        wall_hit_group = pygame.sprite.spritecollide(self, game.allwall_group, False)
        for wall in wall_hit_group:
            # If we are moving right, set our right side to the left side of the wall we hit
            if self.change_x > 0:
                self.rect.right = wall.rect.left
            else:
                # Otherwise if we are moving left, do the opposite
                self.rect.left = wall.rect.right

    def movevertical(self):
        # Move the player up/down
        self.rect.y += self.change_y
        # Did we hit a WALL while moving up/down
        wall_hit_group = pygame.sprite.spritecollide(self, game.allwall_group, False)
        for wall in wall_hit_group:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = wall.rect.top
            else:
                self.rect.top = wall.rect.bottom


# Outerwall class
class outerwall(pygame.sprite.Sprite):
    # Define the constructor for the wall class
    def __init__(self, color, width, height, x, y):
        super().__init__()
        # Create a sprite and fill it with a the image
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Innerwall class (basically the construction bars that player runs along) - inherits everything from the outerwall class
class innerwall(outerwall):
    pass

# Ladder class - when player collides with this he should be able to move up and down it - this is how he gets to the next construction piece/ layer
class ladder(pygame.sprite.Sprite):
    # Define the constructor for the wall class
    def __init__(self, color, width, height, x, y):
        super().__init__()
        # Create a sprite and fill it with a the image
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Game class
class Game(object):
    def __init__(self):
        # CREATE GROUPS for each sprite here
        self.player_group = pygame.sprite.Group()
        self.allwall_group = pygame.sprite.Group()   # All wall group is a group including all inner and outer walls
        self.outerwall_group = pygame.sprite.Group()
        self.innerwall_group = pygame.sprite.Group()
        self.ladder_group = pygame.sprite.Group()

        # Create a group of all sprites together
        self.all_sprites_group = pygame.sprite.Group()

        # Setting the gameRunning flag to false - when the game is exited, the eventprocess() method returns True, making done = True, which exits the game
        self.gameRunning = True

        # Variables
        self.gravity = True

        # CREATING THE LAYOUT OF THE GAME USING A LIST 
        # Plan for creating the walls: have a list of 1200 items, create wall at a specific x and y coordinates if there is a 1; once you get to the 48th element (to the end of the screen), go you down 40 pixels and start at x coord 0
        # Rows are sets of 48 elements
        # Columns are 25 elements
        # There are 1200 total elements because each element represent a block of 48 by 40 and 48 x 40 = 1200
        # Top and bottom walls (48 1s) = 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
        # Side walls = 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
        # 0 = nothing present
        # 1 = outer wall present
        # 2 = inner wall present
        # 3 = player start point
        self.level1 =  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,2,2,2,2,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,2,2,2,2,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,2,2,2,2,2,2,2,2,2,4,4,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,2,2,4,2,2,2,2,2,2,0,0,0,0,0,0,0,1,
                        1,0,0,0,2,2,2,2,2,2,2,2,2,4,4,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,2,2,4,2,2,2,2,2,2,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,3,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        # Calls the method levelsetup() so to build the map - this is still in the __init__() function
        self.levelsetup()

    # Method where all the game logic goes
    def runlogic(self):
        self.all_sprites_group.update()

    def display(self,screen):
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
        for i in range (0,1200):
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
            elif i % 48 == 0:
                temp_x = 0
                temp_y = temp_y + 40
                # 1s in the array represent outer walls
            if self.level1[i] == 1:
                self.myOuterWall = outerwall(RED, 40, 40, temp_x, temp_y)
                self.outerwall_group.add(self.myOuterWall)
                self.allwall_group.add(self.myOuterWall)
                self.all_sprites_group.add(self.myOuterWall)
            # 2s in the array represent inner walls
            if self.level1[i] == 2:
                self.myInnerWall = innerwall(RED, 40, 40, temp_x, temp_y)
                self.innerwall_group.add(self.myInnerWall)
                self.allwall_group.add(self.myInnerWall)
                self.all_sprites_group.add(self.myInnerWall)
            # 4s in the array represen the ladders
            if self.level1[i] == 4:
                # Need to make is so the player can go down the ladders again
                self.myLadder = ladder(YELLOW, 40, 40,temp_x, temp_y)
                # Add the ladder to a player group and an all sprites group
                self.ladder_group.add(self.myLadder)
                self.all_sprites_group.add(self.myLadder)
            # 3s in the array represent the starting position of the player
            if self.level1[i] == 3:
                # Instantiate the player class - colour, width, height, x, y, speed
                # I need to make the player a better size so that its easier to go up ladders - but also need him to start on the floor
                self.myPlayer = player(BLUE, 40, 40, 20, 20, temp_x, temp_y)
                # Add the player to a player group and an all sprites group
                self.player_group.add(self.myPlayer)
                self.all_sprites_group.add(self.myPlayer)



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
