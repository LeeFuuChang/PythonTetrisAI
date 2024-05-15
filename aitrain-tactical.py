import pygame
import Tetris
import TetrisAI

import math



FPS = 30

boardWidth = 10
boardHeight = 20

borderWidth = 10
windowWidth = 960
windowHeight = 960

population = 4
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
player = TetrisAI.TetrisAI_Tactical()
# [71.30678990413776, 30.266552449819756, 73.21066810173231, 17.656112583976416, 15.226362785089487, 351.5321237309898, 5.833080771080187, -147.28255537223404]
# [80.57667259167566, 15.526741406757536, 62.961174567489785, 19.774846094053586, 19.099949477616253, 362.07808744291947, 7.291350963850234, -144.33690426478935]
# [69.71493712631778, 10.027324867898086, 40.59736536111742, 19.18160071123198, 24.829934320901128, 539.49635028995, 6.128645835606074, -137.1777938132558]
trainer = TetrisAI.Trainer(population, [80.57667259167566, 15.526741406757536, 62.961174567489785, 19.774846094053586, 19.099949477616253, 362.07808744291947, 7.291350963850234, -144.33690426478935])
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
                boards[i].drop(droplock=False)
            moves[i].pop(0)
            if(not boards[i].update(autoFall=False)):
                moves[i] = []
                break
            if(not moves[i]): boards[i].lockTile(instant=True)




