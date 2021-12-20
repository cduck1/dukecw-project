import pygame
import random
import time
import math
from os import path

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
GREY = (180, 180, 180)

pygame.init()

# Set the screen size
size = (1920,1000)
screen = pygame.display.set_mode(size) 

# Title of new window/screen
pygame.display.set_caption("Donkey Kong")

# Manages how fast screen refreshes 
clock = pygame.time.Clock()

# This is the main menu interface
def mainmenu():
    intro = True
    while intro:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                intro = False # Flag that we are done so we exit this loop
                pygame.quit # If the cross in the top right is pressed while in the menu, we exit the game
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    intro = False
        # -- Drawing the menu screen
        screen.fill(BLACK)
        font = pygame.font.Font('freesansbold.ttf', 84)
        text = font.render(str("DONKEY KONG REVAMP"), 1, WHITE)
        text_rect = text.get_rect(center=(960, 250))
        screen.blit(text, text_rect)

        button_1("PLAY",840,330,250,60,WHITE,GREY,0,"1")
        button_1("SHOP",840,410,250,60,WHITE,GREY,0,"2")
        button_1("QUIT",840,490,250,60,WHITE,GREY,0,"Q")
            
        pygame.display.flip()
        clock.tick(60)

# The method for buttons
def button_1(msg1,xb1,yb1,wb1,hb1,icb1,acb1,buttonpressed,action1=None): # msg1 = the message inside the button, xb1 = x coords of button, yb1 = y coords, wb1 = width, hb1 = height, icb1 = inactive colour, acb1 = active colour, action = the output when button is pressed, buttonpressed = the button that was pressed - e.g. if luigi's button was pressed it would say "luigi"
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if xb1+wb1 > mouse[0] > xb1 and yb1+hb1 > mouse[1] > yb1:
        pygame.draw.rect(screen, icb1,(xb1,yb1,wb1,hb1),5)
        if click[0] == 1 and action1 !=None:
            if buttonpressed > 0: # If the button pressed is anything other than 0 (i.e. a button not related to the skins shop), it is saved to a skinselected variable
                global skinselected
                skinselected = buttonpressed # skin selected allows us to identify which skin the user clicked on and is trying to buy
            if action1 == "1":
                gameloop()
            elif action1 == "2":
                shop() # The skins shop
            # Actions related to the skins shop
            elif action1 == "3":
                confirmpurchase() # This calls the method that requests the user confirms their purchase for the skin
            elif action1 == "4":
                skinpurchased(skinselected) # This calls the method that removes the user's coins in exchange for the skin
            elif action1 == "5": # If the user presses "no" on the confirm purchase screen, they are taken back to the shop
                shop()
            elif action1 == "M":
                mainmenu()
            elif action1 == "Q":
                pygame.quit()
    else:
        pygame.draw.rect(screen, acb1,(xb1,yb1,wb1,hb1),5)
        
    smallText = pygame.font.Font("freesansbold.ttf",30)
    textSurf, textRect = text_objects(msg1, smallText)
    textRect.center = ((xb1+(wb1/2)),(yb1+(hb1/2)))
    screen.blit(textSurf, textRect)

def text_objects(text,font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

# The method for the shop
def shop():
    shop = True
    while shop:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                shop = False # Flag that we are done so we exit this loop
                pygame.quit # If the cross in the top right is pressed while in the menu, we exit the game
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    shop = False
        # -- Drawing the menu screen
        screen.fill(BLACK)
        # Displays "THE SHOP"
        font = pygame.font.Font('freesansbold.ttf', 84)
        text = font.render(str("THE SHOP"), 1, WHITE)
        text_rect = text.get_rect(center=(960, 75))
        screen.blit(text, text_rect)
        # Tells the user what they can do in the shop
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(str("HERE YOU CAN SPEND YOU HARD EARNED COINS ON COSMETIC UPGRADES"), 1, WHITE)
        text_rect = text.get_rect(center=(960, 120))
        screen.blit(text, text_rect)

        # Shows a preview of the skin in the shop
        # I made the button larger do I could fit in a completely unrelated (not part of the button function) piece of text that shows the price of the skin
        screen.blit(pygame.image.load("shopmariopreview.PNG"),(330,200))
        button_1("MARIO",330,450,250,80,WHITE,GREY,1,"3")
        font = pygame.font.Font('freesansbold.ttf', 15)
        text = font.render(str("FREE - DEFAULT"), 1, WHITE)
        text_rect = text.get_rect(center=(455, 515))
        screen.blit(text, text_rect)

        # Shows a preview of the skin in the shop
        screen.blit(pygame.image.load("shopluigipreview.PNG"),(630,200))

        # Reads the purchasedluigi text file to see if luigi has previously been purchased - if he has a different button with a different function (no function) is displayed
        luigipurchased = False # Initiates the variable
        # Try to read the luigipurchased from a file
        try:
            luigi_file = open("purchasedluigi.txt", "r") # Reads the text file and saves it to the luigi_file variable
            luigipurchased = str(luigi_file.read()) # saves what was read from the text file to the luigipurchased variable - this should be either "True" or "False"
            luigi_file.close() # closes the coins variable
        except:
            # If there is some kind of error, set the luigipurchased variable to False
            luigipurchased = False

        # This checks if luigi has already been purchased an displays a different button with a different description message (already purchased/ 1000 coins) depending on that - if luigi has already been purchased, a button with no function is displayed
        if luigipurchased == False:
            button_1("LUIGI",630,450,250,80,WHITE,GREY,2,"3")
            font = pygame.font.Font('freesansbold.ttf', 15)
            text = font.render(str("1000 COINS"), 1, WHITE)
            text_rect = text.get_rect(center=(755, 515))
            screen.blit(text, text_rect)
        else:
            button_1("LUIGI",630,450,250,80,WHITE,GREY,0,"0")
            font = pygame.font.Font('freesansbold.ttf', 15)
            text = font.render(str("ALREADY PURCHASED"), 1, WHITE)
            text_rect = text.get_rect(center=(755, 515))
            screen.blit(text, text_rect)

        # Main menu button
        button_1("MAIN MENU",840,850,250,60,WHITE,GREY,0,"M") # This button take you to the main menu

        pygame.display.flip()
        clock.tick(60)

# Confirm purchase method - used when the user tries to buy a skin in the shop, they must confirm their purchase
def confirmpurchase():
    confirm = True
    while confirm:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                confirm = False # Flag that we are done so we exit this loop
                pygame.quit # If the cross in the top right is pressed while in the menu, we exit the game
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    confirm = False
        # -- Drawing the menu screen
        screen.fill(BLACK)
        # Displays "CONFIRM PURCHASE" text
        font = pygame.font.Font('freesansbold.ttf', 60)
        text = font.render(str("CONFIRM PURCHASE"), 1, WHITE)
        text_rect = text.get_rect(center=(960, 400))
        screen.blit(text, text_rect)
        button_1("YES",690,450,250,60,WHITE,GREY,0,"4") # This button is pressed when the user is confirming the purchase for the skin they previously clicked on
        button_1("NO",980,450,250,60,WHITE,GREY,0,"5") # This button is pressed when the user is declining the purchase for the skin they previously clicked on

        pygame.display.flip()
        clock.tick(60)

# If the user has clicked yes on confirm purchase, this method is run
def skinpurchased(skinselected):
    # This is essentially the same as the loadcoins() method but we must recreate the loading of coins in the same method as where they are changed because of python having difficulties with passing variables by reference
    # We get the variable "coins" from the file "coins.txt"
    coins = 0 # Initiates the variable
    # Try to read coins from a file
    try:
        coins_file = open("coins.txt", "r") # Reads the text file and saves it to the coins_file variable
        coins = int(coins_file.read()) # saves the number read from the text file to the coins variable
        coins_file.close() # closes the coins variable
    except:
        # If there is some kind of error, set the coins variable to 0
        coins = 0

    # If the skin selected was luigi, we first check that we haven't already purchased the luigi skin - this allows us to determine whether the player can buy the skin for the first time 
    if skinselected == 2:
        luigipurchased = False # Initiates the variable
        # Try to read the luigipurchased from a file
        try:
            luigi_file = open("purchasedluigi.txt", "r") # Reads the text file and saves it to the luigi_file variable
            luigipurchased = str(luigi_file.read()) # saves what was read from the text file to the luigipurchased variable - this should be either "True" or "False"
            luigi_file.close() # closes the coins variable
        except:
            # If there is some kind of error, set the luigipurchased variable to False
            luigipurchased = False

    # If the player has at least 1000 coins, they have enough money to make the purchase and the purchase is made (and they haven't already purchased the skin) we minus 1000 from coins and give them access to the skin. If the player does not have enough money, this is printed in the console and they are returned to the shop
    if coins >= 1000 and luigipurchased == False:
        coins -= 1000
        luigipurchased = True
        # We write to the text file that we have purchased the luigi skin by writing "True"
        # Save the new value for coins to the text file
        try:
            # Write the file to disk
            luigi_file = open("purchasedluigi.txt", "w")
            luigi_file.write(str(luigipurchased))
            luigi_file.close()
            print("Transaction confirmed")
        except:
            # Can't write it
            print("Unable to write whether luigi was purchased.")
        shop()
    else:
        print("You do not have sufficient funds to make the purchase")
        shop()

    # Save the new value for coins to the text file
    try:
        # Write the file to disk
        coins_file = open("coins.txt", "w")
        coins_file.write(str(coins))
        coins_file.close()
    except:
        # Can't write it
        print("Unable to save coins.")

def gameloop():
    done = False
    # CLASSES
    # Making the player class
    class player(pygame.sprite.Sprite):
        # Define the constructor for the player
        def __init__(self, color, width, height, x_speed, y_speed, x, y):
            # Call the super class (the super class for the player is sprite)
            super().__init__()
            # Set the position of the sprite
            self.image = pygame.image.load('mario1nobg.PNG')
            self.currentleftimage = 0 # The start variable for the array image
            self.currentrightimage = 0 # The start variable for the array image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            # Set a speed vector
            self.change_x = 0
            self.change_y = 0
            # Flags
            self.isJump = False
            self.gravity = True
            self.moveright = False
            self.moveleft = False
            # Variables
            self.startjumptime = 0
            self.animationcounterleft = 0
            self.animationcounterright = 0
            self.startposx = 0
            self.startposy = 0

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
                self.moveleft = True
                self.moveright = False
            if keys[pygame.K_RIGHT]:
                self.changespeed(5, 0)
                self.moveright = True
                self.moveleft = False

            # Made this code functions because it cleans up the previously cluttered update function significantly
            self.die()
            self.jumping()
            self.gravityon()
            self.movehorizontal()
            self.movevertical()
            self.barrelhit()
            self.coinhit()
            self.portalhit()
            self.animateleft()
            self.animateright()

            # Resets the speed change to 0 every update so that the speed doesn't accelerate infinitely
            self.change_x = 0
            self.change_y = 0
            self.moveright = False
            self.moveleft = False

        # Change the x and y speed of the player
        def changespeed(self, x, y):
            self.change_x += x
            self.change_y += y
        
        def die(self):
            if game.lives < 0:
                game.youlose = True

        def jumping(self):
            nowtime = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()
            # Jumping
            if self.isJump == False: # If mario is not jumping
                if keys[pygame.K_SPACE]: # and if space is pressed
                    self.startjumptime = pygame.time.get_ticks()
                    self.changespeed(0,-6)
                    self.isJump = True
            # Here we use time so that the player essentially goes up a certain number of pixels (3 - because -6 from the jumping method + 3 from the gravity every tick = -3) every tick for a certain amount of time (180 milliseconds) - this gives a slower uplift section of the jump
            if self.isJump == True:
                airtime = nowtime - self.startjumptime
                if airtime < 180:
                    self.changespeed(0,-6)
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
                # Mario starts from the beginning of the level
                self.rect.x = game.startposx
                self.rect.y = game.startposy
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

        def animateleft(self):
            if self.animationcounterleft % 6 == 0:
                if self.moveleft == True and self.moveright == False:
                    self.currentleftimage += 1
                    if self.currentleftimage>= len(Game.mariorunleft):
                        self.currentleftimage = 0
                    self.image = Game.mariorunleft[self.currentleftimage]
            self.animationcounterleft += 1

        def animateright(self):
            if self.animationcounterright % 6 == 0: # Slows down the animation
                if self.moveright == True and self.moveleft == False:
                    # Updates the current image to the next image in the array (for animations) - if self.currentimage = 10, we restart the array from image number 0. It only does this every 6 ticks because otherwise it spins really (too) fast
                    self.currentrightimage += 1
                    if self.currentrightimage >= len(Game.mariorunright):
                        self.currentrightimage = 0
                    self.image = Game.mariorunright[self.currentrightimage]
            self.animationcounterright += 1

    # This is the player but in the arena - we have a different class for this player because it allows us to change the players movement along with many other things (e.g: no jumping, and no need for if statement before every difference between the two players checking whether it is level 10 yet or not)
    class arenaplayer(pygame.sprite.Sprite):
        # Define the constructor for the wall class
        def __init__(self, color, width, height, x, y):
            super().__init__()
            # Create a sprite and fill it with a the image
            self.image = pygame.image.load('mariotopdownS.PNG')
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            # Set a speed vector
            self.change_x = 0
            self.change_y = 0
            # Variables
            self.swingcooldown = False
            self.hammerswings = 0
            self.starttimer = 0 # timer for the cooldown on hammer swings
            self.starttime = 0 # timer for the hammer animation
            self.hammerpresent = False
            self.health = 200
            # Health bar variables
            self.maxhealth = 200
            self.health_bar_length = 60
            self.health_ratio = self.maxhealth / self.health_bar_length

        def update(self):
            # Resets the speed change to 0 every update so that the speed doesn't accelerate infinitely
            self.change_x = 0
            self.change_y = 0
            # ARENA PLAYER MOVEMENT
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.changespeed(-5, 0)
                self.animateW()
            if keys[pygame.K_RIGHT]:
                self.changespeed(5, 0)
                self.animateE()
            if keys[pygame.K_UP]:
                self.changespeed(0, -5)
                self.animateN()
            if keys[pygame.K_DOWN]:
                self.changespeed(0, 5)
                self.animateS()

            # Made this code functions because it cleans up the previously cluttered update function significantly
            self.die()
            self.movementx()
            self.movementy()
            self.barrelhit()
            self.hammerpickuphit()
            self.hammercooldown()
            self.swinghammer()
            self.hammeranimation()

        # Change the x and y speed of the player
        def changespeed(self, x, y):
            self.change_x += x
            self.change_y += y

        def die(self):
            if self.health <= 0:
                game.youlose = True

        def healthbar(self):
            pygame.draw.rect(screen, (255,0,0),(self.rect.x-10,self.rect.y - 15,self.health/self.health_ratio,10))
            pygame.draw.rect(screen,(255,255,255),(self.rect.x-10,self.rect.y - 15,self.health_bar_length,10),2)

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
                self.hammerswings += 3 # When you pick up the hammerpickup, you gain 5 hits with the hammer

        # Is responsible for a cooldown meaning the hammer can only be swung once every 2 seconds
        def hammercooldown(self):
            if self.swingcooldown == True:
                now = pygame.time.get_ticks()
                if now - self.starttimer > 2000: # 2000 milliseconds (ticks) is 2 seconds
                    self.swingcooldown = False
                    self.starttimer = now

        def swinghammer(self):
            if pygame.key.get_pressed()[pygame.K_SPACE]: # This is so you must press the space bar to swing the hammer - not just hold it down constantely
                if (self.hammerswings > 0) and (self.swingcooldown == False) and (self.hammerpresent == False):
                    self.myHammer = hammer(PINK, 30, 15, self.rect.x + 40, self.rect.y + 18)
                    game.hammer_group.add(self.myHammer)
                    game.moving_sprites_group.add(self.myHammer)
                    game.all_sprites_group.add(self.myHammer)
                    self.hammerswings -= 1
                    self.hammerpresent = True
                    self.swingcooldown = True

        def hammeranimation(self):
            if self.hammerpresent == True:
                now = pygame.time.get_ticks()
                if now - self.starttime > 1000: # the animation of the hammer being swung lasts 1 second 
                    self.myHammer.kill()
                    self.hammerpresent = False
                    self.starttime = now

        def animateN(self):
            # Changes the image of the arena player to the coresponding image that faces north in the array of images named "arenamarioimages"
            self.image = Game.arenamarioimages[0]

        def animateE(self):
            # Changes the image of the arena player to the coresponding image that faces east in the array of images named "arenamarioimages"
            self.image = Game.arenamarioimages[1]

        def animateS(self):
            # Changes the image of the arena player to the coresponding image that faces south in the array of images named "arenamarioimages"
            self.image = Game.arenamarioimages[2]

        def animateW(self):
            # Changes the image of the arena player to the coresponding image that faces west in the array of images named "arenamarioimages"
            self.image = Game.arenamarioimages[3]


    # The donkey kong class - used in the boss fight at level 10
    class donkeykong(pygame.sprite.Sprite):
        # Define the constructor for the wall class
        def __init__(self, color, width, height, x, y):
            super().__init__()
            # Create a sprite and fill it with a the image
            self.image = pygame.image.load('donkeykongEnobg.PNG')
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
            # Health bar variables
            self.maxhealth = 1000
            self.health_bar_length = 1000
            self.health_ratio = self.maxhealth / self.health_bar_length

        def update(self):
            self.die()
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

        def die(self):
            if self.health <= 0:
                game.coins += 200 # You gain 200 coins when you win/ beat the game
                game.youwin = True

        def healthbar(self):
            pygame.draw.rect(screen, (255,0,0),(420,50,self.health/self.health_ratio,25))
            pygame.draw.rect(screen,(255,255,255),(420,50,self.health_bar_length,25),4)

        def movementx(self):
            # Moves donkey kong towards mario slowly on the x axis - the + 20 and + 40 are to ensure donkey kong goes to the centre of the player
            if self.isMove == True:
                # Movement right
                if game.myArenaplayer.rect.x + 20 > self.rect.x + 40:
                    self.changespeed(1,0)
                    self.image = pygame.image.load('donkeykongEnobg.PNG')
                # Movement left
                if game.myArenaplayer.rect.x + 20 < self.rect.x + 40:
                    self.changespeed(-1,0)
                    self.image = pygame.image.load('donkeykongWnobg.PNG')

            # Move donkey kong left/right
            self.rect.x += self.change_x

            # Making sure the player doesn't go through donkey kong
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
            self.image = pygame.image.load('throwingbarrel.PNG')
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
            pygame.sprite.groupcollide(game.donkeybarrel_group,game.arenainnerwall_group, True, True)

        def die(self):
            if pygame.sprite.spritecollide(self,game.outerwall_group, False):
                self.kill()
            
    # This is the hammerpickup class used to gain acces to the hammer that the player can then weild (for level 10)
    class hammerpickup(pygame.sprite.Sprite):
        # Define the constructor for the wall class
        def __init__(self, color, width, height, x, y):
            super().__init__()
            # Create a sprite and fill it with a the image
            self.image = pygame.image.load('hammerpickup.PNG')
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        
    # This is the actual hammer that the player weilds and does damage with (for level 10)
    class hammer(pygame.sprite.Sprite):
        # Define the constructor for the wall class
        def __init__(self, color, width, height, x, y):
            super().__init__()
            # Create a sprite and fill it with a the image
            self.image = pygame.image.load('hammernobgresize.PNG')
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
            if pygame.sprite.spritecollide(self,game.donkeykong_group,False): # The hammer is killed when it hits donkey kong
                self.kill()
                game.myDonkeykong.health -= 100
                print("DONKEY KONG HEALTH: ", game.myDonkeykong.health)

    # Outerwall class
    class outerwall(pygame.sprite.Sprite):
        # Define the constructor for the wall class
        def __init__(self, color, width, height, x, y):
            super().__init__()
            # Create a sprite and fill it with a the image
            self.image = pygame.image.load('outerwallpiece.PNG')
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    # Innerwall class (basically the construction bars that player runs along) - inherits everything from the outerwall class apart from the image which is overridden
    class innerwall(pygame.sprite.Sprite):
        # Define the constructor for the wall class
        def __init__(self, color, width, height, x, y):
            super().__init__()
            # Create a sprite and fill it with a the image
            self.image = pygame.image.load('constructionpiece.PNG')
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    # Arenainnerwall is a innerwall spawned only on level 10 - this exists so we can easily change the image to a barrel from a construction piece as it is in levels 1-9
    class arenainnerwall(pygame.sprite.Sprite):
        # Define the constructor for the wall class
        def __init__(self, color, width, height, x, y):
            super().__init__()
            # Create a sprite and fill it with a the image
            self.image = pygame.image.load('topdownbarrel.PNG')
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
 
    class barreldeathwall(outerwall):
        pass

    # Ladder class - when player collides with this he should be able to move up and down it - this is how he gets to the next construction piece/ layer
    class ladder(pygame.sprite.Sprite):
        # Define the constructor for the wall class
        def __init__(self, color, width, height, x, y):
            super().__init__()
            # Create a sprite and fill it with a the image
            self.image = pygame.image.load('ladderpiece.PNG')
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
            self.currentleftimage = 0 # The start variable for the array of left rolling images
            self.currentrightimage = 0 
            self.image = pygame.image.load('barrel0.PNG') # This is the start image for the barrel
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
            self.animationcounter = 0 # A counter used ot slow down the speed at which the coin spins

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
                    self.animateleft()

                # If goright = True, go right
                if self.goright == True:
                    self.changespeedbarrel(1, 0)
                    self.animateright()

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
        
        def animateleft(self):
            if self.goleft == True and self.goright == False:
                # Updates the current image to the next image in the array (for animations) - if self.currentimage = 10, we restart the array from image number 0. It only does this every 6 ticks because otherwise it spins really (too) fast
                self.currentleftimage += 1
                if self.currentleftimage >= len(Game.spinleft):
                    self.currentleftimage = 0
                self.image = Game.spinleft[self.currentleftimage]

        def animateright(self):
            if self.goright == True and self.goleft == False:
                # Updates the current image to the next image in the array (for animations) - if self.currentimage = 10, we restart the array from image number 0. It only does this every 6 ticks because otherwise it spins really (too) fast
                self.currentrightimage += 1
                if self.currentrightimage >= len(Game.spinright):
                    self.currentrightimage = 0
                self.image = Game.spinright[self.currentrightimage]
        
        def die(self):
            if pygame.sprite.spritecollide(self,game.barreldeathwall_group, False):
                self.kill()

    # Coins class
    class coins(pygame.sprite.Sprite):
        # Define the constructor for the wall class
        def __init__(self, color, width, height, x, y):
            super().__init__()
            self.currentimage = 0 # The start variable for the array image
            self.image = Game.allcoinimages[self.currentimage]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            # Variables
            self.animationcounter = 0 # A counter used ot slow down the speed at which the coin spins
        def update(self):
            self.animate()

        def animate(self):
            # Updates the current image to the next image in the array (for animations) - if self.currentimage = 10, we restart the array from image number 0. It only does this every 6 ticks because otherwise it spins really (too) fast
            if self.animationcounter % 6 == 0:
                self.currentimage += 1
                if self.currentimage >= len(Game.allcoinimages):
                    self.currentimage = 0
                self.image = Game.allcoinimages[self.currentimage]
            self.animationcounter += 1
            
    # Game class
    class Game(object):
        def __init__(self):
            # CREATE GROUPS for each sprite here
            self.player_group = pygame.sprite.Group()
            self.allwall_group = pygame.sprite.Group()   # All wall group is a group including all inner and outer walls
            self.outerwall_group = pygame.sprite.Group()
            self.innerwall_group = pygame.sprite.Group()
            self.arenainnerwall_group = pygame.sprite.Group()
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

            # Loads all the images at the start of the game, instead of loading every image needed every tick which is very inefficient - we use captial "G" in "Game" because we are making a static variable, not an attribute of an object - I have only done this for the objects being animated as the other objects won't make a big difference
            # Create a sprite and fill it with a the image - we have an array as this allows for 'animations'
            Game.allcoinimages = [pygame.image.load('goldCoin1.PNG'),pygame.image.load('goldCoin2.PNG'),pygame.image.load('goldCoin3.PNG'),pygame.image.load('goldCoin4.PNG'),pygame.image.load('goldCoin5.PNG'),pygame.image.load('goldCoin6.PNG'),pygame.image.load('goldCoin7.PNG'),pygame.image.load('goldCoin8.PNG'),pygame.image.load('goldCoin9.PNG')]
            Game.spinleft = [pygame.image.load('barrel8.PNG'),pygame.image.load('barrel7.PNG'),pygame.image.load('barrel6.PNG'),pygame.image.load('barrel5.PNG'),pygame.image.load('barrel4.PNG'),pygame.image.load('barrel3.PNG'),pygame.image.load('barrel2.PNG'),pygame.image.load('barrel1.PNG'),pygame.image.load('barrel0.PNG')]
            Game.spinright = [pygame.image.load('barrel0.PNG'),pygame.image.load('barrel1.PNG'),pygame.image.load('barrel2.PNG'),pygame.image.load('barrel3.PNG'),pygame.image.load('barrel4.PNG'),pygame.image.load('barrel5.PNG'),pygame.image.load('barrel6.PNG'),pygame.image.load('barrel7.PNG'),pygame.image.load('barrel8.PNG')]
            Game.mariorunleft = [pygame.image.load('mario2nobgleft.PNG'),pygame.image.load('mario3nobgleft.PNG'),pygame.image.load('mario4nobgleft.PNG'),pygame.image.load('mario5nobgleft.PNG')]
            Game.mariorunright = [pygame.image.load('mario2nobg.PNG'),pygame.image.load('mario3nobg.PNG'),pygame.image.load('mario4nobg.PNG'),pygame.image.load('mario5nobg.PNG')]
            Game.arenamarioimages = [pygame.image.load('mariotopdownN.PNG'),pygame.image.load('mariotopdownE.PNG'),pygame.image.load('mariotopdownS.PNG'),pygame.image.load('mariotopdownW.PNG')]

            # Variables
            self.level = 1
            self.lives = 3 # We refer to the game for the lives of the player as this allows the lives to be continued from level to level - the lives do not reset back to 3 every time you go to the next level
            self.loadcoins()
            self.startposx = 0
            self.startposy = 0

            self.hammerspawned = False # Ensures only one hammer is spawned every three seconds
            self.endscreen = False # This is used to stop the barrels from spawning during the youlose screen and to stop previous text front being drawn again
            self.youlose = False
            self.youwin = False

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
                            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                            1,0,0,0,0,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,11,0,0,0,0,0,1,
                            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,0,0,0,0,1,
                            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,0,0,0,0,1,
                            1,0,0,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,11,11,0,0,0,0,0,0,0,0,1,
                            1,0,0,0,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,0,0,0,0,11,0,0,0,0,1,
                            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,0,0,0,0,1,
                            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,0,0,0,0,1,
                            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                            1,0,0,0,0,0,0,0,0,0,0,0,0,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,0,0,0,0,0,0,0,0,0,0,0,0,1,
                            1,0,0,0,0,0,0,0,0,0,0,0,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                            1,0,0,0,0,0,0,0,0,0,0,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,11,0,0,0,0,0,0,0,0,0,0,0,0,11,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                            1,0,0,0,0,0,0,0,0,0,0,0,0,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,11,11,0,0,0,0,0,0,0,0,0,0,0,0,1,
                            1,0,0,0,0,0,0,0,0,0,0,0,0,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                            1,0,0,0,0,0,0,0,0,0,0,0,0,11,0,0,0,0,0,0,0,0,0,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,11,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,11,0,0,1,
                            1,0,0,0,0,11,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,9,0,0,1,
                            1,0,0,0,0,0,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                            1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]


            # This list is used in the nextlevel() method
            # We have a 0 at index 0 to represent that there is nothing there, this is done because there is no level 0, levels start at 1, so the first map that can be iterated through is at index 1
            self.alllevels = [0,self.level1,self.level2,self.level3,self.level4,self.level5,self.level6,self.level7,self.level8,self.level9,self.level10]

            # Calls the method levelsetup() so to build the map - this is still in the __init__() function
            self.levelsetup()

        def loadcoins(self):
            # We get the variable "self.coins" from the file "coins.txt"
            self.coins = 0 # Initiates the variable
            # Try to read coins from a file
            try:
                coins_file = open("coins.txt", "r") # Reads the text file and saves it to the coins_file variable
                self.coins = int(coins_file.read()) # saves the number read from the text file to the coins variable
                coins_file.close() # closes the coins variable
            except:
                # If there is some kind of error, set the coins variable to 0
                self.coins = 0

        def update(self):
            self.spawnbarrels()
            self.spawnhammerpickup()

        def spawnbarrels(self):
            if (self.level < 10) and (self.endscreen == False):
                now = pygame.time.get_ticks()
                if now - self.start > 3000: # 3000 milliseconds is 3 seconds
                    self.myBarrel = barrel(BROWN, 19, 19, self.barrelspawncoordx, self.barrelspawncoordy)
                    # Add the barrel to a barrel group and an all sprites group
                    self.barrel_group.add(self.myBarrel)
                    self.moving_sprites_group.add(self.myBarrel)
                    self.all_sprites_group.add(self.myBarrel)
                    self.start = now
            
        def spawnhammerpickup(self):
            if self.level == 10:
                now = pygame.time.get_ticks()
                if now - self.starttimer > 5000: # 5000 milliseconds is 5 seconds
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
                            spawnhammerpickup = random.randint(0,1400) # There is a 1 in 1000 chance of a hammerpickup spawning at each empty "tile" in the map
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
            if self.level == 10:
                game.myDonkeykong.healthbar()
                game.myArenaplayer.healthbar()

            # Draws variables - lives, level, coins
            if self.endscreen == False:
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

            self.losescreen()
            self.winscreen()

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
                    self.startposx = temp_x
                    self.startposy = temp_y
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
                    self.myBarrel = barrel(BROWN, 19, 19, temp_x+10, temp_y+10) # The + values are to centre the barrels within that 40x40 block
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
                    self.myCoin = coins(GOLD,10,10,temp_x+4,temp_y+4) # The + values on the temp_x and temp_y are to centre and ensure the coin is on the ground (actually slightly off the ground because this makes it look cooler)
                    self.coin_group.add(self.myCoin)
                    self.background_group.add(self.myCoin)
                    self.all_sprites_group.add(self.myCoin)
                # 9s in the array represent the starting position of arena players - this is only used for level 10
                if self.levelselected[i] == 9:
                    self.myArenaplayer = arenaplayer(BLUE,40,40,temp_x,temp_y)
                    self.arenaplayer_group.add(self.myArenaplayer)
                    self.moving_sprites_group.add(self.myArenaplayer)
                    self.all_sprites_group.add(self.myArenaplayer)
                # 10s in the array represents the starting position of donkey kong - this is only used for level 10
                if self.levelselected[i] == 10:
                    self.myDonkeykong = donkeykong(DARKBROWN,80,80,temp_x,temp_y)
                    self.donkeykong_group.add(self.myDonkeykong)
                    self.moving_sprites_group.add(self.myDonkeykong)
                    self.all_sprites_group.add(self.myDonkeykong)
                # 11s in the array represents arenainnerwalls - only used in level 10
                if self.levelselected[i] == 11:
                    self.myArenainnerwall = arenainnerwall(RED,80,80,temp_x,temp_y)
                    self.arenainnerwall_group.add(self.myArenainnerwall)
                    self.allwall_group.add(self.myArenainnerwall)
                    self.background_group.add(self.myArenainnerwall)
                    self.all_sprites_group.add(self.myArenainnerwall)

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
        
        # The method for what happens when you die
        def losescreen(self):
            if self.youlose == True:
                self.endscreen = True
                # This get's rid of the current level's sprites
                for sprite in game.all_sprites_group:
                    sprite.kill()
                    
                screen.fill(BLACK) # Removes any written text (e.g. on-screen variables, healthbars, etc...)

                # Displays "GAME OVER" on the end screen - signifying you died
                font = pygame.font.Font('freesansbold.ttf', 80)
                text = font.render(("GAME OVER"), 1, WHITE)
                text_rect = text.get_rect(center=(960, 250))
                screen.blit(text, text_rect)

                # Displays "YOU LOSE" on the end screen below "GAME OVER" - signifying you died
                font = pygame.font.Font('freesansbold.ttf', 80)
                text = font.render(("YOU LOSE"), 1, WHITE)
                text_rect = text.get_rect(center=(960, 350))
                screen.blit(text, text_rect)

                # Displayes the player's coins in the endscreen
                font = pygame.font.Font('freesansbold.ttf', 30)
                text = font.render(("COINS: " + str(self.coins)), 1, WHITE)
                text_rect = text.get_rect(center=(960, 425))
                screen.blit(text, text_rect)

                button_1("MAIN MENU",840,475,250,60,WHITE,GREY,0,"M") # This button take you to the main menu
                # Save the new value for coins to the text file
                try:
                    # Write the file to disk
                    coins_file = open("coins.txt", "w")
                    coins_file.write(str(self.coins))
                    coins_file.close()
                except:
                    # Can't write it
                    print("Unable to save coins.")

                # Updates the screen
                pygame.display.flip()
        
        def winscreen(self):
            if self.youwin == True:
                self.endscreen = True
                # This get's rid of the current level's sprites
                for sprite in game.all_sprites_group:
                    sprite.kill()
                    
                screen.fill(BLACK) # Removes any written text (e.g. on-screen variables, healthbars, etc...)

                # Displays "GAME OVER" - signifying you died
                font = pygame.font.Font('freesansbold.ttf', 80)
                text = font.render(("GAME OVER"), 1, WHITE)
                text_rect = text.get_rect(center=(960, 250))
                screen.blit(text, text_rect)

                # Displays "YOU WIN" on the end screen below "GAME OVER" - signifying you died
                font = pygame.font.Font('freesansbold.ttf', 80)
                text = font.render(("YOU WIN"), 1, WHITE)
                text_rect = text.get_rect(center=(960, 350))
                screen.blit(text, text_rect)

                # Displayes the player's coins in the endscreen
                font = pygame.font.Font('freesansbold.ttf', 30)
                text = font.render(("COINS: " + str(self.coins)), 1, WHITE)
                text_rect = text.get_rect(center=(960, 425))
                screen.blit(text, text_rect)

                button_1("MAIN MENU",840,475,250,60,WHITE,GREY,0,"M") # This button take you to the main menu

                # Save the new value for coins to the text file
                try:
                    # Write the file to disk
                    coins_file = open("coins.txt", "w")
                    coins_file.write(str(self.coins))
                    coins_file.close()
                except:
                    # Can't write it
                    print("Unable to save coins.")
                
                # Updates the screen
                pygame.display.flip()

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

mainmenu() # Calls the main menu
# Close the window and quit.
pygame.quit()