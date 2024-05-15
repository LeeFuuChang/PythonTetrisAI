import pygame
import Tetris
import TetrisAI

import math
import time
import os



FPS = 60

boardWidth = 10
boardHeight = 20

borderWidth = 10
windowWidth = 960
windowHeight = 960

population = 36
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
# [82.54615179266266, 9.226965178845376, 32.200679611575026, 27.134371684334898, 11.452042279649534, 394.05649965756584, 5.135398483510829, -169.54357235615342]
# [86.14300816630856, 11.329511784418937, 47.635254103423726, 27.956625371738987, 15.64121807266744, 460.58551908027175, 6.3698692728163175, -152.13630123995483]
trainer = TetrisAI.Trainer(population, [82.54615179266266, 9.226965178845376, 32.200679611575026, 27.134371684334898, 11.452042279649534, 394.05649965756584, 5.135398483510829, -169.54357235615342])
trainer.enableRecord(os.path.join(os.getcwd(), __file__+".txt"))
randomizer = Tetris.Tiles.TileRandomizer()
for i in range(population):
    moves.append([])
    boards.append(Tetris.Board(boardWidth, boardHeight, randomizer))
    surfaces.append(pygame.Surface((populationWidth, populationHeight)))



stime = time.time()


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
        print(population-deadCount, "Alive", f"{round(time.time()-stime)}s")
        if( deadCount == population ):
            stime = time.time()
            randomizer = Tetris.Tiles.TileRandomizer()
            fitnesses = []
            for i in range(population):
                fitnesses.append(boards[i].ptime)
                boards[i].reset(randomizer)
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




