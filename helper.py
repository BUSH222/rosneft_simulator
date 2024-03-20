import random
from perlin_noise import PerlinNoise
import numpy as np


class Tile:
    """Class for handling a singular tile - square with pipes, oil, etc"""
    def __init__(self, x, y, price) -> None:
        """
        x, y - coordinates
        isowned, issurveyed, price - arguments for buying things and visibility of oil, upkeep will be calculated later
        pipetype - can be None, 'basic'
        None - no pipe, building - pipe under construction, basic - basic pipe, export - pipe is an export pipe.
        connection - connections of the pipe if exists (u, d, r, l, and all combinations of those, sorted) or None
        oiltype - can be None if no oil is present, 'simple' if oil is present but not central or 'central'
        oilquantity - only matters if oiltype is central
        hasrig - if the segment has a rig
        rigtype can be None, 'basic'
        spawntile - purely cosmetic - if the tile is spawn
        pipepreviewtype = 'valid', 'invalid', None
        rigpreviewtype = 'valid', 'invalid', None
        """
        self.x = x
        self.y = y
        self.price = price
        self.isowned = False
        self.issurveyed = False
        self.haspipe = False
        self.pipetype = None
        self.exportpipe = False
        self.connection = None
        self.oiltype = None
        self.oilquantity = 0
        self.originaloilquantity = self.oilquantity
        self.centraltilelocation = [-1, -1]
        self.hasrig = False
        self.rigtype = None
        self.spawntile = False
        self.pipepreviewtype = None
        self.rigpreviewtype = None

    def __repr__(self) -> str:
        return str(self.haspipe)
        # return str(self.connection)

    def can_place_pipe(self):
        """Whether or not a pipe can be placed on this segment"""
        return (not self.hasrig) and (not self.haspipe)  # and self.isowned and self.issurveyed

    def can_place_rig(self):
        """Whether or not a rig can be placed on this segment"""
        return (not self.hasrig) and (not self.haspipe)  # and self.isowned and self.issurveyed

    def place_pipe(self):
        """Place a pipe on the tile"""
        if not self.can_place_pipe():
            return False
        self.haspipe = True
        self.pipetype = 'basic'

    def delete_pipe(self):
        """Delete the pipe on the tile"""
        self.haspipe = False
        self.pipetype = None

    def place_rig(self, grid):

        if not self.can_place_rig():
            return False
        self.haspipe = False
        self.hasrig = True
        self.pipetype = 'basic'

    def validate(self, grid, sizex, sizey):
        """Validate if this segment's tile data is in order"""

        # validate grid placement
        if self.haspipe or self.hasrig:
            nearbypipes = []
            if self.y-1 >= 0:
                if grid[self.y-1][self.x].haspipe or grid[self.y-1][self.x].hasrig:
                    nearbypipes.append('u')
            if self.y+1 < sizex:
                if grid[self.y+1][self.x].haspipe or grid[self.y+1][self.x].hasrig:
                    nearbypipes.append('d')
            if self.x-1 >= 0:
                if grid[self.y][self.x-1].haspipe or grid[self.y][self.x-1].hasrig:
                    nearbypipes.append('l')
            if self.x+1 < sizey:
                if grid[self.y][self.x+1].haspipe or grid[self.y][self.x+1].hasrig:
                    nearbypipes.append('r')
            self.connection = ''.join(sorted(nearbypipes))
            # for s in grid:
            #    print(*s)
            print(self.x, self.y, self.connection)
        else:
            self.connection = None
            self.pipetype = None

    def draw(self):
        """This function handles the colors of the tile and the icons"""
        if self.pipepreviewtype == 'valid':
            return (0, 255, 0)
        elif self.pipepreviewtype == 'invalid':
            return (255, 0, 0)
        else:
            if self.haspipe:
                return (200, 200, 200)
            else:
                return (0, 0, 0)


class TileGrid:
    """Class for handling a 2d list of tiles - the playing field"""
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

    def place_pipes(self, x_origin, y_origin, x_dest, y_dest, preview, delete=False):
        """Function for placing a pipe in a triangle side shape, where:
        starter point is x_origin, y_origin
        end point is x_dest, y_dest
        preview doesn't actually place the pipes, only turns preview mode on.
        delete - delete the pipe if True"""
        if abs(x_dest-x_origin) > abs(y_dest-y_origin):
            initialdirection = 'x'
            turn = [x_dest, y_origin]
        else:
            initialdirection = 'y'
            turn = [x_origin, y_dest]
        xstep = 1
        ystep = 1
        if x_origin > x_dest:
            xstep = -1
        if y_origin > y_dest:
            ystep = -1

        potentialpipes = []
        current_point = [x_origin, y_origin]
        while current_point != turn:
            if initialdirection == 'x':
                if current_point == [x_origin, y_origin]:
                    potentialpipes.append(self.grid[current_point[0]][current_point[1]])
                else:
                    potentialpipes.append(self.grid[current_point[0]][current_point[1]])
                current_point = [current_point[0]+xstep, current_point[1]]
            else:
                if current_point == [x_origin, y_origin]:
                    potentialpipes.append(self.grid[current_point[0]][current_point[1]])
                else:
                    potentialpipes.append(self.grid[current_point[0]][current_point[1]])
                current_point = [current_point[0], current_point[1]+ystep]

        initialdirection = 'y' if initialdirection == 'x' else 'x'

        while current_point != [x_dest, y_dest]:
            if initialdirection == 'x':
                if current_point == turn:
                    potentialpipes.append(self.grid[current_point[0]][current_point[1]])
                else:
                    potentialpipes.append(self.grid[current_point[0]][current_point[1]])
                current_point = [current_point[0]+xstep, current_point[1]]
            else:
                if current_point == turn:
                    potentialpipes.append(self.grid[current_point[0]][current_point[1]])
                else:
                    potentialpipes.append(self.grid[current_point[0]][current_point[1]])
                current_point = [current_point[0], current_point[1]+ystep]

        potentialpipes.append(self.grid[x_dest][y_dest])
        if delete is True:
            for item in potentialpipes:
                item.delete_pipe()
            return True
        if not preview:
            if not all([tile.can_place_pipe() for tile in potentialpipes]):
                return False
            for item in potentialpipes:
                item.place_pipe()
        else:
            if all([tile.can_place_pipe() for tile in potentialpipes]):
                for item in potentialpipes:
                    item.pipepreviewtype = 'valid'
            else:
                for item in potentialpipes:
                    item.pipepreviewtype = 'invalid'

    def place_rig(self, x, y, preview=False):
        """Function for placing a rig on the tile:
        x, y are rig coordinates
        preview - if preview mode is on"""
        tile = self.grid[x][y]

        if tile.can_place_rig() and preview:
            tile.rigpreviewtype = 'valid'
        elif tile.can_place_rig() and not preview:
            tile.hasrig = True
        elif not tile.can_place_rig() and preview:
            tile.rigpreviewtype = 'invalid'

    def validate_all(self):
        """Validate and form connections between every single pipe"""
        for row in self.grid:
            for tile in row:
                tile.validate(self.grid, self.sizex, self.sizey)

    def clear_previews(self):
        """Clear all previews"""
        for row in self.grid:
            for tile in row:
                tile.pipepreviewtype = None


class Game:
    def __init__(self, budget) -> None:
        self.budget = budget
        self.grid = TileGrid(10, 10)
        self.exportpipecoords = [5, 0]
        self.exportpipedirection = 'r'
        self.exportpipelength = 2

    def generate_everything(self):
        pass

    def calculate_total_exports(self):
        pass

    def buy_tiles(self, x_origin, y_origin, x_dest, y_dest):
        pass

    def survey_tiles(self, x_origin, y_origin, x_dest, y_dest):
        pass


if __name__ == '__main__':
    g = TileGrid(10, 10)
