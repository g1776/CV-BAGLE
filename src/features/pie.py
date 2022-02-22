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
        return np.around(np.random.dirichlet(np.ones(n),size=1)[0], decimals = 2)
    
    # Each of these instances provide the labels, as well as what functions to call to generate random values in each axis
    LABELS = [
        RandLabelGenerator(None, None, 
                            "Where I Spend My Day", 
                            y_func=lambda: PieChartGenerator.randomPcnts(5) * 100,
                            categories=["School", "Home", "Work", "Gym", "Mall"]
                            ),
        RandLabelGenerator(None, None, 
                            "What is your favorite fruit?", 
                            y_func=lambda: PieChartGenerator.randomPcnts(3) * 100,
                            categories=["Apple", "Pear", "Banana"]
                            ),
        RandLabelGenerator(None, None, 
                            "Breakdown of Dogs in a Dog Park", 
                            y_func=lambda: PieChartGenerator.randomPcnts(4) * 100,
                            categories=["Golden Retriever", "Poodle", "Schnauzer", "Corgi"]
                            ),
        RandLabelGenerator(None, None, 
                            r"% of categories listened to on Spotify", 
                            y_func=lambda: PieChartGenerator.randomPcnts(7) * 100,
                            categories=["Country", "Screamo", "Jazz", "LoFi", "Pop", "Hip-Hop", "Disney Soundtracks"]
                            ),
        RandLabelGenerator(None, None, 
                            "Population of Insects in the American Backyard", 
                            y_func=lambda: PieChartGenerator.randomPcnts(5) * 100,
                            categories=["Ants", "Caterpillars", "Rollie-pollies", "Butterflies", "Other"]
                            ),
        RandLabelGenerator(None, None, 
                            "Flower Shop Revenues", 
                            y_func=lambda: PieChartGenerator.randomPcnts(5) * 100,
                            categories=["Roses", "Daisies", "Black-Eyed Susans", "Chrysthanemoums", "Dandelions"]
                            ),
        RandLabelGenerator(None, None, 
                            "Equipment Found on Playgrounds", 
                            y_func=lambda: PieChartGenerator.randomPcnts(6) * 100,
                            categories=["Slide", "Merry-Go-Round", "Swing Set", "Balance Beam", "See-Saw", "Monkey Bars"]
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
        title_padding = ChartGenerator.randFloats(15, 40)[0]
        show_shadow = ChartGenerator.randBool()
        show_legend = ChartGenerator.randBool()
        start_angle = ChartGenerator.randChoice([0, 90, 180, 270])
        labels_in_slices = ChartGenerator.randBool()
        autopct = None if not labels_in_slices else '%1.1f%%'
        radius = ChartGenerator.randFloats(0.5, 1.3)[0]
        should_explode = ChartGenerator.randBool()
        explode = [0]*len(categories)
        if should_explode:

            pcnt_to_explode = 100
            # we don't want to explode a slice that is >50%. It looks weird
            while pcnt_to_explode >= 50:
                idx_to_explode = ChartGenerator.randChoice(list(range(len(categories))))
                pcnt_to_explode = pcnts[idx_to_explode]

            amount_to_explode = ChartGenerator.randFloats(.1, .2)[0]
            explode[idx_to_explode] = amount_to_explode

        
        ChartGenerator.setRandTheme()
        ChartGenerator.setRandFontsizes()

    
        # plot
        fig, ax = plt.subplots(1,1, figsize=ChartGenerator.FIGSIZE)
        ax.set_title(labels.title, pad=title_padding)

        # change colors
        theme = plt.get_cmap(ChartGenerator.randChoice(['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2','Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c']))
        ax.set_prop_cycle("color", [theme(1. * i / len(categories)) for i in range(len(categories))])

        ax.pie(pcnts,
                labels=categories if not show_legend else ['']*len(categories),
                shadow=show_shadow,
                startangle=start_angle,
                autopct=autopct,
                radius=radius,
                explode=explode
        )

        ax.axis('equal')

        if show_legend:
            ax.legend(labels=categories)
        
        # save to png
        self.save(id, labels, pcnts)

if __name__ == "__main__":

    n = 6000

    pcg = PieChartGenerator()
    for i in range(n):
        if i%50==0:
            print(i,'/',n)
        pcg.generate(i)
    