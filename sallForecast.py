import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Préparation des données
df = pd.read_excel('online_retail_II.xlsx')
df.dropna(subset=["Customer ID"], inplace=True)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df_positive = df[df['Quantity'] > 0].copy()
df_positive.loc[:, 'Month'] = df_positive['InvoiceDate'].dt.to_period('M')

monthly_sales = df_positive.groupby('Month')['Quantity'].sum()
monthly_sales_series = monthly_sales.to_timestamp()

# Détermination du type de modèle
if len(monthly_sales_series) < 24:
    print("Pas assez de données pour un modèle saisonnier. Utilisation d'un modèle sans composante saisonnière.")
    model = ExponentialSmoothing(monthly_sales_series, trend='add').fit()
else:
    model = ExponentialSmoothing(monthly_sales_series, seasonal='add', seasonal_periods=12).fit()

forecast = model.forecast(12)

# Prévisions
plt.figure(figsize=(12, 8))
plt.plot(monthly_sales_series, label='Ventes Réelles')
plt.plot(forecast, label='Prévisions', linestyle='--')
plt.title('Prévisions des Ventes Mensuelles')
plt.xlabel('Date')
plt.ylabel('Quantité Vendue')
plt.legend()
plt.grid(True)
plt.show()
