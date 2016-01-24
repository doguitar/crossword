import os
import db
import puzpy
import json
import uuid

class Manager(object):
    database = None
    base_path = None

    def __init__(self, base_path, db_file):
        self.database = db.DB(db_file)
        self.base_path = base_path
        return

    def read_puzzle(self, path):
        return self.puzzle_to_json(puzpy.read(path))

    def puzzle_to_json(self, puzzle):
        js = dict()

        js["title"] = puzzle.title
        js["height"] = puzzle.height
        js["width"] = puzzle.width

        js["rows"] = [[]]
        js["clues"] = [{},{}]

        x, y, c, i = 0, 0, 1, 0
        for char in list(puzzle.fill):
            if x >= puzzle.width:
                x = 0
                y += 1
                js["rows"].append([])
            black = char == '.'
            horz_clue = not black and (x == 0 or js["rows"][y][x-1]["black"])
            vert_clue = not black and (y == 0 or js["rows"][y-1][x]["black"])

            clue = c if horz_clue or vert_clue else None
            if clue is not None: c += 1

            js["rows"][y].append({
                "black" : black,
                "clue" : clue
            })
            if horz_clue:
                js["clues"][0][clue] = puzzle.clues[i]
                i += 1
            if vert_clue:
                js["clues"][1][clue] = puzzle.clues[i]
                i += 1
            x += 1
        return js