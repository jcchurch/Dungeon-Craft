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

        self.__grid = []
        for h in range(height):
            self.__grid.append( ["|X"] * width )

        # 0 for an enterance on the width
        # 1 for an enterance on the height
        which = random.randint(0, 1)
        w = 0
        h = 0

        if which == 0:
            w = random.randint(0, width-1)
            h = random.randint(0, 1) * (height-1)
        else:
            w = random.randint(0, 1) * (width-1)
            h = random.randint(0, height-1)

        self.__grid[h][w] = "EE"
        self.__enterance = (w, h)
        self.__rooms = 0;
        self.__perimeter = [ (h, w) ]

    def enterance(self): return self.__enterance
    def width(self): return self.__width
    def height(self): return self.__height
    def size(self): return (self.__width, self.__height)

    def __str__(self):
       visual = ""
       for row in self.__grid:
           for cell in row:
               assert len(cell) == 2
               visual += cell
           visual += "\n"
       return visual

    def addRoom(self, minwidth, minheight, maxwidth, maxheight):
        width = random.randint(minwidth, maxwidth)
        height = random.randint(minheight, maxheight)

        # First, we randomly select a perimeter point
        (y, x) = random.choice(self.__perimeter)

        # Next, we want to position the new room with an edge on the perimeter,
        # but no other open spaces collide.
        
        # First, compile a list of all new room perimeter points and shuffle them.
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

            # Scan the internals of the shape. If any internals equal "  ",
            # reject the room.
            good_room = True
            j = top + 1
            while j < top + height - 1:
                i = left + 1
                while i < left + width - 1:
                    if self.__grid[j][i] == "  ":
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
                    self.__grid[j][i] = "  "
                    i += 1
                j += 1

            # While we're at it, let's rebuild the perimeter array
            # from scratch.
            self.__perimeter = []
            j = 1
            while j < self.__height - 1:
                i = 1
                while i < self.__width - 1:
                    if self.__grid[j][i] == "  ":
                        # If any of the 4 cardinal directions represent a non-space,
                        # add it to the list.
                        if self.__grid[j+1][i] == "|X" or \
                           self.__grid[j-1][i] == "|X" or \
                           self.__grid[j][i+1] == "|X" or \
                           self.__grid[j][i-1] == "|X":
                              self.__perimeter.append( (j, i) )
                    i += 1
                j += 1

            # We may overwrite the enterance, so let's add that back in.
            self.__grid[self.__enterance[1]][self.__enterance[0]] = "EE"
            return True
        return False
