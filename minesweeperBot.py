import pyautogui
import random
import math
from PIL import ImageGrab
import time
from pynput import keyboard
from pynput.mouse import Controller, Button
from multiprocessing import Process

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

def locateCorner():
    im = pyautogui.screenshot(region=(1511,0, 3431 - 1511, 1079))

    ref = [0,0]

    c = im.getpixel(ref)

    dif = abs(c[0] - 207) + abs(c[1] - 204) + abs(c[2] - 31)

    while dif > 10:
        if ref[0] < 3431 - 1511 - 1:
            ref[0] = ref[0] + 1
        else:
            ref[0] = 0
            ref[1] = ref[1] + 1
        c = im.getpixel(ref)
        dif = abs(c[0] - 207) + abs(c[1] - 204) + abs(c[2] - 31)
    
    ref[1] = ref[1] - 50

    c = im.getpixel(ref)

    while (c[0] + c[1] + c[2])/3 > 100:
        ref[0] = ref[0] - 1
        c = im.getpixel(ref)
    
    ref2 = [ref[0] + 10, ref[1]]
    c = im.getpixel(ref2)

    while (c[0] + c[1] + c[2])/3 > 100:
        ref2[0] = ref2[0] + 1
        c = im.getpixel(ref2)

    w = abs(ref[0] - ref2[0])

    ref2 = [ref[0] + 10, ref[1] + 10]
    c = im.getpixel(ref2)

    while (c[0] + c[1] + c[2])/3 > 50:
        ref2[1] = ref2[1] + 1
        c = im.getpixel(ref2)
    
    h = abs(ref[1] - ref2[1])

    pyautogui.moveTo(1511,1)
    pyautogui.move(ref)
    ref = pyautogui.position()

    return [ref, w, h]

def scanBoard(w, h, ref):
    board = createBoard(w,h,0)
    im2 = pyautogui.screenshot(region=(ref.x + 30,ref.y + 135,w - 30,h - 135))

    wTileCount = round((w-44)/40)
    hTileCount = round((h-130-22)/40) - 1

    board = []

    for m in range(0, hTileCount):
        row = []
        for n in range(0, wTileCount):

            c = im2.getpixel((20 + n * 40, 20 + m * 40))

            if abs(c[0] - 113) < 10 and abs(c[1] - 192) < 10 and abs(c[2] - 255) < 10:
                row.append("1")
            elif abs(c[0] - 91) < 10 and abs(c[1] - 186) < 10 and abs(c[2] - 91) < 10:
                row.append("2")
            elif abs(c[0] - 255) < 10 and abs(c[1] - 108) < 10 and abs(c[2] - 125) < 10:
                row.append("3")
            elif abs(c[0] - 235) < 10 and abs(c[1] - 125) < 10 and abs(c[2] - 255) < 10:
                row.append("4")
            elif abs(c[0] - 216) < 10 and abs(c[1] - 160) < 10 and abs(c[2] - 31) < 10:
                row.append("5")
            elif abs(c[0] - 91) < 10 and abs(c[1] - 197) < 10 and abs(c[2] - 197) < 10:
                row.append("6")
            elif abs(c[0] - 202) < 10 and abs(c[1] - 210) < 10 and abs(c[2] - 219) < 10:
                row.append("8")
            elif abs(c[0] - 49) < 10 and abs(c[1] - 56) < 10 and abs(c[2] - 63) < 10:
                row.append("0")
            else:
                c2 = im2.getpixel((20 + n * 40, 10 + m * 40))
                if abs(c2[0] - 142) < 10 and abs(c2[1] - 142) < 10 and abs(c2[2] - 142) < 10:
                    row.append("7")
                else:
                    row.append("o")
        
        board.append(row)
    
    return board

def removeDuplicates(L):
    result = []
    for i in L:
        if not(isIn(i,result)):
            result.append(i)
    return result

def isIn(x,A):
    for i in A:
        if x == i:
            return True
    return False

def calculateMove(board):
    newOpens = []
    newMines = []
    partialMines = []
    chord = True

    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] != "o" and board[i][j] != "x":
                adj = []
                for n in range(-1,2):
                    for m in range(-1,2):
                        if not(n == 0 and m == 0) and i + n > -1 and j + m > -1 and i + n < len(board) and j + m < len(board[i]):
                            adj.append([board[i + n][j + m], [i + n, j + m]])
                #collects metrics on the adjacent tiles
                open = 0
                clicked = 0
                mines = 0
                for n in adj:
                    if n[0] == "o":
                        open = open + 1
                    elif n[0] == "x":
                        mines = mines + 1
                    else:
                        clicked = clicked + 1
                mineSubset = [int(board[i][j]) - mines,[]]
                if mineSubset[0] > 0:
                    for n in adj:
                        if n[0] == "o":
                            mineSubset[1].append(n[1])
                    partialMines.append(mineSubset)

    partialMines = removeDuplicates(partialMines)

    #loops through each tile in the board
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            #for each tile it collects the adjacent tiles
            adj = []
            for n in range(-1,2):
                for m in range(-1,2):
                    if not(n == 0 and m == 0) and i + n > -1 and j + m > -1 and i + n < len(board) and j + m < len(board[i]):
                        adj.append([board[i + n][j + m], [i + n, j + m]])
            #collects metrics on the adjacent tiles
            open = 0
            clicked = 0
            mines = 0
            partialMineCount = 0
            partialMineRestrictions = []
            adjTiles = []
            for n in adj:
                if n[0] == "o":
                    open = open + 1
                elif n[0] == "x":
                    mines = mines + 1
                else:
                    clicked = clicked + 1
                adjTiles.append(n[1])
            
            for n in partialMines:
                isSubSet = True
                for m in n[1]:
                    if not(isIn(m, adjTiles)):
                        isSubSet = False
                        break
                if isSubSet:
                    partialMineCount = partialMineCount + n[0]
                    for k in n[1]:
                        partialMineRestrictions.append(k)
            
            #if this the amount of open tiles is equal to this tiles number - the amount of mine tiles then all open tiles are mines
            if board[i][j] != "o" and board[i][j] != "x":
                if open == int(board[i][j]) - mines:
                    for n in adj:
                        if n[0] == "o":
                            newMines.append(n[1])
                            #return [removeDuplicates(newOpens), removeDuplicates(newMines)]
            
            #if the amount of mines is equal to the tile number then all other adjacent tiles are safe
            if str(mines) == board[i][j] and board[i][j] != "0" and open > 0:
                if chord:
                    newOpens.append([i,j])
                    return [removeDuplicates(newOpens), removeDuplicates(newMines)]
                else:
                    for n in adj:
                        if n[0] == "o":
                            newOpens.append(n[1])
                            #return [removeDuplicates(newOpens), removeDuplicates(newMines)]
            
            #checks for safe tiles using partial mines
            if board[i][j] != "o" and board[i][j] != "x" and False:
                if int(board[i][j]) == mines + partialMineCount:
                    for n in adj:
                        if n[0] == "o" and not(isIn(n[1], partialMineRestrictions)):
                            newOpens.append(n[1])
                      
    #if all previous strategies failed pick a random tile
    if len(newOpens) == 0 and len(newMines) == 0:
        r = []
        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                if board[i][j] == "o":
                    rTest = True
                    for n in newMines:
                        if board[i][j] == n:
                            rTest = False
                    if rTest:
                        r.append([i,j])
        newOpens.append(random.choice(r))
    
    return [removeDuplicates(newOpens), removeDuplicates(newMines)]

def newMoveTo(x,y, mouse):
    c = mouse.position
    mouse.move(x - c[0], y - c[1])

def runGame():
    mouse = Controller()
    #locates the top left of the screen
    ref = locateCorner()
    w = ref[1]
    h = ref[2]
    ref = ref[0]

    wTileCount = round((w-44)/40)
    hTileCount = round((h-130-22)/40) - 1

    #makes sure the mouse is focused on the game board
    pyautogui.moveTo(ref)
    pyautogui.click()
    pyautogui.click()


    topLeftTile = [ref.x + 50, ref.y + 155]

    mines = []

    gameEnd = False

    board = scanBoard(w,h,ref)

    prevLastMove = None

    noFlags = False

    while not(gameEnd):
        #gets move list
        moves = calculateMove(board)
        temp = []

        #combines newMines and newOpens into one list
        for i in moves[0]:
            temp.append([i, "open"])
        for i in moves[1]:
            temp.append([i, "mine"])
        
        #sorts the move list to minimize distance between successive moves
        moves = temp
        temp = []
        while len(moves) > 0:
            if prevLastMove == None:
                temp.append(random.choice(moves))
                moves.remove(temp[-1])
            else:
                minDist = math.inf
                minDistIndex = None
                for i in range(0, len(moves)):
                    d = math.sqrt(pow(moves[i][0][0] - prevLastMove[0],2) + pow(moves[i][0][1] - prevLastMove[1],2))
                    if d < minDist:
                        minDist = d
                        minDistIndex = i
                temp.append(moves[minDistIndex])
                moves.remove(temp[-1])
        moves = temp
        prevLastMove = moves[-1][0]

        if len(moves) == 1 and False:
            break

        #executes each move
        for m in moves:
            if m[1] == "open":
                #pyautogui.moveTo(topLeftTile[0] + m[0][1] * 40, topLeftTile[1] + m[0][0] * 40)
                organicMove(topLeftTile[0] + m[0][1] * 40, topLeftTile[1] + m[0][0] * 40, random.random()/5)
                pyautogui.click()
            else:
                if not(noFlags):
                    #pyautogui.moveTo(topLeftTile[0] + m[0][1] * 40, topLeftTile[1] + m[0][0] * 40)
                    organicMove(topLeftTile[0] + m[0][1] * 40, topLeftTile[1] + m[0][0] * 40, random.random()/5)
                    pyautogui.rightClick()
                mines.append(m[0])
        
        #scans board for new info
        board = scanBoard(w,h,ref)
        #adds each mine location to the board
        for n in mines:
            board[n[0]][n[1]] = "x"
        
        #checks if the game has finished by looking at the icon at the top of the board
        im4 = pyautogui.screenshot(region=(ref.x + (wTileCount / 2) * 40, ref.y + 38,60,60))
        c = im4.getpixel((25,25))
        c2 = im4.getpixel((20,20))
        if (abs(c[0] - 207) < 10 and abs(c[1] - 210) < 10 and abs(c[2] - 68) < 10 )or (abs(c2[0] - 197) < 10 and abs(c2[1] - 197) < 10 and abs(c2[2] - 197) < 10):
            gameEnd = True
        else:
            gameEnd = False
        
def organicMove(x,y, speed):
    mouse = Controller()
    c = mouse.position
    n = 500
    path = smooth_random_path(c, (x, y), num_points=n, random_strength=0.2)
    for i in path:
        mouse.move(i[0] - c[0], i[1] - c[1])
        c = mouse.position
        time.sleep(speed/n)

def smooth_random_path(start, end, num_points=100, random_strength=0.3, seed=None):
    """
    Creates a smooth random path between two points using a cubic Bézier curve.

    Parameters:
        start (tuple): (x, y) starting point
        end (tuple): (x, y) ending point
        num_points (int): Number of points in the path
        random_strength (float): Controls how curvy the path is (0 = straight line)
        seed (int): Optional random seed for reproducibility

    Returns:
        list of tuple: [(x1, y1), (x2, y2), ..., (xn, yn)]
    """
    if seed is not None:
        random.seed(seed)

    x1, y1 = start
    x4, y4 = end

    # Compute direction and distance
    dx = x4 - x1
    dy = y4 - y1
    distance = (dx**2 + dy**2) ** 0.5

    # Normalized direction vector
    if distance == 0:
        return [start] * num_points

    nx, ny = dx / distance, dy / distance

    # Perpendicular direction (for sideways curvature)
    px, py = -ny, nx

    # Random control points
    def rand_offset():
        return (random.uniform(-random_strength, random_strength) * distance)

    # Control point 1 (about 1/3 along the way)
    c1x = x1 + dx * random.uniform(0.25, 0.4) + px * rand_offset()
    c1y = y1 + dy * random.uniform(0.25, 0.4) + py * rand_offset()

    # Control point 2 (about 2/3 along the way)
    c2x = x1 + dx * random.uniform(0.6, 0.75) + px * rand_offset()
    c2y = y1 + dy * random.uniform(0.6, 0.75) + py * rand_offset()

    path = []
    for i in range(num_points):
        t = i / (num_points - 1)
        # Cubic Bézier interpolation
        x = (1 - t)**3 * x1 + 3 * (1 - t)**2 * t * c1x + 3 * (1 - t) * t**2 * c2x + t**3 * x4
        y = (1 - t)**3 * y1 + 3 * (1 - t)**2 * t * c1y + 3 * (1 - t) * t**2 * c2y + t**3 * y4
        path.append((x, y))

    return path

def loopGame():
    while True:
        runGame()
        pyautogui.press('space')

"""
if __name__ == '__main__':
    #exit()
    process = Process(target=loopGame)
    process.start()

    def on_activate():
        process.terminate()
        exit()

    def for_canonical(f):
        return lambda k: f(l.canonical(k))

    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse('<ctrl>+<shift>'),
        on_activate)
    with keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release)) as l:
        l.join()


"""