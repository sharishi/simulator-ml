import pandas as pd
import numpy as np


def limit_gmv(df: pd.DataFrame) -> pd.DataFrame:
    """GMV predict"""
    df = df.copy()
    df['gmv'] = np.where(
        (df['gmv'] / df['price']) < df['stock'],
        (np.minimum(df['gmv'],np.floor(df['gmv'] / df['price'])*df['price'])).astype(int),
        df['stock'] * df['price']
    )
    return df
