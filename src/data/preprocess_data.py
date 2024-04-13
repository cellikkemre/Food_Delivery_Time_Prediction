from src.utils.helpers import check_df,grab_col_names,cat_summary,num_summary,check_outlier,quick_missing_imp
import warnings
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
from geopy.distance import geodesic
from datetime import datetime, timedelta



pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.max_rows', 500)
warnings.simplefilter(action='ignore', category=Warning)


df.head()
df.info()
df.replace({"NaN": np.nan}, regex=True, inplace = True)

## Veri Tiplerini Düzenleme
df['Time_Orderd']=pd.to_timedelta(df['Time_Orderd'])
df['Time_Order_picked']=pd.to_timedelta(df['Time_Order_picked'])
# Yaş değişkenini float'a çevirme
df['Delivery_person_Age'] = df['Delivery_person_Age'].astype(float)

# Rating değişkenini  float'a çevirme
df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype(float)

# Time değişkenini float'a çevirme
df['Time_taken(min)'] = df['Time_taken(min)'].str.extract('(\d+)').astype(float)

# multiple_deliveries değişkenini floata çevirme
df['multiple_deliveries'] = df['multiple_deliveries'].astype(float)

# Order Date değişkenini yıl,ay,gün olarak ayırma
df['Order_Date']=pd.to_datetime(df['Order_Date'])


"""
df['year']= df['Order_Date'].dt.year
df['month']= df['Order_Date'].dt.month
df['day']= df['Order_Date'].dt.day
"""


# Time_Order_picked değişkenini saat ve dakika olarak ayırma
"""
df['Time_Order_picked_Hour']=df['Time_Order_picked'].str.split(":",expand=True)[0].astype('int')
df['Time_Order_picked_Min']=df['Time_Order_picked'].str.split(":",expand=True)[1].astype('int')
"""

# Time_Orderd değişkenini saat ve dakika olarak ayırma
"""
df['Time_Orderd_Hour']=df['Time_Orderd'].str.split(':',expand=True)[0]

df['Time_Orderd_Min']=df['Time_Orderd'].str.split(':',expand=True)[1]
df['Time_Orderd_Hour']=df['Time_Orderd_Hour'].astype('int64')
df['Time_Orderd_Min']=df['Time_Orderd_Min'].astype('int64')
"""



df.head()
df.tail()
df.info()

### KEŞİFÇİ VERİ ANALİZİ ###

# veriye genel bakış
check_df(df)

# kategorik, kategorik ancak kardinal ve sayısal değişkenleri belirleme
cat_cols, cat_but_car, num_cols = grab_col_names(df)
print("Kategorik değişkenler:")
print(cat_cols)
print("\nNumerik değişkenler:")
print(num_cols)
print("\nKategorik görünümlü kardinal değişkenler:")
print(cat_but_car)


# kategorik değişken analizi
for col in cat_cols:
    cat_summary(df,col)

# numerik değişken analizi
for col in num_cols:
    num_summary(df,col,True)

# korelasyon analizi
corr = df[num_cols].corr()

sns.set(rc={'figure.figsize': (15, 15)})
sns.heatmap(corr, cmap="RdBu")
plt.show()

### AYKIRI DEĞER ANALİZİ ###

for col in num_cols:
    if col != "Time_taken(min)":
      print(col, check_outlier(df, col))

### EKSİK DEĞER ANALİZİ ###

def missing_values_table(dataframe, na_name=False):
    na_columns = [col for col in dataframe.columns if dataframe[col].isnull().sum() > 0]

    n_miss = dataframe[na_columns].isnull().sum().sort_values(ascending=False)

    ratio = (dataframe[na_columns].isnull().sum() / dataframe.shape[0] * 100).sort_values(ascending=False)

    missing_df = pd.concat([n_miss, np.round(ratio, 2)], axis=1, keys=['n_miss', 'ratio'])

    print(missing_df, end="\n")

    if na_name:
        return na_columns

missing_values_table(df)

# eksik değerleri grafik ile gösterme
msno.bar(df)
plt.show()

# eksik değerleri doldurma
df = quick_missing_imp(df, num_method="median", cat_length=20)

