import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os
from faker import Faker # https://faker.readthedocs.io/

from utils import ChartGenerator, RandLabelGenerator


class BarGenerator(ChartGenerator):

    DIRECTIONS = ["vertical", "horizontal"]

    fake = Faker()
    
    # Each of these instances provide the labels, as well as what functions to call to generate random values in each axis
    LABELS = [
        RandLabelGenerator("Person", 
                            "Age", 
                            "Ages of People", 
                            x_func=lambda: BarGenerator.fake.name(), 
                            y_func=lambda: ChartGenerator.randFloats(1,100)[0]
                            ),
        RandLabelGenerator("Cat", 
                            "# Whiskers", 
                            "# Whiskers on cats affected by nuclear meltdowns",
                            x_func=lambda: BarGenerator.fake.name(),
                            y_func=lambda: ChartGenerator.randFloats(1,100)[0]
                            )
    ]


    def __init__(self, direction):

        if direction not in BarGenerator.DIRECTIONS:
            raise ValueError("Bar Chart type must be vertical or horizontal")

        super().__init__(f"{direction}-bar-chart")

        self.direction = direction
    
    def generate(self, id):

        # globals
        labels = ChartGenerator.randChoice(BarGenerator.LABELS)

        # randomize parameters
        n_bars = ChartGenerator.randInts(2, 10)[0]
        ys = [labels.y_func() for _ in range(n_bars)]
        xs = [labels.x_func() for _ in range(n_bars)]
        multiple_colors = ChartGenerator.randBool()
        show_err = ChartGenerator.randBool()
        err = ChartGenerator.randFloats(0, max(ys)/15, size = n_bars) if show_err else []
        bar_color = ChartGenerator.randHex() if not multiple_colors else None
        ChartGenerator.setRandTheme()
        ChartGenerator.setRandFontsizes()

        # build data
        data = pd.DataFrame({labels.x: xs, labels.y: ys})


        # generate plot
        fig, ax = plt.subplots(1,1, figsize=ChartGenerator.FIGSIZE)

        ax.set_title(labels.title)

        if self.direction == "vertical":
            sns.barplot(data=data,
                        x=labels.x,
                        y=labels.y,
                        ax=ax,
                        color = bar_color,
                        **{'yerr':err if show_err else [0]*n_bars}
                        )
            ChartGenerator.setRandTickParams(ax, 'x')
            ChartGenerator.setRandTickParams(ax, 'y', labelrotation=False)
        else:
            sns.barplot(data=data,
                        x=labels.y,
                        y=labels.x,
                        ax=ax,
                        color = bar_color,
                        **{'xerr':err if show_err else [0]*n_bars}
                        )
            ChartGenerator.setRandTickParams(ax, 'y')
            ChartGenerator.setRandTickParams(ax, 'x', labelrotation=False)

        # output to png
        self.save(id)


if __name__ == "__main__":

    for direction in BarGenerator.DIRECTIONS:
        bg = BarGenerator(direction)
        for i in range(1):
            bg.generate(1)
