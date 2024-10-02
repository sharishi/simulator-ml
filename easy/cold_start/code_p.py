import pandas as pd
import numpy as np


def fillna_with_mean(
    df: pd.DataFrame, target: str, group: str
) -> pd.DataFrame:
    """Fill the null data"""
    df = df.copy()
    df[target] = np.floor(df[target].fillna(df.groupby(group)[target].transform('mean')))
    return df
