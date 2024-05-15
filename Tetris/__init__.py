from .constant import *

from . import Tiles

import random
import os



class Board:
    def __init__(self, w, h, tileRandomizer=None):
        self.w, self.h = w, h
        self.reset(tileRandomizer)


    def reset(self, tileRandomizer=None):
        self.alive = True
        self.ptime = 0
        self.score = 0
        self.clearCount = 0

        self.board = []
        self.fillEmptyRows()

        self.fallDelay = 0
        self.lockDelay = 0

        self.availableTiles = Tiles.getAllTiles()
        self.preloadTileCount = 1
        self.tileCount = 0

        self.tileRandomizer = tileRandomizer

        self.heldTile = None
        self.loadedTiles = []
        self.cx = 0
        self.cy = self.py = self.fy = 0
        self.fillPreloadTile()


    def setTileRandomizer(self, randomizer):
        self.tileRandomizer = randomizer


    def fillPreloadTile(self):
        for i in range((1+self.preloadTileCount) - len(self.loadedTiles)):
            if(self.tileRandomizer):
                self.loadedTiles.append(self.tileRandomizer.get(self.tileCount)())
            else:
                self.loadedTiles.append(self.availableTiles.pop(random.randrange(0, len(self.availableTiles)))())
            self.tileCount += 1
            if(self.tileCount%7 == 0 or len(self.availableTiles) == 0): self.availableTiles = Tiles.getAllTiles()
        self.cx = self.w//2 - self.loadedTiles[0].w//2 - self.loadedTiles[0].w%2 - self.loadedTiles[0].Loffset
        self.cy = self.py = -self.loadedTiles[0].Toffset
        if(self.checkCollision(self.cx, self.cy, Bedge=True, Ledge=True, Redge=True)): self.alive = False
        if(self.checkCollision(self.cx, self.cy+1, Bedge=True, Ledge=True, Redge=True)): self.alive = False


    def fillEmptyRows(self):
        self.board = [[0]*self.w for i in range(self.h-len(self.board))] + self.board


    def checkCollision(self, x, y, Bedge=True, Ledge=True, Redge=True):
        if(Bedge):
            if(y + self.loadedTiles[0].size - self.loadedTiles[0].Boffset > self.h):
                return True
        if(Ledge):
            if(x + self.loadedTiles[0].Loffset < 0):
                return True
        if(Redge):
            if(x + self.loadedTiles[0].size - self.loadedTiles[0].Roffset > self.w):
                return True
        Lx, Rx = max(x, 0), min(self.loadedTiles[0].size+x, self.w)
        Ly, Ry = max(y, 0), min(self.loadedTiles[0].size+y, self.h)
        for xx in range(Lx, Rx):
            for yy in range(Ly, Ry):
                if(self.board[yy][xx] and self.loadedTiles[0].mass[yy-y][xx-x]):
                    return True


    def checkClear(self):
        cnt = 0
        for idx, row in sorted(enumerate(self.board), reverse=True):
            if(not all(row)): continue
            self.board.pop(idx)
            cnt += 1
        self.score += [0, 40, 100, 300, 1200][cnt]
        self.clearCount += cnt
        self.fillEmptyRows()


    def setDropPosition(self):
        self.fy = self.cy
        while(not self.checkCollision(self.cx, self.fy+1, Bedge=True, Ledge=True, Redge=True)):
            self.fy += 1


    def lockTile(self, instant):
        self.lockDelay += 1
        if(not instant and self.lockDelay != LOCK_DELAY//FALL_DELAY): return False
        self.lockDelay = 0
        fx, fy = self.cx, self.cy
        Lx, Rx = max(fx, 0), min(self.loadedTiles[0].size+fx, self.w)
        Ly, Ry = max(fy, 0), min(self.loadedTiles[0].size+fy, self.h)
        for x in range(Lx, Rx):
            for y in range(Ly, Ry):
                if(not self.loadedTiles[0].mass[y-fy][x-fx]): continue
                self.board[y][x] = self.loadedTiles[0].displayID
        self.checkClear()
        self.loadedTiles.pop(0)
        self.fillPreloadTile()
        return True


    def hold(self):
        if(self.heldTile):
            self.heldTile, self.loadedTiles[0] = self.loadedTiles[0], self.heldTile
        else:
            self.heldTile = self.loadedTiles.pop(0)
            self.fillPreloadTile()
        self.cx = self.w//2 - self.loadedTiles[0].w//2 - self.loadedTiles[0].w%2 - self.loadedTiles[0].Loffset
        self.cy = self.py = -self.loadedTiles[0].Toffset


    def fall(self):
        self.py = self.cy
        if(self.checkCollision(self.cx, self.cy+1, Bedge=True, Ledge=True, Redge=True)):
            return self.lockTile(instant=False)
        self.cy += 1
        self.lockDelay = 0
        return False


    def drop(self, droplock=True):
        while(not self.checkCollision(self.cx, self.cy+1, Bedge=True, Ledge=True, Redge=True)):
            self.cy += 1
        if(droplock): self.lockTile(instant=True)
        else: self.py = self.cy


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
        self.loadedTiles[0].rotate(d)
        if(self.kick(d)): return
        self.loadedTiles[0].rotate(-d) # rotate back


    def update(self, autoFall=True):
        if(not self.alive): return False
        self.ptime += 1
        self.fallDelay += 1
        if(self.fallDelay == FALL_DELAY):
            self.fallDelay = 0
            if(autoFall):
                self.fall()
            elif(self.checkCollision(self.cx, self.cy+1, Bedge=True, Ledge=True, Redge=True)):
                self.lockTile(instant=False)
        self.setDropPosition()
        return True


    def makeMoves(self, moves):
        for move in moves:
            if move == "HD":
                self.hold()
            elif move == "ML":
                self.moveL()
            elif move == "MR":
                self.moveR()
            elif move == "RL":
                self.rotate(-1)
            elif move == "RR":
                self.rotate(1)
            elif move == "FL":
                self.fall()
            elif move == "DP":
                self.drop()


    def printDigital(self):
        os.system("cls")
        print("-"*(self.w+2)*2)
        for y in range(self.h):
            row = ""
            for x in range(self.w):
                m = self.board[y][x]
                if(
                    (self.cx <= x and x < self.cx+self.loadedTiles[0].size) and
                    (self.cy <= y and y < self.cy+self.loadedTiles[0].size)
                ): m = m or self.loadedTiles[0].mass[y-self.cy][x-self.cx]
                row += "[]" if(m)else "  "
            print("| " + row + " |")
        print("-"*(self.w+2)*2)



