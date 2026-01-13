import pygame
import random
import math
import time
import sys
sys.setrecursionlimit(3000)

class Bot:
    def __init__(self, board):
        pass
        self.board = board
        self.noFlags = False
        self.mines = []
        self.guess = False
        self.makeGuess = False

    def calculateMove(self, board):

        newOpens = []
        newMines = []
        adjs = []

        flagCount = 0
        for j in range(0, len(board)):
            for i in range(0, len(board[j])):
                if board[j][i] == "f":
                    flagCount = flagCount + 1
        flagCount = len(mines) - flagCount

        if flagCount == 0 and not(gameOver):
            result = [[],[]]
            for j in range(0, len(board)):
                for i in range(0, len(board[j])):
                    if board[j][i] == "o":
                        result[0].append([j,i])
            return result

        for j in range (len(board)):
            row = []
            for i in range(len(board[j])):
                adj = []
                for m in range(-1,2):
                        for n in range(-1,2):
                            if not(n == 0 and m == 0) and i + m > -1 and j + n > -1 and i + m < len(board[j]) and j + n < len(board):
                                adj.append([board[j + n][i + m], [j + n, i + m]])
                row.append(adj)
            adjs.append(row)
        
        
        for j in range(len(board)):
            for i in range(len(board[j])):
                #for each tile
                mineCount = 0
                openCount = 0
                adj = adjs[j][i]
                adjCount = len(adj)
                tile = board[j][i]
                #get the mine and open counts for the adj tiles
                for k in adj:
                    if k[0] == "f":
                        mineCount = mineCount + 1
                    if k[0] == "o":
                        openCount = openCount + 1
                
                #if the mine count equals tile then click all open adj tiles
                try:
                    if mineCount == int(tile) and tile != "0":
                        for k in adj:
                            if k[0] == "o":
                                newOpens.append(k[1])
                except:
                    pass
                
                try:
                    if openCount == int(tile) - mineCount and tile != "0":
                        for k in adj:
                            if k[0] == "o":
                                newMines.append(k[1])
                except:
                    pass

        #if no new moves are found with the 2 basic rules
        if len(newOpens) == 0 and len(newMines) == 0:
            openSubsets = []
            for j in range(len(adjs)):
                for i in range(len(adjs[j])):
                    if board[j][i] != "0" and board[j][i] != "o" and board[j][i] != "f" and board[j][i] != "x":
                        openSubset = [int(board[j][i])]
                        for k in range(len(adjs[j][i])):
                            if adjs[j][i][k][0] == "o":
                                openSubset.append(adjs[j][i][k][1])
                            if adjs[j][i][k][0] == "f":
                                openSubset[0] = openSubset[0] - 1
                        if len(openSubset) > 1:
                            openSubsets.append(openSubset)

            #remove duplicate
            fixedSets = removeSubsets(openSubsets)
            while fixedSets != openSubsets:
                openSubsets = fixedSets
                fixedSets = removeSubsets(openSubsets)


            emptySubsets = []
            for o in openSubsets:
                if o[0] == 0:
                    emptySubsets.append(o[1:])
                    openSubsets.remove(o)

            for e in emptySubsets:      
                for t in e:
                    newOpens.append(t)

            for j in range(len(board)):
                for i in range(len(board[j])): 
                    #for each tile
                    mineCount = 0
                    openCount = 0
                    adj = adjs[j][i]
                    adjCount = len(adj)
                    tile = board[j][i]
                    #get the mine and open counts for the adj tiles
                    for k in adj:
                        if k[0] == "f":
                            mineCount = mineCount + 1
                        if k[0] == "o":
                            openCount = openCount + 1
                    
                    #find all valid open subsets
                    validOpenSubsets = []
                    adjTileLocation = []
                    for a in adj:
                        if a[0] == "o":
                            adjTileLocation.append(a[1])
                    for o in openSubsets:
                        isValid = True
                        for t in o[1:]:
                            if not(isIn(t, adjTileLocation)):
                                isValid = False
                                break
                        if isValid and len(o) - 1 != len(adjTileLocation):
                            validOpenSubsets.append(o)
                    
                    usedSubsets = []
                    for o in validOpenSubsets:
                        mineCount = mineCount + o[0]
                        openCount = openCount - (len(o)-1)
                        for t in o[1:]:
                            usedSubsets.append(t)
                        #only use one item from validOpenSubsets
                        break
                    
                    try:
                        if mineCount == int(tile) and tile != "0":
                            for k in adj:
                                if k[0] == "o" and not(isIn(k[1], usedSubsets)):
                                    newOpens.append(k[1])
                    except:
                        pass
                    
                    try:
                        if openCount == int(tile) - mineCount and tile != "0":
                            for k in adj:
                                if k[0] == "o" and not(isIn(k[1], usedSubsets)):
                                    newMines.append(k[1])
                    except:
                        pass


        return [newOpens,newMines]
    
    def makeMove(self, board):
        moves = self.calculateMove(board)
        opens = removeDuplicates(moves[0])
        mines = removeDuplicates(moves[1])
        if len(mines) == 0 and len(opens) == 0 and self.makeGuess:
            randomMove()
        for m in opens:
            clickTile(m[0], m[1], 1)
        for m in mines:
            clickTile(m[0], m[1], 3)
    


def createBoard(w,h,n):
    result = []

    for i in range(0,w):
        row = []
        for j in range(0,h):
            row.append("o")
        result.append(row)
  
    for i in random.sample(range(0,w * h - 1),n):
        result[math.floor(i / h)][((i + 1) % h) - 1] = "x"

    return result

def printBoard(b):
    for i in b:
        print(i)

def initGame(w,h,n):
    global board
    global mines
    global tileSize
    global viewArea 
    global screenSize
    global clickedOpenTiles
    global counter
    global currentTime
    global errorTiles
    clickedOpenTiles = 0
    board = createBoard(w,h,n)
    mines = []
    counter = 0
    currentTime = time.time()
    errorTiles = []
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] == 'x':
                mines.append([i,j])
                board[i][j] = "o"
    
    h = len(board) * tileSize
    w = len(board[0]) * tileSize
    #viewArea = [(screenSize[0] - w)/2,(screenSize[1] - h)/2]
    viewArea = [(screenSize[0] - w)/2,tileSize*4]

def drawTile(x,y,type):
    tile = pygame.image.load('/Users/chrisguzun/Desktop/MinesweeperPython/minesweeperIcons/minesweeperIcons' + type + '.png').convert()
    tile = pygame.transform.scale(tile, (tileSize, tileSize))
    screen.blit(tile, (x,y))

def drawBorder(x,y,w,h,t):
    borderScale = tileSize * 0.75
    #pygame.draw.rect(screen, pygame.Color(38,42,47), (x - t, y - t, w + t + t, h + t + t))

    pygame.draw.rect(screen, pygame.Color(70,76,83), (x, y - tileSize * (137/40) + borderScale, w - tileSize * (2/40), borderScale*2.6))
    pygame.draw.rect(screen, pygame.Color(0,0,0), (x + tileSize * (10/40), y - tileSize * (127/40) + borderScale, tileSize * (100/40), tileSize * (60/40)))
    pygame.draw.rect(screen, pygame.Color(0,0,0), (x + w - tileSize * (110/40), y - tileSize * (127/40) + borderScale, tileSize * (100/40), tileSize * (60/40)))

    flagCount = 0
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] == "f":
                flagCount = flagCount + 1
    flagCount = str(gameSettings[2] - flagCount)
    if len(flagCount) == 1:
        flagCount = "00" + flagCount
    elif len(flagCount) == 2:
        flagCount = "0" + flagCount
    elif len(flagCount) > 3:
        flagCount = "999"

    my_font = pygame.font.SysFont('vcrosdmono1001', int(tileSize * 1.3))

    text_surface = my_font.render(flagCount, False, (255,0,0))
    screen.blit(text_surface,(x + tileSize * (15/40), y - tileSize * (122/40) + borderScale))

    counterString = str(counter)
    if len(counterString) == 1:
        counterString = "00" + counterString
    elif len(counterString) == 2:
        counterString = "0" + counterString
    elif len(counterString) > 3:
        counterString = "999"

    text_surface = my_font.render(counterString, False, (255,0,0))
    screen.blit(text_surface,(x + w - tileSize * (105/40), y - tileSize * (122/40) + borderScale))

    #drawSevenSegDisplay(0,(x + tileSize * (10/40), y - tileSize * (127/40) + borderScale, tileSize * (100/40), tileSize * (60/40)),0)

    borderVertical = pygame.image.load('/Users/chrisguzun/Desktop/MinesweeperPython/minesweeperIcons/minesweeperBorderVertical.png').convert()
    borderVertical = pygame.transform.scale(borderVertical, (borderScale, tileSize))
    for i in range(0, len(board)):
        screen.blit(borderVertical, (x - borderScale, y + i * tileSize))
        screen.blit(borderVertical, (x + w, y + i * tileSize))
    
    borderHorizontal = pygame.image.load('/Users/chrisguzun/Desktop/MinesweeperPython/minesweeperIcons/minesweeperBorderHorizontal.png').convert()
    borderHorizontal = pygame.transform.scale(borderHorizontal, (tileSize, borderScale))
    for i in range(0, len(board[0])):
        screen.blit(borderHorizontal, (x + i * tileSize, y - tileSize * (137/40)))
        screen.blit(borderHorizontal, (x + i * tileSize, y - borderScale + 20/tileSize))
        screen.blit(borderHorizontal, (x + i * tileSize, y + h))
    
    borderTopLeft = pygame.image.load('/Users/chrisguzun/Desktop/MinesweeperPython/minesweeperIcons/minesweeperBorderTopLeft.png').convert()
    borderTopLeft = pygame.transform.scale(borderTopLeft, (tileSize * (32/40), tileSize * (137/40)))
    screen.blit(borderTopLeft, (x - borderScale, y - tileSize * (137/40)))

    borderTopRight = pygame.image.load('/Users/chrisguzun/Desktop/MinesweeperPython/minesweeperIcons/minesweeperBorderTopRight.png').convert()
    borderTopRight = pygame.transform.scale(borderTopRight, (tileSize * (32/40), tileSize * (137/40)))
    screen.blit(borderTopRight, (x + w - tileSize * (2/40), y - tileSize * (137/40)))

    borderBottomLeft = pygame.image.load('/Users/chrisguzun/Desktop/MinesweeperPython/minesweeperIcons/minesweeperBorderBottomLeft.png').convert()
    borderBottomLeft = pygame.transform.scale(borderBottomLeft, (borderScale, borderScale))
    screen.blit(borderBottomLeft, (x - borderScale, y + h - tileSize * (2/40)))
    
    borderBottomRight = pygame.image.load('/Users/chrisguzun/Desktop/MinesweeperPython/minesweeperIcons/minesweeperBorderBottomRight.png').convert()
    borderBottomRight = pygame.transform.scale(borderBottomRight, (borderScale, borderScale))
    screen.blit(borderBottomRight, (x + w, y + h - tileSize * (2/40)))

    iconScale = tileSize * (65/40)
    if allowBot:
        if gameOver:
            if win:
                topIcon = pygame.image.load('/Users/chrisguzun/Desktop/MinesweeperPython/minesweeperIcons/minesweeperIconsWinBot.png').convert()
            else:
                topIcon = pygame.image.load('/Users/chrisguzun/Desktop/MinesweeperPython/minesweeperIcons/minesweeperIconsLoseBot.png').convert()
        else:
            topIcon = pygame.image.load('/Users/chrisguzun/Desktop/MinesweeperPython/minesweeperIcons/minesweeperIconsOngoingBot.png').convert()
    else:
        if gameOver:
            if win:
                topIcon = pygame.image.load('/Users/chrisguzun/Desktop/MinesweeperPython/minesweeperIcons/minesweeperIconsWin.png').convert()
            else:
                topIcon = pygame.image.load('/Users/chrisguzun/Desktop/MinesweeperPython/minesweeperIcons/minesweeperIconsLose.png').convert()
        else:
            topIcon = pygame.image.load('/Users/chrisguzun/Desktop/MinesweeperPython/minesweeperIcons/minesweeperIconsOngoing.png').convert()
    topIcon = pygame.transform.scale(topIcon, (iconScale, iconScale))
    screen.blit(topIcon, (x + w / 2 - iconScale/2, y - iconScale - iconScale/2 - tileSize * (2/40), iconScale, iconScale))

def drawMenu(focus):
    global menuWidth
    global menuHeight
    global menuCorner
    menuBackgroundColor = (30,38,46)
    menuBorderColor = (70,78,86)
    borderWidth = 10
    pygame.draw.rect(screen, menuBorderColor, (menuCorner[0] - borderWidth,menuCorner[1] - borderWidth,menuWidth + 2*borderWidth,menuHeight + 2*borderWidth))
    pygame.draw.rect(screen, menuBackgroundColor, (menuCorner[0],menuCorner[1],menuWidth,menuHeight))

    my_font = pygame.font.SysFont('vcrosdmono1001', int(tileSize * 1))

    text_surface = my_font.render("Height", False, (255,255,255))
    screen.blit(text_surface,(menuCorner[0] + 20, menuCorner[1] + 40))

    text_surface = my_font.render("Width", False, (255,255,255))
    screen.blit(text_surface,(menuCorner[0] + 20, menuCorner[1] + 90))

    text_surface = my_font.render("Mines", False, (255,255,255))
    screen.blit(text_surface,(menuCorner[0] + 20, menuCorner[1] + 140))

    if focus != None:
        pygame.draw.rect(screen, (255,255,255), (menuCorner[0] + 300 - 5, menuCorner[1] + 40 + focus*50 - 5, 90,50))

    pygame.draw.rect(screen, menuBorderColor, (menuCorner[0] + 300, menuCorner[1] + 40, 80,40))
    pygame.draw.rect(screen, menuBorderColor, (menuCorner[0] + 300, menuCorner[1] + 90, 80,40))
    pygame.draw.rect(screen, menuBorderColor, (menuCorner[0] + 300, menuCorner[1] + 140, 80,40))

    settingStrings = [None, None, None]
    if newSettings[0] == None:
        settingStrings[0] = str(gameSettings[0])
    else:
        settingStrings[0] = newSettings[0]
    
    if newSettings[1] == None:
        settingStrings[1] = str(gameSettings[1])
    else:
        settingStrings[1] = newSettings[1]
    
    if newSettings[2] == None:
        settingStrings[2] = str(int(gameSettings[2]))
    else:
        settingStrings[2] = newSettings[2]
    
    text_surface = my_font.render(settingStrings[0], False, (255,255,255))
    screen.blit(text_surface,(menuCorner[0] + 300, menuCorner[1] + 40))

    text_surface = my_font.render(settingStrings[1], False, (255,255,255))
    screen.blit(text_surface,(menuCorner[0] + 300, menuCorner[1] + 90))
    
    text_surface = my_font.render(settingStrings[2], False, (255,255,255))
    screen.blit(text_surface,(menuCorner[0] + 300, menuCorner[1] + 140))

def drawSevenSegDisplay(n, p, s):
    a = tileSize * (5/40)
    b = tileSize * (10/40)
    pointsList = [[0, 0], [500, 0], [500, 500]]
    for i in pointsList:
        i[0] = i[0]/tileSize + p[0]
        i[1] = i[1]/tileSize + p[1]
    pygame.draw.polygon(screen, (255, 0, 0), pointsList)

def isIn(x,A):
    for i in A:
        if x == i:
            return True
    return False

def clickTile(i,j,button):
    global gameOver
    global clickedOpenTiles
    global win
    global errorTiles
    #if game is not over
    if not(gameOver):
        #if left click and tile is not a flag
        if button == 1 and board[i][j] != "f":
            #if tile is a mine end game
            if isIn([i,j], mines):
                for n in mines:
                    board[n[0]][n[1]] = "x"
                gameOver = True
                win = False
                playSound("bomb")
                errorTiles.append([j,i])
                for i in range(0, len(board)):
                    for j in range(0, len(board[i])):
                        if board[i][j] == "f" and not(isIn([i,j], mines)):
                            errorTiles.append([j,i])
            else:
                #get all adjacent tiles
                adj = []
                for n in range(-1,2):
                    for m in range(-1,2):
                        if not(n == 0 and m == 0) and i + n > -1 and j + m > -1 and i + n < len(board) and j + m < len(board[i]):
                            #adj.append([board[i + n][j + m], [i + n, j + m]])
                            adj.append([i + n, j + m])
                mineCount = 0
                flagCount = 0
                #count flags and mines in adj
                for n in adj:
                    if isIn(n, mines):
                        mineCount = mineCount + 1
                    if board[n[0]][n[1]] == "f":
                        flagCount = flagCount + 1
                #if tile is open display mine count
                if board[i][j] == "o":
                    board[i][j] = str(mineCount)
                    clickedOpenTiles = clickedOpenTiles + 1
                    #if tile is a zero count automatically click all adjacent tiles
                    if mineCount == 0:
                        for n in adj:
                            clickTile(n[0], n[1], 1)
                else:
                    #if flag count equals mine count auto click all adjacent tiles (chording)
                    if int(board[i][j]) == flagCount:
                        for n in adj:
                            if board[n[0]][n[1]] == "o":
                                clickTile(n[0], n[1], 1)
        #if the button is a right click place a flag
        elif button == 3 and (board[i][j] == "f" or board[i][j] == "o"):
            if board[i][j] == "f":
                board[i][j] = "o"
            else:
                board[i][j] = "f"
        #check if all the non mine open tiles have been click, if yes then the game is over
        if clickedOpenTiles == len(board) * len(board[0]) - gameSettings[2]:
            gameOver = True
            win = True
            playSound("win")
            #auto place any unplaced flags
            for n in mines:
                board[n[0]][n[1]] = "f"

def convertKeyToString(k):
    if k == pygame.K_0:
        return "0"
    elif k == pygame.K_1:
        return "1"
    elif k == pygame.K_2:
        return "2"
    elif k == pygame.K_3:
        return "3"
    elif k == pygame.K_4:
        return "4"
    elif k == pygame.K_5:
        return "5"
    elif k == pygame.K_6:
        return "6"
    elif k == pygame.K_7:
        return "7"
    elif k == pygame.K_8:
        return "8"
    elif k == pygame.K_9:
        return "9"
    else:
        return None

def removeDuplicates(L):
    result = []
    for i in L:
        if not(isIn(i,result)):
            result.append(i)
    return result

def playSound(sound):
    if unmuteSounds:
        clickSound = pygame.mixer.Sound("/Users/chrisguzun/Desktop/MinesweeperPython/minesweeperSounds/" + sound + ".mp3")
        pygame.mixer.Sound.play(clickSound)

def botMove():
    bot.makeMove(board)

def removeSubsets(subsets):
    for o in subsets:
        for u in subsets:
            if o != u:
                if len(o) == len(u):
                    sameSet = True
                    for t in o[1:]:
                        if not(isIn(t, u)):
                            sameSet = False
                            break
                    if sameSet:
                        o[0] = max(o[0], u[0])
                        subsets.remove(u)
                    continue

                if len(o) < len(u):
                    smaller = o
                    larger = u
                else:
                    smaller = u
                    larger = o
                        
                SisInL = True
                for t in smaller[1:]:
                    if not(isIn(t, larger)):
                        SisInL = False
                        break
                        
                if SisInL:
                    for t in larger[1:]:
                        if isIn(t, smaller):
                            larger.remove(t)
                    larger[0] = larger[0] - smaller[0]
                        
                if len(o) < len(u):
                    o = smaller
                    u = larger
                else:
                    u = smaller
                    o = larger

    return removeDuplicates(subsets)

def safeMove():
    options = []
    for j in range(len(board)):
        for i in range(len(board[j])):
            if board[j][i] == "o" and not(isIn([j,i],mines)):
                options.append([j,i])
    if len(options) > 0:
        r = random.choice(options)
        clickTile(r[0], r[1], 1)

def safeStart():
    if not(gameOver):
        safeMove()
        zeroTileCount = 0
        for j in range(len(board)):
            for i in range(len(board[j])):
                if board[j][i] == "0":
                    zeroTileCount = zeroTileCount + 1
                    
        while zeroTileCount == 0:
            safeMove()
            for j in range(len(board)):
                for i in range(len(board[j])):
                    if board[j][i] == "0":
                        zeroTileCount = zeroTileCount + 1 

def randomMove():
    options = []
    for j in range(len(board)):
        for i in range(len(board[j])):
            if board[j][i] == "o":
                options.append([j,i])
    if len(options) > 0:
        r = random.choice(options)
        clickTile(r[0], r[1], 1)

pygame.init()
pygame.font.init()
#print(pygame.font.get_fonts())

global tileSize
global viewArea
global board
global mines
global mouseDown
global keys
global screenSize
global gameOver
global clickedOpenTiles
global mouseDownTimer
global win
global counter
global currentTime
global gameSettings
global errorTiles
global menu
global menuFocus
global menuWidth
global menuHeight
global menuCorner
global bot
global allowBot
tileSize = 40
mouseDown = False
keys = []
mouseDownTimer = 0
tempPos = (0,0)
tempViewArea = (0,0)
screenSize = (pygame.display.Info().current_w,pygame.display.Info().current_h)
gameOver = False
win = False
counter = 0
currentTime = None
gameSettings = [30,30,140]
errorTiles = []
menu = False
menuFocus = None
menuWidth = 400
menuHeight = 300
menuCorner = [screenSize[0]/2 - menuWidth/2, screenSize[1]/2 - menuHeight/2]
newSettings = [None, None, None]
allowBot = False
unmuteSounds = True
botTimer = time.time()
autoRestart = False
highlightOpens = False


initGame(gameSettings[0],gameSettings[1],gameSettings[2])
bot = Bot(board)

screen = pygame.display.set_mode(screenSize,pygame.RESIZABLE)

running = True
while running:

    pygame.draw.rect(screen, (0,0,0), (0, 0, screenSize[0], screenSize[1]))

    if gameOver and autoRestart:
        initGame(gameSettings[0],gameSettings[1],gameSettings[2])
        gameOver = False
        win = False

    h= len(board) * tileSize
    w = len(board[0]) * tileSize
    t = max((screenSize[0] - w)/2, (screenSize[1] - h)/2)
    if t <= 0:
        t = 400
    
    if currentTime == None:
        currentTime = time.time()
    else:
        if time.time() - currentTime > 1:
            currentTime = time.time()
            if not(gameOver):
                counter = counter + 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True
            mouseDownTimer = 0
            tempPos = pygame.mouse.get_pos()
            tempViewArea = viewArea

        if event.type == pygame.MOUSEBUTTONUP:
            mouseDown = False
            mouseDownTimer = 0
            currentPos = pygame.mouse.get_pos()

            if menu:
                for n in range(0, 3):
                    rect = pygame.Rect(menuCorner[0] + 300, menuCorner[1] + 40 + n*50, 80,40)
                    if rect.collidepoint(currentPos):
                        if menuFocus == n:
                            menuFocus = None
                        else:
                            menuFocus = n
            else:
                for i in range(0, len(board)):
                    for j in range(0, len(board[i])):
                        rect = pygame.Rect(j * tileSize + viewArea[0], i * tileSize + viewArea[1], tileSize, tileSize)
                        #if rect.collidepoint(tempPos) and rect.collidepoint(currentPos):
                        if rect.collidepoint(tempPos):
                            clickTile(i,j,event.button)
                            playSound("click")

                iconScale = tileSize * (65/40)
                rect = pygame.Rect(viewArea[0] + w / 2 - iconScale/2, viewArea[1] - iconScale - iconScale/2 - tileSize * (2/40), iconScale, iconScale)
                if rect.collidepoint(tempPos) and rect.collidepoint(currentPos):
                    initGame(gameSettings[0],gameSettings[1],gameSettings[2])
                    gameOver = False
                    win = False
        
        if event.type == pygame.KEYDOWN:
            keys.append(event.key)

            if event.key == pygame.K_m:
                if menu:
                    menu = False
                else:
                    menu = True
            
            if event.key == pygame.K_b:
                if allowBot:
                    allowBot = False
                else:
                    allowBot = True
            
            if event.key == pygame.K_n:
                if unmuteSounds:
                    unmuteSounds = False
                else:
                    unmuteSounds = True

            if event.key == pygame.K_v:
                safeStart()
            
            if event.key == pygame.K_c:
                safeMove()
            
            if event.key == pygame.K_t:
                if autoRestart:
                    autoRestart = False
                else:
                    autoRestart = True
            
            if event.key == pygame.K_r:
                if bot.makeGuess:
                    bot.makeGuess = False
                else:
                    bot.makeGuess = True
            
            if event.key == pygame.K_h:
                if highlightOpens:
                    highlightOpens = False
                else:
                    highlightOpens = True

            if event.key == pygame.K_SPACE:
                initGame(gameSettings[0],gameSettings[1],gameSettings[2])
                gameOver = False
                win = False
            
            if menuFocus != None:
                validKeys = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, 
                             pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_BACKSPACE, pygame.K_RETURN]
                keyString = convertKeyToString(event.key)
                if isIn(event.key, validKeys):
                    if event.key == pygame.K_BACKSPACE:
                        if newSettings[menuFocus] == None:
                            newSettings[menuFocus] = str(gameSettings[menuFocus])[0:-1]
                        else:
                            newSettings[menuFocus] = newSettings[menuFocus][0:-1]
                    elif event.key == pygame.K_RETURN:
                        if newSettings[0] == None:
                            newSettings[0] = str(gameSettings[0])
                        if newSettings[1] == None:
                            newSettings[1] = str(gameSettings[1])
                        if newSettings[2] == None:
                            newSettings[2] = str(gameSettings[2])
                        gameSettings = [int(newSettings[0]), int(newSettings[1]), int(newSettings[2])]
                        initGame(gameSettings[0],gameSettings[1],gameSettings[2])
                        gameOver = False
                        win = False
                        newSettings = [None, None, None]
                        menu = False
                    else:
                        if newSettings[menuFocus] == None:
                            newSettings[menuFocus] = str(gameSettings[menuFocus]) + keyString
                        else:
                            newSettings[menuFocus] = newSettings[menuFocus] + keyString

        
        if event.type == pygame.KEYUP:
            keys.remove(event.key)
    
    if mouseDown:
        pos=pygame.mouse.get_pos()
        mouseDownTimer = mouseDownTimer + 1
        #viewArea = [tempViewArea[0] - tempPos[0] + pos[0],tempViewArea[1] - tempPos[1] + pos[1]]
    
    borderScale = tileSize * 0.75
    leftBound = viewArea[0] - borderScale
    rightBound = viewArea[0] + w + borderScale
    topBound = viewArea[1] - 4.5*borderScale
    bottomBound = viewArea[1] + h + borderScale
    scrollSpeed = 20
    for i in keys:
        if i == pygame.K_w:
            viewArea[1] = viewArea[1] + scrollSpeed
        if i == pygame.K_s:
            viewArea[1] = viewArea[1] - scrollSpeed
        if i == pygame.K_a:
            viewArea[0] = viewArea[0] + scrollSpeed
        if i == pygame.K_d:
            viewArea[0] = viewArea[0] - scrollSpeed
        if i == pygame.K_UP:
            tileSize = tileSize + 1
            viewArea = [(screenSize[0] - w)/2,tileSize*4]
        if i == pygame.K_DOWN:
            tileSize = tileSize - 1
            viewArea = [(screenSize[0] - w)/2,tileSize*4]

    """es = tileSize * (30/40)
    eb = tileSize * (130/40)
    if w + 2 * borderScale >= screenSize[0]:
        if viewArea[0] > es:
            viewArea[0] = es
        elif viewArea[0] < screenSize[0] - w - es:
            viewArea[0] = screenSize[0] - w  - es

    if h + borderScale*2.6 + 2 * borderScale >= screenSize[1]:
        if viewArea[1] > eb:
            viewArea[1] = eb 
        elif viewArea[1] < screenSize[1] - h  - es:
            viewArea[1] = screenSize[1] - h - es"""
    
    drawBorder(viewArea[0], viewArea[1], w, h, t)
    
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            type = board[i][j]
            if board[i][j] == "o":
                type = "Open"
            elif board[i][j] == "x":
                type = "Mine"
            elif board[i][j] == "f":
                type = "Flag"
            
            if type == "Open" and highlightOpens:
                type = "OpenHighlight"
            drawTile(viewArea[0] + j * tileSize,viewArea[1] + i * tileSize, type)
    
    #highlight adjacent tiles with holding mouse down
    pos=pygame.mouse.get_pos()
    mouseTileIndex = [math.floor((pos[0] - viewArea[0])/tileSize), math.floor((pos[1] - viewArea[1])/tileSize)]
    if mouseDown and mouseDownTimer > 5 and not(menu):
        adj = []
        i, j = mouseTileIndex[0], mouseTileIndex[1]
        if i > -1 and i < len(board) and j > -1 and j < len(board[0]):
            if board[j][i] == "o":
                 drawTile(viewArea[0] + i * tileSize,viewArea[1] + j * tileSize, "0")
            else:
                for n in range(-1,2):
                    for m in range(-1,2):
                        if not(n == 0 and m == 0) and i + n > -1 and j + m > -1 and i + n < len(board) and j + m < len(board[i]):
                            if board[j + m][i + n] == "o":
                                adj.append([i + n, j + m])
                for n in adj:
                    drawTile(viewArea[0] + n[0] * tileSize,viewArea[1] + n[1] * tileSize, "0")
    
    if gameOver and not(win):
        drawTile(viewArea[0] + errorTiles[0][0] * tileSize,viewArea[1] + errorTiles[0][1] * tileSize, "MineError")
        for e in errorTiles[1:]:
            drawTile(viewArea[0] + e[0] * tileSize,viewArea[1] + e[1] * tileSize, "FlagError")
    
    if menu:
        drawMenu(menuFocus)
    
    """pygame.draw.rect(screen, (255,255,255),(viewArea[0], viewArea[1], 100, 100))
    pygame.draw.rect(screen, (255,255,255),(leftBound, 0, 3, 2000))
    pygame.draw.rect(screen, (255,255,255),(rightBound, 0, 3, 2000))
    pygame.draw.rect(screen, (255,255,255),(0, topBound, 2000, 3))
    pygame.draw.rect(screen, (255,255,255),(0, bottomBound, 2000, 3))"""

    pygame.display.flip()

    if time.time() - botTimer > 0.00 and allowBot:
        botMove()
        botTimer = time.time()

pygame.quit()