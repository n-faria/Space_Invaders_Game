#Nick Faria
#Jun 17, 2018
#Space Invaders
#Re-create the space invaders game

import pygame, time, random, math #Imports

pygame.mixer.pre_init(44100, 16, 2, 4096) #Initialize music

pygame.init() #Initialize pygame

screen_width = 1280
screen_height = 960 #Variables for screen width and height

screen = pygame.display.set_mode([screen_width, screen_height]) #Create the display window/screen

pygame.display.set_caption("Space Invaders") #Set the caption of the display window

#Colours

black = (0, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

#Rgb values for all colours used

#Fonts

text = pygame.font.Font("orena.ttf", 75)
smallText = pygame.font.Font("space_invaders.ttf", 30)
#Font variables for the font used

#Music
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)
laser = pygame.mixer.Sound("laser.wav")
#Loads then plays theme music the whole time

#Classes###########################################################################################

class Player(pygame.sprite.Sprite): #Player Class

    def __init__(self): #Init function

        super().__init__()

        self.width = 80
        self.height = 48 #Variables for width and height
        
        self.image = pygame.transform.scale(pygame.image.load("player.png"), (self.width, self.height)) #Assign the image, correctly resized

        self.rect = self.image.get_rect() #Create a rectangle around the image to use for collision detection

        self.rect.centerx = screen_width/2 #Move the center x coordinate to the middle of the screen, ie starting position

        self.rect.y = screen_height - 100 #Move the y coordinate to the starting position

        self.speed = 5 #Variable for player speed
        
        self.dx = 0 #Variable for change in x value

        
        
    def update(self):

        self.rect.x += self.dx #Change the x coordinate by variable for change in x value

        if self.rect.right > screen_width: #If the right side of the player is past the right side of the screen
            self.rect.right = screen_width #Don't let them go past
        if self.rect.left < 0: #If the left side of the player is past the left side of the screen
            self.rect.left = 0 #Don't let them go past
        
        
class Alien(pygame.sprite.Sprite): #Alien class

    def __init__(self, row, column): #Init function

        super().__init__()

        self.width = 50 
        self.height = 50 #Variables for width and height

        self.row = row 
        self.column = column #Variables to keep track of the row and column of the aliens

        self.image = self.setImage() #Run the set image function to choose the image and set it

        self.rect = self.image.get_rect() #Create a rectangle around the image to use for collision detection

        self.speed = 1 #Variable for alien speed

        self.direction = 1 #Variable to keep track of direction the alien is going, switches between positive and negative
        
    def setImage(self): #Set image function

        if self.row%3 == 0:
            image = pygame.image.load("alien1.png")
        elif self.row%3 == 1:
            image = pygame.image.load("alien2.png")
        elif self.row%3 == 2:
            image = pygame.image.load("alien3.png")

        #Chooses a different image for every 3 rows
        
        image = pygame.transform.scale(image, (self.width, self.height)) #Resizes image to correct size

        return image

    def update(self, aliens):
        if self.rect.right > screen_width - 10 or self.rect.left < 10: #If they reach the edge of the screen
            changeDirection(aliens) #Run the change direction function

        self.rect.x += self.speed*self.direction #Change the alien's x-coordinate by the speed, taking into account which direction

class Bullet(pygame.sprite.Sprite): #Bullet Class

    def __init__(self, colour, direction, x, y): #Init function

        super().__init__()

        self.width = 5
        self.height = 10 #Variables for width and height
        
        self.colour = colour #Sets colour to colour passed in parameters
        self.image = pygame.Surface((self.width, self.height)) #Creates a surface for the image of the bullet
        self.image.fill(self.colour) #Fills that surface with a colour so it appears to have an image
        self.rect = self.image.get_rect() #Create a rectangle around the image to use for collision detection
        self.rect.centerx = x #Locate the center x-coordinate of the rectangle at the x coordinate passed in the parameter
        self.rect.centery = y #Locate the center y-coordinate of the rectangle at the y coordinate passed in the parameter
        self.direction = direction #Set the direction of the bullet (A positive or negative value) to the one passed in the parameter
        self.speed = self.direction*5 #Set the speed to 5, taking into account direction

    def update(self):
        
        self.rect.y -= self.speed #Change the y coordinate by the speed

        if self.rect.top > screen_height: 
            self.kill()
        if self.rect.bottom < 0:
            self.kill()
        #If the bullet gets to the top or bottom of the screen, destroy it
        
     
class Blocker(pygame.sprite.Sprite): #Blocker Class

    def __init__(self, row, column): #Init function

        super().__init__()

        self.width = 10
        self.height = 10 #Variables for width and height
        
        self.colour = green #Set the colour to green
        
        self.image = pygame.Surface((self.width, self.height)) #Creates a surface for the image of the blocker
        self.image.fill(self.colour) #Fills that surface with a colour so it appears to have an image
        self.rect = self.image.get_rect() #Create a rectangle around the image to use for collision detection
        self.row = row #Variable for the row of the blocker in the blocker pattern array
        self.column = column #Variable for the column of the blocker in the blocker pattern array
        
#Functions##########################################################################

def text_objects(text, font): #Function that helps with displaying text
    textSurface = font.render(text, True, black) #Creates a surface (image of text) in order to blit it on a surface, as just text on its own cannot be blitted
    return textSurface, textSurface.get_rect() #Returns the values of the surface

def shoot(aliens, bullets): #Function that chooses which alien shoots and creates the bullet

    columnList = [] #Create a list to put all of the columns of alive aliens
    for alien in aliens: #For every alive alien
        columnList.append(alien.column) #Add what column they are in to the column list

    columnList = set(columnList) 
    columnList = list(columnList) #Gets rid of all duplicates in the list - it can now choose a column to shoot from

    column = random.choice(columnList) #Chooses a random column to shoot from

    rowList = [] #Create a list to put all of the rows of alive aliens
    
    for alien in aliens: #For each alive alien
        if alien.column == column: #If that alien is in the previously selected column
            rowList.append(alien.row) #Add it to the row list
    row = max(rowList) #Find the largest value in the row list, that is the bottom most row of that column, and the alien that will be shooting

    for alien in aliens: #For each alive alien
        if alien.column == column and alien.row == row: #If it is the alien that is shooting
            bullet = Bullet(white, -1, alien.rect.centerx, alien.rect.centery + alien.height) #Create the bullet right below the alien
            bullets.add(bullet) #Add it to the bullets sprite group

def changeDirection (aliens): #Method that changes the direction of the aliens

    for alien in aliens: #For each alien still alive
        alien.direction *= -1 #Reverse the direction its traveling
        alien.rect.y += alien.height/2 #Move the alien down slightly
        alien.rect.x += alien.speed*alien.direction #Update the alien's x-coordinate in the correct direction

def makeBlocker(number): #Method that makes the big blocker out of all of the little pixels
    blockerGroup = pygame.sprite.Group() #Create a group for all the blocker sprites

    for row in range(10): 
        for column in range(14): #10 by 14 grid of blockers
            blocker = Blocker(row, column) #Create a blocker at each possible row/column location using blocker class
            blocker.rect.x = 150 + (blocker.width*column) + (280*(number-1)) 
            blocker.rect.y = 700 + (blocker.height*row) #Set the blockers x and y coordinates corresponding to its position in the grid
            blockerGroup.add(blocker) #Add it to the group of blocker sprites

    blockerArray = [ [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                     [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    ]
    #Array to illustrate the design of a blocker
    
    for blocker in blockerGroup: #For each pixel in the blocker sprite group
        if blockerArray[blocker.row][blocker.column] == 0: #If in the design, it shouldn't actually be there (one was added in every location at the beginning):
            blocker.kill() #Destroy the sprite, so it will not be drawn
    return blockerGroup #return the newly updated sprite group
    
def makeAliens(rows, columns): #Method to handle positioning all the aliens to draw on screen, passes # of rows and columns of aliens
    aliens = pygame.sprite.Group() #Create a group for all the alien sprites

    for row in range(rows):
        for column in range(columns): #For each alien in the row/column grid
            alien = Alien(row, column) #Create an alien using the alien class
            alien.rect.x = 165 + ((column)*(2*alien.width))
            alien.rect.y = 100 + (row*(1.5*alien.height)) #Set the aliens x and y coordinates corresponding to location regarding grid
            aliens.add(alien) #Add the alien to the aliens sprite group
    return aliens #Return the sprite group

#Screens#########################################################################

def introScreen(): #Method for running the menu screen

    Exit = False #Create a variable to check in the while loop
    
    while not Exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Exit = True
                #If pygame is closed, exit the loop and pygame quits later

        buttonWidth = 500
        buttonHeight = 100 #Variables for button width and height
        
        screen.fill(black) #Fill the screen with the background colour
   
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #get the mouse position and see if the mouse is being pressed

        screen.blit(pygame.transform.scale(pygame.image.load("logo.jpg"), (440, 130)), (screen_width/2 - 220, 100))
        screen.blit(pygame.transform.scale(pygame.image.load("ships.png"), (300, 100)), (screen_width/2 - 150, 250)) #Images for decoration
        
        #Draw play button, when hovered over highlight border, when clicked run the game loop
        if  screen_width/2 + buttonWidth/2 > mouse[0] > screen_width/2 - buttonWidth/2 and 450 > mouse[1] > 350:
            pygame.draw.rect(screen, green, [screen_width/2 - buttonWidth/2, 350, buttonWidth, buttonHeight], 0)
            pygame.draw.rect(screen, white, [screen_width/2 - buttonWidth/2, 350, buttonWidth, buttonHeight], 5)
            if click[0] == 1:
                gameLoop()
        else:
            pygame.draw.rect(screen, green, [screen_width/2 - buttonWidth/2, 350, buttonWidth, buttonHeight], 0)
            pygame.draw.rect(screen, black, [screen_width/2 - buttonWidth/2, 350, buttonWidth, buttonHeight], 5)

        #Draw help button, when hovered over highlight border, when clicked go to instructions page
        if screen_width/2 + buttonWidth/2 > mouse[0] > screen_width/2 - buttonWidth/2 and 600 > mouse[1] > 500:
            pygame.draw.rect(screen, green, [screen_width/2 - buttonWidth/2, 500, buttonWidth, buttonHeight], 0)
            pygame.draw.rect(screen, white, [screen_width/2 - buttonWidth/2, 500, buttonWidth, buttonHeight], 5)
            if click[0] == 1:
                pygame.event.pump()
                instructionsScreen()
        else:
            pygame.draw.rect(screen, green, [screen_width/2 - buttonWidth/2, 500, buttonWidth, buttonHeight], 0)
            pygame.draw.rect(screen, black, [screen_width/2 - buttonWidth/2, 500, buttonWidth, buttonHeight], 5)

        #Draw quit button, when hovered over highlight border, when clicked quit the game
        if screen_width/2 + buttonWidth/2 > mouse[0] > screen_width/2 - buttonWidth/2 and 750 > mouse[1] > 650:
            pygame.draw.rect(screen, green, [screen_width/2 - buttonWidth/2, 650, buttonWidth, buttonHeight], 0)
            pygame.draw.rect(screen, white, [screen_width/2 - buttonWidth/2, 650, buttonWidth, buttonHeight], 5)
            if click[0] == 1:
                Exit = True
        else:
            pygame.draw.rect(screen, green, [screen_width/2 - buttonWidth/2, 650, buttonWidth, buttonHeight], 0)
            pygame.draw.rect(screen, black, [screen_width/2 - buttonWidth/2, 650, buttonWidth, buttonHeight], 5)

        textSurf, textRect = text_objects("Play", text)
        textRect.center = (screen_width/2, 400)
        screen.blit(textSurf, textRect) #Creates the play text and blits it to the screen

        textSurf, textRect = text_objects("Help", text)
        textRect.center = (screen_width/2, 550)
        screen.blit(textSurf, textRect) #Creates the instructions text and blits it too the screen

        textSurf, textRect = text_objects("Quit", text)
        textRect.center = (screen_width/2, 700)
        screen.blit(textSurf, textRect) #Creates the quit text and blits it to the screen
        
        pygame.display.update() #Updates the pygame display
    pygame.quit() #If quit was pressed, it will go here and quit pygame
    
def loseScreen(score):

    Exit = False #Create a variable to check in the while loop
    
    while not Exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Exit = True
                #If pygame is closed, exit the loop and pygame quits later

        screen.fill(black) #Fill the screen with the background colour
        
        screen.blit(pygame.transform.scale(pygame.image.load("logo.jpg"), (440, 130)), (screen_width/2 - 220, 700))
        screen.blit(pygame.transform.scale(pygame.image.load("ships.png"), (300, 100)), (screen_width/2 - 150, 150)) #Images for decoration
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #get the mouse position and see if the mouse is being pressed

        pygame.draw.rect(screen, green, [screen_width/2 - 250, 250, 500, 200], 0)
        pygame.draw.rect(screen, black, [screen_width/2 - 250, 250, 500, 200], 5)
        #Draw the center rectangle where the score is displayed

        buttonWidth = 200
        gap = 50
        #Draw retry button, when hovered over change colour slightly, when clicked restart the game loop
        if screen_width/2 - gap > mouse[0] > screen_width/2 - (buttonWidth + gap) and 600 > mouse[1] > 500:
            pygame.draw.rect(screen, green, [screen_width/2 - buttonWidth - gap, 500, 200, 100], 0)
            pygame.draw.rect(screen, white, [screen_width/2 - buttonWidth - gap, 500, 200, 100], 5)
            if click[0] == 1:
                gameLoop()
        else:
            pygame.draw.rect(screen, green, [screen_width/2 - buttonWidth - gap, 500, 200, 100], 0)
            pygame.draw.rect(screen, black, [screen_width/2 - buttonWidth - gap, 500, 200, 100], 5)

        #Draw quit button, when hovered over change colour slightly, when clicked quit the game
        if screen_width/2 + buttonWidth + gap > mouse[0] > screen_width/2 + gap and 600 > mouse[1] > 500:
            pygame.draw.rect(screen, green, [screen_width/2 + gap, 500, 200, 100], 0)
            pygame.draw.rect(screen, white, [screen_width/2 + gap, 500, 200, 100], 5)
            if click[0] == 1:
                Exit = True
        else:
            pygame.draw.rect(screen, green, [screen_width/2 + gap, 500, 200, 100], 0)
            pygame.draw.rect(screen, black, [screen_width/2 + gap, 500, 200, 100], 5)
            

        textSurf, textRect = text_objects("Retry", smallText)
        textRect.center = (screen_width/2 - 150, 550)
        screen.blit(textSurf, textRect) #Creates the retry text and blits it to the screen

        textSurf, textRect = text_objects("Quit", smallText)
        textRect.center = (screen_width/2 + 150, 550)
        screen.blit(textSurf, textRect) #Creates the quit text and blits it to the screen

        scoreMessage = ("Score: " + str(score))
        textSurf, textRect = text_objects(scoreMessage, smallText)
        textRect.center = (screen_width/2, 350)
        screen.blit(textSurf, textRect) #Creates the 'Score: _' text and blits it too the screen

        pygame.display.update() #Updates the pygame display
    pygame.quit()


def instructionsScreen():
    Exit = False #Create a variable to check in the while loop
    
    while not Exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Exit = True
                #If pygame is closed, exit the loop and pygame quits later

        screen.fill(black) #Fill the screen with the background colour
        
        screen.blit(pygame.transform.scale(pygame.image.load("logo.jpg"), (440, 130)), (screen_width/2 - 220, 525))
        screen.blit(pygame.transform.scale(pygame.image.load("ships.png"), (300, 100)), (screen_width/2 - 150, 150)) #Images for decoration
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #get the mouse position and see if the mouse is being pressed

        pygame.draw.rect(screen, green, [screen_width/2 - 250, 250, 500, 200], 0)
        pygame.draw.rect(screen, black, [screen_width/2 - 250, 250, 500, 200], 5)
        #Draw the center rectangle where the score is displayed

        buttonWidth = 350
        gap = 50
        #Draw back button, when hovered over change colour slightly, when clicked go back to intro screen
        if screen_width/2 + buttonWidth/2 > mouse[0] > screen_width/2 - buttonWidth/2 and 850 > mouse[1] > 750:
            pygame.draw.rect(screen, green, [screen_width/2 - buttonWidth/2, 750, buttonWidth, 100], 0)
            pygame.draw.rect(screen, white, [screen_width/2 - buttonWidth/2, 750, buttonWidth, 100], 5)
            if click[0] == 1:
                pygame.event.pump()
                introScreen()
        else:
            pygame.draw.rect(screen, green, [screen_width/2 - buttonWidth/2, 750, buttonWidth, 100], 0)
            pygame.draw.rect(screen, black, [screen_width/2 - buttonWidth/2, 750, buttonWidth, 100], 5)
            


        textSurf, textRect = text_objects("Back", smallText)
        textRect.center = (screen_width/2, 800)
        screen.blit(textSurf, textRect)
        #Creates back button text
        
        textSurf, textRect = text_objects("Space...........................shoot", smallText)
        textRect.center = (screen_width/2, 400)
        screen.blit(textSurf, textRect)

        textSurf, textRect = text_objects("Right Arrow.......Go Right", smallText)
        textRect.center = (screen_width/2, 350)
        screen.blit(textSurf, textRect)

        textSurf, textRect = text_objects("Left Arrow...........Go Left", smallText)
        textRect.center = (screen_width/2, 300)
        screen.blit(textSurf, textRect)
        
        #Create the controls text and blit them to the screen (last 3 blocks)
        
        pygame.display.update() #Updates the pygame display
    pygame.quit()




#################################################################################
#Gameloop

def gameLoop():
    running = True #Variable for while loop condition

    score = 0 #Create a variable for the score
    
    player = Player() #Create the player
    level = 1 #Set the level to 1
    blockers = pygame.sprite.Group() #Group for blockers sprites
    aliens = makeAliens(2 + level, 10) #Create group for alien sprites using makeAliens method

    for i in range(1, 5, 1): #Make 4 blockers and add them to the blockers sprite group
        blockers.add(makeBlocker(i))

    bullets = pygame.sprite.Group() #Create a sprite group for bullets

    while running: #Actual loop

        screen.fill(black) #Fill the screen black
        pygame.draw.rect(screen, green, [screen_width - 280, 0, 280, 50], 0)
        #pygame.draw.rect(screen, white, [screen_width/2 - 140, 0, 280, 50], 5)
        textSurf, textRect = text_objects("Score: " + str(score), smallText)
        textRect.center = (screen_width - 140, 25)
        screen.blit(textSurf, textRect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False #If the window is closed, stop running the game loop

            if event.type == pygame.KEYDOWN: #If a key is pressed down

                if event.key == pygame.K_RIGHT: #If that key is right
                    player.dx += player.speed #Move the player right according to player speed
                if event.key == pygame.K_LEFT: #If the key is left
                    player.dx -= player.speed #Move the player left according to player speed
                if event.key == pygame.K_SPACE: #If the key is space
                    bullet = Bullet(green, 1, player.rect.centerx, player.rect.centery - player.height) #Create a bullet shot from the player
                    bullets.add(bullet) #Add it to bullets sprite group
                    laser.play()
                    
            if event.type == pygame.KEYUP: #If a key is released

                if event.key == pygame.K_RIGHT: #If that key is right
                    player.dx -= player.speed #Stop player movement
                if event.key == pygame.K_LEFT: #If that key is left
                    player.dx += player.speed #Stop player movement
        pygame.event.pump() #Clear events so they do not pile up, lets it run smoother

        if aliens.sprites() == []: #If there are no aliens left
            level +=1 #Next level
            screen.fill(black) #Clear screen
            aliens = makeAliens(2 + level, 10) #Next level creates aliens with 1 more row
        
        if pygame.time.get_ticks() % 100 == 0 and aliens.sprites() != []: #If it has been 200 ms and there are still aliens left
            shoot(aliens, bullets) #An alien shoots
            laser.play()

        hitList = pygame.sprite.groupcollide(bullets, aliens, True, True) #Collision detection between aliens and bullets: If a bullet hits an alien, destroy bullet and alien

        if hitList != []:
            score += len(hitList)*100
        
        pygame.sprite.groupcollide(bullets, blockers, True, True) #Collision detection between blockers and bullets: If a bullet hits a blocker, destroy bullet and blocker pixel

        collisionList = pygame.sprite.spritecollide(player, bullets, True) #Check for collision between player and a bullet
        
        if collisionList != []: #If there is a collision
            loseScreen(score) #Go to the losing screen
            break
        
        aliens.update(aliens) #Update alien sprite group
        bullets.update() #Update bullet sprite group
        for alien in aliens: 
            if alien.rect.bottom  >= player.rect.top: #If any alien has reached the player's y position
                loseScreen(score) #Go to the losing screen
                break #Break game loop
        
        player.update() #Update the player 
        screen.blit(player.image, player.rect) #Draw the player
        blockers.draw(screen) #Draw blockers
        aliens.draw(screen) #Draw aliens
        bullets.draw(screen) #Draw bullets
        pygame.display.flip() #Update display
    pygame.quit() #If loop is broken (ie they quit), quit 

#main
introScreen() #Start the game by running intro screen method 
