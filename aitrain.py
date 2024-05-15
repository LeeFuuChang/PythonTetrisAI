import pygame
import Tetris
import TetrisAI

import math



FPS = 60

boardWidth = 10
boardHeight = 20

borderWidth = 10
windowWidth = 960
windowHeight = 960

population = 16
populationRow = math.sqrt(population)
populationDisplaySize = windowWidth/populationRow - borderWidth*2

blockSize = populationDisplaySize/max(boardWidth, boardHeight)

populationWidth = blockSize*boardWidth
populationHeight = blockSize*boardHeight


window = pygame.display.set_mode((windowWidth, windowHeight))
clock = pygame.time.Clock()


moves = []
boards = []
surfaces = []
player = TetrisAI.TetrisAI_Shifting()
# [42.28317065750501, 3.3676061386693013, 834.965863340299, 1.726468329049444, 42.28317065750501, 35.59391030241327, -16.426687241188226]
# [40.709548000762155, 3.728414508607831, 878.7848718483981, 2.570270155403706, 22.284220836270038, 37.5558466382823, -8.78358326553536]
# [25.25037783337517, 2.4709917199014213, 1048.2996414237455, 1.3540819244595348, 25.54305197834549, 32.61465073104434, -20.518535987780094]
# [62.89535350574501, 4.565206020324364, 647.2144626800879, 0.8974372512581871, 73.21370049592201, 18.50787233642316, 28.67702655601408, -36.46525284612536]
trainer = TetrisAI.Trainer(population, [40, 5, 650, 2, 80, 20, 30, -35])
for i in range(population):
    moves.append([])
    boards.append(Tetris.Board(boardWidth, boardHeight))
    surfaces.append(pygame.Surface((populationWidth, populationHeight)))






while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    window.fill("#ffffff")

    for i in range(population):
        b, s = boards[i], surfaces[i]

        g = max(1, blockSize//10)

        s.fill("#000000")

        for y in range(b.loadedTiles[0].size):
            for x in range(b.loadedTiles[0].size):
                if b.loadedTiles[0].mass[y][x]:
                    pygame.draw.rect(s, (0, 0, 0), ((b.cx+x)*blockSize, (b.cy+y)*blockSize, blockSize, blockSize))
                    pygame.draw.rect(s, Tetris.TILE_COLORS[b.loadedTiles[0].displayID], ((b.cx+x)*blockSize + g, (b.cy+y)*blockSize + g, blockSize - g*2, blockSize - g*2))

        for y in range(boardHeight):
            for x in range(boardWidth):
                if b.board[y][x]:
                    pygame.draw.rect(s, (0, 0, 0), (x*blockSize, y*blockSize, blockSize, blockSize))
                    pygame.draw.rect(s, Tetris.TILE_COLORS[b.board[y][x]], (x*blockSize + g, y*blockSize + g, blockSize - g*2, blockSize - g*2))

        r = s.get_rect()
        x = i%populationRow
        y = i//populationRow
        r.center = (borderWidth*(2*x + 1) + populationDisplaySize*x + populationDisplaySize//2, borderWidth*(2*y + 1) + populationDisplaySize*y + populationDisplaySize//2)

        window.blit(s, r)

    pygame.display.update()
    clock.tick(FPS)




    if(all([len(moves[i])==0 for i in range(population)])):
        deadCount = 0
        for i in range(population):
            deadCount += not boards[i].alive
            if(not boards[i].alive): continue
            moves[i] = player.getMove(
                boardWidth, boardHeight, 
                boards[i].board, 
                boards[i].loadedTiles[0].name, 
                costWeight=trainer.players[i]
            )
        print(population-deadCount, "Alive")
        if( deadCount == population ):
            fitnesses = []
            for i in range(population):
                fitnesses.append(boards[i].score)
                boards[i].reset()
                moves[i] = []
            trainer.setFitness(fitnesses)
            trainer.setBestPlayer()
            trainer.naturalSelection()
    else:
        for i in range(population):
            if not moves[i]: continue
            if moves[i][0] == "ML":
                boards[i].moveL()
            elif moves[i][0] == "MR":
                boards[i].moveR()
            elif moves[i][0] == "RL":
                boards[i].rotate(-1)
            elif moves[i][0] == "RR":
                boards[i].rotate(1)
            elif moves[i][0] == "MD":
                boards[i].fall()
            elif moves[i][0] == "DP":
                boards[i].drop()
            moves[i].pop(0)
            if(not boards[i].update(autoFall=False)):
                moves[i] = []
                break




