
# Othello states
#   self.grid   list with 63 elements 0=empty, 1=white, 2=black
#   self.player current player 1 or 2

class OthelloState:

    # Create a new state (possibly a successor of another)

    def __init__(self,ostate=None):
        if ostate==None:
            # No predecessor given, so create the initial configuration
            # Black starts
            self.player = 2
            # Empty grid
            self.grid = [0]*64
            # Initial configuration
            self.grid[3+3*8] = 2
            self.grid[4+4*8] = 2
            self.grid[3+4*8] = 1
            self.grid[4+3*8] = 1
            # A flag to show if the previous player moved or not
            self.previousMoved = True
        else:
            # Make a copy of the given predecessor state
            self.player = 3-ostate.player # The other player
            self.grid = ostate.grid.copy()
            self.previousMoved = False

    # Not the current player, but the other one

    def otherPlayer(self):
        return 3-self.player

    # Test if coordinate within grid.

    def inBounds(self,c):
        return (0 <= c and c <= 7)

    # Test if there is a contiguous line of opponent
    # pieces ending with a player piece from x,y to
    # x+i*dx,y+i*dx for some i>1

    def hasLine(self,x,y,dx,dy):
        lx = x+dx
        ly = y+dy
        opponentSeen = False
        while True:
#            if not self.inBounds(lx) or not self.inBounds(ly): # SLOW!
            if lx < 0 or lx > 7 or ly < 0 or ly > 7:
                return False
            if self.getCell(lx,ly) == self.otherPlayer():
                opponentSeen = True
            elif self.getCell(lx,ly) == 0:
                return False
            elif self.getCell(lx,ly) == self.player:
                return opponentSeen
            lx = lx + dx
            ly = ly + dy

    # Reverse a contiguous line of opponent
    # pieces ending with a player piece from x+xd,y+yd to
    # x+i*dx,y+i*dx for some i>1

    def setLine(self,x,y,dx,dy,player):
        lx = x+dx
        ly = y+dy
        opponentSeen = False
        while True:
            if not self.inBounds(lx) or not self.inBounds(ly):
                return # No line
            if self.getCell(lx,ly) == 3-player:
                opponentSeen = True
            elif self.getCell(lx,ly) == 0:
                return # No line
            elif self.getCell(lx,ly) == player:
                if opponentSeen:
                    lx = lx - dx
                    ly = ly - dy
#                    print("Setting cells from " + str(lx) + "," + str(ly) + " to " + str(x+dx) + "," + str(y+dy))
                    cnt = 0
                    while lx != x or ly != y:
                        self.setCell(lx,ly,player)
                        lx = lx - dx
                        ly = ly - dy
                        cnt = cnt + 1
#                    print(str(cnt) + " cells reversed")
                return
            lx = lx + dx
            ly = ly + dy

    # Actions possible in a state
    # Each action represented by triple (x,y,player)

    def actions(self):
        moves = list()
        for x in range(0,8):
            for y in range(0,8):
                if self.getCell(x,y) == 0 and (self.hasLine(x,y,0,1) or self.hasLine(x,y,1,1) or self.hasLine(x,y,1,0) or self.hasLine(x,y,0,-1) or self.hasLine(x,y,-1,-1) or self.hasLine(x,y,-1,0) or self.hasLine(x,y,-1,1) or self.hasLine(x,y,1,-1)):
                    moves.append( (x,y,self.player) )
        return moves

    # Get board contents. x is 0..7, y is 0..7

    def getCell(self,x,y):
        return self.grid[x+8*y]

    # Set board content.

    def setCell(self,x,y,value):
        self.grid[x+8*y] = value

    # Get successor of state with action

    def successor(self,action):
        sstate = OthelloState(self)
        x,y,player = action
        if sstate.getCell(x,y) != 0:
            print("Cell not empty. Cannot move.")
            exit(1)
        if self.player != player:
            print("Wrong player. Cannot move.")
            exit(1)
        sstate.setCell(x,y,player)
        sstate.setLine(x,y,-1,-1,player)
        sstate.setLine(x,y,-1,0,player)
        sstate.setLine(x,y,-1,1,player)
        sstate.setLine(x,y,0,-1,player)
        sstate.setLine(x,y,0,1,player)
        sstate.setLine(x,y,1,-1,player)
        sstate.setLine(x,y,1,0,player)
        sstate.setLine(x,y,1,1,player)
        # Turn all opponent pieces between the new piece
        # and the player old pieces.
        sstate.previousMoved = True
        return sstate

    # Count cells

    def count(self,player):
        count = 0
        for x in self.grid:
            if x == player:
                count = count + 1
        return count

    # Show state

    def printstate(self):
        for y in range(7,-1,-1):
            print(str(y) + "",end='')
            for x in range(0,8):
                if self.getCell(x,y) == 0:
                    print(".",end='')
                elif self.getCell(x,y) == 1:
                    print("O",end='')
                else:
                    print("X",end='')
            print("")
        print(" 01234567")

