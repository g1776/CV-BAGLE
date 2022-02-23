from audioop import mul
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import math
import os
from faker import Faker # https://faker.readthedocs.io/

from utils import ChartGenerator, RandLabelGenerator

class RegressionPlotGenerator(ChartGenerator):
    
    LABELS = [
        RandLabelGenerator("Number of Hours Studying Per Week",
                        "Grade in Class",
                        "Student Grades",
                        x_func=lambda: ChartGenerator.randFloats(0, 24)[0],
                        y_func=lambda: ChartGenerator.randFloats(0, 100)[0]
                        ),
        
        RandLabelGenerator("Miles Per Gallon",
                           "Number of Gallons",
                           "Miles Traveled",
                           x_func=lambda: ChartGenerator.randFloats(0, 15)[0],
                           y_func=lambda: ChartGenerator.randFloats(0, 400)[0]
                           ),
        
        RandLabelGenerator("Cost per diamond Carat",
                           "Diamond Carat",
                           "Cost (in thousands)",
                           x_func=lambda: ChartGenerator.randInts(1, 24)[0],
                           y_func=lambda: ChartGenerator.randFloats(1, 200)[0]),
        
        RandLabelGenerator("Trees Per Acres of Land",
                           "Acres",
                           "Number of Trees(in hundreds)",
                           x_func=lambda: ChartGenerator.randFloats(1, 10)[0],
                           y_func=lambda: ChartGenerator.randInts(1, 8)[0]),
        
        RandLabelGenerator("Profits per Number of Employees",
                           "Number of Employees",
                           "Profits (in thousands)" ,
                           x_func=lambda: ChartGenerator.randInts(50, 100)[0],
                           y_func=lambda: ChartGenerator.randFloats(100, 500)[0])
        ]
    
    MARKERS = [".", "o", "v","^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "+"]
    
    def __init__(self, regression_line):
        
        if regression_line:
            super().__init__(f"fit-regression-plot")
        else:
            super().__init__(f"unfit-regression-plot")

        self.regression_line = regression_line
        
    def generate(self, id):
        
        # globals
        labels = ChartGenerator.randChoice(RegressionPlotGenerator.LABELS)
        plot_markers = ChartGenerator.randChoice(RegressionPlotGenerator.MARKERS)
        
        # randomize parameters
        n_points = ChartGenerator.randInts(50, 100)[0] #if not labels.x_func() else len(labels.x_func())
        transform = ChartGenerator.randChoice([
            lambda y: math.pow(y, 2),
            lambda y: math.log10(y),
            lambda y: math.pow(y, 3),
            lambda y: y,
        ])
        ys = [transform(labels.y_func()) for _ in range(n_points)] if not labels.unique_y else labels.y_func()
        xs = [labels.x_func() for _ in range(n_points)] if not labels.unique_x else labels.x_func()
        multiple_colors = ChartGenerator.randBool()
        point_color = ChartGenerator.randHex() if not multiple_colors else None
        title_padding = ChartGenerator.randFloats(15, 40)[0]
        marker_size = ChartGenerator.randFloats(200, 600)[0]
        ChartGenerator.setRandTheme()
        ChartGenerator.setRandFontsizes()
    
        # build data
        data = pd.DataFrame({labels.x: xs, labels.y: ys})

        # plot
        fig, ax = plt.subplots(1,1, figsize=ChartGenerator.FIGSIZE)
        ax.set_title(labels.title, pad=title_padding)
    
        sns.regplot(data=data,
                    x=labels.x,
                    y=labels.y,
                    ax=ax,
                    fit_reg=self.regression_line,
                    scatter=False)
        sns.scatterplot(data=data,
                        x=labels.x,
                        y=labels.y,
                        ax=ax,
                        color=point_color,
                        marker=plot_markers,
                        s=marker_size
                        )
        ChartGenerator.setRandTickParams(ax, 'x')
        ChartGenerator.setRandTickParams(ax, 'y')

        self.save(id, labels, data)

if __name__ == "__main__":

    n = 6000

    for regression_line in [True, False]:
        rg = RegressionPlotGenerator(regression_line)
        for i in range(0, n):
            print(i,'/',n)
            rg.generate(i)