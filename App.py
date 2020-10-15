import random
from os import system

class Tic:
    def __init__(self):
        self.board = ["-"]*9
    def printboard(self):
        print(" | ".join([i for i in self.board[0:3]]))
        print(" | ".join([i for i in self.board[3:6]]))
        print(" | ".join([i for i in self.board[6:10]]))
        print()
    def CheckForWin(self,BoardCheck,Li):
        return (BoardCheck[0]==BoardCheck[1]==BoardCheck[2]==Li or 
               BoardCheck[3]==BoardCheck[4]==BoardCheck[5]==Li or 
               BoardCheck[6]==BoardCheck[7]==BoardCheck[8]==Li or 
               BoardCheck[0]==BoardCheck[3]==BoardCheck[6]==Li or  
               BoardCheck[1]==BoardCheck[4]==BoardCheck[7]==Li or 
               BoardCheck[2]==BoardCheck[5]==BoardCheck[8]==Li or 
               BoardCheck[0]==BoardCheck[4]==BoardCheck[8]==Li or 
               BoardCheck[2]==BoardCheck[4]==BoardCheck[6]==Li)  
    def HumanMove(self,Num=None):
        if Num != None:
            self.board[Num-1] = "X"
            return
        self.run = True
        while self.run:
            self.Humanpos = input("Choose a position 1-9: ")
            if self.Humanpos.isdigit() == False or not 0 < int(self.Humanpos) < 10 or self.board[int(self.Humanpos)-1] != "-":
                continue
            self.board[int(self.Humanpos)-1] = "X"
            self.run = False
    def NonHumanMove(self):
        self.PossibleBotMoves = [c for c,let in enumerate(self.board) if let=="-"]
        self.BoardCopy = self.board.copy()
        for i in ["O","X"]:
            for move in self.PossibleBotMoves:
                self.BoardCopy = self.board.copy()
                self.BoardCopy[move] = i
                if self.CheckForWin(self.BoardCopy,i):  
                    return move
            
        if 4 in  self.PossibleBotMoves:
            return 4

        self.cornerlist = []
        for move in self.PossibleBotMoves:
            if move == 0 or move == 2 or move == 8 or move == 6:
                self.cornerlist.append(move)
        if len(self.cornerlist) > 0:
            self.r = int(random.choice(self.cornerlist))
            return self.r 

        self.edgeList = []
        for move in self.PossibleBotMoves:
            if move == 1 or move == 3 or move == 5 or move == 7:
                self.edgeList.append(move)
        if len(self.edgeList) > 0:
            return int(random.choice(self.edgeList))
        

        return -1
    def start(self):
        self.printboard()
        while True:
            if not self.CheckForWin(self.board,"O"):
                self.HumanMove()
            else:
                print("Bot won, You lost gg")
                break
            if not self.CheckForWin(self.board,"X"):
                self.MoveToMake = self.NonHumanMove()
                if self.MoveToMake == -1:    
                    system("cls")
                    self.printboard()
                    print("Tie.")
                    break
                self.board[self.MoveToMake] = "O"
            else:
                system("cls")
                self.printboard()
                print("Nice you won")
                break
            system("cls")
            self.printboard()
            

if __name__ == "__main__":
    T = Tic()   
    T.start()