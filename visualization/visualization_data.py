import matplotlib.pyplot as plt
import seaborn as sns


# Hava durumu (WEATHER) ve trafik yoğunluğu (TRAFFIC_DENSITY) dağılımları
plt.figure(figsize=(10, 6))
sns.boxplot(x='WEATHER', y='DELIVERY_TIME', data=df)
plt.title('Delivery Time by Weather')
plt.xlabel('Weather')
plt.ylabel('Delivery Time')
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x='TRAFFIC_DENSITY', y='DELIVERY_TIME', data=df)
plt.title('Delivery Time by Traffic Density')
plt.xlabel('Traffic Density')
plt.ylabel('Delivery Time')
plt.show()


# Teslimat süresi ile hava durumu arasındaki ilişki
plt.figure(figsize=(10, 6))
sns.boxplot(x='WEATHER', y='DELIVERY_TIME', data=df)
plt.title('Delivery Time by Weather')
plt.xlabel('Weather')
plt.ylabel('Delivery Time')
plt.show()



# Teslimat süresi ile diğer değişkenler arasındaki ilişkiyi gösteren scatter plotlar
# Mesafeyi 5 eşit parçaya bölmek
df['DISTANCE_GROUP'], distance_bins = pd.cut(df['DISTANCE'], bins=5, labels=False, retbins=True)

# Her mesafe grubunun başlangıç ve bitiş değerlerini hesapla
distance_labels = [f'{int(distance_bins[i]):}-{int(distance_bins[i+1]):}' for i in range(len(distance_bins)-1)]

# Her mesafe grubunun ortalama teslimat süresini hesapla
distance_delivery_mean = df.groupby('DISTANCE_GROUP')['DELIVERY_TIME'].mean()

# Sütun grafiği oluştur
plt.figure(figsize=(10, 6))
distance_delivery_mean.plot(kind='bar', color='skyblue')
plt.title('Average Delivery Time by Distance Group')
plt.xlabel('Distance Group')
plt.ylabel('Average Delivery Time')
plt.xticks(range(len(distance_labels)), distance_labels, rotation=45)
plt.show()






