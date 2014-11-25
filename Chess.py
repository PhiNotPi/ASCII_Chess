from enum import Enum

Player = Enum('Player', 'PlayerOne PlayerTwo Undefined')
Pieces = ['King', 'Queen', 'Rook', 'Knight', 'Bishop', 'Pawn']

class Piece(str):

    def IsValidMove(self, FromCoord, ToCoord):
        print(self)
        print("Validation not done")

class King(Piece):

    CastleLegal = True  # Set to False when king or both rooks move
    CanCastle = False   # Set to True if CastleLegal and no pieces between king and rook
    
    def IsValidMove(self, FromCoord, ToCoord):

        move = [abs(ord(ToCoord[0]) - ord(FromCoord[0])),abs(ord(ToCoord[1]) - ord(FromCoord[1]))]

        # One square in any direction
        if move[0] <= 1 and move[1] <= 1:
            print("Valid move")
            return True

        # Castling - AND has higher priority than OR
        if King.CanCastle and move[1] == 0 and (move[0] == 2 or move[0] == 3):
            if self == "Player.PlayerOne" and FromCoord == "E0" or self == "Player.PlayerTwo" and FromCoord == "D7":
                print("Valid move")
                return True
        
        print("Invalid King move")
        return False

class Queen(Piece):

    def IsValidMove(self, FromCoord, ToCoord):

        move = [abs(ord(ToCoord[0]) - ord(FromCoord[0])),abs(ord(ToCoord[1]) - ord(FromCoord[1]))]

        # Diagonal and straight moves
        if move[0] == move[1] or move[0] == 0 or move[1] == 0:
            print("Valid Move")
            return True

        print("Invalid Queen move")
        return False

class Rook(Piece):

    def IsValidMove(self, FromCoord, ToCoord):
        
        move = [abs(ord(ToCoord[0]) - ord(FromCoord[0])),abs(ord(ToCoord[1]) - ord(FromCoord[1]))]

        # Straight moves
        if move[0] == 0 or move[1] == 0:
            print("Valid Move")
            return True

        print("Invalid Rook move")
        return False

class Knight(Piece):

    def IsValidMove(self, FromCoord, ToCoord):

        move = [abs(ord(ToCoord[0]) - ord(FromCoord[0])),abs(ord(ToCoord[1]) - ord(FromCoord[1]))]

        # L-shaped moves
        if move[0] == 1 and move[1] == 2 or move[0] == 2 and move[1] == 1:
            print("Valid Move")
            return True

        print("Invalid Knight move")
        return False

class Bishop(Piece):
    
    def IsValidMove(self, FromCoord, ToCoord):

        move = [abs(ord(ToCoord[0]) - ord(FromCoord[0])),abs(ord(ToCoord[1]) - ord(FromCoord[1]))]

        # Can only move diagonal
        if move[0] == move[1]:
            print("Valid Move")
            return True

        print("Invalid Bishop move")
        return False

class Pawn(Piece):

    # Set to True when a pawn moves two squares past
    # Pawn must be on square 3 for PlayerOne or square 4 for PlayerTwo
    CaptureEnPassant = False 
    
    def IsValidMove(self, FromCoord, ToCoord):

        move = [ord(ToCoord[0]) - ord(FromCoord[0]), ord(ToCoord[1]) - ord(FromCoord[1])]

        # Pawn on back row
        if FromCoord[1] == "0" or FromCoord[1] == "7":
            print("Pawn cannot start on back row")
            return False

        # Player.PlayerOne capture
        if self == "Player.PlayerOne" and abs(move[0]) == move[1] == 1:
            print("Valid Move")
            return True

        # Player.PlayerTwo capture
        if self == "Player.PlayerTwo" and abs(move[0]) == 1 and move[1] == -1:
            print("Valid Move")
            return True

        # Player.PlayerOne first move
        if self == "Player.PlayerOne" and FromCoord[1] == "1" and move[0] == 0 and move[1] == 2:
            print("Valid Move")
            return True

        # Player.PlayerTwo first move
        if self == "Player.PlayerTwo" and FromCoord[1] == "6" and move[0] == 0 and move[1] == -2:
            print("Valid Move")
            return True

        # Player.PlayerOne move
        if self == "Player.PlayerOne" and move[0] == 0 and move[1] == 1:
            print("Valid Move")
            return True

        # Player.PlayerTwo move
        if self == "Player.PlayerTwo" and move[0] == 0 and move[1] == -1:
            print("Valid Move")
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
            print("Valid Input")
            return True

    print("Invalid input")
    return False

if __name__ == "__main__":
    print("GAME START")

    # FOR TESTING PURPOSES ONLY
    # WORKS TO INPUT A PIECE AND MOVE
    
    pieces = ["King(Player.PlayerOne)", "Queen(Player.PlayerOne)", "Rook(Player.PlayerOne)",
              "Knight(Player.PlayerOne)", "Bishop(Player.PlayerOne)", "Pawn(Player.PlayerOne)"]

    move = input("Enter your piece, the starting square, and the ending square (i.e. King E0 F1) ").split(" ")
    if len(move) == 3 and IsValidInput(move[0], move[1], move[2]):
        exec(pieces[Pieces.index(move[0])]+".IsValidMove('"+move[1]+"','"+move[2]+"')")
    else:
        print("Invalid input")

    print("GAME_END")
