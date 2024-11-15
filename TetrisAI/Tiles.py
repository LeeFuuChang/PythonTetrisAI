import random




class Tile:
    def __init__(self):
        self.rotation = 0
        self.name = self._name
        self.w, self.h = self._w, self._h
        self.size = self._size
        self.mass = [[n for n in self._mass[i]] for i in range(self.size)]
        self.setOffset()
    def setOffset(self):
        self.Toffset = self.size
        self.Boffset = self.size
        self.Loffset = self.size
        self.Roffset = self.size
        for y in range(self.size):
            for x in range(self.size):
                if(not self.mass[y][x]): continue
                self.Toffset = min(self.Toffset, y)
                self.Boffset = min(self.Boffset, self.size-y-1)
                self.Loffset = min(self.Loffset, x)
                self.Roffset = min(self.Roffset, self.size-x-1)
    def rotateL(self):
        self.rotation = (self.rotation-1 + 4)%4
        new = []
        for i in range(self.size):
            new.append([])
            for j in range(self.size):
                new[-1].append(self.mass[j][self.size-i-1])
        self.mass = new
        self.w, self.h = self.h, self.w
        self.setOffset()
    def rotateR(self):
        self.rotation = (self.rotation+1)%4
        new = []
        for i in range(self.size):
            new.append([])
            for j in range(self.size):
                new[-1].append(self.mass[self.size-j-1][i])
        self.mass = new
        self.w, self.h = self.h, self.w
        self.setOffset()
    def rotate(self, d):
        (self.rotateR if(d>0)else self.rotateL)()
    def setRotation(self, r):
        needed = r-self.rotation
        sign = 1 if(needed>0)else -1
        for i in range(0, needed, sign):
            self.rotate(sign)
    def clone(self):
        new = self.__class__()
        new.mass = self.mass
        new.w, new.h = self.w, self.h
        new.size = self.size
        new.setOffset()
        return new




class TileI(Tile):
    _name = "I"
    _w, _h = 4, 1
    _size = 4
    _mass = [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]


class TileO(Tile):
    _name = "O"
    _w, _h = 2, 2
    _size = 2
    _mass = [
        [1, 1],
        [1, 1],
    ]


class TileT(Tile):
    _name = "T"
    _w, _h = 3, 2
    _size = 3
    _mass = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0],
    ]


class TileS(Tile):
    _name = "S"
    _w, _h = 3, 2
    _size = 3
    _mass = [
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0],
    ]


class TileZ(Tile):
    _name = "Z"
    _w, _h = 3, 2
    _size = 3
    _mass = [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0],
    ]


class TileJ(Tile):
    _name = "J"
    _w, _h = 3, 2
    _size = 3
    _mass = [
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
    ]


class TileL(Tile):
    _name = "L"
    _w, _h = 3, 2
    _size = 3
    _mass = [
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0],
    ]



def getAllTiles():
    return [TileI, TileO, TileT, TileS, TileZ, TileJ, TileL]

def getRandomTile():
    return random.choice()()

def getTileByName(name):
    if(not name): return None
    name = name.upper()
    nameList = ["I", "O", "T", "S", "Z", "J", "L"]
    classList = [TileI, TileO, TileT, TileS, TileZ, TileJ, TileL]
    if(name not in nameList): return None
    return classList[nameList.index(name)]()