import pandas as pd
from matplotlib import pyplot as plt

def __init__():
    pass


def signo(value):
    res = 0
    if value < 0:
        res  = -1
    elif value > 0:
        res = 1
    return res

def get_pandas_dataframe(file_path, price_col):

    sp = pd.read_csv(file_path)

    sp = sp[sp.Volume.notna()].reset_index()
    sp = sp[['Date', price_col, 'Volume']]
    sp = sp.rename(columns={price_col:"Price"})

    mod = sp[:-1][['Price', 'Volume']]
    modified = pd.DataFrame([[0, 0]], columns=['Price', 'Volume']).append(mod[['Price', 'Volume']], ignore_index=True)
    modified = modified.rename(columns={"Price":"Prior_Price", "Volume":"Prior_Volume"})

    dataset = sp.join(modified)
    dataset['Rt'] = dataset['Price'] - dataset['Prior_Price']
    dataset['Vt'] = dataset['Volume'] - dataset['Prior_Volume']
    Rt_1 = [0]
    Rt_1.extend(list(dataset.Rt.values))
    dataset['Rt-1'] = pd.DataFrame(Rt_1)
    dataset['At'] = abs(dataset['Rt']) - abs(dataset['Rt-1'])
    dataset = dataset[['Date', 'Price', 'Prior_Price', 'Rt', 'Rt-1', 'At', 'Volume', 'Prior_Volume', 'Vt']]

    dataset['Mt'] = dataset.Rt.apply(signo)
    dataset['Dt'] = dataset.Vt.apply(signo)
    dataset['Yt'] = dataset.At.apply(signo)

    dataset = dataset[['Date', 'Price', 'Prior_Price', 'Rt', 'Rt-1', 'At', 'Volume', 'Prior_Volume', 'Vt', 'Mt', 'Dt', 'Yt']]

    return dataset[2:].reset_index()
