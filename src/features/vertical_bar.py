from audioop import mul
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os
from faker import Faker # https://faker.readthedocs.io/

from utils import ChartGenerator


class VerticalBarGenerator(ChartGenerator):

    def __init__(self):
        super().__init__("vertical-bar-chart")
    
    def generate(self, id):

        # globals
        sns.set_style(ChartGenerator.randTheme())
        fake = Faker()

        # parameters
        n_bars = ChartGenerator.randInts(2, 10)[0]
        ys = ChartGenerator.randFloats(1, 100, n_bars)
        xs = [fake.name() for _ in range(n_bars)]
        multiple_colors = ChartGenerator.randBool()
        if not multiple_colors:
            bar_color = ChartGenerator.randHex()

        # generate plot
        data = pd.DataFrame({"person": xs, "age": ys})

        fig, ax = plt.subplots(1,1, figsize=ChartGenerator.FIGSIZE)

        sns.barplot(data=data,
                    x="person",
                    y="age",
                    ax=ax,
                    color = None if multiple_colors else bar_color
                    )

        # output
        output_folder = os.path.join("..", "..", "volume", "raw")
        fp = os.path.join(output_folder, f"{self.type}-{id}.png")
        plt.savefig(fp)


if __name__ == "__main__":

    vbg = VerticalBarGenerator()
    for i in range(10):
        print(i)
        vbg.generate(i)
