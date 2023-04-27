from datetime import timedelta
from time import time


class Timer(object):

    def __init__(self, start=False):
        if start:
            self.start = time()
        else:
            self.start = None
        self.end = None

    def begin(self):
        self.start = time()
        # someone could call begin after finishing the counter
        self.end = None

    def finish(self):
        self.end = time()
        if not self.start or (self.end < self.start):
            raise ValueError("start value is empty or greater than the end value: s:{} - e:{}"
                             .format(self.start, self.end))
        return self.end - self.start


    def __finishing_if_not(self):
        if not (self.end and (self.end >= self.start)):
            self.end = time()

        return self.end - self.start

    def sec(self):
        return self.__finishing_if_not()

    def ms(self):
        return self.__finishing_if_not() * 1000

    def us(self):
        return self.ms() * 1000

    def curr_sec(self):
        return time() - self.start

    def human(self):
        return str(timedelta(seconds=self.__finishing_if_not()))