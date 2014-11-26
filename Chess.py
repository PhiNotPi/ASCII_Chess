from enum import Enum

Player = Enum('Player', 'PlayerOne PlayerTwo Undefined')
Pieces = ['King', 'Queen', 'Rook', 'Knight', 'Bishop', 'Pawn']

class Board():

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
            self.data[6].append(Pawn(['P', Player.PlayerTwo]))

        self.data[7].append(Rook(['R', Player.PlayerTwo]))
        self.data[7].append(Knight(['N', Player.PlayerTwo]))
        self.data[7].append(Bishop(['B', Player.PlayerTwo]))
        self.data[7].append(Queen(['Q', Player.PlayerTwo]))
        self.data[7].append(King(['K', Player.PlayerTwo]))
        self.data[7].append(Bishop(['B', Player.PlayerTwo]))
        self.data[7].append(Knight(['N', Player.PlayerTwo]))
        self.data[7].append(Rook(['R', Player.PlayerTwo]))

    def Render(self, player):
        # Returns an ASCII representation of the board.
        # Prints board as other player views it (current player, not current viewer)

        if player is Player.PlayerOne:
            s = '   A B C D E F G H \n'
            for n in range(8):
                s += '  +-+-+-+-+-+-+-+-+\n'
                s += '%i |%s|\n' % (n, '|'.join([self.data[n][p][0] for p in range(8)]))
        else:
            s = '   H G F E D C B A \n'
            for n in range(8):
                s += '  +-+-+-+-+-+-+-+-+\n'
                s += '%i |%s|\n' % (7-n, '|'.join([self.data[7-n][7-p][0] for p in range(8)]))
        s += '  +-+-+-+-+-+-+-+-+'
        print(s)

    def Move(self, Mover, PieceName, FromCoord, ToCoord):
        blank = [' ', Player.Undefined]

        FromCoord = [int(ord(FromCoord[0])) - 65, int(ord(FromCoord[1])) - 48]
        ToCoord = [int(ord(ToCoord[0])) - 65, int(ord(ToCoord[1])) - 48]

        # Ensure player is moving a piece
        if self.data[FromCoord[1]][FromCoord[0]] == blank:
            print("No piece there")
            return False

        # Ensure player moves their own piece
        print(Mover)
        if self.data[FromCoord[1]][FromCoord[0]][1] != Mover:
            print("Please do not cheat - you are not allowed to move your opponent's piece")
            return False

        # Ensure player is moving specified piece
        if PieceName == 'K': PieceName = 'N'
        if self.data[FromCoord[1]][FromCoord[0]][0] != PieceName:
            print("Attempt to move wrong piece")
            return False

        # Ensure player is not capturing their own piece
        if self.data[FromCoord[1]][FromCoord[0]][1] == self.data[ToCoord[1]][ToCoord[0]][1]:
            print("Cannot capture your own piece")
            return False

        # Compile list of squares traveled on - don't do King or Knight
        Path = None
        if PieceName is 'R':
            t = True

        # Move piece is move is valid
        if self.data[FromCoord[1]][FromCoord[0]].IsValidMove(Path, FromCoord, ToCoord):
            self.data[ToCoord[1]][ToCoord[0]] = board.data[FromCoord[1]][FromCoord[0]]
            self.data[FromCoord[1]][FromCoord[0]] = blank
            self.Render(Player.PlayerOne if Mover == Player.PlayerTwo else Player.PlayerOne)
            return True
        else:
            print("Invalid move")
            return False

class Piece(list, Board):

    def IsValidMove(self, Path, FromCoord, ToCoord):
        print(self)
        print("Validation not done")
        return False

class King(Piece):

    CastleLegal = True  # Set to False when king or both rooks move
    CanCastle = False   # Set to True if CastleLegal and no pieces between king and rook
    
    def IsValidMove(self, Path, FromCoord, ToCoord):

        move = [abs(ToCoord[0] - FromCoord[0]), abs(ToCoord[1] - FromCoord[1])]

        # One square in any direction
        if move[0] <= 1 and move[1] <= 1:
            return True

        # Castling - AND has higher priority than OR
        if King.CanCastle and move[1] == 0 and (move[0] == 2 or move[0] == 3):
            if self[1] == Player.PlayerOne and FromCoord == "E0" or self[1] == Player.PlayerTwo and FromCoord == "E7":
                return True
        
        print("Invalid King move")
        return False

class Queen(Piece):

    def IsValidMove(self, Path, FromCoord, ToCoord):

        move = [abs(ToCoord[0] - FromCoord[0]), abs(ToCoord[1] - FromCoord[1])]

        # Diagonal and straight moves
        if move[0] == move[1] or move[0] == 0 or move[1] == 0:
            return True

        print("Invalid Queen move")
        return False

class Rook(Piece):

    def IsValidMove(self, Path, FromCoord, ToCoord):
        
        move = [abs(ToCoord[0] - FromCoord[0]), abs(ToCoord[1] - FromCoord[1])]

        # Straight moves
        if move[0] == 0 or move[1] == 0:
            return True

        print("Invalid Rook move")
        return False

class Knight(Piece):

    def IsValidMove(self, Path, FromCoord, ToCoord):

        move = [abs(ToCoord[0] - FromCoord[0]), abs(ToCoord[1] - FromCoord[1])]

        # L-shaped moves
        if move[0] == 1 and move[1] == 2 or move[0] == 2 and move[1] == 1:
            return True

        print("Invalid Knight move")
        return False

class Bishop(Piece):
    
    def IsValidMove(self, Path, FromCoord, ToCoord):

        move = [abs(ToCoord[0] - FromCoord[0]), abs(ToCoord[1] - FromCoord[1])]

        # Can only move diagonal
        if move[0] == move[1]:
            return True

        print("Invalid Bishop move")
        return False

class Pawn(Piece):

    # Set to True when a pawn moves two squares past
    # Pawn must be on square 3 for PlayerOne or square 4 for PlayerTwo
    Capture = False 
    
    def IsValidMove(self, Path, FromCoord, ToCoord):

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
            print("Valid Move")
            return True

        # Player.PlayerTwo move
        if self[1] == Player.PlayerTwo and move[0] == 0 and move[1] == -1:
            return True

        print("Invalid Pawn move")
        return False

def IsValidInput(PieceName, FromCoord, ToCoord):

    if PieceName not in Pieces:
        print("Invalid piece")
        print(Pieces)
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
    board.Render(Player.PlayerTwo)
    
    while True:
        
        turn = Player.PlayerOne
        
        while turn is Player.PlayerOne:
            move = input("Enter your piece, the starting square, and the ending square (i.e. King E0 F1) ").split(" ")
            if len(move) == 3 and IsValidInput(move[0], move[1], move[2]):
                if board.Move(Player.PlayerOne, move[0][0], move[1], move[2]):
                    turn = Player.PlayerTwo
            else:
                print("Invalid input")

        while turn is Player.PlayerTwo:
            move = input("Enter your piece, the starting square, and the ending square (i.e. King E0 F1) ").split(" ")
            if len(move) == 3 and IsValidInput(move[0], move[1], move[2]):
                if board.Move(Player.PlayerTwo, move[0][0], move[1], move[2]):
                    turn = Player.PlayerOne
            else:
                print("Invalid input")
