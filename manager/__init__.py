import os
import db
import puzpy
import datetime
import json

class Manager(object):
    database = None
    base_path = None
    crossword_path = None

    def __init__(self, base_path, db_file):
        self.database = db.DB(db_file)
        self.base_path = base_path
        self.crossword_path = os.path.join(self.base_path, "crosswords")
        self.scan_puzzles()
        return

    def scan_puzzles(self):
        puzzles = self.database.select_puzzles()
        for obj in os.listdir(self.crossword_path):
            full_path = os.path.join(self.crossword_path, obj)
            js = None
            if os.path.isfile(full_path) and obj.endswith(".puz"):
                js = self.read_puz(full_path)
                title = obj.replace(".puz", "")
            if os.path.isfile(full_path) and obj.endswith(".xml"):
                js = self.read_xml(full_path)
                title = obj.replace(".xml", "")

            if js and title not in map(lambda p: p["Title"], puzzles):
                self.database.insert_puzzle(title, db.get_timestamp(datetime.datetime.utcnow()), json.dumps(js))

    def read_puz(self, path):
        return self.puz_to_json(puzpy.read(path))
    def read_xml(self, path):
        xml = None
        with open(path, 'r') as obj:
            xml = obj.read()
        return self.xml_to_json(xml)

    def xml_to_json(self, puzzle):
        return None
    def puz_to_json(self, puzzle):
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