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

    MARKERS = [".", "o", "v","^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "+", ""]

    fake = Faker()
    
    # Each of these instances provide the labels, as well as what functions to call to generate random values in each axis
    LABELS = [
        RandLabelGenerator("Temp (F)", 
                            "# Birds in Sky", 
                            "Temperature vs # birds in the sky", 
                            x_func=lambda: list(range(30, 90, 2)), 
                            y_func=lambda: LineGenerator.randFloats(30, 90)[0],
                            categories=["Geese", "Hummingbird", "Eagle"],
                            unique_x=True
                            ),
        # RandLabelGenerator("Year",
        #                 "Unemployment Rate(%)",
        #                 "Unemployment Rate vs Year",
        #                 x_func = lambda n_points: list(range(2000,2020, 5)),
        #                 y_func = lambda: LineGenerator.randFloats(1,20)[0],
        #                 unique_x=True
        #                 ),
        # RandLabelGenerator("Year",
        #                 "Sales in Thousands",
        #                 "Sale Numbers from 1960 Onward",
        #                 x_func = lambda n_points: list(range(1960,1960+(n_points*2), 2)),
        #                 y_func = lambda: ChartGenerator.randFloats(10,100)[0],
        #                 unique_x = True
        #                 )
    ]


    def __init__(self):

        super().__init__("line-chart")

    
    def generate(self, id):

        # globals
        labels = ChartGenerator.randChoice(LineGenerator.LABELS)
        

        # randomize parameters
        n_points_per_cat = ChartGenerator.randInts(5, 30)[0]
        
        
        xs = []
        ys = []
        if labels.categories is not None:
            for cat in labels.categories:
                cat_xs = [labels.x_func() for _ in range(n_points_per_cat)] if not labels.unique_x else labels.x_func()
                cat_ys = [labels.y_func() for _ in range(len(cat_xs))]
                xs.extend(cat_xs)
                ys.extend(cat_ys)


        show_markers = True # ChartGenerator.randBool()
        color = ChartGenerator.randHex()
        title_padding = ChartGenerator.randFloats(15, 40)[0]
        ChartGenerator.setRandTheme()
        ChartGenerator.setRandFontsizes()

        # build data
        data = pd.DataFrame({
            labels.x: xs, 
            labels.y: ys, 
            "category": labels.categories*int(len(xs)/len(labels.categories))
            })
        

        # plot
        fig, ax = plt.subplots(1,1, figsize=ChartGenerator.FIGSIZE)
        ax.set_title(labels.title, pad=title_padding)
        try:
            sns.lineplot(data=data,
                        x=labels.x,
                        y=labels.y,
                        hue="category",
                        color=color,
                        ci=None,
                        marker=ChartGenerator.randChoice(LineGenerator.MARKERS),
                        ax=ax
                        )

            ChartGenerator.setRandTickParams(ax, 'x')
            ChartGenerator.setRandTickParams(ax, 'y')

            # output to png
            self.save(id, labels, data)
        except ValueError:
            print(f"Passing {self.type}-{id}. Ran into seaborn error.") # cannot figure out where certain value error is being thrown, so ignoring :/


if __name__ == "__main__":

    n = 6000

    lg = LineGenerator()
    for i in range(n):
        if i%50==0:
            print(i,'/',n)
        lg.generate(i)
    