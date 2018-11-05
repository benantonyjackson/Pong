import sys, pygame, time

#Keeps a number between two specified values
def clamp(num, min, max):
    if num < min:
        return min
    if num > max:
        return max
    return num

#Class which draws text, text will be centred around the x and y values
class Text:
    pygame.font.init()
    text = ""
    font = None
    x = 0
    y = 0
    r = 255
    g = 255
    b = 255


    def __init__(self, text, x, y, fontSize):
        self.text = text
        self.font = pygame.font.Font("SFSquareHead.ttf", fontSize)
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.font.render(self.text, False, (self.r, self.g, self.b)), (self.x - (self.font.size(self.text)[0] / 2), self.y -(self.font.size(self.text)[1] / 2)))


#Class for an on screen countdown
class Countdown:
    pygame.font.init()
    font = None
    #Stores the currnet time
    time = "3"
    #Stores the number of milliseconds that have passed in the current second
    timePassed = 0
    #Stores the position of the timer
    pause = False
    x=0
    y=0
    
    #Constructor, called when an object of countdown is created
    def __init__(self, time, x, y, fontSize):
        #Initialises variables
        self.time = time
        self.font = pygame.font.Font("SFSquareHead.ttf", fontSize)
        self.x = x
        self.y = y
    #Tick function, called everytime the game loop is run
    def tick(self, deltaTime):
        if self.pause == False:
                
            #Adds the time that paseed since the last frame was called
            self.timePassed += deltaTime
            #If a second has passed
            if self.timePassed >= 1000:
                #Take one second away from time passed 
                self.timePassed -= 1000
                #Set the time to one second less than what it previously was
                self.time = str(int(self.time) - 1)
        
    #Draws the count down timer to the screen
    def draw(self, screen):
        screen.blit(self.font.render(self.time, False, (255, 255, 255)), (self.x - (self.font.size(self.time)[0] / 2), abs(self.y -(self.font.size(self.time)[1] / 2))))

    def reset(self, time):
        self.time = time
        
#Child class of Countdown that can change the state of the game
class MidRoundCounter(Countdown):
    def tick(self, deltaTime):
        #Calls the tick function of the parent class to handle time messurement
        super().tick(deltaTime)
        #Changes the state of the game when the countdown reaches 0
        if self.time == "0":
            return "playing"
        return "midround"

#Class that allows the user to enter text
class TextEntry:
    text = Text("", 1280/2, 720/2, 40)
    
    def keyPressed(self, e):
        #If the user pressed backspace, remove a character
        if e.unicode == "\b":
            self.text.text = self.text.text[:-1]
        #If the user presses enter, add a new line
        elif e.unicode == "\r":
            self.text.text += "\n"
        else:
            #Add the character the user pressed
            self.text.text += e.unicode
        
    #Draws characters the user has entered
    def draw(self, screen):
        self.text.draw(screen)

#Class for the scoreboard
class Scoreboard:
    pygame.font.init()
    #Stores the font for the scoreboard
    font = pygame.font.Font("SFSquareHead.ttf", 16)
    #Stores the players score
    scores = {"pl1" : "0",
              "pl2": "0"}
    #Creates a countdown object
    timer = Countdown("60" ,640, 40, 20)
    

    def tick(self, deltaTime):
       
        self.timer.tick(deltaTime)
        
    #Draws the scoreboard
    def draw(self, screen):
        text = self.scores["pl1"] + " | " + self.scores["pl2"]
        screen.blit(self.font.render(text, False,(255,255,255)), (640 - (self.font.size(text)[0] / 2),10))
        self.timer.draw(screen)

    def goal(self, player):
        self.scores[player] = str(int(self.scores[player]) + 1)

#Class for the ball
class Ball:
    #pygame rectangle for the position and size of the ball
    rect = pygame.Rect(640, 360, 10, 10)
    #Stores the movement value of the ball
    volx = float(1)
    voly = float(0)
    #Stores the pygame rect objects of the players
    playerRect = []

    def __init__(self, pl1, pl2):
        #Stores the players rectangles for collision detection
        self.playerRect.append(pl1)
        self.playerRect.append(pl2)
        
    #Draws the ball
    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color(255,255,255), self.rect)
    #Resets the ball
    def reset(self):
        self.rect = pygame.Rect(640, 360, 10, 10)
        self.voly = 0

    #Tick function, called every time a frame is drawn
    def tick(self, deltaTime):
        #Checks if the ball is in any players goal and returns the name of the player that scored if a goal has been scored
        if self.rect.left <= 0:
            return "pl2"
        if self.rect.left >= 1270:
            return "pl1"
        
        #Makes the ball bounce when it hits the edge of the screen
        if self.rect.top <= 0:
            self.voly = float(abs(self.voly))
        elif self.rect.top >= 710:
            self.voly = float(-abs(self.voly))

        

        #Checks if the ball has bounced off of any of the paddles
        for i in range (0, len(self.playerRect)):
            if self.playerRect[i].colliderect(self.rect):

                if self.volx < 0:
                    self.rect.left = self.playerRect[i].left + 10
                else:
                    self.rect.left = self.playerRect[i].left - 10
                
                self.volx = -(self.volx)
                
                

                self.voly = float(((self.rect.top - self.playerRect[i].top) / 100 - 0.5))    

        #Moves the ball
        self.rect.left += (self.volx * deltaTime)
        self.rect.top += (self.voly * deltaTime)
        
        
        return ""
        

    
#Class for the paddles
class Paddle:
    rect = pygame.Rect(10, 290, 10, 100)
    voly=0
    #Called every time the game loop is run
    def tick(self, deltaTime):
        #Moves the paddle up or down depending on the key pressed
        if pygame.key.get_pressed()[pygame.K_w]:
           self.voly = -1 * deltaTime
        if pygame.key.get_pressed()[pygame.K_s]:
           self.voly = 1 * deltaTime
        #Moves the paddle accordingly
        self.rect.top += self.voly
        #stops the paddle from leaving the screen
        self.rect.top = clamp(self.rect.top, 0, 620)
        #Resets the movement value
        self.voly = 0
        
       
    #Draws the paddle on the screen
    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color(255,255,255), self.rect)
    #Called to reset the position of the paddle when a goal is scored
    def initPos():
        self.rect.top = 590

    def setPosition(self, x, y):
        self.rect.top = y
        self.rect.left = x

#An AI class to act as an opponent
class AI(Paddle):
    #Sets the position of the paddle
    def __init__(self):
        self.rect = pygame.Rect(1260, 290, 10, 100)
        
    #Tick function, called everytime the gameloop is run
    def tick(self, deltaTime, ball):
        ballRect = ball.rect
        
        if ballRect.left > 1000 and ball.volx > 0:
            #Follows the balls y position
            if ballRect.top > self.rect.top:
                self.voly = 1
            elif ballRect.top < self.rect.top:
                self.voly=-1
            else:
                self.voly = 0
            
        
            self.rect.top += self.voly * deltaTime

        self.rect.top = clamp(self.rect.top, 0, 620)

#Class that displays the leaderboard
class Leaderboard:
    #Stores the text object for each leaderboard entry
    scores = []
    def __init__(self, leaderBoardStrings, currentUser, gameWon):
        #x and y value for the first entry on the leaderboard
        x,y = 640, 750
        #Loops through each leaderboard entry
        for i in range(0, len(leaderBoardStrings)):
            #Adds a new text object to the list for the current leaderboard entry
           self.scores.append(Text(leaderBoardStrings[i], x, y, 40))
           #Sets the y value of the next leaderboard entry to be lower than the current one
           y+=40
        #Sets the colour of the current players leaderboard entry to blue
        self.scores[currentUser].g = 0
        self.scores[currentUser].r = 0
        y += 700
        if gameWon == True:
            self.scores.append(Text("You win!", x, y, 30))
        else:
            self.scores.append(Text("You lose", x, y, 30))
            

    #Makes the leaderboard scroll up
    def tick(self, deltaTime):
        for i in range(0, len(scores) + 1):
            self.scores[i].y -= 0.25 * deltaTime
        self.scores[-1].y = clamp(self.scores[-1].y , 360, 100000000)

    #Draws the leaderboard
    def draw(self, screen):
        for i in range(0, len(scores) + 1):
            self.scores[i].draw(screen)
        
        
    
def resetRound():
    ball.reset()
    player1.setPosition(10, 290)
    player2.setPosition(1260, 290)

def drawComponents():
    player1.draw(screen)
    player2.draw(screen)
    scoreboard.draw(screen)

#Parses a single leaderboard entry and return there score minus the opponents score
def calcScore(score):
    return  int(score.split(" ")[-1].split("|")[0]) - int(score.split(" ")[-1].split("|")[1][0:-1])

def updateLeaderboard(score):
    currentUser = 0
    #Opens file
    file = open("Leaderboard.txt", "r+")
    #Stores each line in the updated file
    allScores = []
    #Reads first line
    temp = file.readline()
    i = 0
    while temp != "":
        #If the current user has not yet been inseted
        #and if the users score is higher than the score stored on the current line
        if score != "written" and calcScore(temp) < calcScore(score):
            #Add the current users leaderboard entry to the updated file
            allScores.append(score)
            #Rouge value which indicates that the current users leaderboard entry has been written
            score = "written"
            #Stores the index of the current user
            currentUser = i
        #Adds the current user to the updated file
        allScores.append(temp)
        #Reads the next line
        temp = file.readline()
        i += 1

    #If the current users leaderboard entry has not yet been added to the file
    if score != "written":
        #Add the current users leaderboard entry to the updated file
        allScores.append(score)
        #Stores the index of the current user
        currentUser = i
        
    i = 0

    file.close()
    #Opens file in write mode, this clears the contents of the file
    file = open("Leaderboard.txt", "w")
    #Writes the updated leaderboard to a textfile
    while i <= len(allScores) - 1:
        file.write(allScores[i])
        i += 1 
    file.close()

    return allScores, currentUser

#Starts pygame
pygame.init()

#Defines the size of the screen
size = width, height = 1280, 720
#Creates the screen
screen = pygame.display.set_mode(size)
#Creates a paddle object for the player
player1 = Paddle()
#Creates an opponent
player2 = AI()
#Creates a ball object
ball = Ball(player1.rect, player2.rect)
#Creates a scoreboard object
scoreboard = Scoreboard()
#Creates a clock to record delta time
clock = pygame.time.Clock()
#Stores the state of the game
state = "midround"
#Creates a coundown object which will display a countdown before a round starts 
midRoundTimer = MidRoundCounter("3", 640, 360, 30)
winner = ""
overtime = False
endScreenText = Text("Enter your name:", 640, 320, 30)
testTextEntry = TextEntry()


#Game loop
#Checks for user input and events, then changes the state of objects, then updates the screen
while 1:
    #Makes the background of the screen black
    screen.fill(pygame.Color(0,0,0))
    #Polls for events
    e = pygame.event.poll()
    
    #Ends the game if the player closes the window
    if e.type == pygame.QUIT:
        break
    elif e.type == pygame.KEYDOWN:
        if state == "enter name":
            if e.unicode == "\r":
                gameWon = 0 < calcScore(testTextEntry.text.text + " " + scoreboard.scores["pl1"] + "|" + scoreboard.scores["pl2"] + "\n")
                scores, currentUser = updateLeaderboard(testTextEntry.text.text + " " + scoreboard.scores["pl1"] + "|" + scoreboard.scores["pl2"] + "\n")
                leaderboard = Leaderboard(scores, currentUser, gameWon)
                state = "leaderboard"
            else:
                testTextEntry.keyPressed(e)
            
                
    #Records the time between the last frame and current frame being drawn in milliseconds
    deltaTime = clock.tick(199)
    if state == "playing":
        
        ball.draw(screen)
        drawComponents()
        
        player1.tick(deltaTime)
        player2.tick(deltaTime, ball)
        scr = ball.tick(deltaTime)
        
        
        if scr != "":
            scoreboard.goal(scr)
            if overtime == True:
                state = "enter name"
            else:
                state = "midround"
            
            resetRound()
        scoreboard.tick(deltaTime)


        if scoreboard.timer.time == "0":
            scoreboard.timer.pause = True

            if scoreboard.scores["pl1"] == scoreboard.scores["pl2"]:
                overtime = True
                scoreboard.timer.time = "Overtime"
                resetRound()
                state = "midround"
                
            else:
                state = "enter name"
    elif state == "midround":
        drawComponents()
        state = midRoundTimer.tick(deltaTime)
        midRoundTimer.draw(screen)
        if state == "playing":
            midRoundTimer.reset("3")
    elif state == "enter name":
        endScreenText.draw(screen)
        testTextEntry.draw(screen)
    elif state == "leaderboard":
        leaderboard.tick(deltaTime)
        leaderboard.draw(screen)
        if leaderboard.scores[-2].y < -1500:
            break
        
    #Updates the screen
    pygame.display.flip()
    
#Quits the game when the game loop is exited    
pygame.quit()
