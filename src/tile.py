class tile:
    '''
      Tile class to store all points in polygons as tiles, as well as some other properties
      each tile has some utility properties, or meta data that are saved in each instance of this class
      each tile also has saved states, and colors

      STATES =
        'MINED',  : tile currently has a bomb
        'WARN',   : tile is marked as a potential bomb
        'SAFE',   : tile is revealed and is safe (val > -1)
        'UNKNOWN' : tile is not revealed nor marked
    '''
    def __init__(self,isoX,isoY,tileWidth,tileHeight,color= (255,255,255)):
        self.isoX = isoX
        self.isoY = isoY
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        self.enQueued = False
        self.color = color
        self.defaultColor = (255,255,255)
        self.poly = (
            (isoX, isoY),  # UP
            (isoX - tileWidth / 2, isoY + tileHeight / 2),  # LEFT
            (isoX, isoY + tileHeight),  # DOWN
            (isoX + tileWidth / 2, isoY + tileHeight / 2),  # RIGHT
        )
        self.spriteX = isoX - (tileWidth // 2)
        self.spriteY = isoY
        self.spritePOS = (self.spriteX,self.spriteY)
        self.centerX = isoX
        self.centerY = isoY + (tileHeight / 2)
        self.isClicked = False
        self.state = 'UNKNOWN'
        self.isBomb = False
        self.value = 0

