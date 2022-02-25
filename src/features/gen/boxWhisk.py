from multiprocessing.sharedctypes import Value
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
from faker import Faker # https://faker.readthedocs.io/

from utils import ChartGenerator, RandLabelGenerator

class BoxWhisker(ChartGenerator):

	DIRECTIONS = ["v", "h"]

	fake = Faker()

	LABELS = [
		RandLabelGenerator("Class Number",
							"Score",
							"Exam Statistics by Class",
							x_func = lambda: ["Class 1", "Class 2", "Class 3", "Class 4"],
							y_func = lambda: ChartGenerator.randFloats(0,100)[0],
							unique_x=True
			),

		RandLabelGenerator("Month",
							"Units Sold",
							"Units Sold in 2021 per Month",
							x_func = lambda: RandLabelGenerator.MONTHS,
							y_func = lambda: ChartGenerator.randFloats(0,1000)[0]
			)
		]

	def __init__(self, dir):
		super().__init__(f"{dir}-box-whisker-chart")

		self.dir = dir

	def generate(self, id):
		labels = ChartGenerator.randChoice(BoxWhisker.LABELS)

		# randomize parameters
		n_points_per_cat = 100
		fliersize = ChartGenerator.randFloats(5, 10)[0]
		has_outliers = ChartGenerator.randBool()
		xs = labels.x_func()*n_points_per_cat
		n_points = n_points_per_cat*len(labels.x_func())
		ys = [labels.y_func() for _ in range(n_points)]

		# outlier calculation
		
		if has_outliers:

			outlier_thresh = (max(ys) - min(ys)) / 2

			outliers_high = ChartGenerator.randFloats(max(ys), max(ys)+outlier_thresh, size=ChartGenerator.randInts(1, 5)[0])
			outliers_low = ChartGenerator.randFloats(min(ys)-outlier_thresh, min(ys), size=ChartGenerator.randInts(1, 5)[0])
			ys.extend(outliers_high)
			ys.extend(outliers_low)
			for _ in range(len(outliers_high) + len(outliers_low)):
				xs.append(
					ChartGenerator.randChoice(labels.x_func())
					)
		
		
		title_padding = ChartGenerator.randFloats(15,40)[0]
		ChartGenerator.setRandTheme()
		ChartGenerator.setRandFontsizes()

		print(len(xs), len(ys))
		data = pd.DataFrame({labels.x: xs, labels.y: ys})
		
		# plot
		fig, ax = plt.subplots(1,1, figsize=ChartGenerator.FIGSIZE)
		ax.set_title(labels.title, pad=title_padding)

		if self.dir == "v":
			sns.boxplot(data=data,
						x=labels.x,
						y=labels.y,
						orient=self.dir,
						fliersize=fliersize,
						linewidth = ChartGenerator.randFloats(1, 5)[0]
			)
		else:
			sns.boxplot(data=data,
						x=labels.y,
						y=labels.x,
						orient=self.dir,
						fliersize=fliersize,
						linewidth = ChartGenerator.randFloats(1, 5)[0]
			)


		plt.show()



if __name__ == "__main__":

	n = 1

	for dir in BoxWhisker.DIRECTIONS:
		bwg = BoxWhisker(dir)
		for i in range(n):
			if i%50==0:
				print(i,'/',n)
			bwg.generate(i)
    