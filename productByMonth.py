import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel('online_retail_II.xlsx')

# Préparation des données
df.dropna(subset=["Customer ID"], inplace=True)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df_positive = df[df['Quantity'] > 0].copy()
df_positive.loc[:, 'Month'] = df_positive['InvoiceDate'].dt.to_period('M')

# Préparation des variables à afficher
monthly_sales = df_positive.groupby('Month')['Quantity'].sum()
top_products = df_positive.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10).index
df_top_products = df_positive[df_positive['Description'].isin(top_products)]
monthly_top_product_sales = df_top_products.groupby(['Month', 'Description'])['Quantity'].sum().unstack().fillna(0)

# Créer des subplots
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(18, 8))

# Graphique du nombre total de produits vendus par mois
sns.lineplot(x=monthly_sales.index.astype(str), y=monthly_sales.values, ax=axes[0])
axes[0].set_title('Nombre Total de Produits Vendus par Mois')
axes[0].set_xlabel('Mois')
axes[0].set_ylabel('Quantité Vendue')
axes[0].tick_params(axis='x', rotation=45)

# Graphique à barres empilées pour le top 10 des produits les plus vendus par mois
monthly_top_product_sales.plot(kind='bar', stacked=True, ax=axes[1], colormap='tab20')
axes[1].set_title('Top 10 des Produits les Plus Vendus par Mois')
axes[1].set_xlabel('Mois')
axes[1].set_ylabel('Quantité Vendue')
axes[1].legend(title='Produit', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
