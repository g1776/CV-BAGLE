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

	DIRECTIONS = ["vertical", "horizontal"]

	fake = Faker()

	LABELS = [
		RandLabelGenerator("Class Number",
						    "Score",
						    "Exam Statistics by Class",
						    #x_func =  a list with size 4 labeled [Class 1, Class 2, Class 3, Class 4]. Each class has 30 students 
						    y_func =  ChartGenerator.randFloats(0,100)[0]
			),

		RandLabelGenerator("Month",
							"Units Sold",
							"Units Sold in 2021 per Month",
							x_func = RandLabelGenerator.MONTHS,
							y_func = ChartGenerator.randFloats(0,1000)[0]
			)
		]

	def __init__(self):
		super().__init__("box_and_whisker")

	def generate(self, id):
		labels = ChartGenerator.randChoice(BoxWhisker.LABELS)
		n_box = ChartGenerator.randInts(2,10)[0] if not labels.x_func() else len(labels.x_func())
		ys = [labels.y_func() for _ in range(n_box)] if not labels.unique_y else labels.y_func()
		xs = [labels.x_func() for _ in range(n_box)] if not labels.unique_x else labels.y_func()

		multiple_colors = ChartGenerator.randBool()
		err = ChartGenerator.randFloats(0, max(ys)/15, size = n_box) if show_err else [0]*n_box

		box_color = ChartGenerator.randHex() if not multiple_colors else None
		title_padding = ChartGenerator.randFloats(15,40)[0]
		ChartGenerator.setRandTheme()
		ChartGenerator.setRandFontsizes()

		data = pd.DataFrame({labels.x: xs, labels.y: ys})

