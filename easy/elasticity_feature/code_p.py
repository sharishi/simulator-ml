import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


def elasticity_df(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates elasticity"""
    grouped = df.groupby('sku')

    results = []

    for sku, group in grouped:
        # Логарифм продаж с добавлением 1 (чтобы избежать log(0))
        log_sales = np.log(group['qty'] + 1)
        price = group['price'].values.reshape(-1, 1)

        # Линейная регрессия
        model = LinearRegression()
        model.fit(price, log_sales)

        # Предсказанные значения логарифма продаж
        log_sales_pred = model.predict(price)

        # Коэффициент детерминации R^2
        r_squared = r2_score(log_sales, log_sales_pred)

        results.append({'sku': sku, 'elasticity': r_squared})

    results = pd.DataFrame(results)

    return results
