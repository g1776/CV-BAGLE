from audioop import mul
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import math
import os
from faker import Faker # https://faker.readthedocs.io/

from utils import ChartGenerator, RandLabelGenerator

class HistogramGenerator(ChartGenerator):
    
    LABELS = [
        RandLabelGenerator("Miles",
                            "",
                            "Miles Ran During Ultra-marathon",
                            x_func=lambda: ChartGenerator.randInts(0, 100)[0]),
        RandLabelGenerator("Age",
                           "",
                           "Age of Employees at Apple",
                           x_func=lambda: ChartGenerator.randInts(14, 60)[0]),
        RandLabelGenerator("Length (in ft)",
                           "",
                           "Length of Adult Elephant Trunks in West Africa",
                           x_func=lambda: ChartGenerator.randFloats(5, 7)[0]),
        RandLabelGenerator("Score",
                           "",
                           "MCAT Scores in 2021 From January to June",
                           x_func=lambda: ChartGenerator.randInts(472, 530)[0]),
        RandLabelGenerator("Time (in seconds)",
                           "",
                           "Various AutoML Cross-Validation Time for Classification",
                           x_func= lambda: ChartGenerator.randFloats(30, 70)[0])
        ]
    
    STATS = ["count", "frequency", "proportion", "percent", "density"]
    
    def __init__(self, kernel_density):
        if kernel_density:
            super().__init__(f"fit-density-histogram-plot")
        else:
            super().__init__(f"unfit-density-histogram-plot")
            
        self.kernel_density = kernel_density
        
    def generate(self, id):
        
        # globals
        labels = ChartGenerator.randChoice(HistogramGenerator.LABELS)
        
        # randomize parameters
        data_amount = ChartGenerator.randInts(2000, 4000)[0]
        xs = [labels.x_func() for _ in range(data_amount)] if not labels.unique_x else labels.x_func()
        stat = ChartGenerator.randChoice(HistogramGenerator.STATS)
        multiple_colors = ChartGenerator.randBool()
        bar_color = ChartGenerator.randHex() if not multiple_colors else None
        title_padding = ChartGenerator.randFloats(15, 40)[0]
        fill = ChartGenerator.randBool()
        ChartGenerator.setRandTheme()
        ChartGenerator.setRandFontsizes()
        
        #build data
        data = pd.DataFrame({labels.x: xs})
        print(data)
        
        # plot
        fig, ax = plt.subplots(1,1, figsize=ChartGenerator.FIGSIZE)
        ax.set_title(labels.title, pad=title_padding)
        
        sns.histplot(data = data,
                    x = labels.x,
                    ax = ax,
                    kde = self.kernel_density,
                    color = bar_color,
                    stat = stat,
                    bins = ChartGenerator.randInts(30, 40)[0],
                    fill = fill)
        ChartGenerator.setRandTickParams(ax, 'x')
        ChartGenerator.setRandTickParams(ax, 'y')

        ax.set_ylabel(stat)
        
        #plt.show()
        self.save(id, labels, data)

if __name__ == "__main__":

    n = 10

    for kernel_density in [True, False]:
        hg = HistogramGenerator(kernel_density)
        for i in range(0, n):
            print(i,'/',n)
            hg.generate(i)

                    
                        