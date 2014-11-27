from enum import Enum

Player = Enum('Player', 'PlayerOne PlayerTwo Undefined')
Pieces = ['King', 'Queen', 'Rook', 'Knight', 'Bishop', 'Pawn']

class Board():

    CanCastle = [[False, False, False], [False, False, False]]

    def deepcopy(self):
        
        b = Board()

        for i in range(8):
            for j in range(8):
                if self.data[i][j][0] == 'R':
                    b.data[i][j] = Rook(['R', Player.PlayerOne])
                if self.data[i][j][0] == 'N':
                    b.data[i][j] = Knight(['N', Player.PlayerOne])
                if self.data[i][j][0] == 'B':
                    b.data[i][j] = Bishop(['B', Player.PlayerOne])
                if self.data[i][j][0] == 'Q':
                    b.data[i][j] = Queen(['Q', Player.PlayerOne])
                if self.data[i][j][0] == 'K':
                    b.data[i][j] = King(['K', Player.PlayerOne])

                    
                if self.data[i][j][0] == 'r':
                    b.data[i][j] = Rook(['r', Player.PlayerTwo])
                if self.data[i][j][0] == 'n':
                    b.data[i][j] = Knight(['n', Player.PlayerTwo])
                if self.data[i][j][0] == 'b':
                    b.data[i][j] = Bishop(['b', Player.PlayerTwo])
                if self.data[i][j][0] == 'q':
                    b.data[i][j] = Queen(['q', Player.PlayerTwo])
                if self.data[i][j][0] == 'k':
                    b.data[i][j] = King(['k', Player.PlayerTwo])
                
        return b

    # Constructor
    def __init__(self, blank = [' ', Player.Undefined]):
        self.data = [[]]

        for i in range(8):
            self.data.append([])
        
        self.data[0].append(Rook(['R', Player.PlayerOne]))
        self.data[0].append(Knight(['N', Player.PlayerOne]))
        self.data[0].append(Bishop(['B', Player.PlayerOne]))
        self.data[0].append(Queen(['Q', Player.PlayerOne]))
        self.data[0].append(King(['K', Player.PlayerOne]))
        self.data[0].append(Bishop(['B', Player.PlayerOne]))
        self.data[0].append(Knight(['N', Player.PlayerOne]))
        self.data[0].append(Rook(['R', Player.PlayerOne]))

        for i in range(8):
            self.data[1].append(Pawn(['P', Player.PlayerOne]))

        for i in range(4):
            for j in range(8):
                self.data[i+2].append(Piece(blank))

        for i in range(8):
            self.data[6].append(Pawn(['p', Player.PlayerTwo]))

        self.data[7].append(Rook(['r', Player.PlayerTwo]))
        self.data[7].append(Knight(['n', Player.PlayerTwo]))
        self.data[7].append(Bishop(['b', Player.PlayerTwo]))
        self.data[7].append(Queen(['q', Player.PlayerTwo]))
        self.data[7].append(King(['k', Player.PlayerTwo]))
        self.data[7].append(Bishop(['b', Player.PlayerTwo]))
        self.data[7].append(Knight(['n', Player.PlayerTwo]))
        self.data[7].append(Rook(['r', Player.PlayerTwo]))


    def Render(self, player):
        # Returns an ASCII representation of the board.
        # Prints board as other player views it (current player, not current viewer)

        if player is Player.PlayerOne:
            s = '  +-+-+-+-+-+-+-+-+\n'
            for n in range(8):
                s += '%i |%s|\n' % (8-n, '|'.join([self.data[7-n][p][0] for p in range(8)]))
                s += '  +-+-+-+-+-+-+-+-+\n'
            s += '   A B C D E F G H \n'
        else:
            s = '  +-+-+-+-+-+-+-+-+\n'
            for n in range(8):
                s += '%i |%s|\n' % (n+1, '|'.join([self.data[n][7-p][0] for p in range(8)]))
                s += '  +-+-+-+-+-+-+-+-+\n'
            s += '   H G F E D C B A \n'
        print(s)

    def Move(self, Mover, PieceName, FromCoord, ToCoord):
        blank = [' ', Player.Undefined]

        FromCoord = [int(ord(FromCoord[0])) - 65, int(ord(FromCoord[1])) - 49]
        ToCoord = [int(ord(ToCoord[0])) - 65, int(ord(ToCoord[1])) - 49]
        MoveCoords = [abs(ToCoord[0] - FromCoord[0]), abs(ToCoord[1] - FromCoord[1])]
        
        # Ensure player is moving a piece
        if self.data[FromCoord[1]][FromCoord[0]] == blank:
            print("No piece there")
            return False

        # Ensure player moves their own piece
        if self.data[FromCoord[1]][FromCoord[0]][1] != Mover:
            print("Please do not cheat - you are not allowed to move your opponent's piece")
            return False

        # Ensure player is moving specified piece
        PieceName = 'N' if PieceName == 'Kn' else PieceName[0]
        if self.data[FromCoord[1]][FromCoord[0]][0].upper() != PieceName[0]:
            print("Attempt to move wrong piece")
            return False

        # Ensure player is not capturing their own piece
        if self.data[FromCoord[1]][FromCoord[0]][1] == self.data[ToCoord[1]][ToCoord[0]][1]:
            print("Cannot capture your own piece")
            return False

        # Make sure move follows correct moving pattern
        if not self.data[FromCoord[1]][FromCoord[0]].IsValidMovePattern(FromCoord, ToCoord):
            print("Invalid move")
            return False
            
        # Compile list of squares traveled on - don't do Knight
        if PieceName is 'R':

            # One of these is always 0 because the move pattern was already checked
            # -1 to skip counting new square
            for i in range(MoveCoords[0] + MoveCoords[1] - 1):

                # Vertical move
                if ToCoord[0] - FromCoord[0] == 0:
                    j = (i + 1) if ToCoord[1] - FromCoord[1] > 0 else (-1 - i)
                    if self.data[FromCoord[1] + j][FromCoord[0]][0] is not ' ':
                        print("Your rook cannot run over pieces")
                        return False

                # Horizontal move
                else:
                    j = (i + 1) if ToCoord[0] - FromCoord[0] > 0 else (-1 - i)
                    if self.data[FromCoord[1]][FromCoord[0] + j][0] is not ' ':
                        print("Your rook cannot run over pieces")
                        return False

            # At this point, the move is valid
            # Check if this rook has moved before
            if not self.data[FromCoord[1]][FromCoord[0]].HasMoved:
                self.data[FromCoord[1]][FromCoord[0]].HasMoved = True
                if Mover == Player.PlayerOne:
                    if FromCoord == [0,0]:
                        self.CanCastle[0][0] = True
                    if FromCoord == [7,0]:
                        self.CanCastle[0][1] = True
                else:
                    print(FromCoord)
                    if FromCoord == [0,7]:
                        self.CanCastle[1][0] = True
                    if FromCoord == [7,7]:
                        self.CanCastle[1][1] = True

        if PieceName is 'B':

            # -1 to skip counting new square
            for i in range(abs(MoveCoords[0]) - 1):

                j = (i + 1) if ToCoord[1] - FromCoord[1] > 0 else (-1 - i)
                k = (i + 1) if ToCoord[0] - FromCoord[0] > 0 else (-1 - i)
                
                if self.data[FromCoord[1] + j][FromCoord[0] + k][0] is not ' ':
                    print("Your bishop cannot run over pieces")
                    return False

        if PieceName is 'Q':

            # Same as rook and bishop methods
            if MoveCoords[0] == 0 or MoveCoords[1] == 0:
                for i in range(MoveCoords[0] + MoveCoords[1] - 1):
                    
                    # Vertical move
                    if ToCoord[0] - FromCoord[0] == 0:
                        j = (i + 1) if ToCoord[1] - FromCoord[1] > 0 else (-1 - i)
                        if self.data[FromCoord[1] + j][FromCoord[0]][0] is not ' ':
                            print("Your queen cannot run over pieces")
                            return False
                    else:
                        j = (i + 1) if ToCoord[0] - FromCoord[0] > 0 else (-1 - i)
                        if self.data[FromCoord[1]][FromCoord[0] + j][0] is not ' ':
                            print("Your queen cannot run over pieces")
                            return False

            # Diagonal move
            else:
                for i in range(abs(MoveCoords[0]) - 1):

                    j = (i + 1) if ToCoord[1] - FromCoord[1] > 0 else (-1 - i)
                    k = (i + 1) if ToCoord[0] - FromCoord[0] > 0 else (-1 - i)
                    
                    if self.data[FromCoord[1] + j][FromCoord[0] + k][0] is not ' ':
                        print("Your queen cannot run over pieces")
                        return False

        if PieceName is 'P':

            # Normal move
            if MoveCoords[0] == 0:

                i = 1 if ToCoord[1] - FromCoord[1] > 0 else -1

                # First move
                if MoveCoords[1] == 2:
                    
                    if self.data[ToCoord[1]][ToCoord[0]][0] != ' ' or self.data[ToCoord[1]-i][ToCoord[0]][0] != ' ':
                        print("Your pawn cannot run into pieces")
                        return False

                # Normal move
                else:
                    if self.data[ToCoord[1]][ToCoord[0]][0] != ' ':
                        print("Your pawn cannot run into pieces")
                        return False

            #Capture
            else:
                if self.data[ToCoord[1]][ToCoord[0]][0] == ' ':
                    print("Your pawn cannot move diagonally")
                    return False

        if PieceName is 'K':

            if MoveCoords[0] > 1:

                if self.CanCastle[0 if Mover is Player.PlayerOne else 1][2]:
                    print("You cannot castle after you have moved your king")
                    return False
                
                if MoveCoords[0] == 2:
                    if self.CanCastle[0 if Mover is Player.PlayerOne else 1][1]:
                        print("This rook has been moved already")
                        return False
                    
                    if self.data[ToCoord[1]][ToCoord[0]][0] != ' ' or self.data[ToCoord[1]][ToCoord[0]-1][0] != ' ':
                        print("Cannot castle through pieces")
                        return False

                    self.data[ToCoord[1]][ToCoord[0]-1] = board.data[ToCoord[1]][ToCoord[0]+1]
                    board.data[ToCoord[1]][ToCoord[0]+1] = blank

                if MoveCoords[0] == 3:
                    if self.CanCastle[0 if Mover is Player.PlayerOne else 1][0]:
                        print("This rook has been moved already")
                        return False
                    
                    if self.data[ToCoord[1]][ToCoord[0]][0] != ' ' or self.data[ToCoord[1]][ToCoord[0]+1][0] != ' ' or self.data[ToCoord[1]][ToCoord[0]+2][0] != ' ':
                        print("Cannot castle through pieces")
                        return False

                    self.data[ToCoord[1]][ToCoord[0]+1] = board.data[ToCoord[1]][ToCoord[0]-1]
                    board.data[ToCoord[1]][ToCoord[0]-1] = blank
                    
            # No more castling allowed if king is moved
            self.CanCastle[0 if Mover is Player.PlayerOne else 1] = [True, True, True]
    
        self.data[ToCoord[1]][ToCoord[0]] = board.data[FromCoord[1]][FromCoord[0]]
        self.data[FromCoord[1]][FromCoord[0]] = blank
        return True

class Piece(list):

    def IsValidMovePattern(self, FromCoord, ToCoord):
        print(self)
        print("Validation not done")
        return False

class King(Piece):

    def IsValidMovePattern(self, FromCoord, ToCoord):

        move = [abs(ToCoord[0] - FromCoord[0]), abs(ToCoord[1] - FromCoord[1])]

        # One square in any direction
        if move[0] <= 1 and move[1] <= 1:
            return True

        # Castling - AND has higher priority than OR
        if move[1] == 0 and (move[0] == 2 or move[0] == 3):
            if self[1] == Player.PlayerOne and FromCoord == [4,0] or self[1] == Player.PlayerTwo and FromCoord == [4,7]:
                return True
        
        print("Invalid king move")
        return False

class Queen(Piece):

    def IsValidMovePattern(self, FromCoord, ToCoord):

        move = [abs(ToCoord[0] - FromCoord[0]), abs(ToCoord[1] - FromCoord[1])]

        # Diagonal and straight moves
        if move[0] == move[1] or move[0] == 0 or move[1] == 0:
            return True

        print("Invalid queen move")
        return False

class Rook(Piece):

    HasMoved = False
    
    def IsValidMovePattern(self, FromCoord, ToCoord):

        move = [ToCoord[0] - FromCoord[0], ToCoord[1] - FromCoord[1]]

        if move[0] == 0 or move[1] == 0:
            return True

        print("Invalid rook move")
        return False

class Knight(Piece):

    def IsValidMovePattern(self, FromCoord, ToCoord):

        move = [abs(ToCoord[0] - FromCoord[0]), abs(ToCoord[1] - FromCoord[1])]

        # L-shaped moves
        if move[0] == 1 and move[1] == 2 or move[0] == 2 and move[1] == 1:
            return True

        print("Invalid knight move")
        return False

class Bishop(Piece):
    
    def IsValidMovePattern(self, FromCoord, ToCoord):

        move = [abs(ToCoord[0] - FromCoord[0]), abs(ToCoord[1] - FromCoord[1])]

        # Can only move diagonal
        if move[0] == move[1]:
            return True

        print("Invalid bishop move")
        return False

class Pawn(Piece):

    # Set to True when a pawn moves two squares past
    # Pawn must be on square 3 for PlayerOne or square 4 for PlayerTwo
    Capture = False 
    
    def IsValidMovePattern(self, FromCoord, ToCoord):

        move = [ToCoord[0] - FromCoord[0], ToCoord[1] - FromCoord[1]]
        
        # Player.PlayerOne pawn on back row
        if FromCoord[1] == "0" or FromCoord[1] == "7":
            print("Pawn cannot start on back row")
            return False

        # Player.PlayerOne capture
        if self[1] == Player.PlayerOne and abs(move[0]) == move[1] == 1:
            return True

        # Player.PlayerTwo capture
        if self[1] == Player.PlayerTwo and abs(move[0]) == 1 and move[1] == -1:
            return True

        # Player.PlayerOne first move
        if self[1] == Player.PlayerOne and FromCoord[1] == 1 and move[0] == 0 and move[1] == 2:
            return True

        # Player.PlayerTwo first move
        if self[1] == Player.PlayerTwo and FromCoord[1] == 6 and move[0] == 0 and move[1] == -2:
            return True

        # Player.PlayerOne move
        if self[1] == Player.PlayerOne and move[0] == 0 and move[1] == 1:
            return True

        # Player.PlayerTwo move
        if self[1] == Player.PlayerTwo and move[0] == 0 and move[1] == -1:
            return True

        print("Invalid pawn move")
        return False

def IsValidInput(PieceName, FromCoord, ToCoord):

    if len(FromCoord) != len(ToCoord) != 2:
        print("Invalid input")
        return False

    if PieceName not in Pieces:
        print("Invalid piece")
        return False

    if FromCoord == ToCoord:
        print("You are already on this square")
        return False

    if FromCoord[0] in 'ABCDEFGH' and ToCoord[0] in 'ABCDEFGH':
        if FromCoord[1] in '01234567' and ToCoord[1] in '01234567':
            return True

    print("Invalid input")
    return False

if __name__ == "__main__":

    board = Board()
    board.Render(Player.PlayerOne)
    turn = Player.PlayerOne
    
    while True:
        
        while turn is Player.PlayerOne:
            move = input("Enter your piece, the starting square, and the ending square (i.e. King E0 F1) ").split(" ")
            if len(move) == 3 and IsValidInput(move[0], move[1], move[2]):
                if board.Move(Player.PlayerOne, move[0][0:2], move[1], move[2]):
                    turn = Player.PlayerTwo
                    board.Render(Player.PlayerTwo)
            else:
                print("Invalid input")

        while turn is Player.PlayerTwo:

            move = input("Enter your piece, the starting square, and the ending square (i.e. King E0 F1) ").split(" ")
            if len(move) == 3 and IsValidInput(move[0], move[1], move[2]):
                if board.Move(Player.PlayerTwo, move[0][0:2], move[1], move[2]):
                    turn = Player.PlayerOne
                    board.Render(Player.PlayerOne)
            else:
                print("Invalid input")
