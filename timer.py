from time import time


class Timer():
    def __init__(self):
        self.start_time = time()

    def reset(self):
        self.start_time = time()

    def elapsed(self):
        return time() - self.start_time
