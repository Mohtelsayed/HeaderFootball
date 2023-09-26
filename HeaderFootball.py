#    Name      : Mohamed Elsayed
#    AndrewID  : mtelsaye

#    File Created: 3/11/22
import os, pygame, time, math, socket, chatCommClass

class BALL:
    def __init__(b,scrWidth, scrHeight):
        b.Vx = 0.00000001
        b.Vy = -6
        b.Ay = 0.2
        b.Ax = 0
        b.kEyCoe = 0.35
        b.kExCoe = 0.90
        b.image = pygame.image.load(
        os.path.join("Assets", "football.png"))
        b.ballWandH = int((0.7/21.6)*scrWidth)
        b.image = pygame.transform.scale(b.image, (b.ballWandH,b.ballWandH))
        b.pushed = False
        b.rect = pygame.Rect(scrWidth//2 - b.ballWandH//2, 132, b.ballWandH, b.ballWandH)
        b.tick = 0
        b.rotRate = 0
        b.rotDirection = None
        b.leftGoalRect = pygame.Rect(0,450,55,30)
        b.rightGoalRect = pygame.Rect(scrWidth - 55,450,55,30)
        b.tempTick = -500
        b.goal1Event = pygame.USEREVENT + 1
        b.goal2Event = pygame.USEREVENT + 2
        

    def normalMove(b, scrWidth, scrHeight):
        prevVy = b.Vy
        b.Vy += b.Ay
        b.Vx += b.Ax
        b.rect.y += int(b.Vy)
        if abs(b.Vx) > 15:
            if b.Vx < 0:
                b.Vx = -15
            else:
                b.Vx = 15
                
        b.rect.x += int(b.Vx)
        b.tick += 1
        b.midx = b.rect.x + b.ballWandH//2
        b.midy = b.rect.y + b.ballWandH//2
        b.leftCrossBarHit = b.rect.colliderect(b.leftGoalRect)
        b.rightCrossBarHit = b.rect.colliderect(b.rightGoalRect)
        b.smallestNumIndexes = []
        
        if b.leftCrossBarHit or b.rightCrossBarHit:
            b.smallestNumIndexes = b.handleCrossbarCollision()

        if (b.rect.bottom + 135 >= scrHeight or 2 in b.smallestNumIndexes)\
        and prevVy >= 0:
            if b.Vy - -1 * math.sqrt(b.kEyCoe*(b.Vy**2)) > 2:
                BOUNCE_SOUND.play()
            b.Vy = -1 * math.sqrt(b.kEyCoe*(b.Vy**2))
            if b.Vx < 0:
                b.Vx = math.sqrt(b.kExCoe*(b.Vx**2))
                b.Vx *= -1
                b.rotDirection = "ANTI"
            else:
                b.Vx = math.sqrt(b.kExCoe*(b.Vx**2))
                b.rotDirection = "CLOCKWISE"
            if 2 in b.smallestNumIndexes and b.rect.x < 500 and int(b.Vx) == 0:
                b.rotDirection = "CLOCKWISE"
                b.Vx += 0.1
            elif 2 in b.smallestNumIndexes and b.rect.x > 500 and int(b.Vx) == 0:
                b.rotDirection = "ANTI"
                b.Vx -= 0.1
            b.rotRate = 10/abs(b.Vx) + 1.75
            
        if (b.rect.top < 0 or 3 in b.smallestNumIndexes) and b.Vy < 0:
            BOUNCE_SOUND.play()
            b.Vy *= -1
            if b.Vx < 0:
                b.rotDirection = "CLOCKWISE"
            else:
                b.rotDirection = "ANTI"
            b.rotRate -= 0.5
            
        if (b.rect.right > scrWidth or 1 in b.smallestNumIndexes) and b.Vx > 0:
            BOUNCE_SOUND.play()
            b.tempTick = b.tick
            b.Vx *= -1
            if b.Vy < 0:
                b.rotDirection = "CLOCKWISE"
            else:
                b.rotDirection = "ANTI"
            b.rotRate -= 1

        
                
        if (b.rect.left < 0 or 0 in b.smallestNumIndexes) and b.Vx < 0:
            BOUNCE_SOUND.play()
            b.tempTick = b.tick
            b.Vx *= -1
            if b.Vy < 0:
                b.rotDirection = "ANTI"
            else:
                b.rotDirection = "CLOCKWISE"
            b.rotRate -= 1
                
        if round(b.rotRate) != 0 and b.tick%round(b.rotRate) == 0:
            if b.rotDirection == "CLOCKWISE":
                b.image = pygame.transform.rotate(b.image, -90)
            elif b.rotDirection == "ANTI":
                b.image = pygame.transform.rotate(b.image, 90)

        if b.rect.top > 486 and (b.rect.right < 55 or b.rect.left > scrWidth - 55):
            if b.rect.right < 55:
                pygame.event.post(pygame.event.Event(b.goal1Event))
            elif b.rect.left > scrWidth - 55:
                pygame.event.post(pygame.event.Event(b.goal2Event))

    def handleCrossbarCollision(b):
        if b.leftCrossBarHit:
            rightSide = abs(b.leftGoalRect.right -  b.rect.left)
            leftSide = abs(b.leftGoalRect.left -  b.rect.right)
            topSide = abs(b.leftGoalRect.top - b.rect.bottom)
            bottomSide = abs(b.leftGoalRect.bottom - b.rect.top)
        else:
            rightSide = abs(b.rightGoalRect.right -  b.rect.left)
            leftSide = abs(b.rightGoalRect.left -  b.rect.right)
            topSide = abs(b.rightGoalRect.top - b.rect.bottom)
            bottomSide = abs(b.rightGoalRect.bottom - b.rect.top)
        
        sideArray = [rightSide, leftSide, topSide, bottomSide]
        smallestNumIndexes = [sideArray.index(min(sideArray))]
        for side in sideArray:
            if sideArray.index(side) != smallestNumIndexes[0] and abs(smallestNumIndexes[0] - side) < 18:
                smallestNumIndexes.append(sideArray.index(side))
        return smallestNumIndexes
            
class CHARACTER:
    def __init__(c, scrWidth, scrHeight, characterImage, Goals = 0):
        c.rect = 0
        c.tick = 0
        c.jumping = False
        c.Ay = 0.2
        c.Vy = 0
        c.goals = Goals
        c.tempTick = -500
        c.tempTickKick = 0
        c.kicking = False
        c.Freeze = False
        c.directionX = "None"
    
    def handleBallCollision(c,b, scrWidth, scrHeight):
        rightSide = abs(c.rect.right -  b.rect.left)
        leftSide = abs(c.rect.left -  b.rect.right)
        topSide = abs(c.rect.top - b.rect.bottom)
        bottomSide = abs(c.rect.bottom - b.rect.top)
        sideArray = [rightSide, leftSide, topSide, bottomSide+30]
        smallestNumIndexes = [sideArray.index(min(sideArray))]
        for side in sideArray:
            if sideArray.index(side) != smallestNumIndexes[0] and abs(smallestNumIndexes[0] - side) < 30:
                smallestNumIndexes.append(sideArray.index(side))
                
        if 0 in smallestNumIndexes:
            if b.Vx < 0:
                BOUNCE_SOUND.play()
                b.Vx *= -1
            if c.directionX == "Right":
                if b.rect.bottom + 135 >= scrHeight:
                    b.Vx += 4
                else:
                    b.Vx += 2
            if b.Vy < 0:
                b.rotDirection = "ANTI"
            else:
                b.rotDirection = "CLOCKWISE"

        if 1 in smallestNumIndexes:
            if b.Vx > 0:
                BOUNCE_SOUND.play()
                b.Vx *= -1
            if c.directionX == "Left":
                if b.rect.bottom + 135 >= scrHeight:
                    b.Vx -= 4
                else:
                    b.Vx -= 2
            if b.Vy < 0:
                b.rotDirection = "CLOCKWISE"
            else:
                b.rotDirection = "ANTI"

        if 2 in smallestNumIndexes:
            if c.Vy < 0 :
                if b.Vy > 0:
                    BOUNCE_SOUND.play()
                    b.Vy *= -1
                    b.Vy -= 3
                elif b.Vy < 0:
                    b.Vy -= 3
            else:
                if b.Vy - (-1 * math.sqrt(b.kEyCoe*(b.Vy**2))) >3:
                    BOUNCE_SOUND.play()
                b.Vy = -1 * math.sqrt(b.kEyCoe*(b.Vy**2))
                if int(b.Vy) == 0:
                    b.Ay = 0
                    b.Vy = -1

            if b.Vx < 0:
                b.rotDirection = "ANTI"
            else:
                b.rotDirection = "CLOCKWISE"
                
                

        if 3 in smallestNumIndexes:
            if c.rect.bottom + b.rect.height >= 560 and round(b.Vy) == 0:
                c.rect.y = 560 - b.rect.height + 4
                c.Vy = 0
                c.jumping = False

            else:
                BOUNCE_SOUND.play()
                b.Vy *= -1

                
class CHARACTER1(CHARACTER):
    def __init__(c, scrWidth, scrHeight, characterImage, shirtColor):
        super().__init__(scrWidth, scrHeight, characterImage)
        c.Frames = [pygame.transform.scale(pygame.image.load(os.path.join(shirtColor+"Assets", "walkingFrame"+str(i)+".png")), (70,40)) for i in range (7)]
        c.kickingFrames = [pygame.transform.scale(pygame.image.load(os.path.join(shirtColor+"Assets", "kickingFrame"+str(i)+".png")), (70,40)) for i in range (4)]
        c.bodyImage = c.Frames[0]
        c.headImage = pygame.transform.scale(pygame.image.load(os.path.join("Assets", characterImage)), (85,85))
        c.rect = pygame.Rect(300, 560, 85, 105)
        

    def handleMovement(c, keysPressed, scrWidth, scrHeight, b, otherPlayer):
        c.tick += 1
        c.Vy += c.Ay
        c.rect.y += c.Vy
        ballMid = b.rect.x + b.ballWandH//2
        char1Mid = c.rect.x + c.rect.width//2
        char2Mid = otherPlayer.rect.x + otherPlayer.rect.width//2
        ballBetween = (char1Mid < ballMid and ballMid < char2Mid and
                    (b.rect.bottom - b.rect.height//2 > c.rect.top and b.rect.bottom - b.rect.height//2 > otherPlayer.rect.top
                     and b.rect.top < c.rect.bottom and b.rect.top < otherPlayer.rect.bottom)
                    and otherPlayer.rect.left - c.rect.right <= b.rect.width + 2)

        if c.rect.y >= 560:
            c.rect.y = 560
            c.Vy = 0
            c.jumping = False

        if keysPressed[pygame.K_w] and not c.jumping:
            JUMP_SOUND.play()
            JUMP_GRUNT.play()
            c.bodyImage = c.Frames[0]
            c.jumping = True
            c.Vy -= 5.25

        if keysPressed[pygame.K_d] and not keysPressed[pygame.K_a] and not c.kicking:
            c.directionX = "Right"
            if c.tick%4 and not c.jumping and not c.kicking:
                if not CHANNEL5.get_busy():
                    CHANNEL5.play(WALKING_SOUND)
                if c.Frames.index(c.bodyImage) == len(c.Frames)-1:
                    c.bodyImage = c.Frames[0]
                else:
                    c.bodyImage = c.Frames[c.Frames.index(c.bodyImage)+1]
            if not ballBetween and c.rect.right + 6 < otherPlayer.rect.left:
                c.rect.x += 6
            if otherPlayer.directionX == "None" and abs(c.rect.right - otherPlayer.rect.left) < 6 and otherPlayer.rect.right < scrWidth:
                c.rect.x += 3
                otherPlayer.rect.x += 3
            elif otherPlayer.directionX == "None" and ballBetween and otherPlayer.rect.right + 2 < scrWidth:
                c.rect.x += 2
                otherPlayer.rect.x += 2
                b.rect.x += 2
            
        elif keysPressed[pygame.K_a] and not keysPressed[pygame.K_d] and not c.kicking:
            c.directionX = "Left"
            if c.tick%4 and not c.jumping and not c.kicking:
                if not CHANNEL5.get_busy():
                    CHANNEL5.play(WALKING_SOUND)
                if c.Frames.index(c.bodyImage) == 0:
                    c.bodyImage = c.Frames[-1]
                else:
                    c.bodyImage = c.Frames[c.Frames.index(c.bodyImage)-1]
            c.rect.x -= 6

        elif not c.jumping and not c.kicking:
            c.directionX = "None"
            c.bodyImage = c.Frames[0]

        if c.rect.left < 0:
            c.directionX = "None"
            c.rect.x = 0
            
        elif c.rect.right > scrWidth:
            c.directionX = "None"
            c.rect.x = scrWidth - c.rect.width

        if keysPressed[pygame.K_c] and not c.kicking:
            c.kicking = True
            c.tempTickKick = c.tick
            c.bodyImage = c.kickingFrames[0]

        elif c.kicking:
            if (c.tick - c.tempTickKick)%4 == 0:
                try:
                    c.bodyImage = c.kickingFrames[c.kickingFrames.index(c.bodyImage) + 1]
                    if b.rect.left - c.rect.right < 50 and b.rect.left - char1Mid > 0 and \
                    b.rect.y > c.rect.top + 52 and b.rect.top + b.rect.height//2 < c.rect.bottom:
                        b.Vx += 9
                        if ballBetween:
                            b.Vy -= 20
                        else:
                            b.Vy -= 11
                except:
                    c.bodyImage = c.Frames[0]
                    c.kicking = False
                    
        if c.rect.colliderect(b.rect) and not c.collideBall:
            c.collideBall = True
            c.tempTick = c.tick
            c.handleBallCollision(b, scrWidth, scrHeight)

        elif not c.rect.colliderect(b.rect) or c.tick - c.tempTick >= 8:
            c.collideBall = False

        if not c.rect.colliderect(b.rect):
            b.Ay = 0.2

        if ballBetween:
            BOUNCE_SOUND.set_volume(0)
            c.collideBall = False
            b.rect.x = c.rect.right
            b.Vx = 0.000000001
        else:
            BOUNCE_SOUND.set_volume(1)
        
    def resetPosition(c):
        c.rect = pygame.Rect(300, 560, 85, 105)
            
class CHARACTER2(CHARACTER):
    def __init__(c, scrWidth, scrHeight, characterImage, shirtColor):
        super().__init__(scrWidth, scrHeight, characterImage)
        c.Frames = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(shirtColor+"Assets", "walkingFrame"+str(i)+".png")), (70,40)),True,False) for i in range (7)]
        c.kickingFrames = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(shirtColor+"Assets", "kickingFrame"+str(i)+".png")), (70,40)),True,False) for i in range (4)]
        c.bodyImage = c.Frames[0]
        c.headImage = pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join("Assets", characterImage)), (85,85)),True,False)
        c.rect = pygame.Rect(scrWidth - 300 - 85, 560, 85, 105)
        

    def handleMovement(c, keysPressed, scrWidth, scrHeight, b, otherPlayer):
        c.tick += 1
        c.Vy += c.Ay
        c.rect.y += c.Vy
        ballMid = b.rect.x + b.ballWandH//2
        char1Mid = otherPlayer.rect.x + otherPlayer.rect.width//2
        char2Mid = c.rect.x + c.rect.width//2
        ballBetween = (char1Mid < ballMid and ballMid < char2Mid and
                    (b.rect.bottom - b.rect.height//2 > c.rect.top and b.rect.bottom - b.rect.height//2> otherPlayer.rect.top
                     and b.rect.top < c.rect.bottom and b.rect.top < otherPlayer.rect.bottom)
                    and c.rect.left - otherPlayer.rect.right <= b.rect.width + 2)
        
        if c.rect.y >= 560:
            c.rect.y = 560
            c.Vy = 0
            c.jumping = False

        if keysPressed[pygame.K_UP] and not c.jumping:
            JUMP_SOUND.play()
            JUMP_GRUNT.play()
            c.bodyImage = c.Frames[0]
            c.jumping = True
            c.Vy -= 5.25
            
        if keysPressed[pygame.K_RIGHT] and not keysPressed[pygame.K_LEFT] and not c.kicking:
            c.directionX = "Right"
            if c.tick%4 and not c.jumping and not c.kicking:
                if not CHANNEL6.get_busy():
                    CHANNEL6.play(WALKING_SOUND)
                if c.Frames.index(c.bodyImage) == 0:
                    c.bodyImage = c.Frames[-1]
                else:
                    c.bodyImage = c.Frames[c.Frames.index(c.bodyImage)-1]
            
            c.rect.x += 6
            
        elif keysPressed[pygame.K_LEFT] and not keysPressed[pygame.K_RIGHT] and not c.kicking:
            c.directionX = "Left"
            if c.tick%4 and not c.jumping and not c.kicking:
                if not CHANNEL6.get_busy():
                    CHANNEL6.play(WALKING_SOUND)
                if c.Frames.index(c.bodyImage) == len(c.Frames)-1:
                    c.bodyImage = c.Frames[0]
                else:
                    c.bodyImage = c.Frames[c.Frames.index(c.bodyImage)+1]
            if not ballBetween and c.rect.left - 6 > otherPlayer.rect.right:
                c.rect.x -= 6
            if otherPlayer.directionX == "None" and abs(c.rect.left - otherPlayer.rect.right) < 6 and otherPlayer.rect.left > 0:
                c.rect.x -= 3
                otherPlayer.rect.x -= 3
            elif otherPlayer.directionX == "None" and ballBetween and otherPlayer.rect.left - 2 > 0:
                c.rect.x -= 2
                otherPlayer.rect.x -= 2
                b.rect.x -= 2
                
            
            
        elif not c.jumping and not c.kicking:
            c.directionX = "None"
            c.bodyImage = c.Frames[0]

        if c.rect.left < 0:
            c.rect.x = 0
            
        elif c.rect.right > scrWidth:
            c.rect.x = scrWidth - c.rect.width

        if keysPressed[pygame.K_m] and not c.kicking:
            c.kicking = True
            c.tempTickKick = c.tick
            c.bodyImage = c.kickingFrames[0]

        elif c.kicking:
            if (c.tick - c.tempTickKick)%4 == 0:
                try:
                    c.bodyImage = c.kickingFrames[c.kickingFrames.index(c.bodyImage)+1]
                    if c.rect.left - b.rect.right < 50 and char2Mid - b.rect.right > 0 and \
                    b.rect.y > c.rect.top + 52 and b.rect.top + b.rect.height//2 < c.rect.bottom:
                        b.Vx -= 9
                        if ballBetween:
                            b.Vy -= 20
                        else:
                            b.Vy -= 11
                except:
                    c.bodyImage = c.Frames[0]
                    c.kicking = False

        if c.rect.colliderect(b.rect) and not c.collideBall:
            c.collideBall = True
            c.tempTick = c.tick
            c.handleBallCollision(b, scrWidth, scrHeight)

        elif not c.rect.colliderect(b.rect) or c.tick - c.tempTick >= 8:
            c.collideBall = False
        
        if not c.rect.colliderect(b.rect):
            b.Ay = 0.2
            
        if ballBetween:
            c.collideBall = False
            b.rect.x = otherPlayer.rect.right
            b.Vx = 0.000000001


    def resetPosition(c):
        c.rect = pygame.Rect(1536 - 300 - 85, 560, 85, 105)
            
        
        
pygame.init()
info = pygame.display.Info()
WIDTH = 1536
HEIGHT = 864
# COMM = chatCommClass.chatComm("86.36.42.136", 15112)
# COMM.startConnection()
WHITE = (255, 255, 255)
BLACK = (0,0,0)
WIN = pygame.display.set_mode((1536, 804))
WIDTH = WIN.get_width()
HEIGHT = WIN.get_height()
people = {}
pygame.display.set_caption("Header Football")
CHANNEL5 = pygame.mixer.Channel(5)
CHANNEL6 = pygame.mixer.Channel(6)
GOAL_SCORED_SOUND = pygame.mixer.Sound(os.path.join("Assets", "goalScored.mp3"))
JUMP_SOUND = pygame.mixer.Sound(os.path.join("Assets", "jump.mp3"))
JUMP_GRUNT = pygame.mixer.Sound(os.path.join("Assets", "jump2.mp3"))
WHISTLE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "start_whistle.mp3"))
BOUNCE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "ball_bounce.mp3"))
WALKING_SOUND = pygame.mixer.Sound(os.path.join("Assets", "walking.mp3"))
BUTTON_SOUND = pygame.mixer.Sound(os.path.join("Assets", "button_press.mp3"))
INVITE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Invite.mp3"))
BACKGROUND = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "background.png")),(WIDTH, HEIGHT))
GOAL1 = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "Goal_Image_1.png")),(80,250))
GOAL1BACK = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "Goal_Image_1_BACK.png")),(53,250))
GOAL2 = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "Goal_Image_2.png")),(80,250))
GOAL2BACK = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "Goal_Image_2_BACK.png")),(53,250))
PLAYLOCALBUTTON = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "Same_Device.png")),(200,200))
PLAYONLINEBUTTON = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "Online.png")),(200,200))
INFOBUTTON = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "info_button.png")),(100,100))
START_BUTTON = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "start.png")),(350,100))
RIGHT_BUTTON = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "right_button.png")),(50,50))
LEFT_BUTTON = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "left_button.png")),(50,50))
UP_BUTTON = pygame.transform.rotate(RIGHT_BUTTON, 90)
DOWN_BUTTON = pygame.transform.rotate(RIGHT_BUTTON, -90)
LOGIN_BUTTON = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "login.png")),(175,50))
INVITE_BUTTON = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "invite.png")),(230,80))
REQUEST_BUTTON = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "request.png")),(130,35))
ACCEPT_BUTTON = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "accept.png")),(350,100))
REJECT_BUTTON = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "reject.png")),(350,100))
READY_BUTTON = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "ready.png")),(350,100))
CANCEL_BUTTON = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "cancel.png")),(350,100))

BORDERX = pygame.Rect(395,0,1,HEIGHT)
BORDERY = pygame.Rect(0,330,WIDTH,1)
TITLE1 = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 150).render("HEADER", 1, WHITE)
TITLE2 = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 150).render("FOOTBALL", 1, WHITE)
CLICK_TO_PLAY = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 50).render("Click anywhere to go back", 1, WHITE)
PLAYER_1_CONTROLS = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 50).render("Player 1 Controls: W,A,D(movement) and C(kick)", 1, WHITE)
PLAYER_2_CONTROLS = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 50).render("Player 2 Controls: Up,Left,Right(movement) and M(kick)", 1, WHITE)
CHAR_OPTIONS = ["Christos", "Eduardo", "Gianni", "Giselle", "Hammoud", "Harras", "Madhavi", "Riley", "Saquib", "Temoor", "Eric"]
CHAR_IMAGES = [pygame.transform.scale(pygame.image.load(os.path.join("Assets", character + ".png")), (255,255)) for character in CHAR_OPTIONS]
COLOR_OPTIONS = ["Blue", "Green", "Orange", "Pink", "Red", "Yellow"]
FLAG_COLORS = [(44,34,238),(11,175,57),(255,127,39),(255,108,155),(236,28,36),(246,255,0)]
COLOR_IMAGES = [pygame.transform.scale(pygame.image.load(os.path.join(color+"Assets", "walkingFrame0.png")), (210,120)) for color in COLOR_OPTIONS]
CHARSEL_PLATFORM = pygame.transform.scale(pygame.image.load(os.path.join("Assets","platform.png")), (WIDTH-300,HEIGHT-100))
CHARSEL_TITLE = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 75).render("CHARACTER SELECT", 1, WHITE)
PLAYER1_TITLE = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 50).render("PLAYER 1", 1, WHITE)
PLAYER2_TITLE = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 50).render("PLAYER 2", 1, WHITE)
HEAD_TITLE = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 50).render("HEAD", 1, WHITE)
BODY_TITLE = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 50).render("BODY", 1, WHITE)
READY_TITLE = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 50).render("Ready!", 1, WHITE)
LOGIN_PLATFORM = pygame.transform.scale(pygame.image.load(os.path.join("Assets","platform.png")), (WIDTH-600,HEIGHT-200))
LOGIN_TITLE = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 90).render("LOGIN:", 1, WHITE)
USERNAME_ENTER = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 50).render("Username:", 1, WHITE)
PASSWORD_ENTER = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 50).render("Password:", 1, WHITE)
USERNAME_RECT = pygame.Rect(750,300,350,60)
PASSWORD_RECT = pygame.Rect(750,400,350,60)
INCORRECT_LOGIN = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 30).render("The username or password you entered are incorrect!", 1, (136,0,27))
WELCOME_LOGIN = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 50).render("Welcome!", 1, (WHITE))
LOGIN_BUTTON_RECT = pygame.Rect(WIDTH//2 - LOGIN_BUTTON.get_width()//2, 575,175,50)
INVITE_TITLE = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 90).render("INVITE FRIEND:", 1, WHITE)
FRIEND_RECT = pygame.Rect(750,350,350,60)
INVITE_BUTTON_RECT = pygame.Rect(WIDTH//2 - INVITE_BUTTON.get_width()//2, 500,230,80)
USER_NOT_EXIST = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 30).render("The user you entered does not exist!", 1, (136,0,27))
NOT_FRIENDS = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 30).render("You are not friends with this user! Send a", 1, (136,0,27))
INVITE_SUCCESSFUL = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 30).render("Invite successful! Waiting for response...", 1, (WHITE))
REQUEST_BUTTON_RECT = pygame.Rect(984,430,130,35)
REQUEST_SUCCESSFUL = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 30).render("Request successful!", 1, (WHITE))
GAME_INVITE_TITLE = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 120).render("GAME INVITE!", 1, WHITE)
FRIEND_REQUEST_TITLE = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 100).render("FRIEND REQUEST:", 1, WHITE)
ACCEPT_BUTTON_RECT = pygame.Rect(WIDTH//2 - ACCEPT_BUTTON.get_width() - 20,500,350,100)
REJECT_BUTTON_RECT = pygame.Rect(WIDTH//2 + 20,500,350,100)
FRIEND_ACCEPT_BUTTON_RECT = pygame.Rect(WIDTH//2 - ACCEPT_BUTTON.get_width()//2,500,350,100)

def drawGame(ball, character1, character2, timer, goalScored, currentChar1, currentColor1, currentChar2, currentColor2, username1 = "Player 1", username2 = "Player 2"):
    WIN.blit(BACKGROUND,(0,0))
    WIN.blit(GOAL1, (-7,445))
    WIN.blit(GOAL2, (1460,445))
    WIN.blit(character1.bodyImage,(character1.rect.x+10, character1.rect.y+70))
    WIN.blit(character1.headImage,(character1.rect.x, character1.rect.y))
    WIN.blit(character2.bodyImage,(character2.rect.x+10, character2.rect.y+70))
    WIN.blit(character2.headImage,(character2.rect.x, character2.rect.y))
    if 2 in ball.smallestNumIndexes:
        WIN.blit(GOAL1BACK, (-7,445))
        WIN.blit(GOAL2BACK, (1486,445))
        WIN.blit(ball.image, (ball.rect.x,ball.rect.y))
    else:
        WIN.blit(ball.image, (ball.rect.x,ball.rect.y))
        WIN.blit(GOAL1BACK, (-7,445))
        WIN.blit(GOAL2BACK, (1486,445))
    timeText = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 50).render(timer, 1, WHITE)
    WIN.blit(timeText, (1536//2 - timeText.get_width()//2,0))
    
    player1ScoreText = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 70).render(f"{username1}: " + str(character1.goals), 1, WHITE)
    WIN.blit(player1ScoreText, (1536//2 - player1ScoreText.get_width()- timeText.get_width()//2 - 50,0))
    player2ScoreText = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 70).render(f"{username2}: " + str(character2.goals), 1, WHITE)
    WIN.blit(player2ScoreText, (1536//2 + timeText.get_width()//2 + 50,0))
    if goalScored:
        goalText = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 300).render("GOAL!", 1, WHITE)
        WIN.blit(goalText, (1536//2 - goalText.get_width()//2, 432 - goalText.get_height()//2 - 50))
    pygame.display.update()

def updateTime(timer):
    if timer == "1:00":
        timer = "0:59"
    elif timer == "0:00":
        return timer
    else:
        timer = timer[:2] + "0"*(2-len(str(int(timer[2:])-1))) + str(int(timer[2:])-1)
    return timer

def drawOutline(string, xytuple, size, fontsize = 50):
    whiteVer = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', fontsize).render(string, 1, BLACK)
    WIN.blit(whiteVer,(xytuple[0]+size,xytuple[1]+size))
    WIN.blit(whiteVer,(xytuple[0]-size,xytuple[1]-size))
    WIN.blit(whiteVer,(xytuple[0]-size,xytuple[1]+size))
    WIN.blit(whiteVer,(xytuple[0]+size,xytuple[1]-size))
    
def drawMenu():
    WIN.blit(BACKGROUND,(0,0))
    WIN.blit(GOAL1, (-7,445))
    WIN.blit(GOAL2, (1460,445))
    WIN.blit(PLAYLOCALBUTTON, (WIDTH//2 - 250, HEIGHT//2 - 50 + 50))
    WIN.blit(PLAYONLINEBUTTON, (WIDTH//2 + 50, HEIGHT//2 - 50 + 50))
    WIN.blit(INFOBUTTON, (WIDTH - 100, 0))
    drawOutline("HEADER",(WIDTH//2 - TITLE1.get_width()//2,0),5,150)
    drawOutline("FOOTBALL",(WIDTH//2 - TITLE2.get_width()//2,TITLE1.get_height()),5,150)
    WIN.blit(TITLE1, (WIDTH//2 - TITLE1.get_width()//2,0))
    WIN.blit(TITLE2, (WIDTH//2 - TITLE2.get_width()//2,TITLE1.get_height()))
    pygame.display.update()

def drawInfo():
    WIN.blit(BACKGROUND,(0,0))
    WIN.blit(GOAL1, (-7,445))
    WIN.blit(GOAL2, (1460,445))
    drawOutline("Click anywhere to go back", (WIDTH//2 - CLICK_TO_PLAY.get_width()//2,
                                           HEIGHT//2 - CLICK_TO_PLAY.get_height()//2 + 150),2)
    drawOutline("Player 1 Controls: W,A,D(movement) and C(kick)", (WIDTH//2 - PLAYER_1_CONTROLS.get_width()//2,
                                               HEIGHT//2 - PLAYER_1_CONTROLS.get_height()//2 - 100 + PLAYER_1_CONTROLS.get_height()),2)
    drawOutline("Player 2 Controls: Up,Left,Right(movement) and M(kick)", (WIDTH//2 - PLAYER_2_CONTROLS.get_width()//2,
                                               HEIGHT//2 - PLAYER_2_CONTROLS.get_height()//2 - 100 + PLAYER_2_CONTROLS.get_height()*2),2)
    WIN.blit(CLICK_TO_PLAY, (WIDTH//2 - CLICK_TO_PLAY.get_width()//2,
                             HEIGHT//2 - CLICK_TO_PLAY.get_height()//2 + 150))
    WIN.blit(PLAYER_1_CONTROLS, (WIDTH//2 - PLAYER_1_CONTROLS.get_width()//2,
                                 HEIGHT//2 - PLAYER_1_CONTROLS.get_height()//2 - 100 + PLAYER_1_CONTROLS.get_height()))
    WIN.blit(PLAYER_2_CONTROLS, (WIDTH//2 - PLAYER_2_CONTROLS.get_width()//2,
                                 HEIGHT//2 - PLAYER_2_CONTROLS.get_height()//2 - 100 + PLAYER_2_CONTROLS.get_height()*2))
    pygame.display.update()

def drawLogin(currentUsername,currentPassword, usernameSelected, passwordSelected):
    WIN.blit(BACKGROUND,(0,0))
    WIN.blit(GOAL1, (-7,445))
    WIN.blit(GOAL2, (1460,445))
    WIN.blit(LOGIN_PLATFORM, (WIDTH//2 - LOGIN_PLATFORM.get_width()//2, HEIGHT//2 - LOGIN_PLATFORM.get_height()//2))
    WIN.blit(LOGIN_TITLE, (WIDTH//2 - LOGIN_TITLE.get_width()//2, HEIGHT//2 - LOGIN_PLATFORM.get_height()//2 + 20))
    WIN.blit(USERNAME_ENTER, (500,300))
    WIN.blit(PASSWORD_ENTER, (500,400))
    pygame.draw.rect(WIN, (55, 140, 49), USERNAME_RECT)
    if usernameSelected:
        pygame.draw.rect(WIN, (88, 219, 79), USERNAME_RECT)
    pygame.draw.rect(WIN, BLACK, USERNAME_RECT,  2)
    pygame.draw.rect(WIN, (55, 140, 49), PASSWORD_RECT)
    if passwordSelected:
        pygame.draw.rect(WIN, (88, 219, 79), PASSWORD_RECT)
    pygame.draw.rect(WIN, BLACK, PASSWORD_RECT,  2)
    if len(currentUsername) < 500:
        usernameText = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 50).render(currentUsername, 1, BLACK)
        WIN.blit(usernameText, (USERNAME_RECT.x + 10,USERNAME_RECT.y))
    if len(currentPassword) < 500:
        passwordText = pygame.font.SysFont("calibri", 50).render("*"*(len(currentPassword)), 1, BLACK)
        WIN.blit(passwordText, (PASSWORD_RECT.x + 10,PASSWORD_RECT.y + 20))
    WIN.blit(LOGIN_BUTTON, (WIDTH//2 - LOGIN_BUTTON.get_width()//2, 575))
    pygame.display.update()

def drawOnline(currentFriend,friendBoxSelected,waiting):
    WIN.blit(BACKGROUND,(0,0))
    WIN.blit(GOAL1, (-7,445))
    WIN.blit(GOAL2, (1460,445))
    WIN.blit(LOGIN_PLATFORM, (WIDTH//2 - LOGIN_PLATFORM.get_width()//2, HEIGHT//2 - LOGIN_PLATFORM.get_height()//2))
    WIN.blit(INVITE_TITLE, (WIDTH//2 - INVITE_TITLE.get_width()//2, HEIGHT//2 - LOGIN_PLATFORM.get_height()//2 + 20))
    pygame.draw.rect(WIN, (55, 140, 49), FRIEND_RECT)
    WIN.blit(USERNAME_ENTER, (500,350))
    if friendBoxSelected:
        pygame.draw.rect(WIN, (88, 219, 79), FRIEND_RECT)
    pygame.draw.rect(WIN, BLACK, FRIEND_RECT,  2)
    usernameText = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 50).render(currentFriend, 1, BLACK)
    WIN.blit(usernameText, (FRIEND_RECT.x + 10,FRIEND_RECT.y))
    if not waiting:
        WIN.blit(INVITE_BUTTON, (WIDTH//2 - INVITE_BUTTON.get_width()//2, 500))
    WIN.blit(pygame.transform.scale(LEFT_BUTTON,(100,100)), (320,120))
    pygame.display.update()

def checkFriend(currentFriend, currentUsername):
    inviteButton = False
    if currentFriend not in COMM.getUsers():
        drawOnline(currentFriend,False,False)
        WIN.blit(USER_NOT_EXIST, (WIDTH//2 - USER_NOT_EXIST.get_width()//2, 430))
        
    
    elif currentFriend not in COMM.getFriends() or currentFriend == currentUsername:
        drawOnline(currentFriend,False,False)
        WIN.blit(NOT_FRIENDS, (WIDTH//2 - NOT_FRIENDS.get_width()//2 - REQUEST_BUTTON.get_width()//2, 430))
        WIN.blit(REQUEST_BUTTON ,(WIDTH//2 + NOT_FRIENDS.get_width()//2 - REQUEST_BUTTON.get_width()//2 + 10, 430))
        inviteButton = True

    else:
        drawOnline(currentFriend,False,True)
        WIN.blit(INVITE_SUCCESSFUL, (WIDTH//2 - INVITE_SUCCESSFUL.get_width()//2, 450))
        COMM.sendMessage(currentFriend,"INVITE")
        pygame.display.update()
        return True, inviteButton
    pygame.display.update()
    return False, inviteButton

def checkForInvite():
    mail = COMM.getMail()
    people = {}
    for message in mail[0]:
        people[message[0]] = people.get(message[0],[])+[message[1]]
    for person in people:
        try:
            lastInvite = len(people[person]) - people[person][::-1].index("INVITE") - 1
        except:
            lastInvite = -1
        try:
            lastCancelInvite = len(people[person]) - people[person][::-1].index("INVITE DONE") - 1
        except:
            lastCancelInvite = -1
        if lastInvite > -1 and lastCancelInvite < lastInvite:
            return person
    return "Nobody"

def getReplyInvitation(name):
    mail = COMM.getMail()
    people = {}
    for message in mail[0]:
        people[message[0]] = people.get(message[0],[])+[message[1]]
    if name in people:
        try:
            acceptInvite = people[name].index("INVITE ACCEPTED")
        except:
            acceptInvite = -1
        try:
            rejectInvite = people[name].index("INVITE REJECTED")
        except:
            rejectInvite = -1
            
        if acceptInvite != -1:
            return "accepted"
        elif rejectInvite != -1:
            return "rejected"
        else:
            return "no reply"

def drawGameInvite(name):
    WIN.blit(BACKGROUND,(0,0))
    WIN.blit(GOAL1, (-7,445))
    WIN.blit(GOAL2, (1460,445))
    WIN.blit(LOGIN_PLATFORM, (WIDTH//2 - LOGIN_PLATFORM.get_width()//2, HEIGHT//2 - LOGIN_PLATFORM.get_height()//2))
    WIN.blit(GAME_INVITE_TITLE, (WIDTH//2 - GAME_INVITE_TITLE.get_width()//2, HEIGHT//2 - LOGIN_PLATFORM.get_height()//2 + 20))
    invitationString = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 40).render(name+" has invited you to join their game!", 1, (WHITE))
    WIN.blit(invitationString,(WIDTH//2 - invitationString.get_width()//2, HEIGHT//2 - invitationString.get_height()//2))
    WIN.blit(ACCEPT_BUTTON,(WIDTH//2 - ACCEPT_BUTTON.get_width() - 20, 500))
    WIN.blit(REJECT_BUTTON,(WIDTH//2 + 20, 500))
    pygame.display.update()

def drawFriendRequest(name):
    WIN.blit(BACKGROUND,(0,0))
    WIN.blit(GOAL1, (-7,445))
    WIN.blit(GOAL2, (1460,445))
    WIN.blit(LOGIN_PLATFORM, (WIDTH//2 - LOGIN_PLATFORM.get_width()//2, HEIGHT//2 - LOGIN_PLATFORM.get_height()//2))
    WIN.blit(FRIEND_REQUEST_TITLE, (WIDTH//2 - FRIEND_REQUEST_TITLE.get_width()//2, HEIGHT//2 - LOGIN_PLATFORM.get_height()//2 + 20))
    requestString = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 40).render(name+" has requested to become you friend!", 1, (WHITE))
    WIN.blit(requestString,(WIDTH//2 - requestString.get_width()//2, HEIGHT//2 - requestString.get_height()//2))
    WIN.blit(ACCEPT_BUTTON,(FRIEND_ACCEPT_BUTTON_RECT.x,FRIEND_ACCEPT_BUTTON_RECT.y))
    pygame.display.update()

def drawCharSelect(currentChar1,currentColor1,currentChar2,currentColor2):
    WIN.blit(BACKGROUND,(0,0))
    WIN.blit(GOAL1, (-7,445))
    WIN.blit(GOAL2, (1460,445))
    WIN.blit(CHARSEL_PLATFORM, (150, 50))
    WIN.blit(CHARSEL_TITLE, (WIDTH//2 - CHARSEL_TITLE.get_width()//2, 70))
    WIN.blit(PLAYER1_TITLE, (450,150))
    WIN.blit(PLAYER2_TITLE, (950,150))
    WIN.blit(HEAD_TITLE, (200,300))
    WIN.blit(BODY_TITLE, (200,500))
    WIN.blit(CHAR_IMAGES[currentChar1], (420,220))
    WIN.blit(pygame.transform.flip(CHAR_IMAGES[currentChar2],True,False), (920,220))
    WIN.blit(COLOR_IMAGES[currentColor1], (430,470))
    WIN.blit(pygame.transform.flip(COLOR_IMAGES[currentColor2],True,False), (930,470))
    WIN.blit(START_BUTTON, (WIDTH//2 - START_BUTTON.get_width()//2, 600))
    WIN.blit(pygame.transform.scale(LEFT_BUTTON,(100,100)), (190,80))
    WIN.blit(LEFT_BUTTON, (370,305))
    WIN.blit(RIGHT_BUTTON, (680,305))
    WIN.blit(LEFT_BUTTON, (870,305))
    WIN.blit(RIGHT_BUTTON, (1180,305))
    WIN.blit(LEFT_BUTTON, (370,505))
    WIN.blit(RIGHT_BUTTON, (680,505))
    WIN.blit(LEFT_BUTTON, (870,505))
    WIN.blit(RIGHT_BUTTON, (1180,505))
    pygame.display.update()

def getCharSelChanges(opponentName):
    global people
    mail = COMM.getMail()
    lastResponse = None
    for message in mail[0]:
        people[message[0]] = people.get(message[0],[])+[message[1]]
    if opponentName in people:
        for msg in people[opponentName]:
            if msg == "CANCEL" or msg[:4] == "data":
                lastResponse = people[opponentName].index(msg)
        if lastResponse != None:
            if people[opponentName][lastResponse] == "CANCEL":
                del people[opponentName][0:lastResponse+1]
                return "CANCEL"
            elif people[opponentName][lastResponse][:4] == "data":
                temp = people[opponentName][lastResponse][5:].split(',')
                del people[opponentName][0:lastResponse+1]
                return temp
            else:
                return False
    return False

def drawCharSelectPlayer1(currentChar1,currentColor1,currentChar2,currentColor2, player1Ready, player2Ready):
    WIN.blit(BACKGROUND,(0,0))
    WIN.blit(GOAL1, (-7,445))
    WIN.blit(GOAL2, (1460,445))
    WIN.blit(CHARSEL_PLATFORM, (150, 50))
    WIN.blit(CHARSEL_TITLE, (WIDTH//2 - CHARSEL_TITLE.get_width()//2, 70))
    WIN.blit(PLAYER1_TITLE, (450,150))
    WIN.blit(PLAYER2_TITLE, (950,150))
    WIN.blit(HEAD_TITLE, (200,300))
    WIN.blit(BODY_TITLE, (200,500))
    WIN.blit(CHAR_IMAGES[currentChar1], (420,220))
    WIN.blit(pygame.transform.flip(CHAR_IMAGES[currentChar2],True,False), (920,220))
    WIN.blit(COLOR_IMAGES[currentColor1], (430,470))
    WIN.blit(pygame.transform.flip(COLOR_IMAGES[currentColor2],True,False), (930,470))
    if not player1Ready:   
        WIN.blit(READY_BUTTON, (WIDTH//2 - READY_BUTTON.get_width()-50, 600))
        WIN.blit(LEFT_BUTTON, (370,305))
        WIN.blit(RIGHT_BUTTON, (680,305))
        WIN.blit(LEFT_BUTTON, (370,505))
        WIN.blit(RIGHT_BUTTON, (680,505))
    else:
        WIN.blit(CANCEL_BUTTON, (WIDTH//2 - CANCEL_BUTTON.get_width()-50, 600))
    if player2Ready:
        WIN.blit(READY_TITLE, (WIDTH//2 + 200, 620))
    WIN.blit(pygame.transform.scale(LEFT_BUTTON,(100,100)), (190,80))
    pygame.display.update()

def charSelectPlayer1(opponentName):
    clock = pygame.time.Clock()
    runCharSelect = True
    currentChar1 = 0
    currentColor1 = 0
    currentChar2 = 0
    currentColor2 = 0
    player1Ready = False
    player2Ready = False
    ReadyButtonRect = pygame.Rect(WIDTH//2 - START_BUTTON.get_width()-50, 600,350,100)
    drawCharSelectPlayer1(currentChar1,currentColor1,currentChar2,currentColor2,player1Ready,player2Ready)
    lastUpdateTick = 0
    charSelTick = 0
    while runCharSelect:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                COMM.sendMessage(opponentName,"CANCEL")
                return "closed"
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                distFrom11 = math.sqrt((x - 395)**2 + (y - 330)**2)
                distFrom12 = math.sqrt((x - 705)**2 + (y - 330)**2)
                distFrom21 = math.sqrt((x - 395)**2 + (y - 530)**2)
                distFrom22 = math.sqrt((x - 705)**2 + (y - 530)**2)
                distFromBack = math.sqrt((x - 240)**2 + (y - 130)**2)
                if not player1Ready:
                    if distFrom11 < 25:
                        BUTTON_SOUND.play()
                        if currentChar1 - 1 == -1:
                            currentChar1 = len(CHAR_OPTIONS) - 1
                        else:
                            currentChar1 -= 1

                    elif distFrom12 < 25:
                        BUTTON_SOUND.play()
                        if currentChar1 + 1 == len(CHAR_OPTIONS):
                            currentChar1 = 0
                        else:
                            currentChar1 += 1
                            
                    elif distFrom21 < 25:
                        BUTTON_SOUND.play()
                        if currentColor1 - 1 == -1:
                            currentColor1 = len(COLOR_OPTIONS) - 1
                        else:
                            currentColor1 -= 1
                            
                    elif distFrom22 < 25:
                        BUTTON_SOUND.play()
                        if currentColor1 + 1 == len(COLOR_OPTIONS):
                            currentColor1 = 0
                        else:
                            currentColor1 += 1
                if distFromBack < 50:
                    COMM.sendMessage(opponentName,"CANCEL")
                    return "cancelled"
                
                if not player1Ready and ReadyButtonRect.collidepoint(x,y):
                    BUTTON_SOUND.play()
                    player1Ready = True
                
                elif player1Ready and ReadyButtonRect.collidepoint(x,y):
                    BUTTON_SOUND.play()
                    player1Ready = False
                COMM.sendMessage(opponentName,f"data={currentChar1},{currentColor1},{player1Ready}")
        if abs(charSelTick - lastUpdateTick) == 10:
            lastUpdateTick = charSelTick
            reply = getCharSelChanges(opponentName)
            if not reply:
                pass
            elif reply == "CANCEL":
                return "cancelled"
            else:
                currentChar2 = int(reply[0])
                currentColor2 = int(reply[1])
                player2Ready = reply[2] == "True"
        if player1Ready and player2Ready:
            return ("done",currentChar1,currentColor1,currentChar2,currentColor2)
        drawCharSelectPlayer1(currentChar1,currentColor1,currentChar2,currentColor2, player1Ready, player2Ready)
        charSelTick += 1

def drawCharSelectPlayer2(currentChar1,currentColor1,currentChar2,currentColor2, player1Ready, player2Ready):
    WIN.blit(BACKGROUND,(0,0))
    WIN.blit(GOAL1, (-7,445))
    WIN.blit(GOAL2, (1460,445))
    WIN.blit(CHARSEL_PLATFORM, (150, 50))
    WIN.blit(CHARSEL_TITLE, (WIDTH//2 - CHARSEL_TITLE.get_width()//2, 70))
    WIN.blit(PLAYER1_TITLE, (450,150))
    WIN.blit(PLAYER2_TITLE, (950,150))
    WIN.blit(HEAD_TITLE, (200,300))
    WIN.blit(BODY_TITLE, (200,500))
    WIN.blit(CHAR_IMAGES[currentChar1], (420,220))
    WIN.blit(pygame.transform.flip(CHAR_IMAGES[currentChar2],True,False), (920,220))
    WIN.blit(COLOR_IMAGES[currentColor1], (430,470))
    WIN.blit(pygame.transform.flip(COLOR_IMAGES[currentColor2],True,False), (930,470))
    if not player2Ready:   
        WIN.blit(READY_BUTTON, (WIDTH//2 + 105, 600))
        WIN.blit(LEFT_BUTTON, (870,305))
        WIN.blit(RIGHT_BUTTON, (1180,305))
        WIN.blit(LEFT_BUTTON, (870,505))
        WIN.blit(RIGHT_BUTTON, (1180,505))
    else:
        WIN.blit(CANCEL_BUTTON, (WIDTH//2 + 105, 600))
    if player1Ready:
        WIN.blit(READY_TITLE, (WIDTH//2 - CANCEL_BUTTON.get_width()+40, 620))
    WIN.blit(pygame.transform.scale(LEFT_BUTTON,(100,100)), (190,80))
    pygame.display.update()

def charSelectPlayer2(opponentName):
    clock = pygame.time.Clock()
    runCharSelect = True
    currentChar1 = 0
    currentColor1 = 0
    currentChar2 = 0
    currentColor2 = 0
    player1Ready = False
    player2Ready = False
    ReadyButtonRect = pygame.Rect(WIDTH//2 + 50, 600,350,100)
    drawCharSelectPlayer2(currentChar1,currentColor1,currentChar2,currentColor2,player1Ready,player2Ready)
    lastUpdateTick = 0
    charSelTick = 0
    while runCharSelect:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                COMM.sendMessage(opponentName,"CANCEL")
                return "closed"
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                distFrom13 = math.sqrt((x - 895)**2 + (y - 330)**2)
                distFrom14 = math.sqrt((x - 1205)**2 + (y - 330)**2)
                distFrom23 = math.sqrt((x - 895)**2 + (y - 530)**2)
                distFrom24 = math.sqrt((x - 1205)**2 + (y - 530)**2)
                distFromBack = math.sqrt((x - 240)**2 + (y - 130)**2)
                if not player2Ready:
                    if distFrom13 < 25:
                        BUTTON_SOUND.play()
                        if currentChar2 - 1 == -1:
                            currentChar2 = len(CHAR_OPTIONS) - 1
                        else:
                            currentChar2 -= 1

                    elif distFrom14 < 25:
                        BUTTON_SOUND.play()
                        if currentChar2 + 1 == len(CHAR_OPTIONS):
                            currentChar2 = 0
                        else:
                            currentChar2 += 1
                            
                    elif distFrom23 < 25:
                        BUTTON_SOUND.play()
                        if currentColor2 - 1 == -1:
                            currentColor2 = len(COLOR_OPTIONS) - 1
                        else:
                            currentColor2 -= 1

                    elif distFrom24 < 25:
                        BUTTON_SOUND.play()
                        if currentColor2 + 1 == len(COLOR_OPTIONS):
                            currentColor2 = 0
                        else:
                            currentColor2 += 1
                if distFromBack < 50:
                    COMM.sendMessage(opponentName,"CANCEL")
                    return "cancelled"
                
                if not player2Ready and ReadyButtonRect.collidepoint(x,y):
                    BUTTON_SOUND.play()
                    player2Ready = True
                
                elif player2Ready and ReadyButtonRect.collidepoint(x,y):
                    BUTTON_SOUND.play()
                    player2Ready = False
                COMM.sendMessage(opponentName,f"data={currentChar2},{currentColor2},{player2Ready}")
        if abs(charSelTick - lastUpdateTick) == 10:
            lastUpdateTick = charSelTick
            reply = getCharSelChanges(opponentName)
            if not reply:
                pass
            elif reply == "CANCEL":
                return "cancelled"
            else:
                currentChar1 = int(reply[0])
                currentColor1 = int(reply[1])
                player1Ready = reply[2] == "True"
        if player1Ready and player2Ready:
            return ("done",currentChar1,currentColor1,currentChar2,currentColor2)
        drawCharSelectPlayer2(currentChar1,currentColor1,currentChar2,currentColor2, player1Ready, player2Ready)
        charSelTick += 1

def syncPlayers(opponentName):
    WIN.blit(BACKGROUND,(0,0))
    WIN.blit(GOAL1, (-7,445))
    WIN.blit(GOAL2, (1460,445))
    WIN.blit(LOGIN_PLATFORM, (WIDTH//2 - LOGIN_PLATFORM.get_width()//2, HEIGHT//2 - LOGIN_PLATFORM.get_height()//2))
    loadingTitle = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 90).render("LOADING...", 1, WHITE)
    WIN.blit(loadingTitle, (WIDTH//2 - loadingTitle.get_width()//2, HEIGHT//2 - loadingTitle.get_height()//2))
    pygame.display.update()
    COMM.getMail()
    myIP = socket.gethostbyname(socket.gethostname())
    time.sleep(3)
    COMM.sendMessage(opponentName,f"SYNC{myIP}")
    while True:
        mail = COMM.getMail()
        if len(mail[0]) >= 1:
            if mail[0][0][1][:4] == 'SYNC':
                return myIP,mail[0][0][1][4:]


def figureOutKeysP1(keyArray):
    keysDict = {'\x1a':pygame.K_w, '\x04':pygame.K_a, '\x07':pygame.K_d, '\x06':pygame.K_c,}
    keysPressed = {pygame.K_w:False, pygame.K_a:False, pygame.K_d:False, pygame.K_c:False}

    for key in keyArray:
        if key in keysDict:
            keysPressed[keysDict[key]] = True

    return keysPressed

def figureOutKeysP2(keyArray):
    keysDict = {'R':pygame.K_UP, 'O':pygame.K_RIGHT, 'P':pygame.K_LEFT, '\x10':pygame.K_m}
    keysPressed = {pygame.K_UP:False, pygame.K_RIGHT:False, pygame.K_LEFT:False, pygame.K_m:False}

    for key in keyArray:
        if key in keysDict:
            keysPressed[keysDict[key]] = True

    return keysPressed

def startServering(myIP):
    HOST = myIP
    PORT = 6432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        return conn
    
def startClienting(opponentIP):
    HOST = opponentIP
    PORT = 6432
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((HOST, PORT))
    return conn
    
def playersPlayOnline(playerNum,currentUsername,opponentName,currentChar1,currentColor1,currentChar2,currentColor2):
    clock = pygame.time.Clock()
    timer = "1:01"
    run = True
    goalScored = False
    tempTickGoal = None
    ball = BALL(WIDTH, HEIGHT)
    character1 = CHARACTER1(WIDTH, HEIGHT, CHAR_OPTIONS[currentChar1]+".png", COLOR_OPTIONS[currentColor1])
    character2 = CHARACTER2(WIDTH, HEIGHT, CHAR_OPTIONS[currentChar2]+".png", COLOR_OPTIONS[currentColor2])
    COMM.getMail()
    myIP,opponentIP = syncPlayers(opponentName)
    if playerNum == 1:
        connection = startServering(myIP)
    elif playerNum == 2:
        connection = startClienting(opponentIP)
    WHISTLE_SOUND.play()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                connection.sendall(b"cancelled")
                return "closed"
            
            if event.type in (ball.goal1Event, ball.goal2Event) and not goalScored:
                goalScored = True
                GOAL_SCORED_SOUND.play()
                tempTickGoal = character1.tick
                if event.type == ball.goal1Event:
                    character2.goals += 1
                else:
                    character1.goals += 1
                    
        if character1.tick%60 == 0 and not goalScored:
            timer = updateTime(timer)

        if isinstance(tempTickGoal,int) and character1.tick - tempTickGoal == 120:
            character1.resetPosition()
            character2.resetPosition()
            ball = BALL(WIDTH, HEIGHT)
            tempTickGoal = None
            goalScored = False
            
        pressed = pygame.key.get_pressed()
        buttons = [pygame.key.name(k) for k,v in enumerate(pressed) if v]
        if playerNum == 1:
            keysPressed = figureOutKeysP1(buttons)
        elif playerNum == 2:
            keysPressed = figureOutKeysP2(buttons)
        stringVer = str(keysPressed).encode()
        connection.sendall(stringVer)
        try:
            otherPlayerPressed = eval(connection.recv(1024).decode())
        except:
            connection.sendall(b'cancelled')
            return "cancelled"
        keysPressed.update(otherPlayerPressed)
        character1.handleMovement(keysPressed, WIDTH, HEIGHT, ball, character2)
        character2.handleMovement(keysPressed, WIDTH, HEIGHT, ball, character1)
        ball.normalMove(WIDTH, HEIGHT)
        if playerNum == 1:
            drawGame(ball, character1, character2, timer, goalScored, currentChar1, currentColor1, currentChar2, currentColor2, currentUsername, opponentName)
        elif playerNum == 2:
            drawGame(ball, character1, character2, timer, goalScored, currentChar1, currentColor1, currentChar2, currentColor2, opponentName, currentUsername)

    if timer == "0:00":
            if character1.goals > character2.goals or character2.goals > character1.goals:
                if character1.goals > character2.goals:
                    winnerNum = 1
                else:
                    winnerNum = 2
                winnerText = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 200).render("Player " + str(winnerNum) + " wins!", 1, WHITE)
            else:
                winnerText = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 300).render("DRAW", 1, WHITE)
            WIN.blit(winnerText, (1536//2 - winnerText.get_width()//2, 432 - winnerText.get_height()//2 - 50))
            pygame.display.update()
            time.sleep(3)
            return "done"



def main(loggedIn = False, currentUsername = ""):
    global people
    clock = pygame.time.Clock()
    timer = "1:01"
    run = True
    goalScored = False
    tempTickGoal = None
    menu = True
    informationClicked = False
    charSelectLocal = False
    charSelectOnline = False
    playOnline = False
    playOnlineMenu = False
    loginScreen = True
    currentUsername = currentUsername
    currentPassword = ""
    usernameBoxClicked = True
    passwordBoxClicked = False
    if not loggedIn:
        drawLogin(currentUsername,currentPassword, usernameBoxClicked, passwordBoxClicked)
        # while loginScreen:
        #     clock.tick(60)
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             pygame.quit()
        #             return
        #         elif event.type == pygame.MOUSEBUTTONDOWN:
        #             x,y = event.pos
        #             if USERNAME_RECT.collidepoint(x,y):
        #                 usernameBoxClicked = True
        #                 passwordBoxClicked = False
                        
        #             elif PASSWORD_RECT.collidepoint(x,y):
        #                 usernameBoxClicked = False
        #                 passwordBoxClicked = True
                        
        #             else:
        #                 usernameBoxClicked = False
        #                 passwordBoxClicked = False

        #             if LOGIN_BUTTON_RECT.collidepoint(x,y):
        #                 BUTTON_SOUND.play()
        #                 if COMM.login(currentUsername, currentPassword):
        #                     loginScreen = False
        #                     WIN.blit(WELCOME_LOGIN, (WIDTH//2 - WELCOME_LOGIN.get_width()//2, 500))
        #                     pygame.display.update()
        #                     time.sleep(1)
        #                 else:
        #                     drawLogin(currentUsername,currentPassword, usernameBoxClicked, passwordBoxClicked)
        #                     WIN.blit(INCORRECT_LOGIN, (WIDTH//2 - INCORRECT_LOGIN.get_width()//2, 500))
        #                     pygame.display.update()
        #                     break
        #             drawLogin(currentUsername,currentPassword, usernameBoxClicked, passwordBoxClicked)

        #         elif event.type == pygame.KEYDOWN :
        #             if event.key != pygame.K_RETURN and event.key != pygame.K_TAB:
        #                 if usernameBoxClicked:
        #                     if event.key == pygame.K_BACKSPACE and len(currentUsername) > 0:
        #                         currentUsername = currentUsername[:-1]
        #                     elif len(currentUsername) < 10 and not event.key == pygame.K_BACKSPACE:
        #                         currentUsername += event.unicode
        #                 elif passwordBoxClicked:
        #                     if event.key == pygame.K_BACKSPACE and len(currentPassword) > 0:
        #                         currentPassword = currentPassword[:-1]
        #                     elif len(currentPassword) < 10 and not event.key == pygame.K_BACKSPACE:
        #                         currentPassword += event.unicode
        #                 drawLogin(currentUsername,currentPassword, usernameBoxClicked, passwordBoxClicked)
        #             else:
        #                 if usernameBoxClicked:
        #                     usernameBoxClicked = False
        #                     passwordBoxClicked = True
        #                     drawLogin(currentUsername,currentPassword, usernameBoxClicked, passwordBoxClicked)
        #                 elif COMM.login(currentUsername, currentPassword):
        #                     loggedIn = True
        #                     loginScreen = False
        #                     WIN.blit(WELCOME_LOGIN, (WIDTH//2 - WELCOME_LOGIN.get_width()//2, 500))
        #                     pygame.display.update()
        #                     time.sleep(1)
        #                 else:
        #                     drawLogin(currentUsername,currentPassword, usernameBoxClicked, passwordBoxClicked)
        #                     WIN.blit(INCORRECT_LOGIN, (WIDTH//2 - INCORRECT_LOGIN.get_width()//2, 500))
        #                     pygame.display.update()
                              
    drawMenu()
    inviteLastChecked = 0
    
    menuTick = 0
    menuTick += 1
    playLocal = False
    while menu:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                distFromPlayLocal = math.sqrt((x - (WIDTH//2 - 150))**2 + (y - (HEIGHT//2 + 100))**2)
                distFromPlayOnline = math.sqrt((x - (WIDTH//2 + 150))**2 + (y - (HEIGHT//2 + 100))**2)
                distFromInfo = math.sqrt((x - (WIDTH-50))**2 + (y - 50)**2)
                if distFromPlayLocal <= 100:
                    BUTTON_SOUND.play()
                    charSelectLocal = True

                if distFromPlayOnline <= 100:
                    BUTTON_SOUND.play()
                    playOnlineMenu = False  #True  - Changed so that game can be played when server is down
                    
                elif distFromInfo <= 50:
                    informationClicked = True
                    BUTTON_SOUND.play()


        if informationClicked:
            clicked = False
            drawInfo()
            while not clicked:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        clicked = True
                        informationClicked = False
                        drawMenu()

        if charSelectLocal:
            runCharSelect = True
            currentChar1 = 0
            currentColor1 = 0
            currentChar2 = 0
            currentColor2 = 0
            drawCharSelect(currentChar1,currentColor1,currentChar2,currentColor2)
            while runCharSelect:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x,y = event.pos
                        distFrom11 = math.sqrt((x - 395)**2 + (y - 330)**2)
                        distFrom12 = math.sqrt((x - 705)**2 + (y - 330)**2)
                        distFrom13 = math.sqrt((x - 895)**2 + (y - 330)**2)
                        distFrom14 = math.sqrt((x - 1205)**2 + (y - 330)**2)
                        distFrom21 = math.sqrt((x - 395)**2 + (y - 530)**2)
                        distFrom22 = math.sqrt((x - 705)**2 + (y - 530)**2)
                        distFrom23 = math.sqrt((x - 895)**2 + (y - 530)**2)
                        distFrom24 = math.sqrt((x - 1205)**2 + (y - 530)**2)
                        distFromBack = math.sqrt((x - 240)**2 + (y - 130)**2)
                        onStart = (x > WIDTH//2 - START_BUTTON.get_width()//2 and
                        x < WIDTH//2 - START_BUTTON.get_width()//2 + 350 and y > 600 and y < 700)
                        if distFrom11 < 25:
                            BUTTON_SOUND.play()
                            if currentChar1 - 1 == -1:
                                currentChar1 = len(CHAR_OPTIONS) - 1
                            else:
                                currentChar1 -= 1

                        elif distFrom12 < 25:
                            BUTTON_SOUND.play()
                            if currentChar1 + 1 == len(CHAR_OPTIONS):
                                currentChar1 = 0
                            else:
                                currentChar1 += 1

                        elif distFrom13 < 25:
                            BUTTON_SOUND.play()
                            if currentChar2 - 1 == -1:
                                currentChar2 = len(CHAR_OPTIONS) - 1
                            else:
                                currentChar2 -= 1
                                
                        elif distFrom14 < 25:
                            BUTTON_SOUND.play()
                            if currentChar2 + 1 == len(CHAR_OPTIONS):
                                currentChar2 = 0
                            else:
                                currentChar2 += 1
                                
                        elif distFrom21 < 25:
                            BUTTON_SOUND.play()
                            if currentColor1 - 1 == -1:
                                currentColor1 = len(COLOR_OPTIONS) - 1
                            else:
                                currentColor1 -= 1
                                
                        elif distFrom22 < 25:
                            BUTTON_SOUND.play()
                            if currentColor1 + 1 == len(COLOR_OPTIONS):
                                currentColor1 = 0
                            else:
                                currentColor1 += 1

                        elif distFrom23 < 25:
                            BUTTON_SOUND.play()
                            if currentColor2 - 1 == -1:
                                currentColor2 = len(COLOR_OPTIONS) - 1
                            else:
                                currentColor2 -= 1

                        elif distFrom24 < 25:
                            BUTTON_SOUND.play()
                            if currentColor2 + 1 == len(COLOR_OPTIONS):
                                currentColor2 = 0
                            else:
                                currentColor2 += 1
                                
                        elif onStart:
                            BUTTON_SOUND.play()
                            time.sleep(1)
                            runCharSelect = False
                            menu = False
                            playLocal = True
                        
                        elif distFromBack < 50:
                            runCharSelect = False
                            charSelectLocal = False
                            drawMenu()
                        if distFromBack >= 50:
                            drawCharSelect(currentChar1,currentColor1,currentChar2,currentColor2)
                            
        if playOnlineMenu:
            runOnline = True
            waiting = False
            currentFriend = ""
            friendBoxClicked = True
            drawOnline(currentFriend,friendBoxClicked,waiting)
            while runOnline:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        if waiting:
                            COMM.sendMessage(currentFriend,"INVITE DONE")
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x,y = event.pos
                        distFromBack = math.sqrt((x - 370)**2 + (y - 170)**2)
                        if FRIEND_RECT.collidepoint(x,y) and not waiting:
                            friendBoxClicked = True
                            drawOnline(currentFriend,friendBoxClicked,waiting)
                            
                        elif INVITE_BUTTON_RECT.collidepoint(x,y) and not waiting:
                            BUTTON_SOUND.play()
                            check = (checkFriend(currentFriend,currentUsername))
                            if check[0]:
                                waiting = True
                            if check[1]:
                                inviteButton = True
                            
                        elif distFromBack < 50:
                            runOnline = False
                            playOnlineMenu = False
                            COMM.sendMessage(currentFriend,"INVITE DONE")
                            drawMenu()
                            
                        else:
                            friendBoxClicked = False
                            drawOnline(currentFriend,friendBoxClicked,waiting)
                            
                        if REQUEST_BUTTON_RECT.collidepoint(x,y) and not waiting and inviteButton:
                            BUTTON_SOUND.play()
                            WIN.blit(REQUEST_SUCCESSFUL, (WIDTH//2 - REQUEST_SUCCESSFUL.get_width()//2, 450))
                            COMM.sendFriendRequest(currentFriend)
                            pygame.display.update()

                        else:
                            inviteButton = False
                            

                        
                    elif event.type == pygame.KEYDOWN :
                        if event.key != pygame.K_RETURN:
                            if friendBoxClicked:
                                if event.key == pygame.K_BACKSPACE and len(currentFriend) > 0:
                                    currentFriend = currentFriend[:-1]
                                elif len(currentFriend) < 10 and not event.key == pygame.K_BACKSPACE:
                                    currentFriend += event.unicode
                                drawOnline(currentFriend,friendBoxClicked,waiting)
                        elif not waiting:
                            friendBoxClicked = False
                            check = (checkFriend(currentFriend,currentUsername))
                            if check[0]:
                                waiting = True
                            if check[1]:
                                inviteButton = True
                                
                # if abs(menuTick - inviteLastChecked) == 60 and waiting:
                #     inviteLastChecked = menuTick
                #     reply = getReplyInvitation(currentFriend)
                #     if reply == "accepted":
                #         playOnline = True
                #         playerNum = 1
                #         menu = False
                #         runOnline = False
                #     elif reply == "rejected":
                #         waiting = False
                #         inviteRejectedString = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 30).render("Invite rejected by "+currentFriend+".", 1, (WHITE))
                #         COMM.sendMessage(currentFriend,"INVITE DONE")
                #         drawOnline(currentFriend,friendBoxClicked,waiting)
                #         WIN.blit(inviteRejectedString, (WIDTH//2 - inviteRejectedString.get_width()//2, 450))
                #         pygame.display.update()
                # elif abs(menuTick - inviteLastChecked) == 60:
                    inviteLastChecked = menuTick
                menuTick += 1  
                
                            
                    
        if abs(menuTick - inviteLastChecked) == 60:
            requests = COMM.getRequests()
            for request in requests:
                clicked = False
                drawFriendRequest(request)
                while not clicked:
                    clock.tick(60)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            x,y = event.pos
                            if FRIEND_ACCEPT_BUTTON_RECT.collidepoint(x,y):
                                BUTTON_SOUND.play()
                                COMM.acceptFriendRequest(request)
                                clicked = True
                                drawMenu()       
                            
        # if abs(menuTick - inviteLastChecked) == 60:
        #     inviteLastChecked = menuTick
        #     opponentName = checkForInvite()
        #     if opponentName != "Nobody":
        #         runInvitation = True
        #         INVITE_SOUND.play()
        #         drawGameInvite(opponentName)
        #     else:
        #         runInvitation = False
        #     while runInvitation:
        #         clock.tick(60)
        #         for event in pygame.event.get():
        #             if event.type == pygame.QUIT:
        #                 pygame.quit()
        #                 return
        #             elif event.type == pygame.MOUSEBUTTONDOWN:
        #                 x,y = event.pos
        #                 if ACCEPT_BUTTON_RECT.collidepoint(x,y):
        #                     BUTTON_SOUND.play()
        #                     COMM.sendMessage(opponentName,"INVITE ACCEPTED")
        #                     playOnline = True
        #                     playerNum = 2
        #                     menu = False
        #                     runInvitation = False
        #                 elif REJECT_BUTTON_RECT.collidepoint(x,y):
        #                     BUTTON_SOUND.play()
        #                     runInvitation = False
        #                     COMM.sendMessage(opponentName,"INVITE REJECTED")
        #                     drawMenu()
        menuTick += 1                
                            
                            
                    
    if playOnline:
        if playerNum == 1:
            opponentName = currentFriend
            retValue = charSelectPlayer1(opponentName)
            people = {}
            if retValue == "cancelled":
                main(True,currentUsername)
            elif retValue == "closed":
                return
            elif retValue[0] == "done":
                returnVal = playersPlayOnline(playerNum,currentUsername,opponentName,retValue[1],retValue[2],retValue[3],retValue[4])
                if returnVal == "closed":
                    return
                elif returnVal == "cancelled" or returnVal == "done":
                    main(True,currentUsername)
            
        elif playerNum == 2:
            retValue = charSelectPlayer2(opponentName)
            people = {}
            if retValue == "cancelled":
                main(True,currentUsername)
            elif retValue == "closed":
                return
            elif retValue[0] == "done":
                returnVal = playersPlayOnline(playerNum,currentUsername,opponentName,retValue[1],retValue[2],retValue[3],retValue[4])
                if returnVal == "closed":
                    return
                elif returnVal == "cancelled" or returnVal == "done":
                    main(True,currentUsername)
    if playLocal:
        ball = BALL(WIDTH, HEIGHT)
        character1 = CHARACTER1(WIDTH, HEIGHT, CHAR_OPTIONS[currentChar1]+".png", COLOR_OPTIONS[currentColor1])
        character2 = CHARACTER2(WIDTH, HEIGHT, CHAR_OPTIONS[currentChar2]+".png", COLOR_OPTIONS[currentColor2])
        WHISTLE_SOUND.play()
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                if event.type in (ball.goal1Event, ball.goal2Event) and not goalScored:
                    goalScored = True
                    GOAL_SCORED_SOUND.play()
                    tempTickGoal = character1.tick
                    if event.type == ball.goal1Event:
                        character2.goals += 1
                    else:
                        character1.goals += 1
                        
            if character1.tick%60 == 0 and not goalScored:
                timer = updateTime(timer)

            if isinstance(tempTickGoal,int) and character1.tick - tempTickGoal == 120:
                character1.resetPosition()
                character2.resetPosition()
                ball = BALL(WIDTH, HEIGHT)
                tempTickGoal = None
                goalScored = False
                
            keysPressed = pygame.key.get_pressed()
            character1.handleMovement(keysPressed, WIDTH, HEIGHT, ball, character2)
            character2.handleMovement(keysPressed, WIDTH, HEIGHT, ball, character1)
            ball.normalMove(WIDTH, HEIGHT)
            drawGame(ball, character1, character2, timer, goalScored, currentChar1, currentColor1, currentChar2, currentColor2)
            if timer == "0:00":
                if character1.goals > character2.goals or character2.goals > character1.goals:
                    if character1.goals > character2.goals:
                        winnerNum = 1
                    else:
                        winnerNum = 2
                    winnerText = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 200).render("Player " + str(winnerNum) + " wins!", 1, WHITE)
                else:
                    winnerText = pygame.font.Font('Berlin Sans FB Demi Bold.ttf', 300).render("DRAW", 1, WHITE)
                WIN.blit(winnerText, (1536//2 - winnerText.get_width()//2, 432 - winnerText.get_height()//2 - 50))
                pygame.display.update()
                time.sleep(3)
                main(True, currentUsername)
        
main()
print("Thanks for playing!")
