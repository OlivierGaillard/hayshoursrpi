#! /usr/bin/env python
from sys import argv, exit


class HaysHours(object):
    """
    Returns endhour given an elapsed time. The default start
    hour is "07:30" or "7.5"
    """

    def __init__(self):
        self.start_hour = 7.5

    def set_db(self, db):
        self.db = db

    def getEnd(self, elapsed):
        if len(elapsed) == 0:
            return ""
        elapsed = float(elapsed)
        end_hour_dec = self.start_hour + elapsed
        correction = 0
        if elapsed <= 7.0:
            correction = 0.25
        elif elapsed <= 8.5:
            correction = 0.5
        else:
            correction = 1
        end_hour_dec += correction
        hours = int(end_hour_dec)
        minutes = (end_hour_dec * 60) % 60
        seconds = round((end_hour_dec * 3600)) % 60
        hh = '{:02.0f}'.format(hours)
        mn = '{:02.0f}'.format(minutes)
        sc = '{:02.0f}'.format(seconds)
        result = '{}:{}:{}'.format(hh, mn, sc)
        self.saveResult(result)
        return result

    def saveResult(self, result):
        self.db.save(result)

    def getLastSaved(self):
        return self.db.readLast()


def main(start_hour):
    h = HaysHours()
    endHour = h.getEnd(start_hour)
    print(endHour)


if __name__ == "__main__":
    if len(argv) == 1:
        print('missing argument start-hour')
        exit(-1)
    start_hour = argv[1]
    if len(start_hour) == 0:
        print('start-hour is empty string')
        exit(-1)
    main(start_hour)
