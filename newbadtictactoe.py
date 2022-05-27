from itertools import cycle
from time import sleep
import pyglet
from pyglet import shapes
import requests
import threading

base = "http://127.0.0.1:5000/"
what_play = input("online(O) or local(L): ")
# what_play = "O"

class plr:
    def setup(self):
        while True:
            self.r = requests.get(base+r'create/matches')
            print('\n'.join([str(x)
                  for x, _ in enumerate(self.r.json()['matches'])]))
            print(self.r.json()['matches'])
            self.create_or_play = input(
                "type number of match to play or create match(C): ")
            if self.create_or_play == "C":
                self.id_of_match = requests.get(base+r'create/create').json()['id']
                self.our_letter = "X"
                self.get_match_info()
                self.turn = True
                break
            else:
                try:
                    self.id_of_match = self.r.json()['matches'][int(self.create_or_play)]
                    self.our_letter = "O"
                    self.turn = False
                    self.get_match_info()
                    break
                except:
                    print("that is not an optipond fhsaufhos")
                    exit()

    def get_match_info(self):
        self.getting = requests.get(base+r'create/status.{}'.format(self.id_of_match))
        self.move_list = self.getting.json()['list']


if what_play == "L":
    the_list_that = ["X", "O"]
    smth = cycle(the_list_that)
    current_letter = next(smth)
    move_list = ["-", "-", "-",
                 "-", "-", "-",
                 "-", "-", "-"]
elif what_play == "O":
    player = plr()
    player.setup()
    current_letter = player.our_letter
    move_list = player.move_list
else:
    print("that is not an optiopns asjdnfijasdfijsadbfjkhasdbfkl")
    exit()

WIDTH, HEIGHT = 600, 600
window = pyglet.window.Window(WIDTH, HEIGHT, resizable=False)
pyglet.gl.glClearColor(1, 1, 1, 1)

line_batch = pyglet.graphics.Batch()
move_batch = pyglet.graphics.Batch()

# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)

line = shapes.Line(195, 0, 195, 600, color=(
    0, 0, 0), width=10, batch=line_batch)
line2 = shapes.Line(415, 0, 415, 600, color=(
    0, 0, 0), width=10, batch=line_batch)
line3 = shapes.Line(0, 195, 600, 195, color=(
    0, 0, 0), width=10, batch=line_batch)
line4 = shapes.Line(0, 415, 600, 415, color=(
    0, 0, 0), width=10, batch=line_batch)


def get_play():
    global move_list
    while True:
        sleep(1)
        r = requests.get(base+r'create/status.{}'.format(player.id_of_match))
        updated_list = r.json()['list']
        if 'win' in r.json()['letter']:
            print(r.json()['letter'])
        if updated_list != move_list:
            move_list = updated_list.copy()
            player.turn = True
            print("Nyeee")

if what_play == "O":
    T1 = threading.Thread(target=get_play)
    T1.start()


def PLACE_MOVE(x, y, letter,pos):
    # THIS FUNCTION WILL PLACE THE LETTER AT THE X AND Y on POSITION PORVIDED
    global current_letter
    global move_list
    if what_play == "L":
        current_letter = next(smth)
    if what_play == "O":
        r = requests.post(base+r"create/NOO",data={'id':player.id_of_match,'position':str(pos)})
        move_list = r.json()['list']

    pyglet.text.Label(letter,
                      font_name='Arial',
                      font_size=160,
                      color=(255, 0, 0, 255),
                      x=x, y=y, batch=move_batch)
    print("Went through",letter)

def checkifwin(_):
    # this  FUNCTION CHECKS IF THERER IS A WINNER THIS IS LOCAL ONLY
    for i in [0, 3, 6]:
        if move_list[i] == move_list[i+1] == move_list[i+2] != "-":
            print(f"{move_list[i]} win")
            
    for x in range(3):
        if move_list[x] == move_list[x+3] == move_list[x+6] != "-":
            print(f"{move_list[x]} win")
            
    if move_list[0] == move_list[4] == move_list[8] != "-":
        print(f"{move_list[4]} win")
        
    if move_list[2] == move_list[4] == move_list[6] != "-":
        print(f"{move_list[4]} win")
        


@window.event
def on_mouse_release(x, y, _, __):
    global current_letter

    if what_play != "L":
        if player.turn == False:
            print("not yo turn")
            return
        else:
            print('you played')
            player.turn = False
    # WILL CHECK FOR POSITION OF CURSOR AND WILL PLACE THE LETTER IN THE SQURE
    if 8 < x < 180 and 425 < y < 596 and move_list[0] == "-":
        move_list[0] = current_letter
        PLACE_MOVE(9, 430, current_letter,0)
    if 204 < x < 405 and 425 < y < 596 and move_list[1] == "-":
        PLACE_MOVE(216, 430, current_letter,1)
        move_list[1] = current_letter
    if 423 < x < 597 and 425 < y < 596 and move_list[2] == "-":
        PLACE_MOVE(436, 430, current_letter,2)
        move_list[2] = current_letter

    if 8 < x < 180 and 204 < y < 408 and move_list[3] == "-":
        PLACE_MOVE(9, 220, current_letter,3)
        move_list[3] = current_letter
    if 204 < x < 405 and 204 < y < 408 and move_list[4] == "-":
        PLACE_MOVE(216, 220, current_letter,4)
        move_list[4] = current_letter
    if 423 < x < 597 and 204 < y < 408 and move_list[5] == "-":
        PLACE_MOVE(436, 220, current_letter,5)
        move_list[5] = current_letter

    if 8 < x < 180 and 3 < y < 187 and move_list[6] == "-":
        PLACE_MOVE(9, 11, current_letter,6)
        move_list[6] = current_letter
    if 204 < x < 405 and 3 < y < 187 and move_list[7] == "-":
        PLACE_MOVE(216, 11, current_letter,7)
        move_list[7] = current_letter
    if 423 < x < 597 and 3 < y < 187 and move_list[8] == "-":
        PLACE_MOVE(436, 11, current_letter,8)
        move_list[8] = current_letter


@window.event
def on_draw():
    window.clear()
    move_batch.draw()
    line_batch.draw()


if what_play == "L":
    pyglet.clock.schedule_interval(checkifwin, 1/120.0)
pyglet.app.run()
