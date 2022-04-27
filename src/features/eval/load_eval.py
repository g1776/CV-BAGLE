import pickle
import pandas as pd

EVAL_FP = r"C:\Users\grego\Documents\GitHub\DataVizCaptionGeneration\volume\processed\eval_fit-density-histogram-plot.pkl"

eval_list = pickle.load(open(EVAL_FP, 'rb'))
df = pd.DataFrame(eval_list)
print(df)
