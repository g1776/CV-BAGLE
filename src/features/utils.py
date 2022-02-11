import numpy as np
import random
import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import seaborn as sns

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
    setRandTheme = lambda: sns.set_style(random.choice(["darkgrid" , "whitegrid" , "dark" , "white" , "ticks"]))
    randChoice = lambda arr: random.choice(arr)


    # common chart randomization methods
    def setRandTickParams (ax, xOrY, labelrotation = True, reverse_rotation = False): 

        rotation = 0
        if labelrotation:
            rotation = ChartGenerator.randChoice([0, 45, 90])
            if reverse_rotation:
                rotation *= -1


        ax.tick_params(
        axis = xOrY,
        which = ChartGenerator.randChoice(['major', 'minor', 'both']),
        direction = ChartGenerator.randChoice(['in', 'out', 'inout']),
        pad = ChartGenerator.randFloats(3, 5)[0],
        bottom = ChartGenerator.randBool(),
        left = ChartGenerator.randBool(),
        labelrotation = rotation,
        grid_color = ChartGenerator.randChoice(["grey", "lightgrey", "black"]),
        grid_alpha = ChartGenerator.randFloats(0.3, 1)[0]
        )

    def setRandFontsizes():
        tick_fontsize = ChartGenerator.randFloats(10, 15)[0]
        params = {'legend.fontsize': ChartGenerator.randFloats(5, 12)[0],
            'axes.labelsize': ChartGenerator.randFloats(13, 18)[0],
            'axes.titlesize':ChartGenerator.randFloats(20, 30)[0],
            'xtick.labelsize': tick_fontsize,
            'ytick.labelsize': tick_fontsize}
        pylab.rcParams.update(params)


    def __init__(self, chart_type: str):
        self.type = chart_type

    def generate(self, id):
        pass

class RandLabelGenerator:
    def __init__(self, x_label, y_label, title, x_func=lambda: None, y_func=lambda: None):
        '''
        Specify labels, title, as well as the functions that should be used to generate the random labels
        
        x_func (function): Function to call when generating random x labels.
        y_func (function): Function to call when generating random y labels.
        
        '''


        self.x = x_label
        self.y = y_label
        self.title = title
        self.x_func = x_func
        self.y_func = y_func

    



