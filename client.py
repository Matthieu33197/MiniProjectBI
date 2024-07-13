import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Préparation des données
df = pd.read_excel('online_retail_II.xlsx')
df.dropna(subset=["Customer ID"], inplace=True)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df_positive = df[df['Quantity'] > 0].copy()

# Calculer la fréquence des achats et le montant total dépensé par client
customer_stats = df_positive.groupby('Customer ID').agg({
    'InvoiceDate': 'nunique',
    'Quantity': 'sum',
    'Price': 'sum' 
})

customer_stats.columns = ['Frequency', 'TotalQuantity', 'TotalSpent']
top_10_customers = customer_stats.sort_values(by='TotalSpent', ascending=False).head(10)

# Segmentation des clients
plt.figure(figsize=(12, 8))
sns.scatterplot(data=customer_stats, x='Frequency', y='TotalSpent')
plt.title('Segmentation des Clients par Fréquence et Dépenses')
plt.xlabel('Fréquence des Achats')
plt.ylabel('Total Dépensé')
plt.grid(True)
plt.show()

print("Top 10 des clients par montant total dépensé :")
print(top_10_customers)
