import select
from collections import deque


class Reader:
    def __init__(self, file: str) -> None:
        self.poll = select.poll()
        self.file = open(file, "r", encoding="utf-8")
        self.poll.register(self.file, select.POLLIN | select.POLLPRI)
        self.buffer = deque()

    def __del__(self):
        self.poll.unregister(self.file)
        self.file.close()

    def __iter__(self):
        return self

    def __next__(self):
        while not self.buffer:
            self.buffer.extend(self.poll.poll())
        ev = self.buffer.popleft()[1]
        if ev & select.POLLIN or ev & select.POLLPRI:
            return self.file.readline().strip()
        elif ev & select.POLLHUP:
            raise StopIteration()
        else:
            raise IOError(f"unhandled event: {ev}")
