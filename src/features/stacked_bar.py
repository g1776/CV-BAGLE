from email.policy import strict
from multiprocessing.sharedctypes import Value
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import matplotlib.pyplot as plt
from faker import Faker # https://faker.readthedocs.io/

from utils import ChartGenerator, RandLabelGenerator


class StackedBarGenerator(ChartGenerator):

    fake = Faker()

    @staticmethod
    def stacked_ys(n_stacks, tops=[], labels=[], normalize=False):
        '''Helper function to generate N stacks of ys

        tops (list, optional): the maximum tops of each stack. Must be of length N.
        
        '''

        if tops != []:
            if len(tops) != n_stacks:
                raise ValueError("Tops must be of length N")

        if labels != []:
            if len(labels) != n_stacks:
                raise ValueError("Labels must be of length N")
        else:
            labels = [f"stack-{i}" for i in range(len(n_stacks))]

        stack = {}
        last_stack_top = 0
        for i in range(n_stacks):

            # initially assign top as a random value greater than the last top.
            top = ChartGenerator.randFloats(last_stack_top + 10, last_stack_top + ChartGenerator.randFloats(15, 30)[0])[0]
            if tops != []:
                # if provided, override with provided value
                top = tops[i] - ChartGenerator.randFloats(0.3, 0.9)[0] * (tops[i] - last_stack_top)
            
            stack.update({labels[i]: top})
            last_stack_top = top

        if normalize:
            total = sum(stack.values(), 0.0) / 100
            stack = {k: v / total for k, v in stack.items()}

        
        return {
            'normalized': normalize,
            'stack': stack
        }

    
    # Each of these instances provide the labels, as well as what functions to call to generate random values in each axis
    LABELS = [
        RandLabelGenerator("Month", 
                            "Temp", 
                            "Aggregate Temperature Statistics Per Month", 
                            x_func=lambda: RandLabelGenerator.MONTHS, 
                            y_func=lambda: StackedBarGenerator.stacked_ys(3, labels=["Low", "Average", "High"], tops=[40, 60, 100]),
                            unique_x=True,
                            ),
        RandLabelGenerator("Year", 
                            r"% of Revenue", 
                            "Revenue for Super Awesome Candy Co.", 
                            x_func=lambda: list(range(1990, 2002)), 
                            y_func=lambda: StackedBarGenerator.stacked_ys(5, 
                                                                    labels=["Bars", "Chocolate", "Ice Cream", "Lollipops", "Frozen Treats"], 
                                                                    normalize=True),
                            unique_x=True,
                            ),

    ]


    def __init__(self):

        super().__init__(f"stacked-bar-chart")

    
    def generate(self, id):

        # globals
        labels = ChartGenerator.randChoice(StackedBarGenerator.LABELS)
        if labels.y_func()['normalized']:
            self.type = "normalized-stacked-bar-chart"
        else:
            self.type = "stacked-bar-chart"

        # randomize parameters
        n_bars = ChartGenerator.randInts(2, 10)[0] if not labels.unique_x else len(labels.x_func())
        ys = [labels.y_func()['stack'] for _ in range(n_bars)] if not labels.unique_y else labels.y_func()
        xs = [labels.x_func() for _ in range(n_bars)] if not labels.unique_x else labels.x_func()
        cmap = LinearSegmentedColormap.from_list("my_colormap", [ChartGenerator.randHex() for _ in range(len(labels.y_func()['stack']))])
        title_padding = ChartGenerator.randFloats(15, 40)[0]
        ChartGenerator.setRandTheme()
        ChartGenerator.setRandFontsizes()

        # build data
        data = pd.DataFrame(ys)
        data.index = xs

        # plot
        fig, ax = plt.subplots(1,1, figsize=ChartGenerator.FIGSIZE)
        ax.set_title(labels.title, pad=title_padding)
        ax.set_xlabel(labels.x)
        ax.set_ylabel(labels.y)

        data.plot(kind="bar",
                    stacked=True,
                    ax=ax,
                    colormap=cmap
                    )
        
        ChartGenerator.setRandTickParams(ax, 'x')
        ChartGenerator.setRandTickParams(ax, 'y', labelrotation=False, rotations=[45, 90])
        

        # save to png
        self.save(id)

if __name__ == "__main__":

    n = 10

    sbg = StackedBarGenerator()
    for i in range(n):
        if i%50==0:
            print(i,'/',n)
        sbg.generate(i)
    