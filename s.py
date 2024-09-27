import pandas as pd

data = {'Value': ['5,994.98', '3,456.78', '7,890.12']}
df = pd.DataFrame(data)

df["Value"] = pd.to_numeric(df["Value"].    ) 
pd.options.display.float_format = "{:,.2f}".format

print(df)
print(df.info())


