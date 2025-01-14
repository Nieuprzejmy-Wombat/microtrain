import select
import config
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


def main():
    reader = Reader(config.train_central_pipe_name)
    with (
        open("slow.log", "w") as slow,
        open("normal.log", "w") as normal,
        open("fast.log", "w") as fast,
    ):
        for i in reader:
            msg_type, msg_value = i.split(":")
            match msg_type.strip():
                case "speed":
                    msg_value = float(msg_value)
                    if msg_value < 40:
                        print(msg_value, file=slow, flush=True)
                    elif msg_value < 140:
                        print(msg_value, file=normal, flush=True)
                    else:
                        print(msg_value, file=fast, flush=True)
                case "station":
                    pass
                case _:
                    print(f"unknown message type: {msg_type}")
                    exit(1)


if __name__ == "__main__":
    main()
