from multiprocessing.sharedctypes import Value
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
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
                            x_func=lambda: BarGenerator.fake.first_name(), 
                            y_func=lambda: ChartGenerator.randFloats(1,100)[0]
                            ),
        RandLabelGenerator("Cat", 
                            "# Whiskers", 
                            "# Whiskers on cats affected by nuclear meltdowns",
                            x_func=lambda: BarGenerator.fake.first_name(),
                            y_func=lambda: ChartGenerator.randFloats(1,100)[0]
                            ),
        RandLabelGenerator("Grade", 
                            "Frequency", 
                            "Distribution of Letter Grades in the 4th Grade",
                            x_func=lambda: RandLabelGenerator.LETTER_GRADES,
                            y_func=lambda: ChartGenerator.randFloats(1,30)[0],
                            unique_x=True
                            ),
        RandLabelGenerator("Month", 
                            "# Days", 
                            "Number of Rainy Days in each Month",
                            x_func=lambda: RandLabelGenerator.MONTHS,
                            y_func=lambda: ChartGenerator.randFloats(0,32)[0],
                            unique_x=True
                            ),
        RandLabelGenerator("Year", 
                            "$ Profit (in Millions)", 
                            "Yearly Profits for the Super Awesome Chocolate Company",
                            x_func=lambda: [str(v) for v in range(1970, 1981)],
                            y_func=lambda: ChartGenerator.randFloats(200, 700)[0],
                            unique_x=True
                            ),
        RandLabelGenerator("File Path",
                            "Size (MB)",
                            "Comparison of File Sizes on My Computer",
                            x_func=lambda: BarGenerator.fake.file_path(depth=0),
                            y_func=lambda: ChartGenerator.randFloats(40, 400)[0],
                            rot_x=[-90, 90]
                            ),
        RandLabelGenerator("City",
                            "Area (Sq km)",
                            "Area of Cities",
                            x_func=lambda: BarGenerator.fake.city(),
                            y_func=lambda: ChartGenerator.randFloats(1500, 8000)[0],
                            rot_x=[-90, 90]
                            ),
        RandLabelGenerator("Country",
                            "Population (Millions)",
                            "Country Populations",
                            x_func=lambda: BarGenerator.fake.city(),
                            y_func=lambda: ChartGenerator.randFloats(0.2, 100)[0],
                            rot_x=[-90, 90]
                            ),
        RandLabelGenerator("Street",
                            "Length (km)",
                            f"Lengths of Streets in Europe",
                            x_func=lambda: BarGenerator.fake.street_name(),
                            y_func=lambda: ChartGenerator.randFloats(5, 50)[0],
                            rot_x=[-90, 90]
                            ),
        RandLabelGenerator("Occupation",
                            "Yearly Salary (in thousands)",
                            f"Salaries for Occupatations",
                            x_func=lambda: BarGenerator.fake.job(),
                            y_func=lambda: ChartGenerator.randFloats(30, 120)[0],
                            rot_x=[-90, 90]
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
        n_bars = ChartGenerator.randInts(2, 10)[0] if not labels.x_func() else len(labels.x_func())
        ys = [labels.y_func() for _ in range(n_bars)] if not labels.unique_y else labels.y_func()
        xs = [labels.x_func() for _ in range(n_bars)] if not labels.unique_x else labels.x_func()
        multiple_colors = ChartGenerator.randBool()
        show_err = ChartGenerator.randBool()
        err = ChartGenerator.randFloats(0, max(ys)/15, size = n_bars) if show_err else [0]*n_bars
        bar_color = ChartGenerator.randHex() if not multiple_colors else None
        title_padding = ChartGenerator.randFloats(15, 40)[0]
        ChartGenerator.setRandTheme()
        ChartGenerator.setRandFontsizes()

        # build data
        data = pd.DataFrame({labels.x: xs, labels.y: ys})

        # plot
        fig, ax = plt.subplots(1,1, figsize=ChartGenerator.FIGSIZE)
        ax.set_title(labels.title, pad=title_padding)
        try:
            if self.direction == "vertical":
                sns.barplot(data=data,
                            x=labels.x,
                            y=labels.y,
                            ax=ax,
                            color = bar_color,
                            **{'yerr':err}
                            )
                ChartGenerator.setRandTickParams(ax, 'x', rotations=[90])
                ChartGenerator.setRandTickParams(ax, 'y', labelrotation=False)
            else:
                sns.barplot(data=data,
                            x=labels.y,
                            y=labels.x,
                            ax=ax,
                            color = bar_color,
                            **{'xerr':err}
                            )
                ChartGenerator.setRandTickParams(ax, 'y', rotations=[0])
                ChartGenerator.setRandTickParams(ax, 'x', labelrotation=False)

            # output to png
            self.save(id, labels, data)
        except ValueError:
            print(f"Passing {self.type}-{id}. Ran into seaborn error.") # cannot figure out where certain value error is being thrown, so ignoring :/


if __name__ == "__main__":

    n = 6000

    for direction in BarGenerator.DIRECTIONS:
        bg = BarGenerator(direction)
        for i in range(n):
            if i%50==0:
                print(i,'/',n)
            bg.generate(i)
    