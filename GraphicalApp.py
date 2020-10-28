import pygame
from App import Tic

pygame.font.init() 
Width,Height = 570,587
screen = pygame.display.set_mode((Width,Height))
pygame.display.set_caption("TicTacToe")
clock = pygame.time.Clock()

Letter_x = pygame.image.load("letter-x.png")
Letter_o = pygame.image.load("circle.png")
Background = pygame.image.load("BlueBack.jpg")
My_Font = pygame.font.SysFont('Comic Sans MS', 50)
My_Font2 = pygame.font.SysFont('Arial', 30)

App = Tic()
class Rectangle:
    def __init__(self,screen,color,XY,Width_Height,RectPos):
        self.RectPos = RectPos
        self.Hitted = False
        self.color = color
        self.XY_Width_Height = XY + Width_Height
        self.Rect = pygame.draw.rect(screen,self.color,self.XY_Width_Height)
    def hit(self,Position):
        if self.Rect.collidepoint(Position) and not self.Hitted:
            self.Hitted = True
            return True,self.RectPos
        return False,"NO"
    def draw(self,screen):
        self.Rect = pygame.draw.rect(screen,self.color,self.XY_Width_Height)


Rectangle_List = [Rectangle(screen,(255,255,255),(0,0),(185,190),1),Rectangle(screen,(255,255,255),(193,0),(185,190),2),
                  Rectangle(screen,(255,255,255),(386,0),(185,190),3),Rectangle(screen,(255,255,255),(0,198),(185,190),4),
                  Rectangle(screen,(255,255,255),(193,198),(185,190),5),Rectangle(screen,(255,255,255),(386,198),(185,190),6),
                  Rectangle(screen,(255,255,255),(0,397),(185,190),7),Rectangle(screen,(255,255,255),(193,397),(185,190),8),
                  Rectangle(screen,(255,255,255),(386,397),(185,190),9)]

def draw_text(Text,Text_position,End=None):
    global screen,run,Rectangle_List
    if "you" in Text.lower():
        textsurface = My_Font.render(Text, False, (0, 255, 0))
    else:
        textsurface = My_Font.render(Text, False, (255, 0, 0))
    screen.blit(textsurface,Text_position)
    if End==True:   
        for R in Rectangle_List:
            R.Hitted = False
            App.__init__()
        run = False

def draw_game(screen,Rectangle_List):
    screen.fill((149, 165, 166 ))
    for R in Rectangle_List:
        R.draw(screen)

def draw_menu(screen):
    screen.blit(Background,(0,0))
    Possible = pygame.draw.rect(screen,(93, 173, 226),(Width/2-90,Height/2-60,175,35))
    Impossible = pygame.draw.rect(screen,(93, 173, 226),(Width/2-90,Height/2-100,175,35))
    screen.blit(My_Font2.render("Possible", False, (0, 255, 0)),(Width/2-87,Height/2-60))
    screen.blit(My_Font2.render("Impossible", False, (255, 0, 0)),(Width/2-87,Height/2-100))
    return Possible,Impossible

def Tic_setup(To_Put):
    App.HumanMove(To_Put)
    BotMove = App.NonHumanMove()
    if BotMove == -1:   print("Tie.");draw_text("Tie.",(Width/2-85,14),True);return None,""
    App.board[BotMove] = "O"
    App.printboard()

    if App.CheckForWin(App.board,"X"):
        print("You won.")
        draw_text("You won.",(Width/2-85,14),True)
        return
    if App.CheckForWin(App.board,"O"):
        print("Bot won.")
        draw_text("Bot won.",(Width/2-85,14),True)
        return BotMove,"Bot"

    return BotMove,"NO"
        
run = False
timer_start = False
timer = 0

while True:
    clock.tick(60)
    if timer_start:
        timer +=1
        if timer == 60*5:
            timer_start=False;timer=0
            continue
        for event in  pygame.event.get():   
            if event.type == 12:
               exit()
        continue
    if run == False:
        Possible,Impossible = draw_menu(screen)
    for event in  pygame.event.get():   
        if event.type == 12:
            exit()
        if event.type == 6:
            pos = pygame.mouse.get_pos()
            if run == False:
                if Possible.collidepoint(pos):
                    draw_game(screen,Rectangle_List)
                    App.Hard = False
                    run = True
                    continue
                elif Impossible.collidepoint(pos):
                    App.Hard = True
                    draw_game(screen,Rectangle_List)
                    run = True
                    continue
            if run == True:
                for R in  Rectangle_List:
                    H = R.hit(pos)
                    if H[0] == True:
                        Return_Value = Tic_setup(H[1])
                        screen.blit(Letter_x,(Rectangle_List[H[1]-1].XY_Width_Height[0]+25,Rectangle_List[H[1]-1].XY_Width_Height[1]+30))
                        if Return_Value[0] == None:    pygame.display.flip();timer_start=True;continue
                        Rectangle_List[Return_Value[0]].Hitted = True
                        screen.blit(Letter_o,(Rectangle_List[Return_Value[0]].XY_Width_Height[0]+25,Rectangle_List[Return_Value[0]].XY_Width_Height[1]+30))
                        if Return_Value[1] == "Bot":    pygame.display.flip();timer_start=True;continue
    pygame.display.flip()
