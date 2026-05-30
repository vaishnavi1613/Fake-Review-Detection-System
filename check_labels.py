import pandas as pd

df = pd.read_csv("IMDB_Movies.csv")
print(df['sentiment'].value_counts())
