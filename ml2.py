import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
import pandas as pd
from matplotlib import style
style.use("ggplot")

def Build_data_set(features = ["DE_Ratio","Trailing P/E"]):

    data_df = pd.DataFrame.from_csv("key_stats.csv")
    X = np.array(data_df[features].values)#.tolist())
