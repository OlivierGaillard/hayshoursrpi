#! /usr/bin/env python
from sys import argv


class HaysHours(object):
    """
    Returns endhour given an elapsed time. The default start
    hour is "07:30" or "7.5"
    """

    def __init__(self):
        self.start_hour = 7.5

    def getEnd(self, elapsed):
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
        return result


def main(start_hour):
    h = HaysHours()
    endHour = h.getEnd(start_hour)
    print(endHour)


if __name__ == "__main__":

    start = float(argv[1])
    main(start)
