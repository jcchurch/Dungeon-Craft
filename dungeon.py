import random

class Dungeon:
    """
    This class represents a bare floor with no rooms or hallways.
    It will select one tile along the perimeter of the floor to
    act as an enterance point.

    Dungeon(width=40, height=20)
    enterance() - Returns a (x, y) tuple of the Dungeon Enterance.
    width() - Returns the width of the floor
    height() - Returns the height of the floor
    size() - Returns a (width, height) tuple of the floor
    """

    def __init__(self, width=40, height=20):
        """
    Dungeon(width, height)
    Initalize a floor of desired width and height.
        """

        assert width > 2
        assert height > 2

        self.__width = width
        self.__height = height

        # Grid Constants.
        self.__WALL = 0
        self.__ENTERANCE = 1
        self.__OPEN = 2
        self.__CHEST = 3
        self.__MONSTER = 4

        self.__grid = []
        for h in range(height):
            self.__grid.append( [self.__WALL] * width )

        # 0 for an enterance on the width
        # 1 for an enterance on the height
        w = 0
        h = 0

        if random.randint(0, 1) == 0:
            w = random.randint(1, width-2)
            h = random.randint(0, 1) * (height-1)
        else:
            w = random.randint(0, 1) * (width-1)
            h = random.randint(1, height-2)

        self.__grid[h][w] = self.__ENTERANCE
        self.__enterance = (w, h)
        self.__rooms = 0;
        self.buildPerimeter()

    def enterance(self): return self.__enterance
    def width(self): return self.__width
    def height(self): return self.__height
    def size(self): return (self.__width, self.__height)

    def __str__(self):
       visual = ""
       for row in self.__grid:
           for cell in row:
               if cell == self.__WALL:      visual += "|X"
               if cell == self.__ENTERANCE: visual += "EE"
               if cell == self.__CHEST:     visual += "CC"
               if cell == self.__MONSTER:   visual += "MM"
               if cell == self.__OPEN:      visual += "  "

           visual += "\n"
       return visual

    def buildPerimeter(self):
        self.__perimeter = []
        j = 1
        while j < self.__height - 1:
            i = 1
            while i < self.__width - 1:
                if self.__grid[j][i] == self.__WALL:
                    # If any of the 4 cardinal directions represent a non-space,
                    # add it to the list.
                    if self.__grid[j+1][i] != self.__WALL or \
                       self.__grid[j-1][i] != self.__WALL or \
                       self.__grid[j][i+1] != self.__WALL or \
                       self.__grid[j][i-1] != self.__WALL:
                          self.__perimeter.append( (j, i) )
                i += 1
            j += 1

    def addRoom(self, minwidth, minheight, maxwidth, maxheight, chestProbability, monsterProbability):
        width = random.randint(minwidth, maxwidth)
        height = random.randint(minheight, maxheight)

        # First, we randomly select a perimeter point
        (y, x) = random.choice(self.__perimeter)

        # Next, we want to position the new room with an edge on the perimeter,
        # but no other open spaces collide.

        # Compile a list of all our new room perimeter points and shuffle them.
        new_room_perimeter = []
        for w in range(width):
            new_room_perimeter.append( [0, w] )
            new_room_perimeter.append( [height-1, w] )

        for h in range(1, height-1):
            new_room_perimeter.append( [h, 0] )
            new_room_perimeter.append( [h, width-1] )

        random.shuffle(new_room_perimeter)

        # Now we sequentially go through the randomized order of new_room_perimeter
        # and select the first one that meets our criteria.
        for (p,q) in new_room_perimeter:
            # Compute the top and left corners of the shape.    
            top = y - p
            left = x - q
            # If any position of the room expands past the end of the board,
            # reject the room.
            if top < 0: continue
            if left < 0: continue
            if left + width >= self.__width: continue
            if top + height >= self.__height: continue

            # Scan the internals of the shape. If any internals equal an open space
            # reject the room.
            good_room = True
            j = top + 1
            while j < top + height - 1:
                i = left + 1
                while i < left + width - 1:
                    if self.__grid[j][i] == self.__OPEN:
                        good_room = False
                    i += 1
                j += 1

            if good_room == False:
                continue

            # Let's build our new room.
            # Yes, in the middle of a for loop, but here's the
            # best place to do it.
            j = top
            while j < top + height:
                i = left
                while i < left + width:
                    self.__grid[j][i] = self.__OPEN
                    i += 1
                j += 1

            # Rebuild the perimeter
            self.buildPerimeter()

            # Let's place the chest.
            if random.random() < chestProbability:
                # A chest will appear anywhere along the edge of the room.
                x = random.randint(top, top+height-1)
                y = random.randint(left, left+width-1)
                
                if random.randint(0, 1) == 0:
                    x = top + random.randint(0, 1) * (height-1)
                else:
                    y = left + random.randint(0, 1) * (width-1)

                self.__grid[x][y] = self.__CHEST

            # Let's place a monster.
            if random.random() < monsterProbability:
                # A monster can appear anywhere
                x = random.randint(top, top+height-1)
                y = random.randint(left, left+width-1)
                self.__grid[x][y] = self.__MONSTER

            # We may overwrite the enterance, so let's add that back in.
            self.__grid[self.__enterance[1]][self.__enterance[0]] = self.__ENTERANCE
            self.__rooms += 1
            return True
        return False

    def randomFloor(self, minrooms, maxrooms, minwidth, minheight, maxwidth, maxheight, chestProbability, monsterProbability):
        rooms = random.randint(minrooms, maxrooms)
        i = 0
        while i < rooms:
            self.addRoom(minwidth, minheight, maxwidth, maxheight, chestProbability, monsterProbability)
            i += 1

if __name__ == '__main__':
    f = Dungeon();
    f.randomFloor(4, 20, 2, 6, 2, 6, 0.1, 0.5)
    print f
