import config
import logging
import time
from reader import Reader


def main():
    reader = Reader(config.train_central_pipe_name)
    lineman = Reader(config.lineman_central_pipe_name)
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename="central.log", level=logging.INFO)
    with (
        open("slow.log", "w") as slow,
        open("normal.log", "w") as normal,
        open("fast.log", "w") as fast,
        open(config.central_lineman_pipe_name, "w") as cl,
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
                    logger.info(
                        f"approaching station {msg_value.strip()} at {time.time()}"
                    )
                    print("barrier?", file=cl, flush=True)
                    barrier_state = next(lineman).strip()
                    if barrier_state == True:
                        logger.warning("barrier already closed")
                    else:
                        print("close", file=cl, flush=True)
                        logger.info("sended barrier close request")
                    time.sleep(4)
                    print("open", file=cl, flush=True)
                    logger.info("sended barrier open request")

                case _:
                    print(f"unknown message type: {msg_type}")
                    exit(1)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        exit(0)
