import numpy as np
import random
import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import matplotlib
import seaborn as sns
import io
import pickle

class GeneratedChart:

    def __init__(self, img, labels: dict, data):
        self.img = img
        self.labels = labels
        self.data = data


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
    @staticmethod
    def setRandTickParams (ax, xOrY, labelrotation = True, reverse_rotation = False, rotations=[]): 

        rotation = 0
        if labelrotation:
            rotations = [0, 45, 90] if rotations == [] else rotations
            rotation = ChartGenerator.randChoice(rotations)
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

    @staticmethod
    def setRandFontsizes():
        tick_fontsize = ChartGenerator.randFloats(10, 15)[0]
        params = {'legend.fontsize': ChartGenerator.randFloats(10, 16)[0],
            'axes.labelsize': ChartGenerator.randFloats(13, 18)[0],
            'axes.titlesize':ChartGenerator.randFloats(20, 35)[0],
            'xtick.labelsize': tick_fontsize,
            'ytick.labelsize': tick_fontsize,
            }
        pylab.rcParams.update(params)


    def __init__(self, chart_type: str):
        self.type = chart_type

        matplotlib.use('Agg') # must change backend so the memory doesn't get used up

    def generate(self, id, ax):
        '''Please pass an id and a Matplotlib axis in your implementation of this method. At the end call self.save(id)'''

        pass

    def save(self, id, labels, data):
        '''Save figure and metadata to pickle and close.'''

        # scale just in case
        plt.tight_layout()


        directory = os.path.join(ChartGenerator.CHARTS_DIR, self.type)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        fp = os.path.join(directory, f"{self.type}-{id}.pkl")
        
        # save to buffer and pickle
        buf = io.BytesIO()
        plt.savefig(buf)
        buf.seek(0)

        gc = GeneratedChart(buf, labels.to_dict(), data)
        with open(fp, 'wb') as f:
            pickle.dump(gc, f)

        # cleanup
        plt.close('all')


class RandLabelGenerator:

    MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    LETTER_GRADES = ["A", "B", "C", "D", "E", "F"]

    def __init__(self, x_label, y_label, title, x_func=lambda: None, y_func=lambda: None, unique_x=False, unique_y=False, categories=None):
        '''
        Specify labels, title, as well as the functions that should be used to generate the random labels and values on each axis. A dimension, called "categories", is also provided if needed.
        
        x_func (function): Function to call when generating random x labels.
        y_func (function): Function to call when generating random y labels.
        unique_x (bool): Does x_func return a unique set of values (aka not random)? Default False.
        unique_y (bool): Does y_func return a unique set of values (aka not random)? Default False.
        categories (list): List of categories to plot. Default None.
        
        '''

        self.x = x_label
        self.y = y_label
        self.title = title
        self.x_func = x_func
        self.y_func = y_func
        self.unique_x = unique_x
        self.unique_y = unique_y
        self.categories = categories

    def to_dict(self):
        return {
            "title": self.title,
            "x": self.x,
            "y": self.y,
            "categories": self.categories
        }
    
    def __str__(self):
        return f"RandLabelGenerator: \"{self.title}\"\nx: {self.x}\ny: {self.y}"