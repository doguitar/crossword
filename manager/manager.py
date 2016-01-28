import os
import puzpy
import datetime
import json
import xml.etree.ElementTree as xml_tree
import threading
import time
import db
import downloaders

class Manager(object):
    database = None
    base_path = None
    crossword_path = None
    stopping = False

    download_thread = None

    def __init__(self, base_path, db_file):
        self.database = db.DB(db_file)
        self.base_path = base_path
        self.crossword_path = os.path.join(self.base_path, "crosswords")
        self.download_thread = threading.Thread(target=self.download_loop)
        self.download_thread.start()
        return

    def __del__(self):
        self.stopping = True
        self.database.__del__()

    def download_loop(self):
        delay = 60*60
        i = delay
        while True:
            while delay > i:
                if self.stopping:
                    return
                time.sleep(1)
                i += 1
            i = 0
            self.download_puzzles()

    def download_puzzles(self):
        dl = [
            (downloaders.LATimesDownloader, "{0}-{1}-{2}.LA Times", 'xml', self.read_xml)
        ]
        titles = map(lambda p: p["Title"], self.database.select_puzzles())

        now = datetime.datetime.today()
        for i in range(0, 30):
            current = now - datetime.timedelta(days=i)
            for downloader, mask, extension, reader in dl:
                title = mask.format(current.year, current.month, current.day)
                if title not in titles:
                    filename = os.path.join(self.base_path, "crosswords", title + "." + extension)
                    try:
                        if not os.path.exists(filename):
                            data = downloader.download(now)
                            time.sleep(1)
                            with open(filename, 'w') as puzzle:
                                puzzle.write(data)
                        js = reader(filename)
                        self.database.insert_puzzle(title, db.get_timestamp(current), json.dumps(js))
                    except Exception as e:
                        print "Failed to process " + filename
                        print e

        return

    def scan_puzzles(self):
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
            xml = xml.replace( "xmlns=", "blank=")
        return self.xml_to_json(xml_tree.fromstring(xml))

    def xml_to_json(self, puzzle):
        js = dict()

        crossword = puzzle.find(".//crossword")
        js["title"] = puzzle.find(".//title").text
        grid = crossword.find("./grid")
        js["height"] = int(grid.attrib["height"])
        js["width"] = int(grid.attrib["width"])

        js["rows"] = [[]]
        js["clues"] = [{},{}]

        for y in range(1, js["height"]+1):
            row = []
            for x in range(1, js["width"]+1):
                cell = grid.find("./cell[@x='{0}'][@y='{1}']".format(x,y))
                cell = {
                    "clue" : int(cell.attrib["number"]) if "number" in cell.attrib.keys() else None,
                    "black" : cell.attrib["type"] == "block" if "type" in cell.attrib.keys() else None
                }
                row.append(cell)
            js["rows"].append(row)

        words = crossword.findall("./word")
        for word in words:
            clue = crossword.find(".//clue[@word='{0}']".format(word.attrib["id"]))
            number = clue.attrib["number"]
            clue_index = 0 if "-" in word.attrib["x"] else 1

            js["clues"][clue_index][number] = clue.text

        return js

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