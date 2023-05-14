import pandas as pd


def getSymbolTable(df):
    new_df = df.drop(df.columns[[2, 3]], axis=1)
    symbol_table = new_df.dropna()
    return symbol_table
