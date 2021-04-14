import pygame
import random
import time
import math

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
GOLD = (255,215,0)
BROWN = (165,42,42)
DARKBROWN = (43,29,14)

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
    

    def update(self):
        # PLAYER MOVEMENT
        keys = pygame.key.get_pressed()
        # Player movement up and down ladders
        # Makes it so that player can only go up/down if he is in contact with the ladder and turns gravity off while the player is on the ladder
        if pygame.sprite.groupcollide(game.player_group, game.ladder_group, False, False):
            self.gravity = False # When colliding with the ladder gravity is off
            self.isJump = True # Make isJump true while colliding with the ladder so that the player cannot jump while on the ladder
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
        self.coinhit()
        self.portalhit()

        # Resets the speed change to 0 every update so that the speed doesn't accelerate infinitely
        self.change_x = 0
        self.change_y = 0

    # Change the x and y speed of the player
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def jumping(self):
        nowtime = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        # Jumping
        if self.isJump == False: # If mario is not jumping
            if keys[pygame.K_SPACE]: # and if space is pressed
                global startjumptime # Not exactly sure why the startjumptime must be a global variable but it didnt work when it wasnt
                startjumptime = pygame.time.get_ticks()
                self.changespeed(0,-6)
                self.isJump = True
        # Here we use time so that the player essentially goes up a certain number of pixels (3 - because -6 from the jumping method + 3 from the gravity every tick = -3) every tick for a certain amount of time (180 milliseconds) - this gives a slower uplift section of the jump
        if self.isJump == True:
            airtime = nowtime - startjumptime
            if airtime < 180:
                self.changespeed(0,-6) # Go up 4 pixels each update function (each time jumpingtrigger method is called) - gives a smoother jump motion and gravity brings the player back down. This must be -4 because gravity = +3 every update function so the total movement upwards is 1 pixel a update function
                nowtime = pygame.time.get_ticks()

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
            # Because we are touching the top of a floor, we reset the ability to jump - you cant jump while on ladders
            if (self.rect.bottom == wall.rect.top) or (self.rect.bottom - 3 == wall.rect.top): # The -3 is because the player spawns in 3 pixels above the ground (until you hit left or right key) - not particularly sure why but this fixes it
                self.isJump = False
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = wall.rect.top
            else:
                self.rect.top = wall.rect.bottom

    def barrelhit(self):
        if pygame.sprite.spritecollide(self, game.barrel_group, True):
            game.lives -= 1
            print("Lives: ", int(game.lives))

    def coinhit(self):
        if pygame.sprite.spritecollide(self,game.coin_group, True):
            game.coins += 1
            print("Coins: ", int(game.coins))

    # When we hit a new portal we move to the next level
    def portalhit(self):
        if pygame.sprite.spritecollide(self, game.portal_group, False):
            game.level += 1
            game.coins += 2 # You gain 2 coins when you finish each level
            game.clearlevel() # Clear the level
            game.levelsetup() # And set the level up again

# This is the player but in the arena - we have a different class for this player because it allows us to change the players movement along with many other things (e.g: no jumping, and no need for if statement before every difference between the two players checking whether it is level 10 yet or not)
class arenaplayer(pygame.sprite.Sprite):
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
        self.health = 200
        self.swingcooldown = False
        self.hammerswings = 0
        self.starttimer = 0 # timer for the time the hammer is displayed
        self.starttime = 0 # timer for the cooldown on hammer swings
        self.hammerpresent = False

    def update(self):
        # Resets the speed change to 0 every update so that the speed doesn't accelerate infinitely
        self.change_x = 0
        self.change_y = 0
        # ARENA PLAYER MOVEMENT
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.changespeed(-5, 0)
        if keys[pygame.K_RIGHT]:
            self.changespeed(5, 0)
        if keys[pygame.K_UP]:
            self.changespeed(0, -5)
        if keys[pygame.K_DOWN]:
            self.changespeed(0, 5)

        # Made this code functions because it cleans up the previously cluttered update function significantly
        self.movementx()
        self.movementy()
        self.barrelhit()
        self.hammerpickuphit()
        self.swinghammer()
        self.hammercooldown()
        #self.hammeranimation()

    # Change the x and y speed of the player
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def movementx(self):
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

    def movementy(self):
        # Move the player up/down
        self.rect.y += self.change_y

        # Did we HIT A WALL while moving up/down
        wall_hit_group = pygame.sprite.spritecollide(self, game.allwall_group, False)
        for wall in wall_hit_group:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = wall.rect.top
            else:
                self.rect.top = wall.rect.bottom
            
    def barrelhit(self):
        if pygame.sprite.spritecollide(self, game.donkeybarrel_group, True):
            self.health -= 50
            print("Health: ", int(self.health))
        
    def hammerpickuphit(self):
        if pygame.sprite.spritecollide(self, game.hammerpickup_group, True):
            self.hammerswings += 5 # When you pick up the hammerpickup, you gain 5 hits with the hammer

    
    def swinghammer(self):
        self.starttimer = pygame.time.get_ticks() # not sure why this is needed here but it didnt work without because now was way too high of a value
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if (self.hammerswings > 0) and (self.swingcooldown == False):
                now = pygame.time.get_ticks()
                timedifference = now - self.starttimer
                if (timedifference < 4000) and (self.hammerpresent == False):
                    game.myHammer = hammer(PINK, 10, 4, self.rect.x + 40, self.rect.y + 18)
                    game.hammer_group.add(game.myHammer)
                    game.moving_sprites_group.add(game.myHammer)
                    game.all_sprites_group.add(game.myHammer)
                    self.hammerswings -= 1
                    self.hammerpresent = True
                    self.starttimer = now
                else:
                    self.swingcooldown = True
                    self.hammerpresent = False
                    game.myHammer.kill()               
                    self.starttimer = now

            #if (self.hammerswings > 0) and (self.swingcooldown == False):
            #    game.myHammer = hammer(PINK, 10, 4, self.rect.x + 40, self.rect.y + 18)
            #    game.hammer_group.add(game.myHammer)
            #    game.moving_sprites_group.add(game.myHammer)
            #    game.all_sprites_group.add(game.myHammer)
            #    self.hammerswings -= 1
            #   self.hammerpresent = True
            #    self.swingcooldown = True

    # Is responsible for a cooldown meaning the hammer can only be swung once every 2 seconds
    def hammercooldown(self):
        if self.swingcooldown == True:
            now = pygame.time.get_ticks()
            if now - self.starttime > 2000: # 2000 milliseconds (ticks) is 2 seconds
                self.swingcooldown = False
                self.starttime = now

    def hammeranimation(self):
        if self.hammerpresent == True:
            now = pygame.time.get_ticks()
            if now - self.starttime > 1000: # the animation of the hammer being swung lasts 1 second 
                game.myHammer.kill()
                self.hammerpresent = False
                self.starttime = now

# The donkey kong class - used in the boss fight at level 10
class donkeykong(pygame.sprite.Sprite):
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
        self.isMove = True
        self.isPaused = False
        self.startpause = 0
        self.starttimer = 0
        self.health = 1000

    def update(self):
        # If donkey kong is not meant to be moving (isMove = False), ensure this occurs for a given period of time - this essentially ensures isMove is reset after a given period of time
        self.pausemovement()
        self.throwbarrel()
        self.movementx()
        self.movementy()
        
        # Resets the speed change to 0 every update so that the speed doesn't accelerate infinitely
        self.change_x = 0
        self.change_y = 0

    # Change the x and y speed of the player
    def changespeed(self,x,y):
        self.change_x += x
        self.change_y += y

    def movementx(self):
        # Moves donkey kong towards mario slowly on the x axis - the + 20 and + 40 are to ensure donkey kong goes to the centre of the player
        if self.isMove == True:
            if game.myArenaplayer.rect.x + 20 > self.rect.x + 40:
                self.changespeed(1,0)
            if game.myArenaplayer.rect.x + 20 < self.rect.x + 40:
                self.changespeed(-1,0)

        # Move donkey kong left/right
        self.rect.x += self.change_x

        # Making sure we don't go through donkey kong
        if (pygame.sprite.spritecollide(self,game.arenaplayer_group,False)):
            self.startpause = pygame.time.get_ticks()
            self.isMove = False
            if game.myArenaplayer.change_x > 0:
                game.myArenaplayer.rect.right = self.rect.left
            if game.myArenaplayer.change_x < 0:
                game.myArenaplayer.rect.left = self.rect.right

        # Did we HIT A WALL while moving left/right
        wall_hit_group = pygame.sprite.spritecollide(self, game.allwall_group, False)
        for wall in wall_hit_group:
            # If we are moving right, set our right side to the left side of the wall we hit
            if self.change_x > 0:
                self.rect.right = wall.rect.left
            if self.change_x < 0:
                # Otherwise if we are moving left, do the opposite
                self.rect.left = wall.rect.right

    def movementy(self):
        # Moves donkey kong towards mario slowly on the y axis - the + 20 and + 40 are to ensure donkey kong goes to the centre of the player
        if self.isMove == True:
            if game.myArenaplayer.rect.y + 20 > self.rect.y + 40:
                self.changespeed(0,1)
            if game.myArenaplayer.rect.y + 20 < self.rect.y + 40:
                self.changespeed(0,-1)

        # Move donkey kong up/down
        self.rect.y += self.change_y

        # Making sure we don't go through the player
        if (pygame.sprite.spritecollide(self,game.arenaplayer_group,False)):
            self.startpause = pygame.time.get_ticks()
            self.isMove = False
            if game.myArenaplayer.change_y > 0:
                game.myArenaplayer.rect.bottom = self.rect.top
            if game.myArenaplayer.change_y < 0:
                game.myArenaplayer.rect.top = self.rect.bottom

        # Did we HIT A WALL while moving up/down
        wall_hit_group = pygame.sprite.spritecollide(self, game.allwall_group, False)
        for wall in wall_hit_group:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = wall.rect.top
            if self.change_y < 0:
                self.rect.top = wall.rect.bottom

    def throwbarrel(self):
        now = pygame.time.get_ticks()
        if now - self.starttimer > 3000: # 3000 milliseconds is 3 seconds
            # xdiff and ydiff calculate the difference in x and y values between the centre of donkey kong (where the barrel will be spawned) and the centre of the player
            xdiff = (game.myArenaplayer.rect.x+20) - (self.rect.x+40)
            ydiff = (game.myArenaplayer.rect.y+20) - (self.rect.y+40)
            angle = math.atan2(ydiff,xdiff)
            change_x = math.cos(angle) * 5 # 5 represents the velocity - this number makes the speed constant
            change_y = math.sin(angle) * 5
            # Spawn in the barrel
            game.myDonkeybarrel = donkeybarrel(BROWN, 40, 40,change_x, change_y, self.rect.x + 30, self.rect.y + 30)
            # Add the barrel to a barrel group and an all sprites group
            game.donkeybarrel_group.add(game.myDonkeybarrel)
            game.moving_sprites_group.add(game.myDonkeybarrel)
            game.all_sprites_group.add(game.myDonkeybarrel)
            self.starttimer = now
            self.barrelspawned = True

    # Stops donkey kong from moving for a given time period after getting hit by the player - this essentially ensures isMove is reset after a given period of time
    def pausemovement(self):
        if self.isMove == False:
            nowtime = pygame.time.get_ticks()
            pausedmovementtimer = nowtime - self.startpause
            self.isPaused = True
            if pausedmovementtimer < 1800:
                nowtime = pygame.time.get_ticks()
            else:
                self.isMove = True
                self.isPaused = False

# This is the class for the barrels that donkey kong throws in level 10
class donkeybarrel(pygame.sprite.Sprite):
    # Define the constructor for the wall class
    def __init__(self, color, width, height,change_x,change_y, x, y):
        super().__init__()
        # Create a sprite and fill it with a the image
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Set a speed vector
        self.change_x = change_x
        self.change_y = change_y
        
    def update(self):
        self.movement()
        self.destroyinnerwall()
        self.die()

    # The barrel is thrown towards the player
    def movement(self):
        # Move the barrel
        self.rect.x += self.change_x
        self.rect.y += self.change_y
    
    # When a donkeybarrel (from level 10) hits an innerwall, the innerwall is destroyed along with the donkey barrel
    def destroyinnerwall(self):
        pygame.sprite.groupcollide(game.donkeybarrel_group,game.innerwall_group, True, True)

    def die(self):
        if pygame.sprite.spritecollide(self,game.outerwall_group, False):
            self.kill()
        
# This is the hammerpickup class used to gain acces to the hammer that the player can then weild (for level 10)
class hammerpickup(pygame.sprite.Sprite):
    # Define the constructor for the wall class
    def __init__(self, color, width, height, x, y):
        super().__init__()
        # Create a sprite and fill it with a the image
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Variables
    
    def update(self):
        pass

# This is the actual hammer that the player weilds and does damage with (for level 10)
class hammer(pygame.sprite.Sprite):
    # Define the constructor for the wall class
    def __init__(self, color, width, height, x, y):
        super().__init__()
        # Create a sprite and fill it with a the image
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Variables
        self.start = 0

    def update(self):
        self.movement()
        self.donkeyhit()

    def movement(self):
        self.rect.x = game.myArenaplayer.rect.x + 40
        self.rect.y = game.myArenaplayer.rect.y + 18

    def donkeyhit(self):
        if pygame.sprite.spritecollide(self,game.donkeykong_group,False):
            now = pygame.time.get_ticks()
            if now - self.start > 1000: # This is done so that you only do 100 damage per swing (a swing lasts 1 second (1000 ticks)) - instead of 100 damage per tick that they are collided
                game.myDonkeykong.health -= 100
                print("DONKEY KONG HEALTH: ", game.myDonkeykong.health)
                self.start = now


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
        if pygame.sprite.spritecollide(self,game.barreldeathwall_group, False):
            self.kill()

# Coins class
class coins(pygame.sprite.Sprite):
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
        self.portal_group = pygame.sprite.Group()
        self.barrel_group = pygame.sprite.Group()
        self.barreldeathwall_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.arenaplayer_group = pygame.sprite.Group()
        self.donkeykong_group = pygame.sprite.Group()
        self.donkeybarrel_group = pygame.sprite.Group()
        self.hammerpickup_group = pygame.sprite.Group()
        self.hammer_group = pygame.sprite.Group()
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
        # This is the start timer which allows the hammer to spawn every 30 seconds
        self.starttimer = pygame.time.get_ticks()

        # Variables
        self.level = 10
        self.lives = 3 # We refer to the game for the lives of the player as this allows the lives to be continued from level to level - the lives do not reset back to 3 every time you go to the next level
        self.coins = 0
        self.hammerspawned = False # Ensures only one hammer is spawned every three seconds

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
                        1,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,2,2,2,4,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,2,2,2,2,2,4,2,0,0,0,0,2,4,2,2,2,2,2,2,2,2,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,2,2,4,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,2,2,4,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,2,2,4,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,2,2,4,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,4,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,4,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,0,0,0,0,0,0,0,0,0,0,2,4,2,0,0,0,0,1,
                        1,0,0,0,0,0,0,4,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,2,4,2,0,0,0,0,1,
                        1,0,0,0,0,0,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,1,
                        1,0,0,0,0,0,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,2,2,2,2,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,2,2,2,2,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,2,2,2,2,2,2,2,2,2,4,4,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,2,2,4,2,2,2,2,2,2,0,0,0,0,0,0,0,1,
                        1,0,0,0,2,2,2,2,2,2,2,2,2,4,4,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,2,2,4,2,2,2,2,2,2,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        7,0,3,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,7,
                        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        self.level2 =  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,4,2,2,2,2,2,2,2,4,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,4,2,2,2,2,2,2,2,4,2,2,2,2,2,2,2,4,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,2,2,4,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,4,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,4,2,2,0,0,1,
                        1,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,1,
                        1,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,4,2,2,2,2,2,4,2,2,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,1,
                        1,0,0,0,0,4,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,8,4,0,0,0,0,1,
                        1,0,0,0,2,2,2,4,2,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,8,0,0,4,0,0,0,0,0,0,0,0,0,0,0,2,4,2,2,2,0,0,0,1,
                        1,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,2,2,4,2,2,2,0,2,0,2,2,2,4,2,2,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,2,2,2,2,4,2,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,2,4,2,2,2,2,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,2,2,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,2,2,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,2,4,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,4,2,0,0,0,0,0,0,0,0,1,
                        7,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,7,
                        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        self.level3 =  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,6,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,2,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,8,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,2,4,2,2,2,2,2,2,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,2,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,4,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,2,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,1,
                        1,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,1,
                        1,0,0,2,2,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,1,
                        1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        7,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,7,
                        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        self.level4 =  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,6,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,4,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,1,
                        7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,7,
                        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        self.level5 =  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,4,2,2,2,2,2,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,4,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,2,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,1,
                        1,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,8,0,1,
                        1,0,2,2,2,2,4,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,2,4,2,0,1,
                        1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,4,0,0,1,
                        1,0,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,1,
                        1,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,1,
                        7,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,7,
                        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        self.level6 =  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,2,2,0,0,2,2,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,5,5,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,2,4,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,4,2,0,0,0,0,1,
                        1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,1,
                        1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,1,
                        1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,1,
                        1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,1,
                        1,0,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,2,2,2,2,0,0,0,0,0,0,2,2,2,2,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,8,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,2,2,2,2,2,4,2,2,2,2,2,2,0,0,0,2,2,2,2,2,2,2,4,2,2,2,2,2,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        7,0,0,0,3,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,
                        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        self.level7 =  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,4,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,4,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,4,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,2,2,2,4,2,2,2,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,1,
                        7,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,4,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,7,
                        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                
        self.level8 =  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,6,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,4,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,2,2,2,2,2,4,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,4,2,2,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,2,2,2,2,4,2,2,2,2,2,2,2,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,8,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,2,2,2,4,2,2,2,2,2,2,2,2,2,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,2,2,2,2,4,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,4,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,2,2,2,2,2,2,4,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,4,2,2,2,2,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,1,
                        7,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,7,
                        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                        
        self.level9 =  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,4,2,2,2,2,2,2,4,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,2,4,2,2,2,2,2,2,2,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,2,4,2,2,2,0,0,0,0,0,0,0,2,4,2,2,2,2,2,2,2,2,4,2,0,0,0,0,0,0,0,8,0,0,0,0,0,1,
                        1,0,0,0,0,8,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,2,2,2,4,2,2,0,1,
                        1,0,2,4,2,2,2,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,1,
                        1,0,0,4,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,1,
                        1,0,0,4,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,2,4,2,2,2,2,0,0,0,0,0,2,2,2,2,2,2,2,2,2,4,2,2,2,2,0,0,1,
                        1,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,1,
                        1,0,2,2,2,4,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,1,
                        1,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,1,
                        1,0,0,0,0,4,0,0,0,0,0,0,0,0,2,2,2,2,4,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,4,2,0,1,
                        1,0,0,2,4,2,2,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,1,
                        1,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,1,
                        7,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,7,
                        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            
        # This is the donkey kong boss fight arena
        self.level10 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
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
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,9,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]


        # This list is used in the nextlevel() method
        # We have a 0 at index 0 to represent that there is nothing there, this is done because there is no level 0, levels start at 1, so the first map that can be iterated through is at index 1
        self.alllevels = [0,self.level1,self.level2,self.level3,self.level4,self.level5,self.level6,self.level7,self.level8,self.level9,self.level10]

        # Calls the method levelsetup() so to build the map - this is still in the __init__() function
        self.levelsetup()

    def update(self):
        self.spawnbarrels()
        self.spawnhammerpickup()

    def spawnbarrels(self):
        now = pygame.time.get_ticks()
        if now - self.start > 3000: # 3000 milliseconds is 3 seconds
            self.myBarrel = barrel(BROWN, 20, 20, self.barrelspawncoordx, self.barrelspawncoordy)
            # Add the barrel to a barrel group and an all sprites group
            self.barrel_group.add(self.myBarrel)
            self.moving_sprites_group.add(self.myBarrel)
            self.all_sprites_group.add(self.myBarrel)
            self.start = now
        
    def spawnhammerpickup(self):
        if self.level == 10:
            now = pygame.time.get_ticks()
            if now - self.starttimer > 3000: # 3000 milliseconds is 3 seconds
                self.hammerspawned = False
                self.starttimer = now
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
                    # 0s in the array represent empty space
                    if self.levelselected[i] == 0 and self.hammerspawned == False:
                        spawnhammerpickup = random.randint(0,1000) # There is a 1 in 1000 chance of a hammerpickup spawning at each empty "tile" in the map
                        if spawnhammerpickup == 1:
                            self.myHammerpickup = hammerpickup(PINK, 40, 40, temp_x, temp_y)
                            self.hammerpickup_group.add(self.myHammerpickup)
                            self.moving_sprites_group.add(self.myHammerpickup)
                            self.all_sprites_group.add(self.myHammerpickup)
                            # If a hammerpickup has been spawned, we stop trying to spawn hammerpickup in the map
                            self.hammerspawned = True

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

        # Draws variables - lives, level, coins
        # For level number
        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render(("LEVEL: " + str(self.level)), 1, WHITE)
        screen.blit(text, (10, 10))
        # For player's lives - we only display lives if mario is in level 1-9, if mario makes it to level 10 the lives become irrelevant and he is given 200 health no matter how many lives he had left
        if self.level < 10:
            font = pygame.font.Font('freesansbold.ttf', 30)
            text = font.render(("LIVES: " + str(self.lives)), 1, WHITE)
            screen.blit(text, (10, 45))
        else:
            font = pygame.font.Font('freesansbold.ttf', 30)
            text = font.render(("HEALTH: " + str(self.myArenaplayer.health)), 1, WHITE)
            screen.blit(text, (10, 45))

            # During level 10 we also display hammerswings
            font = pygame.font.Font('freesansbold.ttf', 30)
            text = font.render(("HAMMER SWINGS: " + str(self.myArenaplayer.hammerswings)), 1, WHITE)
            screen.blit(text, (10, 115))
        # For player's coins
        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render(("COINS: " + str(self.coins)), 1, WHITE)
        screen.blit(text, (10, 80))

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Method which closes the game
    def eventprocess(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def levelsetup(self):
        self.nextlevel()
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
            if self.levelselected[i] == 1:
                self.myOuterWall = outerwall(RED, 40, 40, temp_x, temp_y)
                self.outerwall_group.add(self.myOuterWall)
                self.allwall_group.add(self.myOuterWall)
                self.background_group.add(self.myOuterWall)
                self.all_sprites_group.add(self.myOuterWall)
            # 2s in the array represent inner walls
            if self.levelselected[i] == 2:
                self.myInnerWall = innerwall(RED, 40, 40, temp_x, temp_y)
                self.innerwall_group.add(self.myInnerWall)
                self.allwall_group.add(self.myInnerWall)
                self.background_group.add(self.myInnerWall)
                self.all_sprites_group.add(self.myInnerWall)
            # 3s in the array represent the starting position of the player
            if self.levelselected[i] == 3:
                # Instantiate the player class - colour, width, height, x, y, speed
                # I need to make the player a better size so that its easier to go up ladders - but also need him to start on the floor
                self.myPlayer = player(BLUE, 40, 40, 20, 20, temp_x, temp_y)
                # Add the player to a player group and an all sprites group and a moving sprites group
                self.player_group.add(self.myPlayer)
                self.moving_sprites_group.add(self.myPlayer)
                self.all_sprites_group.add(self.myPlayer)
            # 4s in the array represent the ladders
            if self.levelselected[i] == 4:
                self.myLadder = ladder(YELLOW, 40, 40,temp_x, temp_y-1) # The reason for the temp_y-1 is so that when the player moves across the top of a ladder, then dont start moving down and then get stuck and gravity is off the whole way across with it like this
                # Add the ladder to a ladder group, map group and an all sprites group
                self.ladder_group.add(self.myLadder)
                self.background_group.add(self.myLadder)
                self.all_sprites_group.add(self.myLadder)
            # 5s in the array represent portals
            if self.levelselected[i] == 5:
                self.myPortal = portal(PURPLE, 40, 40, temp_x, temp_y)
                # Add the portal to a portal group and an all sprites group
                self.portal_group.add(self.myPortal)
                self.background_group.add(self.myPortal)
                self.all_sprites_group.add(self.myPortal)
            # 6s in the array represent barrels
            if self.levelselected[i] == 6:
                self.myBarrel = barrel(BROWN, 20, 20, temp_x+10, temp_y+10) # The + values are to centre the barrels within that 40x40 block
                # Add the barrel to a barrel group and an all sprites group
                self.barrel_group.add(self.myBarrel)
                self.moving_sprites_group.add(self.myBarrel)
                self.all_sprites_group.add(self.myBarrel)
                # Have two variables that determine where the "6" is in the map, so we can spawn more barrels there every 3 seconds
                self.barrelspawncoordx = temp_x + 10
                self.barrelspawncoordy = temp_y + 10
            # 7s in the array represent barrel death walls - if the barrel hits this wall, it dies (is deleted)
            if self.levelselected[i] == 7:
                self.myBarreldeathwall = barreldeathwall(RED,40,40,temp_x,temp_y)
                self.barreldeathwall_group.add(self.myBarreldeathwall)
                self.allwall_group.add(self.myBarreldeathwall)
                self.background_group.add(self.myBarreldeathwall)
                self.all_sprites_group.add(self.myBarreldeathwall)
            # 8s in the array represent coins
            if self.levelselected[i] == 8:
                self.myCoin = coins(GOLD,10,10,temp_x+15,temp_y+25) # The + values on the temp_x and temp_y are to centre and ensure the coin is on the ground (actually slightly off the ground because this makes it look cooler)
                self.coin_group.add(self.myCoin)
                self.background_group.add(self.myCoin)
                self.all_sprites_group.add(self.myCoin)
            # 9s in the array represent the starting position of arena players - this is only used for level 10
            if self.levelselected[i] == 9:
                self.myArenaplayer = arenaplayer(BLUE,40,40,temp_x,temp_y)
                self.arenaplayer_group.add(self.myArenaplayer)
                self.moving_sprites_group.add(self.myArenaplayer)
                self.all_sprites_group.add(self.myArenaplayer)
            # 10 in the array represents the starting position of donkey kong - this is only used for level 10
            if self.levelselected[i] == 10:
                self.myDonkeykong = donkeykong(DARKBROWN,80,80,temp_x,temp_y)
                self.donkeykong_group.add(self.myDonkeykong)
                self.moving_sprites_group.add(self.myDonkeykong)
                self.all_sprites_group.add(self.myDonkeykong)

        # Print stuff - this goes at the bottom of this because the player must be created to have myPlayer.lives
        print("Level: ", int(self.level))
        print("Lives: ", int(self.lives))
        print("Coins: ", int(self.coins))

    # Allows us to move on to the next level by clearing the current level first
    def clearlevel(self):
        # This get's rid of the current level's sprites
        for sprite in game.all_sprites_group:
            sprite.kill()

    # Chooses which list is iterated through in the levelsetup() method
    def nextlevel(self):
        # self.alllevels is a list of maps of levels, self.level is the current level that the player is on - if self.level = 1, then the map chosen would be whatever were at index 1 (map/ level 2)
        self.levelselected = self.alllevels[self.level]

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