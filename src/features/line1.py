from multiprocessing.sharedctypes import Value
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
from faker import Faker # https://faker.readthedocs.io/

from utils import ChartGenerator, RandLabelGenerator


class LineGenerator(ChartGenerator):

    fake = Faker()
    
    # Each of these instances provide the labels, as well as what functions to call to generate random values in each axis
    LABELS = [
        RandLabelGenerator("Temp (F)", 
                            "# Birds in Sky", 
                            "Temperature vs # birds in the sky", 
                            x_func=lambda: LineGenerator.randFloats(30, 90)[0], 
                            y_func=lambda: np.random.normal(size=(1, 1))[0][0]
                            )#,
        
        #RandLabelGenerator("Year",
        #                   "Unemployment Rate(%)",
        #                   "Unemployment Rate vs Year",
        #                   x_func = lambda: list(range(2000,2020, 5)),
        #                   y_func = lambda: LineGenerator.randFloats(1,20)[0],
        #                    ),

        #RandLabelGenerator("Month",
        #                   "Sales in Thousands",
        #                   "Sale Numbers in 2021",
        #                   x_func = lambda: RandLabelGenerator.MONTHS,
        #                   y_func = lambda: ChartGenerator.randFloats(10,100)[0],
        #                   )
    ]


    def __init__(self):

        super().__init__("line-chart")

    
    def generate(self, id):

        # globals
        labels = ChartGenerator.randChoice(LineGenerator.LABELS)

        # randomize parameters
        n_points = ChartGenerator.randInts(5, 30)[0]
        ys = [labels.y_func() for _ in range(n_points)]
        xs = [labels.x_func() for _ in range(n_points)]

        show_markers = ChartGenerator.randBool()
        color = ChartGenerator.randHex()
        title_padding = ChartGenerator.randFloats(15, 40)[0]
        ChartGenerator.setRandTheme()
        ChartGenerator.setRandFontsizes()

        # build data
        data = pd.DataFrame({labels.x: xs, labels.y: ys})

        # plot
        fig, ax = plt.subplots(1,1, figsize=ChartGenerator.FIGSIZE)
        ax.set_title(labels.title, pad=title_padding)
        try:
            sns.lineplot(data=data,
                        x=labels.x,
                        y=labels.y,
                        color=color,
                        ax=ax
                        )
            if show_markers:
                sns.scatterplot(data=data,
                        x=labels.x,
                        y=labels.y,
                        color=color,
                        ax=ax)

            ChartGenerator.setRandTickParams(ax, 'x')
            ChartGenerator.setRandTickParams(ax, 'y')

            plt.show()
            # output to png
            # self.save(id, labels, data)
        except ValueError:
            print(f"Passing {self.type}-{id}. Ran into seaborn error.") # cannot figure out where certain value error is being thrown, so ignoring :/


if __name__ == "__main__":

    n = 1

    lg = LineGenerator()
    for i in range(n):
        if i%50==0:
            print(i,'/',n)
        lg.generate(i)