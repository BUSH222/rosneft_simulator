import random


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
        buypreview - buy preview (True - on)
        surveypreview - survey preview (True - on)
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
        self.buypreview = False
        self.surveypreview = False
        self.baseprice = 5

    def __repr__(self) -> str:
        return f'{self.x}, {self.y}'
        # return str(self.connection)

    def can_place_pipe(self):
        """Whether or not a pipe can be placed on this segment"""
        return (not self.hasrig) and (not self.haspipe) and self.isowned and self.issurveyed

    def can_place_rig(self):
        """Whether or not a rig can be placed on this segment"""
        return (not self.hasrig) and (not self.haspipe)\
            and self.oiltype is not None and self.isowned and self.issurveyed

    def place_pipe(self):
        """Place a pipe on the tile"""
        if not self.can_place_pipe():
            return False
        self.haspipe = True
        self.pipetype = 'basic'
        return self.baseprice

    def delete_pipe(self):
        """Delete the pipe on the tile"""
        if not self.exportpipe:
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
            if self.y+1 < sizey:
                if grid[self.y+1][self.x].haspipe or grid[self.y+1][self.x].hasrig:
                    nearbypipes.append('d')
            if self.x-1 >= 0:
                if grid[self.y][self.x-1].haspipe or grid[self.y][self.x-1].hasrig:
                    nearbypipes.append('l')
            if self.x+1 < sizex:
                if grid[self.y][self.x+1].haspipe or grid[self.y][self.x+1].hasrig:
                    nearbypipes.append('r')
            self.connection = ''.join(sorted(nearbypipes))
            # for s in grid:
            #    print(*s)
            # print(self.x, self.y, self.connection)
        else:
            self.connection = None
            self.pipetype = None

    def draw(self):
        """This function handles the colors of the tile and the icons
        Returns a list [color (if exists else None), icon (if exists else None)]"""
        out = [None, None]
        # oil
        if self.oiltype == 'central':
            out[0] = (100, 100, 100)
        elif self.oiltype == 'simple':
            out[0] = (200, 200, 200)
        else:
            out[0] = None

        # pipes and rigs
        if self.haspipe:
            if self.exportpipe:
                out[0] = (0, 0, 255)
            if self.connection is None or self.connection == '':
                out[1] = 'dlru'
            else:
                out[1] = self.connection
        elif self.hasrig:
            out[1] = 'rig'
        if self.pipepreviewtype == 'valid':
            out[1] = 'greendlru'
        elif self.pipepreviewtype == 'invalid':
            out[1] = 'reddlru'
        elif self.rigpreviewtype == 'valid':
            out[0] = (0, 255, 0)
        elif self.rigpreviewtype == 'invalid':
            out[0] = (255, 0, 0)

        if self.buypreview:
            if not self.isowned:
                out[0] = (self.price*4-1, self.price*4-1, 0)
            else:
                out[0] = (100, 100, 100)

        if self.surveypreview:
            if not self.issurveyed:
                out[0] = (100, 100, 0)
            else:
                out[0] = (100, 100, 100)
        return out


class TileGrid:
    """Class for handling a 2d list of tiles - the playing field"""
    def __init__(self, sizex, sizey, budget) -> None:
        self.budget = budget
        self.sizex = sizex
        self.sizey = sizey
        self.grid = [[Tile(x, y, random.randint(16, 64)) for x in range(sizex)] for y in range(sizey)]
        # grid[x][y] - down, right

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

        potentialcoords = []
        current_point = [x_origin, y_origin]
        while current_point != turn:
            if initialdirection == 'x':
                potentialcoords.append(current_point)
                current_point = [current_point[0]+xstep, current_point[1]]
            else:
                potentialcoords.append(current_point)
                current_point = [current_point[0], current_point[1]+ystep]

        initialdirection = 'y' if initialdirection == 'x' else 'x'

        while current_point != [x_dest, y_dest]:
            if initialdirection == 'x':
                potentialcoords.append(current_point)
                current_point = [current_point[0]+xstep, current_point[1]]
            else:
                potentialcoords.append(current_point)
                current_point = [current_point[0], current_point[1]+ystep]
        potentialcoords.append([x_dest, y_dest])

        # keep only valid coordinates
        potentialpipes = []
        for item in potentialcoords:
            if (0 <= item[0] < self.sizey) and (0 <= item[1] < self.sizex):
                potentialpipes.append(self.grid[item[0]][item[1]])

        if delete is True:
            for item in potentialpipes:
                item.delete_pipe()
            return True
        if not preview:
            if not all([tile.can_place_pipe() for tile in potentialpipes]):
                return False
            for item in potentialpipes:
                item.place_pipe()
            return True
        else:
            if all([tile.can_place_pipe() for tile in potentialpipes]):
                for item in potentialpipes:
                    item.pipepreviewtype = 'valid'
                return True
            else:
                for item in potentialpipes:
                    item.pipepreviewtype = 'invalid'
                return False

    def place_rig(self, x, y, preview=False, delete=False):
        """Function for placing a rig on the tile:
        x, y are rig coordinates
        preview - if preview mode is on"""
        if not ((0 <= x < self.sizey) and (0 <= y < self.sizex)):
            return False
        tile = self.grid[x][y]
        if delete:
            tile.hasrig = False
            return True
        if tile.can_place_rig() and preview:
            tile.rigpreviewtype = 'valid'
        elif not tile.can_place_rig() and preview:
            tile.rigpreviewtype = 'invalid'
        elif tile.can_place_rig() and not preview:
            tile.hasrig = True

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
                tile.rigpreviewtype = None
                tile.surveypreview = False
                tile.buypreview = False

    def calculate_total_exports(self):
        pass  # i will do this

    def generate_oil_deposits(self, num_central_tiles=20):
        width = len(self.grid)
        height = len(self.grid[0])

        # Generate central oil tiles
        for _ in range(num_central_tiles):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            self.grid[x][y].oiltype = 'central'
            self.grid[x][y].oilquantity = random.randint(20, 500)

        # Generate oval-like shapes around each central tile
        for x in range(width):
            for y in range(height):
                if self.grid[x][y].oiltype == 'central':
                    oval_width = random.randint(2, 10)
                    oval_height = random.randint(2, 10)
                    for dx in range(-oval_width, oval_width+1):
                        for dy in range(-oval_height, oval_height+1):
                            nx = x + dx
                            ny = y + dy
                            if (nx >= 0 and nx < width and ny >= 0 and ny < height
                               and (dx/oval_width)**2 + (dy/oval_height)**2 <= 1):
                                self.grid[nx][ny].oiltype = 'simple'
                                self.grid[nx][ny].centraltilelocation = (x, y)

    def place_export_pipe(self):
        if random.choice([True, False]):
            x_coord = random.randint(0, self.sizex - 1)
            y_coord = self.sizey - 1
        else:
            x_coord = 0
            y_coord = random.randint(0, self.sizey - 1)

        self.grid[y_coord][x_coord].haspipe = True
        self.grid[y_coord][x_coord].exportpipe = True

    def calculate_total_profit(self):
        pass

    def buy_tiles(self, x_origin, y_origin, x_dest, y_dest, preview=False):
        total_cost = 0

        for x in range(min(x_origin, x_dest), max(x_origin, x_dest) + 1):
            for y in range(min(y_origin, y_dest), max(y_origin, y_dest) + 1):
                if self.sizey > y >= 0 and self.sizex > x >= 0:
                    if not self.grid[y][x].isowned:
                        total_cost += self.grid[y][x].price

        if total_cost > self.budget:
            return False

        for x in range(min(x_origin, x_dest), max(x_origin, x_dest) + 1):
            for y in range(min(y_origin, y_dest), max(y_origin, y_dest) + 1):
                if self.sizey > y >= 0 and self.sizex > x >= 0:
                    if not preview:
                        if not self.grid[y][x].isowned:
                            self.grid[y][x].isowned = True
                            self.budget -= self.grid[y][x].price
                    else:
                        self.grid[y][x].buypreview = True

        return True

    def survey_tiles(self, x_origin, y_origin, x_dest, y_dest, preview=False):
        for x in range(min(x_origin, x_dest), max(x_origin, x_dest) + 1):
            for y in range(min(y_origin, y_dest), max(y_origin, y_dest) + 1):
                if self.sizey > y >= 0 and self.sizex > x >= 0:
                    if not preview:
                        if not self.grid[y][x].issurveyed:
                            self.grid[y][x].issurveyed = True
                            self.budget -= 5  # survey price
                    else:
                        self.grid[y][x].surveypreview = True

        return True


if __name__ == '__main__':
    g = TileGrid(10, 10, 500000)
