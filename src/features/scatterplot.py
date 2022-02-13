from audioop import mul
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os
from faker import Faker # https://faker.readthedocs.io/

from utils import ChartGenerator, RandLabelGenerator

class RegressionPlotGenerator(ChartGenerator):
    
    REGRESSION_LINE = ChartGenerator.randBool()
    
    if REGRESSION_LINE == True:
        REGRESSION_LINE = ["TRUE"]
    else: 
        REGRESSION_LINE = ["FALSE"]
    
    LABELS = [
        RandLabelGenerator("Number of Hours Studying Per Week",
                           "Grade in Class",
                           "Student Grades",
                           x_func=lambda: ChartGenerator.randFloats(0, 24)[0],
                           y_func=lambda: ChartGenerator.randFloats(0, 100)[0]
                           )
        ]
    
    MARKERS = [".", "o", "v","^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "+"]
    
    def __init__(self, regression_line):
        
        super().__init__(f"{regression_line}-regression-plot")
        
        self.regression_line = regression_line
        
    def generate(self, id, ax):
        
        # globals
        labels = ChartGenerator.randChoice(RegressionPlotGenerator.LABELS)
        plot_markers = ChartGenerator.randChoice(RegressionPlotGenerator.MARKERS)
        
       # randomize parameters
        n_points = ChartGenerator.randInts(50, 100)[0] #if not labels.x_func() else len(labels.x_func())
        ys = [labels.y_func() for _ in range(n_points)] if not labels.unique_y else labels.y_func()
        xs = [labels.x_func() for _ in range(n_points)] if not labels.unique_x else labels.x_func()
        multiple_colors = ChartGenerator.randBool()
        point_color = ChartGenerator.randHex() if not multiple_colors else None
        title_padding = ChartGenerator.randFloats(15, 40)[0]
        ChartGenerator.setRandTheme()
        ChartGenerator.setRandFontsizes()
      
       # build data
        data = pd.DataFrame({labels.x: xs, labels.y: ys})

        ax.set_title(labels.title, pad=title_padding)
       
        try:
            if self.regression_line == "TRUE":
                sns.regplot(data=data,
                            x=labels.x,
                            y=labels.y,
                            ax=ax,
                            color=point_color,
                            marker=plot_markers,
                            fit_reg=True)
                ChartGenerator.setRandTickParams(ax, 'x')
                ChartGenerator.setRandTickParams(ax, 'y')
            
            else:
                sns.regplot(data=data,
                            x=labels.x,
                            y=labels.y,
                            ax=ax,
                            color=point_color,
                            marker=plot_markers,
                            fit_reg= False
                            )
                ChartGenerator.setRandTickParams(ax, 'x')
                ChartGenerator.setRandTickParams(ax, 'y')               
            
            self.save(id)
        except:
            print(f"Passing {self.type}-{id}. Ran into seaborn error.") # cannot figure out where certain value error is being thrown, so ignoring :/

if __name__ == "__main__":

    fig, ax = plt.subplots(1,1, figsize=ChartGenerator.FIGSIZE)

    n = 20

    for regression_line in RegressionPlotGenerator.REGRESSION_LINE:
        rg = RegressionPlotGenerator(regression_line)
        for i in range(1, n):
            print(i,'/',n)
            rg.generate(i, ax)

                
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
