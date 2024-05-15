from . import Tiles
import random
import math



def dist2D(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def dist3D(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)

def cost(w, h, state, weights=[1, 1, 1, 1, 1, 1, 1, 1]):
    def getHoleCount():
        nonlocal w, h, state
        checked = [[0]*w for i in range(h)]
        holes = 0
        queue = []
        for i in range(h):
            for j in range(w):
                if(queue):
                    while(queue):
                        ii, jj = queue.pop(0)
                        if(checked[ii][jj]): continue
                        holes += 1
                        checked[ii][jj] = 1
                        if(jj+1 < w and not state[ii][jj+1]): queue.append([ii, jj+1])
                        if(ii+1 < h and not state[ii+1][jj]): queue.append([ii+1, jj])
                elif(not state[i][j] and not checked[i][j]): 
                    queue.append([i, j])
        return holes

    def getPillarCount():
        nonlocal w, h, state
        count = sum([all([state[y][x] for y in range(h)]) for x in range(w)])
        return -1 if(count==1)else 1

    def getShapeHeight():
        nonlocal w, h, state
        for y in range(h):
            if(sum(state[y])):
                break
        return h-y

    def getBumpiness():
        nonlocal w, h, state
        heights = [h-([bool(state[i][j]) for i in range(h)]+[True]).index(True) for j in range(w)]
        bumpiness = 0
        for i in range(0, w-1): bumpiness += abs(heights[i] - heights[i+1])
        return bumpiness

    def getHolesToFillToFullClear():
        nonlocal w, h, state
        holes = 0
        for y in range(h):
            empty = [not state[y][x] for x in range(w)] 
            if(all(empty)): continue
            holes += sum(empty)
        return holes

    def getBlockCountAboveHole():
        nonlocal w, h, state
        count = 0
        for i in range(1, h):
            for j in range(w):
                if(state[i][j]): continue
                count += (state[i-1][j]!=0)
        return count

    def getDepthOfHoles():
        nonlocal w, h, state
        result = 0
        for x in range(w):
            t = ([bool(state[i][x]) for i in range(h)]+[True]).index(True)
            b = h - ([not state[i][x] for i in range(h-1, -1, -1)]+[False]).index(False)
            result += b-t
        return result

    def getLinesToClear():
        return sum([all(state[y]) for y in range(h)])

    functions = [
        getHoleCount, getPillarCount, getShapeHeight, getBumpiness, 
        getHolesToFillToFullClear, getBlockCountAboveHole, getDepthOfHoles, getLinesToClear]
    costs = [functions[i]()*weights[i] for i in range(len(functions))]
    # print(sum(costs), costs)
    return sum(costs)

def checkCollision(w, h, x, y, state, current, Bedge=True, Ledge=True, Redge=True):
    if(Bedge):
        if(y + current.size - current.Boffset > h):
            return True
    if(Ledge):
        if(x + current.Loffset < 0):
            return True
    if(Redge):
        if(x + current.size - current.Roffset > w):
            return True
    Lx, Rx = max(x, 0), min(current.size+x, w)
    Ly, Ry = max(y, 0), min(current.size+y, h)
    for xx in range(Lx, Rx):
        for yy in range(Ly, Ry):
            if(state[yy][xx] and current.mass[yy-y][xx-x]):
                return True

def getFuture(w, h, x, y, state, current):
    future = [[n for n in state[i]] for i in range(h)]
    Lx, Rx = max(x, 0), min(current.size+x, w)
    Ly, Ry = max(y, 0), min(current.size+y, h)
    for xx in range(Lx, Rx):
        for yy in range(Ly, Ry):
            if(not current.mass[yy-y][xx-x]): continue
            future[yy][xx] = current.displayID
    return future





class SimulateBoard:
    def reset(self, w, h, state, current, cx=None, cy=None):
        self.w, self.h = w, h
        self.board = [[n for n in state[i]] for i in range(self.h)]
        self.current = current
        if(cx): self.cx = cx
        else: self.cx = self.w//2 - self.current.w//2 - self.current.w%2 - self.current.Loffset
        if(cy): self.cy = cy
        else: self.cy = -self.current.Toffset


    def checkCollision(self, x, y, Bedge=True, Ledge=True, Redge=True):
        if(Bedge):
            if(y + self.current.size - self.current.Boffset > self.h):
                return True
        if(Ledge):
            if(x + self.current.Loffset < 0):
                return True
        if(Redge):
            if(x + self.current.size - self.current.Roffset > self.w):
                return True
        Lx, Rx = max(x, 0), min(self.current.size+x, self.w)
        Ly, Ry = max(y, 0), min(self.current.size+y, self.h)
        for xx in range(Lx, Rx):
            for yy in range(Ly, Ry):
                if(self.board[yy][xx] and self.current.mass[yy-y][xx-x]):
                    return True


    def fall(self):
        if(self.checkCollision(self.cx, self.cy+1, Bedge=True, Ledge=True, Redge=True)): return
        self.cy += 1


    def drop(self):
        while(not self.checkCollision(self.cx, self.cy+1, Bedge=True, Ledge=True, Redge=True)):
            self.cy += 1


    def moveL(self):
        if(self.checkCollision(self.cx-1, self.cy, Bedge=False, Ledge=True, Redge=False)): return
        self.cx -= 1


    def moveR(self):
        if(self.checkCollision(self.cx+1, self.cy, Bedge=False, Ledge=False, Redge=True)): return
        self.cx += 1


    def kick(self, d):
        # no kick needed
        if(not self.checkCollision(self.cx, self.cy, Bedge=True, Ledge=True, Redge=True)): return True
        # check down
        if(not self.checkCollision(self.cx, self.cy+1, Bedge=True, Ledge=True, Redge=True)):
            self.cy += 1
            return True
        # check rotate direction
        if(not self.checkCollision(self.cx+d, self.cy, Bedge=True, Ledge=True, Redge=True)):
            self.cx += d
            return True
        # check other direction
        if(not self.checkCollision(self.cx-d, self.cy, Bedge=True, Ledge=True, Redge=True)):
            self.cx -= d
            return True
        # check up
        if(not self.checkCollision(self.cx, self.cy-1, Bedge=True, Ledge=True, Redge=True)):
            self.cy -= 1
            return True
        # cant kick
        return False


    def rotate(self, d):
        self.current.rotate(d)
        if(self.kick(d)): return
        self.current.rotate(-d)


    def makeMoves(self, moves):
        for move in moves:
            if move == "ML":
                self.moveL()
            elif move == "MR":
                self.moveR()
            elif move == "RL":
                self.rotate(-1)
            elif move == "RR":
                self.rotate(1)
            elif move == "MD":
                self.fall()
            elif move == "DP":
                self.drop()





class TetrisAI_InstantDrop:
    def getFuture(self, w, h, x, state, current):
        y = -current.Toffset
        while(not checkCollision(w, h, x, y+1, state, current, Bedge=True, Ledge=True, Redge=True)): y += 1
        return getFuture(w, h, x, y, state, current)


    def getMove(self, w, h, state, current=None, hold=None, costWeight=[1, 1, 1, 1, 1, 1, 1, 1]):
        bestMove = []
        bestCost = float("inf")
        current = Tiles.getTileByName(current)
        if(current):
            cX = w//2 - current.w//2 - current.w%2 - current.Loffset
            for rotate in range(4):
                for x in range(-current.Loffset, w-current.w-current.Loffset+1):
                    future = self.getFuture(w, h, x, state, current)
                    cst = cost(w, h, future, weights=costWeight)
                    if(cst >= bestCost): continue
                    bestCost = cst
                    if(x > cX): bestMove = ["RR"]*rotate + ["MR"]*(x-cX)
                    elif(x < cX): bestMove = ["RR"]*rotate + ["ML"]*(cX-x)
                    elif(x == cX): bestMove = ["RR"]*rotate
                current.rotate(1)
        hold = Tiles.getTileByName(hold)
        if(hold):
            for rotate in range(4):
                hX = w//2 - hold.w//2 - hold.w%2 - hold.Loffset
                for x in range(-hold.Loffset, w-hold.w-hold.Loffset+1):
                    future = self.getFuture(w, h, x, state, hold)
                    cst = cost(w, h, future, weights=costWeight)
                    if(cst >= bestCost): continue
                    bestCost = cst
                    if(x > hX): bestMove = ["HD"] + ["RR"]*rotate + ["MR"]*(x-hX)
                    elif(x < hX): bestMove = ["HD"] + ["RR"]*rotate + ["ML"]*(hX-x)
                    elif(x == hX): bestMove = ["HD"] + ["RR"]*rotate
                hold.rotate(1)
        return bestMove + ["DP"]





class TetrisAI_Shifting:
    def getAllAvailableEndPositions(self, w, h, state, current, costWeight):
        endPositions = []
        for y in range(-current.Toffset, h):
            for x in range(-current.Loffset, w-current.w-current.Loffset+1):
                if(checkCollision(w, h, x, y, state, current, Bedge=True, Ledge=True, Redge=True)): continue
                if(not checkCollision(w, h, x, y+1, state, current, Bedge=True, Ledge=True, Redge=True)): continue
                # mightFromT = checkCollision(w, h, x, y-1, state, current, Bedge=True, Ledge=True, Redge=True)
                # mightFromL = checkCollision(w, h, x-1, y, state, current, Bedge=True, Ledge=True, Redge=True)
                # mightFromR = checkCollision(w, h, x+1, y, state, current, Bedge=True, Ledge=True, Redge=True)
                # if(not (mightFromT or mightFromL or mightFromR)): continue
                endPositions.append([x, y, cost(w, h, getFuture(w, h, x, y, state, current), costWeight)])
        return sorted(endPositions, key=lambda p:p[2])


    def getMovesToEndPosition(self, w, h, state, current, startX, startY, endX, endY):
        queue = [[startX, startY, 0]]
        cf = {}
        gs = {(x, y):float("inf") for y in range(-current.Toffset, h) for x in range(-current.Loffset, w-current.w-current.Loffset + 1)}
        gs[(startX, startY)] = 0
        fs = {(x, y):float("inf") for y in range(-current.Toffset, h) for x in range(-current.Loffset, w-current.w-current.Loffset + 1)}
        fs[(startX, startY)] = dist2D(startX, startY, endX, endY)
        while( queue ):
            cp = queue.pop(0)
            if(cp[0] == endX and cp[1] == endY):
                moves = []
                now = (endX, endY)
                while(now != (startX, startY)):
                    f = cf[now]
                    if(  now[0] - f[0] ==  1): moves.append("MR")
                    elif(now[0] - f[0] == -1): moves.append("ML")
                    elif(now[1] - f[1] ==  1): moves.append("MD")
                    now = f
                return moves[::-1]
            d = [[-1, 0], [1, 0], [0, 1]]
            for dx, dy in d:
                if(checkCollision(w, h, cp[0]+dx, cp[1]+dy, state, current, Bedge=True, Ledge=True, Redge=True) or cp[1]+dy < 0): continue
                if(cp[2]+1 < gs[(cp[0]+dx, cp[1]+dy)]):
                    cf[(cp[0]+dx, cp[1]+dy)] = (cp[0], cp[1])
                    gs[(cp[0]+dx, cp[1]+dy)] = cp[2]+1
                    fs[(cp[0]+dx, cp[1]+dy)] = cp[2]+1 + dist2D(cp[0]+dx, cp[1]+dy, endX, endY)
                    queue.append([cp[0]+dx, cp[1]+dy, cp[2]+1])
                    queue.sort(key=lambda x:x[2])
        return False


    def getMove(self, w, h, state, current=None, hold=None, costWeight=[1, 1, 1, 1, 1, 1, 1, 1]):
        bestMove = []
        current = Tiles.getTileByName(current)
        if(current):
            allAvailableEndPositions = []
            for i in range(4):
                allEndPos = self.getAllAvailableEndPositions(w, h, state, current, costWeight)
                allAvailableEndPositions.extend([
                    [endpos[0], endpos[1], -current.Toffset if(i==0)else 0, i, endpos[2]]
                for endpos in allEndPos])
                # for x, y, _ in allEndPos:
                #     f = getFuture(w, h, x, y, state, current)
                #     cost(w, h, f, costWeight)
                #     for r in f:
                #         print(r)
                #     input()
                current.rotate(1)
            allAvailableEndPositions.sort(key=lambda x:x[4])
            cX = w//2 - current.w//2 - current.w%2 - current.Loffset
            for i in range(len(allAvailableEndPositions)):
                crt = current.clone()
                for j in range(allAvailableEndPositions[i][3]): crt.rotate(1)
                moves = self.getMovesToEndPosition(
                    w, h, state, crt, cX, allAvailableEndPositions[i][2], 
                    allAvailableEndPositions[i][0], allAvailableEndPositions[i][1]
                )
                if(moves):
                    bestMove = ["RR"]*allAvailableEndPositions[i][3] + moves + ["DP"]
                    break
        return bestMove





class TetrisAI_Tactical:
    simulator = SimulateBoard()
    def getAllAvailableEndPositions(self, w, h, state, current, costWeight):
        endPositions = []
        for r in range(4):
            current.setRotation(r)
            for y in range(-current.Toffset, h):
                for x in range(-current.Loffset, w-current.w-current.Loffset+1):
                    if(checkCollision(w, h, x, y, state, current, Bedge=True, Ledge=True, Redge=True)): continue
                    if(not checkCollision(w, h, x, y+1, state, current, Bedge=True, Ledge=True, Redge=True)): continue
                    # mightFromT = checkCollision(w, h, x, y-1, state, current, Bedge=True, Ledge=True, Redge=True)
                    # mightFromL = checkCollision(w, h, x-1, y, state, current, Bedge=True, Ledge=True, Redge=True)
                    # mightFromR = checkCollision(w, h, x+1, y, state, current, Bedge=True, Ledge=True, Redge=True)
                    # if(not (mightFromT or mightFromL or mightFromR)): continue
                    endPositions.append([x, y, r, cost(w, h, getFuture(w, h, x, y, state, current), costWeight)])
        return sorted(endPositions, key=lambda p:p[3])


    def getMovesToEndPosition(self, w, h, state, current, startX, startY, startR, endX, endY, endR):
        queue = [[startX, startY, startR, []]] # x, y, r, m
        availableMoves = ["RL", "RR", "ML", "MR", "MD", "DP"]
        step = {}

        while( queue ):
            # print(queue)
            x, y, r, m = queue.pop(0)
            # nowF = dist3D(x, y, r, endX, endY, endR) + len(m)
            for move in availableMoves:
                current.setRotation(0)
                self.simulator.reset(w, h, state, current)
                self.simulator.makeMoves(m + [move])
                nx, ny = self.simulator.cx, self.simulator.cy
                nr = self.simulator.current.rotation
                if((nx, ny, nr) in step and len(m)+1 >= step[(nx, ny, nr)]): continue
                if(move == "ML" and nx == x): continue
                if(move == "MR" and nx == x): continue
                if(move == "MD" and ny == y): continue
                if(move == "DP" and ny == y): continue
                if(move == "RL" and nr == r): continue
                if(move == "RR" and nr == r): continue
                if(y and ny < y): continue
                step[(nx, ny, nr)] = len(m) + 1
                if(nx == endX and ny == endY and nr == endR): return m+[move]
                # newF = dist3D(self.simulator.cx, self.simulator.cy, self.simulator.current.rotation, endX, endY, endR) + len(m) + 1
                queue.append([nx, ny, nr, m+[move]])

            queue.sort(key=lambda s:(dist3D(s[0], s[1], s[2], endX, endY, endR) + len(s[3]), len(s[3])))

        return False


    def getMove(self, w, h, state, current=None, hold=None, costWeight=[1, 1, 1, 1, 1, 1, 1, 1]):
        current = Tiles.getTileByName(current)
        endPositions = self.getAllAvailableEndPositions(w, h, state, current, costWeight)
        for x, y, r, c in endPositions:
            move = self.getMovesToEndPosition(w, h, state, current, None, None, 0, x, y, r)
            if(move): return move





class Trainer:
    mutateRate = 0.1
    def __init__(self, size, initialOutput):
        self.population = size
        self.players = []
        self.bestPlayer = initialOutput
        self.initialOutput = initialOutput
        self.generations = 0
        self.path = None
        self.initialize()


    def enableRecord(self, path):
        self.path = path


    def initialize(self):
        self.players = [self.initialOutput]
        for i in range(self.population-1):
            self.players.append([n*(random.randint(50, 150)/100) for n in self.initialOutput])


    def mutate(self, parent):
        child = [n*( random.randint(95, 105)/100 if(random.random() < self.mutateRate)else 1 ) for n in parent]
        return child


    def setFitness(self, fitnesses):
        self.fitnesses = fitnesses


    def setBestPlayer(self):
        self.bestFitness = self.fitnesses[0]
        self.bestPlayer = self.players[0]
        for i in range(self.population):
            if(self.fitnesses[i] <= self.bestFitness): continue
            self.bestFitness = self.fitnesses[i]
            self.bestPlayer = self.players[i]
        if(self.path):
            with open(self.path, "a") as f:
                allplayers = "\n".join([str(p) for p in self.players])
                f.write(f"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Generation {self.generations:>5}
BestPlayer: {self.bestPlayer}
BestFitness: {self.bestFitness}
AllPlayers: 
{allplayers}
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
""")


    def naturalSelection(self):
        nextGeneration = []
        parent = self.bestPlayer
        allplayers = "\n".join([str(p) for p in self.players])
        print(f"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Generation {self.generations:>5}
BestPlayer: {self.bestPlayer}
BestFitness: {self.bestFitness}
AllPlayers: 
{allplayers}
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
""")
        nextGeneration.append(parent)
        nextGeneration.append(self.mutate(parent))
        while(len(nextGeneration) < self.population):
            nextGeneration.append(self.mutate(self.players[random.randrange(0, self.population)]))
        self.players = nextGeneration
        self.generations += 1



