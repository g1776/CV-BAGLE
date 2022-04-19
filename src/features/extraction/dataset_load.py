import pickle
data = pickle.load(open(r'C:\Users\grego\Documents\GitHub\DataVizCaptionGeneration\volume\processed\features.pkl', 'rb'))
print(len(data[0]))