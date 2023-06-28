from time import time

# Helper class to time code execution speed


class Timer():
    def __init__(self):
        self.start_time = time()

    def reset(self):
        self.start_time = time()

    def elapsed(self):
        return time() - self.start_time
