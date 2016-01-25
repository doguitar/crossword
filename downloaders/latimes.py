import urllib2
import datetime

class LATimesDownloader(object):

    @staticmethod
    def download(puzzle_date=None):
        if not puzzle_date: puzzle_date = datetime.datetime.utcnow()
        url = "http://cdn.games.arkadiumhosted.com/latimes/assets/DailyCrossword/"
        puzzle_name = "la{0:02d}{1:02d}{2:02d}.xml".format(puzzle_date.year-2000, puzzle_date.month, puzzle_date.day)
        headers = {
            "Accept":"*/*",
            "Accept-Charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.3",
            "Accept-Language":"en-US,en;q=0.8",
            "Connection":"keep-alive",
            "Host":"cdn.games.arkadiumhosted.com",
            "Referer":"http://cdn.games.arkadiumhosted.com/latimes/games/daily-crossword/game/crossword-expert.swf",
            "Content-Length":"0",
        }
        req = urllib2.Request(url+puzzle_name, headers=headers)
        try:
            res = urllib2.urlopen(req)
            data =  res.read()
            return data
        except Exception as e:
            raise e
        return None