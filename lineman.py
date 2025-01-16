import config
from reader import Reader
import time


def main() -> None:
    barrier_state = False  # open
    last_change = time.time()
    with open(config.lineman_central_pipe_name, "w") as lc:
        reader = Reader(config.central_lineman_pipe_name)
        for i in reader:
            match i.strip():
                case "barrier?":
                    print(barrier_state, file=lc, flush=True)
                case "close":
                    barrier_state = True
                    last_change = time.time()
                case "open":
                    barrier_state = False
                    last_change = time.time()
                case "changed?":
                    print(last_change, file=lc, flush=True)
                case _:
                    print(f"unhandled message: {i}")
                    exit(1)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        exit(0)
