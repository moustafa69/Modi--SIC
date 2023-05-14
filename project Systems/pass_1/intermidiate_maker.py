import pandas as pd


# Reading the file and editing it
def parser(string1):
    df = pd.read_csv(string1, '\t')

    if len(df.columns) < 2:
        raise Exception('not enough columns, expected more')

    df.drop(df.columns[[0, len(df.columns) - 1]], axis=1, inplace=True)
    dataColumns = list(df.columns.values)
    ProgName = str(dataColumns[0]).upper()
    # the for loop checks if the cell in first column contains '.' or
    # there is no instruction, then the line will be deleted

    rows = []
    for i in range(0, len(df)):
        if (df.iloc[i, 0]) == '.' or pd.isnull(df.iloc[i, 1]):

            continue
        else:
            rows.append(df.iloc[i])

    df = pd.DataFrame(rows)
    # print(df)
    return df

