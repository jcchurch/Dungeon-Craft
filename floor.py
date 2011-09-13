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

    def addRoom(self, minwidth, minheight, minwidth, minheight):
        
