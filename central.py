import select

class Poll:
    def __init__(self, file) -> None:
        self.poll = select.poll()
        self.file = file
        self.buffer = []

    def __enter__(self):
        self.poll.register(self.file, select.POLLIN | select.POLLPRI)
        return self

    def __exit__(self, type, value, traceback):
        self.poll.unregister(self.file)

    def __iter__(self):
        return self

    def __next__(self):
        while not self.buffer:
            self.buffer.extend(self.poll.poll())
        ev = self.buffer.pop(0)[1]
        if ev & select.POLLIN or ev & select.POLLPRI:
            return self.file.readline().strip()
        else:
            raise StopIteration() 


if __name__ == "__main__":
    with open("train_report") as f, Poll(f) as poll, open("slow.log", "w") as slow, open("normal.log", "w") as normal, open("fast.log", "w") as fast:
        for i in poll:
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
