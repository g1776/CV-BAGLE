import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import matplotlib.pyplot as plt
from faker import Faker # https://faker.readthedocs.io/

from utils import ChartGenerator, RandLabelGenerator


class PieChartGenerator(ChartGenerator):

    fake = Faker()
    @staticmethod
    def randomPcnts(n):
        '''Return n random percents that add up to 1'''
        return np.around(np.random.dirichlet(np.ones(n),size=1)[0], decimals = 1)
    
    # Each of these instances provide the labels, as well as what functions to call to generate random values in each axis
    LABELS = [
        RandLabelGenerator(None, None, 
                            "Where I Spend My Day", 
                            y_func=lambda: PieChartGenerator.randomPcnts(5) * 100,
                            categories=["School", "Home", "Work", "Gym", "Mall"]
                            )
    ]


    def __init__(self):

        super().__init__(f"pie-chart")

    
    def generate(self, id):

        # globals
        labels = ChartGenerator.randChoice(PieChartGenerator.LABELS)

        # randomize parameters
        categories = labels.categories
        pcnts = labels.y_func()
        cmap = LinearSegmentedColormap.from_list("my_colormap", [ChartGenerator.randHex() for _ in range(len(labels.categories))])
        title_padding = ChartGenerator.randFloats(15, 40)[0]
        ChartGenerator.setRandTheme()
        ChartGenerator.setRandFontsizes()

        # build data
        data = pd.DataFrame({"pcnt": pcnts})
        data.index = categories

        # plot
        fig, ax = plt.subplots(1,1, figsize=ChartGenerator.FIGSIZE)
        ax.set_title(labels.title, pad=title_padding)

        data.plot.pie(
                    y="pcnt",
                    ax=ax,
                    colormap=cmap
                    )
        
        # ChartGenerator.setRandTickParams(ax, 'x')
        # ChartGenerator.setRandTickParams(ax, 'y', labelrotation=False, rotations=[45, 90])
        
        plt.show()
        # save to png
        # self.save(id)

if __name__ == "__main__":

    n = 1

    pcg = PieChartGenerator()
    for i in range(n):
        if i%50==0:
            print(i,'/',n)
        pcg.generate(i)
    