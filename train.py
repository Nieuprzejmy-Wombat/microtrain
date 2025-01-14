from random import randint, random
from time import sleep
import config

stations = ["Adamowo", "Adamowo (leśniczówka)", "Adampol", "Ahlbeck Grenze", "Aleksandrów", "Aleksandrów Kujawski", "Aleksandrów Kujawski Wąskotorowy","Aleksandrów Łódzki","Alfred","Alwernia" ,"Anastazewo" ,"Andaluzja","Andoria","Andrychów","Andrychów Górnica","Andrzejówka","Anielin Gradowo"] 
stations_len = len(stations)

with open(config.train_central_pipe_name, "w") as f:
    while True:
        for i in range(18):
            print(f"speed: {random() * 180}", file=f, flush=True)
            sleep(1)
        print(f"station: {stations[randint(0, stations_len - 1)]}", file=f, flush=True)
