import random
from perlin_noise import PerlinNoise
import numpy as np


class Tile:
    """Class for handling a singular tile - square with pipes, oil, etc"""
    def __init__(self, x, y, price) -> None:
        """
        x, y - coordinates
        isowned, issurveyed, price - arguments for buying things and visibility of oil, upkeep will be calculated later
        pipetype - can be None, 'building', 'invalid', 'basic'
        None - no pipe, building - pipe under construction, basic - basic pipe, export - pipe is an export pipe.
        pipeconnection - connections of the pipe if exists (u, d, r, l, and all combinations of those, sorted) or None
        oiltype - can be None if no oil is present, 'simple' if oil is present but not central or 'central'
        oilquantity - only matters if oiltype is central
        hasrig - if the segment has a rig
        rigtype can be None, 'building', 'invalid', 'basic'
        rigconnection - to which pipe the rig is connected (u, d, l, r)
        spawntile - purely cosmetic - if the tile is spawn
        """
        self.x = x
        self.y = y
        self.price = price
        self.isowned = False
        self.issurveyed = False
        self.haspipe = False
        self.pipetype = None
        self.exportpipe = False
        self.pipeconnection = None
        self.oiltype = None
        self.oilquantity = 0
        self.originaloilquantity = self.oilquantity
        self.centraltilelocation = [-1, -1]
        self.hasrig = False
        self.rigtype = None
        self.rigconnection = None
        self.spawntile = False

    def __repr__(self) -> str:
        return str(self.price)

    def can_place_pipe(self):
        return (not self.hasrig) and (not self.pipetype) and self.isowned and self.issurveyed

    def can_place_rig(self):
        return (not self.hasrig) and (not self.pipetype) and self.isowned\
            and self.issurveyed and self.oiltype == 'central'

    def place_pipe(self, grid, guaranteed_pipes):
        # Find nearby pipes to connect to:
        nearbypipes = guaranteed_pipes
        if grid[self.x-1][self.y].pipetype is not None:
            nearbypipes.append('d')
        elif grid[self.x+1][self.y].pipetype is not None:
            nearbypipes.append('u')
        elif grid[self.x][self.y-1].pipetype is not None:
            nearbypipes.append('l')
        elif grid[self.x][self.y+1].pipetype is not None:
            nearbypipes.append('r')
        nearbypipes = list(set(nearbypipes))

        if not self.can_place_pipe() or len(nearbypipes) == 4:
            return False
        self.haspipe = True
        self.pipeconnection = sorted(''.join(nearbypipes))
        self.pipetype = 'basic'

    def place_rig(self, grid, guaranteed_pipes):
        nearbypipes = guaranteed_pipes
        if grid[self.x-1][self.y].pipetype is not None:
            nearbypipes.append('d')
        elif grid[self.x+1][self.y].pipetype is not None:
            nearbypipes.append('u')
        elif grid[self.x][self.y-1].pipetype is not None:
            nearbypipes.append('l')
        elif grid[self.x][self.y+1].pipetype is not None:
            nearbypipes.append('r')
        nearbypipes = list(set(nearbypipes))

        if not self.can_place_rig():
            return False
        self.haspipe = False
        self.hasrig = True
        self.rigconnection = sorted(''.join(nearbypipes))
        self.pipetype = 'basic'

    def validate(self):
        """Validate if this segment's tile data is in order"""
        if self.haspipe:
            self.pipetype = 'basic'
        else:
            self.pipetype = None
            self.pipeconnection = None
        if self.hasrig:
            self.rigtype = 'basic'
        else:
            self.rigtype = None
            self.rigconnection = None


class TileGrid:
    def __init__(self, sizex, sizey) -> None:
        self.sizex = sizex
        self.sizey = sizey
        self.grid = [[Tile(x, y, 0) for x in range(sizex)] for y in range(sizey)]
        # grid[x][y] - down, right

        self.perlin_scale = 10
        self.perlin_octaves = 6
        self.perlin_seed = random.randint(0, 1000)
        self.centraltilelocation = (self.sizex // 2, self.sizey // 2)

        self.central_oil_probability = 0.2
        self.simple_oil_probability = 0.2
        self.oil_radius_ratio = 0.25

    def new_grid(self):
        """Do this, here you should do some random fuckery with price, it should somewhat resemble perlin noise
        i guess. Also, you should spread oil randomly"""
        noise = PerlinNoise(octaves=self.perlin_octaves, seed=self.perlin_seed)
        for y in range(self.sizey):
            for x in range(self.sizex):
                noise_val = noise([x / self.perlin_scale, y / self.perlin_scale])
                price = int((noise_val + 1) * 5)
                self.grid[y][x].price = max(1, min(price, 10))

        radius = min(self.sizex, self.sizey) * self.oil_radius_ratio

        for y in range(self.sizey):
            for x in range(self.sizex):
                distance = np.linalg.norm(np.array([x, y]) - np.array(self.centraltilelocation))
                if distance <= radius and random.random() < self.central_oil_probability:
                    self.grid[y][x].oiltype = 'central'
                elif self.grid[y][x].oiltype is None and random.random() < self.simple_oil_probability:
                    self.grid[y][x].oiltype = 'simple'

    def place_pipe(self, x_origin, y_origin, x_dest, y_dest, preview):

        nearbydestpipes = []
        if self.grid[x_dest-1][y_dest].pipetype is not None:
            nearbydestpipes.append('d')
        elif self.grid[x_dest+1][y_dest].pipetype is not None:
            nearbydestpipes.append('u')
        elif self.grid[x_dest][y_dest-1].pipetype is not None:
            nearbydestpipes.append('l')
        elif self.grid[x_dest][y_dest+1].pipetype is not None:
            nearbydestpipes.append('r')

        if abs(x_dest-x_origin) > abs(y_dest-y_origin):
            initialdirection = 'x'
            turn = [x_dest, y_origin]
        else:
            initialdirection = 'y'
            turn = [x_origin, y_dest]
        xstep = 1
        guaranteedxpipe = 'd'
        ystep = 1
        guaranteedypipe = 'r'
        if x_origin > x_dest:
            xstep = -1
            guaranteedxpipe = 'u'
        if y_origin > y_dest:
            ystep = -1
            guaranteedypipe = 'l'

        antixpipe = 'd' if guaranteedxpipe == 'u' else 'u'
        antiypipe = 'r' if guaranteedypipe == 'l' else 'l'

        potentialpipes = []
        current_point = [x_origin, y_origin]
        while current_point != turn:
            if initialdirection == 'x':
                if current_point == [x_origin, y_origin]:
                    potentialpipes.append([self.grid[current_point[0]][current_point[1]], [guaranteedxpipe]])
                else:
                    potentialpipes.append([self.grid[current_point[0]][current_point[1]],
                                          [guaranteedxpipe, antixpipe]])
                current_point = [current_point[0]+xstep, current_point[1]]
            else:
                if current_point == [x_origin, y_origin]:
                    potentialpipes.append([self.grid[current_point[0]][current_point[1]], [guaranteedypipe]])
                else:
                    potentialpipes.append([self.grid[current_point[0]][current_point[1]],
                                          [guaranteedypipe, antiypipe]])
                current_point = [current_point[0], current_point[1]+ystep]

        initialdirection = 'y' if initialdirection == 'x' else 'x'

        while current_point != [x_dest, y_dest]:
            if initialdirection == 'x':
                if current_point == turn:
                    potentialpipes.append([self.grid[current_point[0]][current_point[1]],
                                          [antixpipe, guaranteedypipe]])
                else:
                    potentialpipes.append([self.grid[current_point[0]][current_point[1]],
                                           [guaranteedypipe, antiypipe]])
                current_point = [current_point[0], current_point[1]+ystep]
            else:
                if current_point == turn:
                    potentialpipes.append([self.grid[current_point[0]][current_point[1]],
                                          [antiypipe, guaranteedxpipe]])
                else:
                    potentialpipes.append([self.grid[current_point[0]][current_point[1]],
                                           [guaranteedxpipe, antixpipe]])
                current_point = [current_point[0]+xstep, current_point[1]]

        potentialpipes.append(self.grid[x_dest, y_dest], [antixpipe])

        for tile in potentialpipes:
            tile.place_pipe()

    def place_rig(self, x, y, preview=False):
        tile = self.grid[x][y]

        if tile.can_place_rig() and preview:
            tile.rigtype = 'building'
        elif tile.can_place_rig() and not preview:
            tile.hasrig = True
        elif not tile.can_place_rig() and preview:
            tile.rigtype = 'invalid'


if __name__ == '__main__':
    g = TileGrid(10, 10)
