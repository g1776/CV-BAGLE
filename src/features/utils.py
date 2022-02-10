import numpy as np
import random
import os
from pathlib import Path
import matplotlib.pyplot as plt

class ChartGenerator:

    CHARTS_DIR = os.path.join(Path(os.path.abspath(__file__)).parent.parent.parent, "volume", "raw")
    px = 1/plt.rcParams['figure.dpi']  # pixel in inches
    FIGSIZE = (1028*px, 1028*px)

    # random generator functions
    randInts = lambda low, high, size=1: np.random.randint(low, high, size=size)
    randFloats = lambda low, high, size=1: np.random.uniform(low=low, high=high, size=size)
    randBool = lambda: bool(random.getrandbits(1))
    randHex = lambda: '#%02X%02X%02X' % (
        ChartGenerator.randInts(0,255)[0],
        ChartGenerator.randInts(0,255)[0],
        ChartGenerator.randInts(0,255)[0]
        )
    randTheme = lambda: random.choice(["darkgrid" , "whitegrid" , "dark" , "white" , "ticks"])
    randChoice = lambda arr: random.choice(arr)

    def __init__(self, chart_type: str):
        self.type = chart_type

    def generate(self, id):
        pass

    



