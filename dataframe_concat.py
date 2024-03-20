import pandas as pd
import os

# header = "/Users/panfucheng/Desktop/CMU/ETIM/Data Science/Final Project/Movie-Ratings/"
header = "."
dfs = []
for i in range(10):
    csv_name = f"cast_{i*1000}_to_{i*1000+999}.csv"
    file_name = os.path.join(header, csv_name)
    df = pd.read_csv(file_name)
    dfs.append(df)
dfs = pd.concat(dfs, ignore_index=True)
dfs = dfs.drop(columns=["Unnamed: 0"])
dfs.to_csv("cast.csv")
