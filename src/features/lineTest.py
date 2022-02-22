import seaborn as sns
import pandas as pd
import random
import matplotlib.pyplot as plt
from os import path
import cv2

i = 0
while True:	
	outpath = "C:/Users/ian/Desktop/Graph/LineGraph"
	x_func = [1980,1990,2000,2010,2020]
	y_func = []
	for x in range(len(x_func)):
		y_func.append(random.uniform(1,10))
	plt.plot(x_func, y_func)
	plt.ylabel("Unemployment Rate")
	plt.xlabel("Year")
	plt.title("Unemployment Rate Vs. Year")
	plt.show()
	#plt.savefig('unem_{0}.jpg'.format(x))
	print(i)
	i = i + 1
	if (i > 5):
		break 







