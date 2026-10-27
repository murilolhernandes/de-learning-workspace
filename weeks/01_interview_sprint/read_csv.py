import pandas as pd
df = pd.read_csv("data/raw/transactions_2025_01.csv")
print(df.head(), "\n")
print(df.dtypes)