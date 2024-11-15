import pygame
pygame.init()
pygame.font.init()
import Tetris


FPS = 60

boardWidth = 10
boardHeight = 20
blockSize = 42
borderSize = max(1, blockSize//10)

windowWidth = borderSize + boardWidth*blockSize + borderSize
windowHeight = borderSize + blockSize*3 + borderSize + borderSize + boardHeight*blockSize + borderSize

boardDisplay = pygame.Surface((boardWidth*blockSize, boardHeight*blockSize))
boardDisplayRect = boardDisplay.get_rect()
boardDisplayRect.center = (windowWidth/2, borderSize + blockSize*3 + borderSize + borderSize + boardHeight*blockSize/2)

holdTileDisplayWidth = windowWidth/2 - borderSize*2
holdTileDisplayHeight = blockSize*3
holdTileDisplay = pygame.Surface((holdTileDisplayWidth, holdTileDisplayHeight))
holdTileDisplayRect = holdTileDisplay.get_rect()
holdTileDisplayRect.center = (windowWidth/2 - windowWidth/4, borderSize + blockSize*1.5)

nextTileDisplayWidth = windowWidth/2 - borderSize*2
nextTileDisplayHeight = blockSize*3
nextTileDisplay = pygame.Surface((nextTileDisplayWidth, nextTileDisplayHeight))
nextTileDisplayRect = nextTileDisplay.get_rect()
nextTileDisplayRect.center = (windowWidth/2 + windowWidth/4, borderSize + blockSize*1.5)

window = pygame.display.set_mode((windowWidth, windowHeight))
clock = pygame.time.Clock()
font = pygame.font.SysFont("terminal", 30)

board = Tetris.Board(boardWidth, boardHeight)


while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                board.hold()
            if event.key == pygame.K_LEFT:
                board.moveL()
            if event.key == pygame.K_RIGHT:
                board.moveR()
            if event.key == pygame.K_z:
                board.rotate(-1)
            if event.key == pygame.K_x:
                board.rotate(1)
            if event.key == pygame.K_DOWN:
                board.fall()
            if event.key == pygame.K_SPACE:
                board.drop()



    window.fill("#eeeeee")



    # BOARD -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    boardDisplay.fill("#000000")

    for y in range(board.loadedTiles[0].size):
        for x in range(board.loadedTiles[0].size):
            if board.loadedTiles[0].mass[y][x]:
                # pygame.draw.rect(boardDisplay, (0, 0, 0), ((board.cx+x)*blockSize, (board.fy+y)*blockSize, blockSize, blockSize))
                pygame.draw.rect(boardDisplay, "#666666", ((board.cx+x)*blockSize + borderSize, (board.fy+y)*blockSize + borderSize, blockSize - borderSize*2, blockSize - borderSize*2))

    for y in range(board.loadedTiles[0].size):
        for x in range(board.loadedTiles[0].size):
            if board.loadedTiles[0].mass[y][x]:
                # pygame.draw.rect(boardDisplay, (0, 0, 0), ((board.cx+x)*blockSize, (board.cy+y)*blockSize, blockSize, blockSize))
                pygame.draw.rect(boardDisplay, Tetris.TILE_COLORS[board.loadedTiles[0].displayID], ((board.cx+x)*blockSize + borderSize, (board.cy+y)*blockSize + borderSize, blockSize - borderSize*2, blockSize - borderSize*2))

    for y in range(boardHeight):
        for x in range(boardWidth):
            if board.board[y][x]:
                # pygame.draw.rect(boardDisplay, (0, 0, 0), (x*blockSize, y*blockSize, blockSize, blockSize))
                pygame.draw.rect(boardDisplay, Tetris.TILE_COLORS[board.board[y][x]], (x*blockSize + borderSize, y*blockSize + borderSize, blockSize - borderSize*2, blockSize - borderSize*2))

    board.update()

    window.blit(boardDisplay, boardDisplayRect)



    # HOLD TILE -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    holdTileDisplay.fill("#000000")

    if(board.heldTile):
        tile = board.heldTile.__class__()
        startX = (holdTileDisplayWidth - tile.w*blockSize)/2
        startY = (holdTileDisplayHeight - tile.h*blockSize)/2
        for x in range(tile.Loffset, tile.Loffset+tile.w):
            for y in range(tile.Toffset, tile.Toffset+tile.h):
                if(not tile.mass[y][x]): continue
                xx = x - tile.Loffset
                yy = y - tile.Toffset
                pygame.draw.rect(holdTileDisplay, Tetris.TILE_COLORS[tile.displayID], (startX + xx*blockSize + borderSize, startY+ yy*blockSize + borderSize, blockSize - borderSize*2, blockSize - borderSize*2))

    window.blit(holdTileDisplay, holdTileDisplayRect)



    # NEXT TILE -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    nextTileDisplay.fill("#000000")

    startX = (nextTileDisplayWidth - board.loadedTiles[1].w*blockSize)/2
    startY = (nextTileDisplayHeight - board.loadedTiles[1].h*blockSize)/2
    for x in range(board.loadedTiles[1].Loffset, board.loadedTiles[1].Loffset+board.loadedTiles[1].w):
        for y in range(board.loadedTiles[1].Toffset, board.loadedTiles[1].Toffset+board.loadedTiles[1].h):
            if(not board.loadedTiles[1].mass[y][x]): continue
            xx = x - board.loadedTiles[1].Loffset
            yy = y - board.loadedTiles[1].Toffset
            pygame.draw.rect(nextTileDisplay, Tetris.TILE_COLORS[board.loadedTiles[1].displayID], (startX + xx*blockSize + borderSize, startY+ yy*blockSize + borderSize, blockSize - borderSize*2, blockSize - borderSize*2))

    window.blit(nextTileDisplay, nextTileDisplayRect)



    pygame.display.update()
    clock.tick(FPS)