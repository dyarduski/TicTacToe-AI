import pygame
from App import Tic

pygame.font.init() 
Width,Height = 570,587
screen = pygame.display.set_mode((Width,Height))
clock = pygame.time.Clock()

Letter_x = pygame.image.load("letter-x.png")
Letter_o = pygame.image.load("circle.png")
My_Font = pygame.font.SysFont('Comic Sans MS', 50)

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
def draw_text(Text):
    global screen,run
    if "you" in Text.lower():
        textsurface = My_Font.render(Text, False, (0, 255, 0))
    else:
        textsurface = My_Font.render(Text, False, (255, 0, 0))
    screen.blit(textsurface,(Width/2-85,14))
    run = False

def Tic_setup(To_Put):
    App.HumanMove(To_Put)
    BotMove = App.NonHumanMove()
    if BotMove == -1:   print("Tie.");draw_text("Tie.");return
    App.board[BotMove] = "O"
    App.printboard()
    if App.CheckForWin(App.board,"X"):
        print("You won.")
        draw_text("You won.")
        return
    if App.CheckForWin(App.board,"O"):
        print("Bot won.")
        draw_text("Bot won.")


    return BotMove

screen.fill((149, 165, 166 ))
for R in Rectangle_List:
    R.draw(screen)
run = True
while True:
    for event in  pygame.event.get():   
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONUP and run == True:
            pos = pygame.mouse.get_pos()
            for R in  Rectangle_List:
                H = R.hit(pos)
                if H[0] == True:
                    Return_Value = Tic_setup(H[1])
                    screen.blit(Letter_x,(Rectangle_List[H[1]-1].XY_Width_Height[0]+25,Rectangle_List[H[1]-1].XY_Width_Height[1]+30))
                    if Return_Value == None:    continue
                    screen.blit(Letter_o,(Rectangle_List[Return_Value].XY_Width_Height[0]+25,Rectangle_List[Return_Value].XY_Width_Height[1]+30))
    pygame.display.flip()
