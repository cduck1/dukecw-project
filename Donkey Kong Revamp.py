import pygame
import random
import time

# Defining colours
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PINK = (255,20,147)
PURPLE = (138,43,226)
ORANGE = (255,165,0)

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
        # Flags
        self.isJump = False
        self.gravity = True
        # Variables
        self.lives = 3

    def update(self):
        # PLAYER MOVEMENT
        keys = pygame.key.get_pressed()
        # Player movement up and down ladders
        # Makes it so that player can only go up/down if he is in contact with the ladder and turns gravity off while the player is on the ladder
        if pygame.sprite.groupcollide(game.player_group, game.ladder_group, False, False):
            self.gravity = False # When colliding with the ladder gravity is off
            self.isJump = True # Make isJump true while colliding with the ladder so that the player cannot just while on the ladder
            if keys[pygame.K_UP]:
                self.changespeed(0, -5)
            if keys[pygame.K_DOWN]:
                self.changespeed(0, 5)
        else:
            self.gravity = True # When the player is not touching the ladder, gravity is on
        # Standard left/right movement of the player
        if keys[pygame.K_LEFT]:
            self.changespeed(-5, 0)
        if keys[pygame.K_RIGHT]:
            self.changespeed(5, 0)

        # Made this code functions because it cleans up the previously cluttered update function significantly
        self.jumping()
        self.gravityon()
        self.movehorizontal()
        self.movevertical()
        self.barrelhit()
        self.portalhit()

        # Resets the speed change to 0 every update so that the speed doesn't accelerate infinitely
        self.change_x = 0
        self.change_y = 0

    # Change the x and y speed of the player
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def jumping(self):
        keys = pygame.key.get_pressed()
        # Jumping
        if self.isJump == False: # If mario is not jumping
            if keys[pygame.K_SPACE]: # and if space is pressed
                self.isJump = True
                for x in range (0,30):
                    self.changespeed(0,-1) # Go up 1 pixel 30 times - gives a smoother jump motion and gravity brings the player back down - i think this is not correct

    def gravityon(self):
        # GRAVITY - if the player is not colliding with anything, aka he is in the open space, make him fall to the ground (at which point he will be colliding with the ground)
        if self.gravity == True:
            self.changespeed(0,3)

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
        # This make the self.isJump 'default' to True, so the player cannot jump unless the player's ability to jump is reset when they touch the floor - essentially stop the player jumping in the air
        self.isJump = True
        # Did we hit a WALL while moving up/down
        wall_hit_group = pygame.sprite.spritecollide(self, game.allwall_group, False)
        for wall in wall_hit_group:
            # This self.gravity ensures that there is no gravity acting on the player while the player is touching the ground (not side walls, only ground walls) - this is done because I think it will likely make the game run faster
            self.gravity = False
            # Because we are touching the floor, we reset the ability to jump - you cant jump while on ladders
            self.isJump = False
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = wall.rect.top
            else:
                self.rect.top = wall.rect.bottom

    def barrelhit(self):
        if pygame.sprite.spritecollide(self, game.barrel_group, True):
            self.lives -= 1
            print("Lives: ", int(self.lives))

    # When we hit a new portal we move to the next level
    def portalhit(self):
        if pygame.sprite.spritecollide(self, game.portal_group, False):
            game.level += 1
            game.clearlevel()
            game.levelsetup()

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

class barreldeathwall(outerwall):
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

# portal class - takes you to the next level
class portal(pygame.sprite.Sprite):
    # Define the constructor for the wall class
    def __init__(self, color, width, height, x, y):
        super().__init__()
        # Create a sprite and fill it with a the image
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Barrel class
class barrel(pygame.sprite.Sprite):
    # Define the constructor for the wall class
    def __init__(self, color, width, height, x, y):
        super().__init__()
        # Create a sprite and fill it with a the image
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Set a speed vector
        self.change_x = 0
        self.change_y = 0
        # Variables
        self.gravity = True
        self.goleft = False
        self.goright = False
        self.movex = False # the default value for allowing the barrel to move left or right is false - this is changed to true when the barrel touches the floor
        self.midairchoose = True # The barrel spawns in mid air chooses whether the barrel goes left or right

    def update(self):
        self.barrelgravity()
        self.movementx()
        self.movementy()
        self.die()

        # Resets the speed change to 0 every update so that the speed doesn't accelerate infinitely
        self.change_x = 0
        self.change_y = 0

   # Change the x and y speed of the barrel
    def changespeedbarrel(self, x, y):
        self.change_x += x
        self.change_y += y

    def barrelgravity(self):
        # GRAVITY - if the barrel is not colliding with anything, aka he is in the open space, make him fall to the ground (at which point he will be colliding with the ground)
        # Barrelgravity is slightly slower than player gravity
        if self.gravity == True:
            self.changespeedbarrel(0,2)
    
    def movementx(self):
        # Did we HIT A WALL while moving left/right
        wall_hit_group = pygame.sprite.spritecollide(self, game.allwall_group, False)
        for wall in wall_hit_group:
            # If we are not in midair, we dont choose a number
            self.midairchoose = False
            # If we are touching the floor, we can move left/right
            self.movex = True

        # If the barrel is in mid air we choose whether the barrel goes left or right - it actually going left or right is only acted upon once it hits the ground (once movex = True)
        if (self.midairchoose == True):
            # A random number is generated - if the number is 0, go left, if the number is 1, go right
            leftorright = random.randint(0,1)
            if (leftorright == 0):
                self.goleft = True
                self.goright = False
            else:
                self.goright = True
                self.goleft = False
            self.midairchoose = False

        if self.movex == True:
            # If goleft = True, go left
            if self.goleft == True:
                self.changespeedbarrel(-1, 0)

            # If goright = True, go right
            if self.goright == True:
                self.changespeedbarrel(1, 0)

        # Reset the barrel's ability to move left or right to false every update function so that if in mid air, the barrel cannot move left or right
        self.movex = False
        self.gravity = True
        self.midairchoose = True

        # Move the player left/right
        self.rect.x += self.change_x
        
    def movementy(self):
        # Did we hit a wall while moving up/down
        wall_hit_group = pygame.sprite.spritecollide(self, game.allwall_group, False)
        for wall in wall_hit_group:
            # This self.gravity ensures that there is no gravity acting on the barrel while the barrel is touching the ground (not side walls, only ground walls) - this is done because I think it will likely make the game run faster
            self.gravity = False
            # Ensures the barrel doesn't fall through the wall
            if self.change_y > 0:
                self.rect.bottom = wall.rect.top

        # Move the player up/down
        self.rect.y += self.change_y
    
    def die(self):
        if pygame.sprite.spritecollide(self,game.myBarreldeathwall_group, False):
            self.kill()

# Game class
class Game(object):
    def __init__(self):
        # CREATE GROUPS for each sprite here
        self.player_group = pygame.sprite.Group()
        self.allwall_group = pygame.sprite.Group()   # All wall group is a group including all inner and outer walls
        self.outerwall_group = pygame.sprite.Group()
        self.innerwall_group = pygame.sprite.Group()
        self.ladder_group = pygame.sprite.Group()
        self.portal_group = pygame.sprite.Group()
        self.barrel_group = pygame.sprite.Group()
        self.myBarreldeathwall_group = pygame.sprite.Group()
        # This is a group for object that are part of the map (ladders and all walls) - used in the jumping mechanics and drawing order
        self.background_group = pygame.sprite.Group()
        # This is a group for sprites that move - used in the drawing order - this gets drawn after the background_group does
        self.moving_sprites_group = pygame.sprite.Group()
        # Create a group of all sprites together
        self.all_sprites_group = pygame.sprite.Group()

        # Barrel spawning variables
        # These are temporarily 0 and will be overwritten almost instantely (as soon as the level is setup)
        self.barrelspawncoordx = 0
        self.barrelspawncoordy = 0
        # This is the start timer which allows the barrel to spawn every 3 seconds
        self.start = pygame.time.get_ticks()

        # Variables
        self.level = 1

        # Setting the gameRunning flag to false - when the game is exited, the eventprocess() method returns True, making done = True, which exits the game
        self.gameRunning = True


        # CREATING THE LAYOUT OF THE GAME USING A LIST 
        # Plan for creating the walls: have a list of 1200 items, create wall at a specific x and y coordinates if there is a 1; once you get to the 48th element (to the end of the screen), go you down 40 pixels and start at x coord 0
        # Rows are sets of 48 elements
        # Columns are 25 elements
        # There are 1200 total elements because each element represent a block of 48 by 40 and 48 x 40 = 1200
        # Top and bottom walls (48 1s) = 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
        # Side walls = 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
        self.level1 =  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,2,2,2,4,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,2,2,2,2,2,4,2,0,0,0,0,2,4,2,2,2,2,2,2,2,2,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,2,2,4,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,2,2,4,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,2,2,4,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,2,2,4,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,4,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,4,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,0,0,0,0,0,0,0,0,0,0,2,4,2,0,0,0,0,1,
                        1,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,2,4,2,0,0,0,0,1,
                        1,0,0,0,0,0,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,1,
                        1,0,0,0,0,0,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,2,2,2,2,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,2,2,2,2,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,2,2,2,2,2,2,2,2,2,4,4,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,2,2,4,2,2,2,2,2,2,0,0,0,0,0,0,0,1,
                        1,0,0,0,2,2,2,2,2,2,2,2,2,4,4,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,2,2,4,2,2,2,2,2,2,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        7,0,3,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,7,
                        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        # Calls the method levelsetup() so to build the map - this is still in the __init__() function
        self.levelsetup()

    def update(self):
        self.spawnbarrels()

    def spawnbarrels(self):
        now = pygame.time.get_ticks()
        if now - self.start > 3000: # 3000 milliseconds is 3 seconds
            self.myBarrel = barrel(ORANGE, 20, 20, self.barrelspawncoordx, self.barrelspawncoordy)
            # Add the barrel to a barrel group and an all sprites group
            self.barrel_group.add(self.myBarrel)
            self.moving_sprites_group.add(self.myBarrel)
            self.all_sprites_group.add(self.myBarrel)
            self.start = now

    # Method where all the game logic goes
    def runlogic(self):
        self.update() # This ensures the update function of the game class runs
        self.all_sprites_group.update()

    def display(self,screen):
        # Making the screen background black
        screen.fill(BLACK)

        # Draws the sprites
        self.background_group.draw(screen)
        self.moving_sprites_group.draw(screen)

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
                self.background_group.add(self.myOuterWall)
                self.all_sprites_group.add(self.myOuterWall)
            # 2s in the array represent inner walls
            if self.level1[i] == 2:
                self.myInnerWall = innerwall(RED, 40, 40, temp_x, temp_y)
                self.innerwall_group.add(self.myInnerWall)
                self.allwall_group.add(self.myInnerWall)
                self.background_group.add(self.myInnerWall)
                self.all_sprites_group.add(self.myInnerWall)
            # 3s in the array represent the starting position of the player
            if self.level1[i] == 3:
                # Instantiate the player class - colour, width, height, x, y, speed
                # I need to make the player a better size so that its easier to go up ladders - but also need him to start on the floor
                self.myPlayer = player(BLUE, 40, 40, 20, 20, temp_x, temp_y)
                # Add the player to a player group and an all sprites group and a moving sprites group
                self.player_group.add(self.myPlayer)
                self.moving_sprites_group.add(self.myPlayer)
                self.all_sprites_group.add(self.myPlayer)
            # 4s in the array represent the ladders
            if self.level1[i] == 4:
                self.myLadder = ladder(YELLOW, 40, 40,temp_x, temp_y-1) # The reason for the temp_y-1 is so that when the player moves across the top of a ladder, then dont start moving down and then get stuck and gravity is off the whole way across with it like this
                # Add the ladder to a ladder group, map group and an all sprites group
                self.ladder_group.add(self.myLadder)
                self.background_group.add(self.myLadder)
                self.all_sprites_group.add(self.myLadder)
            # 5s in the array represent portals
            if self.level1[i] == 5:
                self.myPortal = portal(PURPLE, 40, 40, temp_x, temp_y)
                # Add the portal to a portal group and an all sprites group
                self.portal_group.add(self.myPortal)
                self.background_group.add(self.myPortal)
                self.all_sprites_group.add(self.myPortal)
            # 6s in the array represent barrels
            if self.level1[i] == 6:
                self.myBarrel = barrel(ORANGE, 20, 20, temp_x, temp_y)
                # Add the barrel to a barrel group and an all sprites group
                self.barrel_group.add(self.myBarrel)
                self.moving_sprites_group.add(self.myBarrel)
                self.all_sprites_group.add(self.myBarrel)
                # Have two variables that determine where the "6" is in the map, so we can spawn more barrels there every 3 seconds
                self.barrelspawncoordx = temp_x
                self.barrelspawncoordy = temp_y
            # 7s in the array represent barrel death walls - if the barrel hits this wall, it dies (is deleted)
            if self.level1[i] == 7:
                self.myBarreldeathwall = barreldeathwall(RED,40,40,temp_x,temp_y)
                self.myBarreldeathwall_group.add(self.myBarreldeathwall)
                self.allwall_group.add(self.myBarreldeathwall)
                self.background_group.add(self.myBarreldeathwall)
                self.all_sprites_group.add(self.myBarreldeathwall)

        # Print stuff - this goes at the bottom of this because the player must be created to have player.lives
        print("Level: ", int(self.level))
        
    # Allows us to move on to the next level by clearing the current level first
    def clearlevel(self):
        # This get's rid of the current level's sprites
        for sprite in game.all_sprites_group:
            sprite.kill()       

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