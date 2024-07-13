import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Préparation des données
df = pd.read_excel('online_retail_II.xlsx')
df.dropna(subset=["Customer ID"], inplace=True)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Préparation des variable à afficher
df_returns = df[df['Quantity'] < 0].copy()
df_returns['Month'] = df_returns['InvoiceDate'].dt.to_period('M')
top_returned_products = df_returns.groupby('Description')['Quantity'].sum().sort_values().head(10).index
df_top_returns = df_returns[df_returns['Description'].isin(top_returned_products)]
monthly_top_returned_sales = df_top_returns.groupby(['Month', 'Description'])['Quantity'].sum().unstack().fillna(0)

# Créer un graphique à barres empilées pour les retours des top 10 produits
fig_returns, ax_returns = plt.subplots(figsize=(18, 8))
monthly_top_returned_sales.plot(kind='bar', stacked=True, ax=ax_returns, colormap='tab20')
ax_returns.set_title('Top 10 des Produits avec le Plus de Retours par Mois')
ax_returns.set_xlabel('Mois')
ax_returns.set_ylabel('Quantité Retournée')
ax_returns.legend(title='Produit', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
ax_returns.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
