import math,time,random
import pygame
import sys

import tile
from customColors import customColors as cc


DEBUGGING_MODE = False
score = 0
GameOver = False

def cartToIso(cartX,cartY):
    isoX = (cartX - cartY)
    isoY = (cartX + cartY)/2
    pos = (isoX,isoY)
    return pos

def isoToCart(isoX,isoY):
    cartX =  ((2 * isoY + isoX) / 2)
    cartY = ((2 * isoY - isoX) / 2)
    pos = (cartX,cartY)
    return pos

def createGrid(rows,columns,tileWidth,tileHeight,centerX,centerY):
    pList = []
    row = []
    for x in range(rows):
        for y in range(columns):
            cartX = x * tileWidth/2
            cartY = y * tileHeight
            isoX,isoY = cartToIso(cartX,cartY)
            isoX += centerX
            isoY += centerY
            poly = tile.tile(isoX,isoY,tileWidth,tileHeight,cc.ARMOUR)
            poly.defaultColor = cc.ARMOUR
            row.append(poly)
        pList.append(row)
        row = []
    return pList

def populate(screen,grid,count,blockX,blockY,limX,limY): #blockX, blockY = tiles for first click. LimX,limY = grid boundaries
    while count > 0:
        randX = random.randint(1, limX) - 1
        randY = random.randint(1, limY) - 1
        if grid[randX][randY].isBomb == True or (blockX-1 <= randX <= blockX+1 and blockY-1 <= randY <= blockY+1): #creating a 3x3 safezone for first click
            continue
        else:
            grid[randX][randY].isBomb = True
            grid[randX][randY].value = -1
            grid[randX][randY].state = 'MINED'
            if DEBUGGING_MODE:
                pygame.draw.polygon(screen,cc.MAHOGANY,grid[randX][randY].poly)
                pygame.draw.polygon(screen,cc.BLACK,grid[randX][randY].poly,1)
            count -=1
    return grid

def generateValues(screen,grid,limX,limY):
    for i in range(limX):
        for j in range(limY):
            if grid[i][j].value == -1:
                continue
            else:
                grid[i][j].value = countNeighbours(grid,i,j,limX,limY)
                if grid[i][j].value == 0 and DEBUGGING_MODE:
                    pygame.draw.polygon(screen,cc.EMERALD,grid[i][j].poly)
                    pygame.draw.polygon(screen,cc.BLACK,grid[i][j].poly,1)
                elif grid[i][j].value == 1 and DEBUGGING_MODE:
                    pygame.draw.polygon(screen,cc.NAVY_BLUE,grid[i][j].poly)
                    pygame.draw.polygon(screen,cc.BLACK,grid[i][j].poly,1)

def countNeighbours(grid,blockX,blockY,limX,limY):
    n = 0
    for i in range(-1, 2):
        if not (-1 < blockX+i < limX):
            continue
        for j in range(-1, 2):
            if not (-1 < blockY+j < limY):
                continue
            if grid[blockX+i][blockY+j].isBomb == True:
                n += 1
    return n

def revealBlocks (screen,image,grid,blockX,blockY,limX,limY):
    block = grid[blockX][blockY]
    if block.value != -1 and block.state != 'WARN':
        block.isClicked = True
        block.color = cc.GOLD
        block.state = 'SAFE'
        screen.blit(image,(block.spriteX,block.spriteY))
        pygame.draw.aalines(screen, (0, 0, 0), 1, block.poly) #outline
        #pygame.draw.polygon(screen,block.color,block.poly) #fill
        if block.value > 0:
            text_to_screen(screen,block.value,block.centerX,block.centerY)
        else:
            for i in range(-1, 2):
                if not (-1 < blockX + i < limX):
                    continue
                for j in range(-1, 2):
                    if not (-1 < blockY + j < limY):
                        continue
                    if grid[blockX+i][blockY+j].state == 'UNKNOWN':
                        grid[blockX+i][blockY+j].state = 'SAFE'
                        revealBlocks(screen,image,grid,blockX+i,blockY+j,limX,limY)


def text_to_screen(screen, text, x, y, size=10, color = None, font_type=None):
    '''Uses the color argument to distinguish b/w an int or a string passed in the field'''
    if color == None: color = cc.colorlist[text]
    text = str(text)
    if font_type == None:
        font = pygame.font.SysFont('Arial', size, True)
    else: font = font_type
    text_width, text_height = font.size(text)
    text = font.render(text, True, color)
    tRect = screen.blit(text, (x-(text_width/2) , y-(text_height/2)))
    return tRect

#FIXME: buggy implementation
def findRange(screen,grid,blockX,blockY,limX,limY,tileSpriteList):
    #highlights a 3x3 Grid, could use suggestions for a better algorithm
    global GameOver
    flags = 0
    correct_bombs = 0
    bombs = 0
    blocks_in_range = []
    for i in range(-1, 2):
        if (-1 < blockX + i < limX):
            for j in range(-1, 2):
                if (-1 < blockY + j < limY):
                    blocks_in_range.append((grid[blockX + i][blockY + j],blockX + i,blockY + j))
                    if grid[blockX+i][blockY+j].state == 'WARN':
                        flags += 1
                    if grid[blockX+i][blockY+j].isBomb == True:
                        bombs +=1
                    if grid[blockX+i][blockY+j].isBomb == True and grid[blockX+i][blockY+j].state == 'WARN':
                        correct_bombs += 1

    for blocks in blocks_in_range:
        screen.blit(tileSpriteList['SELECT'],blocks[0].spritePOS)
        if flags != correct_bombs and flags > 0:
            drawBombs(screen,grid,limX,limY,tileSpriteList['BOMB'])
            GameOver = True
            break
        if correct_bombs == bombs and blocks[0].state == 'UNKNOWN':
            revealBlocks(screen,tileSpriteList['SAFE'],grid,blocks[1],blocks[2],limX,limY)
            blocks_in_range.remove(blocks)
    return blocks_in_range

def drawBombs(screen,grid,limX,limY,TILE_BOMB, delay=10):
    BOMB = pygame.Surface(TILE_BOMB.get_size()).convert_alpha()
    BOMB.fill(cc.MAHOGANY)
    TILE_BOMB.blit(BOMB,(0,0),special_flags = pygame.BLEND_RGBA_MULT)
    bombList = []
    for i in range(limX):
        for tile in grid[i]:
            if tile.isBomb and not tile.isClicked and tile.state != 'WARN':
                bombList.append(tile)

    tempClock = pygame.time.Clock()
    ticks = 0
    startTicks = 0
    listLength = len(bombList)
    while bombList: #run until bombList is empty, bomb "explosion" animation (revealing random bombs)
        for event in pygame.event.get(): #animation will freeze and crash without event handling
            if event.type == pygame.QUIT:
                break
                pygame.quit()
                sys.exit()

        if startTicks == 0:
            startTicks = pygame.time.get_ticks()

        ticks = (pygame.time.get_ticks() - startTicks)

        if (ticks % delay) == 0:
            randIndex = random.randint(0,listLength-1)
            screen.blit(TILE_BOMB,bombList[randIndex].spritePOS)             #Blit Bomb sprite
            pygame.draw.aalines(screen,cc.BLACK,0,bombList[randIndex].poly)  #Draw a nice outline
            bombList.remove(bombList[randIndex])
            listLength = len(bombList)
            delay -= 1.5 if delay > 1.5 else 0 #Accelerate blitting process
            pygame.display.flip()

        tempClock.tick(60)

#TODO: use arcs instead of circle to implement outline argument properly
def ui_drawRRect(screen,x,y,color,width,height,radius,outline=0): #Draw a rounded rect

    widthVert = width - 2*radius
    heightHori = height - 2*radius
    rectVert = pygame.rect.Rect((x + radius),y,widthVert,height)
    rectHori = pygame.rect.Rect(x, (y + radius),width,heightHori)
    c1 = pygame.draw.rect(screen,color,rectVert,outline)
    c2 = pygame.draw.rect(screen,color,rectHori,outline)
    c3 = pygame.draw.circle(screen,color,((x + radius),( y + radius)),radius,outline)            #top left corner
    c4 = pygame.draw.circle(screen,color,((x + (width - radius)),( y + radius)),radius,outline)  #top right corner
    c5 = pygame.draw.circle(screen,color,((x + radius),(y + (height - radius))),radius,outline)  #bot left corner
    c6 = pygame.draw.circle(screen,color,((x + (width - radius)),(y + (height - radius))),radius,outline) #bot right corner
    
    rect = pygame.rect.Rect(x,y,width,height)

    return  rect

def drawHUD(screen,res):
    HUD = pygame.rect.Rect(0,0,res[0],res[1]//8-2)
    pygame.draw.rect(screen,cc.BLACK,HUD)
    pygame.draw.line(screen,cc.DARK_SALMON,(0,HUD.height),(HUD.width,HUD.height))
    button1 = ui_drawRRect(screen,res[0]//25,res[1]//100,cc.MYRTLE,120,30,2)
    button2 = ui_drawRRect(screen,res[0]//25,res[1]//15,cc.MYRTLE,120,30,2)

    return HUD,button1,button2

def maskRect(screen,maskX,maskY,maskWidth,maskHeight,maskColor):
    #Draw a rect to to clear a frequently updated region
    t_rect = pygame.rect.Rect(maskX,maskY,maskWidth,maskHeight)
    pygame.draw.rect(screen,maskColor,t_rect)
    return t_rect

def drawTimer(screen,HUD,tick):
    #Always keep time in xxx format
    if tick < 10:
        tick = "00"+str(tick)
    elif tick < 100 and tick > 9:
        tick = "0"+str(tick)
    else:
        tick = str(tick)
    timeFont = pygame.font.Font("assets/fonts/Seven Segment.ttf", 70)
    x = HUD.centerx - HUD.width//16 #position X such that the timer is centered
    y = HUD.height//6
    rect = pygame.rect.Rect(x,y,HUD.width//8.3,HUD.height//1.5)
    pygame.draw.rect(screen,cc.MYRTLE,rect)
    text_to_screen(screen,tick,rect.centerx,rect.centery,rect.width*0.8,cc.RAINEE,timeFont)

def drawDebug(screen,res,tileSpriteList):
    if DEBUGGING_MODE:
        l = len(tileSpriteList)
        for i,j in enumerate(tileSpriteList):
            screen.blit(tileSpriteList[j],(i*40,res[1]//7.5))
        text_to_screen(screen,"Debug Mode",50,res[1]//5,color=cc.WHITE,size = 15)
    else: return

def resetGame(res,screen,bomb_count):
    game(res, screen, bomb_count, DEBUGGING_MODE)

def goMainMenu():
    from Menu import mainMenu
    mainMenu()

def gameOverDialogue(screen,res,score,remaining_bombs):
    bodyWidth = 200
    bodyHeight = 250
    body = pygame.rect.Rect(res[0]//2-bodyWidth//2,res[1]//2-bodyHeight//4,bodyWidth,bodyHeight)
    buttonWidth = int(bodyWidth-bodyWidth*0.1)
    buttonheight = int(bodyHeight*0.15)
    buttonX = int(body.x + body.width * 0.05)
    pygame.draw.rect(screen,cc.BLACK,body)
    pygame.draw.rect(screen,cc.DARK_SALMON,body,1)

    if not remaining_bombs:
        text_to_screen(screen, "You Win!", body.centerx, body.y + body.height * 0.1, size=40, color=cc.RAINEE)
    else:
        text_to_screen(screen, "You Lose!", body.centerx, body.y + body.height * 0.1, size=40, color=cc.RAINEE)

    text_to_screen(screen, "Score: ", body.centerx - body.width * 0.3+5, body.y + body.height * 0.3, size=20, color=cc.RAINEE)
    text_to_screen(screen, int(score), body.centerx + body.width *0.3+10, body.y + body.height * 0.3, size=20, color=cc.RAINEE)

    button_reset = ui_drawRRect(screen,buttonX, body.y + int(body.height*0.4), cc.MYRTLE,buttonWidth, buttonheight, 2)
    button_quit = ui_drawRRect(screen, buttonX, body.y + int(body.height * 0.8), cc.MYRTLE, buttonWidth, buttonheight, 2)
    button_Menu = ui_drawRRect(screen, buttonX, body.y + int(body.height*0.6), cc.MYRTLE,buttonWidth, buttonheight, 2)

    return body,button_reset,button_quit,button_Menu

def game(res,screen,bomb_count,debug=False):
    global DEBUGGING_MODE,score,GameOver
    DEBUGGING_MODE = debug

    #sprites
    TILE_GRASS = pygame.image.load("assets/GRASS_TILE.png").convert_alpha()
    TILE_DIRT = pygame.image.load("assets/TILE_DIRT.png").convert_alpha()
    TILE_FLAG = pygame.image.load("assets/TILE_FLAG.png").convert_alpha()
    TILE_SELECT = pygame.image.load("assets/SELECT_TILE2.png").convert_alpha()
    TILE_BOMB = pygame.image.load("assets/TILE_BOMB.png").convert_alpha()
    TILE_UNDERHANG = pygame.image.load("assets/tile_dirt_underhang.png").convert_alpha()
    tileSpriteList = {'WARN': TILE_FLAG,
                      'SAFE': TILE_DIRT,
                      'UNKNOWN': TILE_GRASS,
                      'MINED': TILE_GRASS,
                      'SELECT': TILE_SELECT,
                      'UNDERHANG': TILE_UNDERHANG,
                      'BOMB': TILE_BOMB,
                      }
    #board properties
    tileWidth = 32
    tileHeight = 16
    centerX = 512
    centerY = 75
    limX = 0
    limY = 0
    rows =  33
    columns = 33
    pList = createGrid(rows,columns,tileWidth,tileHeight,centerX,centerY)
    highlighted_tile = pList[0][0]
    limX = rows - 1 #one row and column reserved for hanging edges
    limY = columns - 1
    print(rows,columns, rows*columns,bomb_count)
    score = 0

    #Game properties
    running = True
    blockX = 0
    blockY = 0
    firstClick = True
    bomb_count_approx = bomb_count
    clock = pygame.time.Clock()
    FPS = 60
    MMB = False     #Check for middle mouse button hold
    MMB2 = False    #Check for middle mouse button no longer pressed
    blit_cache = []
    startTicks = 0
    ticks = 0
    prevtick = -1

    #draw stuff
    screen.fill(cc.BLUE_STONE)
    HUD,button_reset,button_menu = drawHUD(screen,res)
    drawTimer(screen,HUD,0)
    text_to_screen(screen,"Menu",button_menu.centerx,button_menu.centery,15,cc.RAINEE)
    text_to_screen(screen,"Reset",button_reset.centerx,button_reset.centery,15,cc.RAINEE)

    drawDebug(screen,res,tileSpriteList)

    for x in range(len(pList)-1): #Draw main grid
        for tile in pList[x]:
            screen.blit(TILE_GRASS,(tile.spriteX,tile.spriteY))
            pygame.draw.aalines(screen, (0, 0, 0), 1,tile.poly,1)

    for x in range(rows): #Draw hanging edges
        screen.blit(TILE_UNDERHANG,(pList[rows-1][x].spritePOS))
        screen.blit(TILE_UNDERHANG,(pList[x][columns-1].spritePOS))

    while running:  #Main Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                MMB = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 2:
                MMB2 = True

        clock.tick(FPS)
        mousex, mousey = pygame.mouse.get_pos()
        if not GameOver:  #Freeze the processing if the player loses

            isoMouseX = (2 * (mousey - centerY) + (mousex-centerX))  # (2 * mousePositionY + mousePositionX)
            isoMouseY= (2 * (mousey - centerY) - (mousex-centerX))/2 # (2 * mousePositionY - mousePositionX)
            blockX = math.floor(isoMouseX / (tileWidth)) if -1 < math.floor(isoMouseX / (tileWidth)) < limX else blockX
            blockY = math.floor(isoMouseY / (tileHeight)) if -1 < math.floor(isoMouseY / (tileHeight)) <limY else blockY
            tileHover = pList[blockX][blockY]

            if not firstClick: #Timer begins only after first click
                if startTicks == 0:
                    startTicks = pygame.time.get_ticks()
                current_ticks = (pygame.time.get_ticks() - startTicks)//1000
                if prevtick != current_ticks: #prevents this function from being called more than once per second
                    prevtick = current_ticks
                    drawTimer(screen,HUD,prevtick)

            #--------------------------Handling Mouse Clicks--------------------------#
            if pygame.mouse.get_pressed()[0] and not HUD.collidepoint(mousex,mousey): #LMB Click handling
                pygame.time.wait(60)
                tileHover.isClicked = True
                if firstClick: #Generate bombs in the grid, as well as values, and reveal the first chunk of safe tiles
                    pList = populate(screen, pList,bomb_count,blockX,blockY,limX,limY)
                    generateValues(screen,pList,limX,limY)
                    revealBlocks(screen,TILE_DIRT,pList,blockX,blockY,limX,limY)
                    firstClick = False

                if tileHover.value == 0: #Reveal a chunk of safe tiles if there are no nearby mines
                    revealBlocks(screen,TILE_DIRT,pList,blockX,blockY,limX,limY)

                    #Reveal just a single tile if there are mines nearby
                elif tileHover.isBomb == False and tileHover.state != 'WARN' and tileHover.state != 'SAFE':
                    tileHover.color = cc.GOLD
                    tileHover.state = 'SAFE'
                    screen.blit(TILE_DIRT, (tileHover.spriteX, tileHover.spriteY))
                    pygame.draw.aalines(screen, (0, 0, 0), 1,  tileHover.poly)  # outline
                    text_to_screen(screen, tileHover.value, tileHover.centerX, tileHover.centerY)

                elif tileHover.isBomb == True and tileHover.state != 'WARN': #Gameover on bomb click
                    tileHover.isClicked = True
                    screen.blit(TILE_BOMB, (tileHover.spritePOS))
                    pygame.draw.aalines(screen, (0, 0, 0), 1,  tileHover.poly)  # outline
                    drawBombs(screen,pList,limX,limY,TILE_BOMB)
                    GameOver = True

            if pygame.mouse.get_pressed()[2] and not HUD.collidepoint(mousex,mousey): #RMB
                pygame.time.wait(100)
                if tileHover.state != 'WARN' and tileHover.isClicked == False: #Place flag if tile is not marked or clicked
                    tileHover.state = 'WARN'
                    tileHover.color = cc.GRAY
                    bomb_count_approx -= 1
                    if tileHover.isBomb == True:
                        score += (bomb_count*0.1 + 5)
                    screen.blit(TILE_FLAG,tileHover.spritePOS)
                    pygame.draw.aalines(screen, (0, 0, 0), 1,  tileHover.poly)  # outline

                elif tileHover.state == 'WARN' and tileHover.isClicked == False:# Remove the flag if place is not clicked or marked
                    tileHover.state = 'UNKNOWN'
                    tileHover.color =  tileHover.defaultColor
                    bomb_count_approx += 1
                    if tileHover.isBomb == True:
                        score -= (bomb_count*0.1 + 5)
                    screen.blit(TILE_GRASS, (tileHover.spriteX,tileHover.spriteY))
                    pygame.draw.aalines(screen, (0, 0, 0), 1, tileHover.poly)

            if MMB and not HUD.collidepoint(mousex,mousey) and not firstClick:
                #Middle Mouse Button Action. Does not work unless first click has been made, band-aid fix for bad algorithm
                pygame.time.wait(70)
                blit_cache = findRange(screen,pList,blockX,blockY,limX,limY,tileSpriteList)
            elif MMB2:  #Once MMB is no longer pressed, blit all the selected with the previous tiles saved in a cache, then clear that cache
                for items in blit_cache:
                    screen.blit(tileSpriteList[items[0].state], (items[0].spritePOS))
                    if items[0].value > 0 and items[0].state == 'SAFE':
                        text_to_screen(screen,items[0].value,items[0].centerX,items[0].centerY)
                    pygame.draw.aalines(screen, (0, 0, 0), 1, items[0].poly)
                blit_cache = []
            #--------------------------Handling Mouse Clicks--------------------------#


            if button_menu.collidepoint(mousex,mousey) and pygame.mouse.get_pressed()[0]: #Return back to the main menu on click
                pygame.time.wait(60)
                pList=[]
                goMainMenu()

            if button_reset.collidepoint(mousex,mousey) and pygame.mouse.get_pressed()[0]:
                pygame.time.wait(60)
                highlighted_tile = None
                pList = []
                resetGame(res,screen,bomb_count)

            # Clear previously selected tile and re-blit the old sprite
            if pList!= [] and highlighted_tile != tileHover and not DEBUGGING_MODE:
                screen.blit(tileSpriteList[highlighted_tile.state],(highlighted_tile.spritePOS))
                pygame.draw.aalines(screen, (0, 0, 0), 1, highlighted_tile.poly)

                # Blit a highlighted sprite over currently hovering tile
                if highlighted_tile.value > 0 and highlighted_tile.state == 'SAFE':
                    text_to_screen(screen,highlighted_tile.value,highlighted_tile.centerX,highlighted_tile.centerY)

                highlighted_tile = tileHover
                screen.blit(TILE_SELECT,(highlighted_tile.spritePOS))
                pygame.draw.aalines(screen, (0, 0, 0), 1, highlighted_tile.poly)

            #Utiliites
            if bomb_count_approx == 0: #Win condition reached
                GameOver = True

            if DEBUGGING_MODE:# Update score every tick
                maskRect(screen,30,140,100,20,cc.BLUE_STONE)
                text_to_screen(screen,"score",50,150,color=cc.MAHOGANY,size=15)
                text_to_screen(screen,int(score),100,150,color=cc.MAHOGANY,size=20)

        ##--------------------------Handling Events after game Over--------------------------#
        else:
            highlighted_tile = None
            pList=[]
            p_body,p_reset,p_quit,p_menu = gameOverDialogue(screen, res, score, bomb_count_approx)
            text_to_screen(screen,"Restart",p_reset.centerx,p_reset.centery,18,color=cc.RAINEE)
            text_to_screen(screen, "Menu", p_menu.centerx, p_menu.centery,18, color=cc.RAINEE)
            text_to_screen(screen, "Quit", p_quit.centerx, p_quit.centery,18, color=cc.RAINEE)

            if pygame.mouse.get_pressed()[0]:

                if p_reset.collidepoint(mousex,mousey):
                    GameOver = False
                    pygame.time.wait(100)
                    resetGame(res,screen,bomb_count)

                elif p_menu.collidepoint(mousex,mousey):
                    GameOver = False
                    pygame.time.wait(100)
                    goMainMenu()

                elif p_quit.collidepoint(mousex,mousey):
                    running = False
                    pygame.quit()
                    sys.exit()
        ##--------------------------Handling Events after game Over--------------------------#

        MMB = False
        MMB2 = False
        pygame.display.flip()
