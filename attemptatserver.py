from flask import Flask, request
from flask_restful import Api, Resource
import random
from string import ascii_lowercase, ascii_uppercase, digits
from itertools import cycle
from time import time

app = Flask(__name__)
api = Api(app)
matches_list = []


class create_match(Resource):
    def get(self, info_for_what_to_do):
        if info_for_what_to_do == 'create':
            m = match_itself()
            matches_list.append(m)
            return {'id':m.id}
        if "status" in info_for_what_to_do:
            id_of_match = info_for_what_to_do.split('.')[1]
            for match in matches_list:
                if id_of_match == match.id:
                    if time() - match.time_created > 120:
                        matches_list.remove(match)
                        return "match ended no move made of no player joined"
                    return {'list':match.move_list,'letter':match.current_letter}
        if "matches" in info_for_what_to_do:
            return {'matches': [i.id for i in matches_list]}

    def post(self,info_for_what_to_do):
        for match in matches_list:
            if request.form['id'] == match.id:
                match.move_list[int(request.form['position'])] = match.current_letter
                match.current_letter = next(match.smth)
                match.checkifwin()
                return {'list':match.move_list,'letter':match.current_letter}
               

class match_itself:
    def __init__(self) -> None:
        self.move_list = ["-", "-", "-",
                          "-", "-", "-",
                          "-", "-", "-"]
        self.id = ''.join(
            [random.choice(ascii_lowercase+ascii_uppercase) for _ in range(30)])
        self.the_list_that = ["X", "O"]
        self.smth = cycle(self.the_list_that)
        self.current_letter = next(self.smth)
        self.time_created = time()

    def checkifwin(self):
        # this  FUNCTION CHECKS IF THERER IS A WINNER THIS IS
        for i in [0, 3, 6]:
            if self.move_list[i] == self.move_list[i+1] == self.move_list[i+2] != "-":
                self.current_letter = f"{self.move_list[i]} win"
        for i in range(3):
            if self.move_list[i] == self.move_list[i+3] == self.move_list[i+6] != "-":
                self.current_letter = f"{self.move_list[i]} win"
        if self.move_list[0] == self.move_list[4] == self.move_list[8] != "-":
            self.current_letter = f"{self.move_list[0]} win"
        if self.move_list[2] == self.move_list[4] == self.move_list[6] != "-":
            self.current_letter = f"{self.move_list[2]} win"


api.add_resource(create_match, '/create/<string:info_for_what_to_do>')

if __name__ == "__main__":
    app.run(debug=True)
