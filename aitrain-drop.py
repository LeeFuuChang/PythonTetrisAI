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
player = TetrisAI.TetrisAI_InstantDrop()
# [27.124446791660937, 5.90438683135533, 799.5395618808736, 0.7829828150388903, 76.7811147077793, 13.035464569802611, 57.8114807614827, -51.67792309950111]
trainer = TetrisAI.Trainer(population, [18.144077546519476, 70.92722120624164, 875.3451999986964, 0.6454252248472624, 100.16172752426482, 6.684112937118667, 33.49594336367219, -48.73739225013835])
randomizer = Tetris.Tiles.TileRandomizer()
for i in range(population):
    moves.append([])
    boards.append(Tetris.Board(boardWidth, boardHeight, randomizer))
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




