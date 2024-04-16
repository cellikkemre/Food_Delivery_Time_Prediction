from src.utils.helpers import extract_and_expand_city,average_rating_by_city,average_rating_by_traffic,average_rating_by_weather,add_rating_columns,calculate_distance,calculate_preparation_time,time_of_day,check_df,grab_col_names,label_encoder,one_hot_encoder,target_summary_with_cat
from geopy.distance import geodesic
import numpy as np

# City
df.columns = ['type_of_city' if col == 'City' else col for col in df.columns]




# Delivery_Personel_ID

df['City'] = df['Delivery_person_ID'].apply(extract_and_expand_city)

# multiple_deliveries

df["multiple_deliveries"]=df["multiple_deliveries"].astype('int64')

# Delivery_person_Age

df["Delivery_person_Age"]=df["Delivery_person_Age"].astype('int64')


# Delivery_person_Rating

add_rating_columns(df)
df.head()
df["Avg_Rating_By_City"].value_counts()
# latitude-longitude
cols=['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']
for col in cols:
    df[col]= abs(df[col])
calculate_distance(df)


# Weatherconditions
df['Weatherconditions'] = df['Weatherconditions'].str.replace('conditions ', '')

# Order Date
df['year']= df['Order_Date'].dt.year.astype('int64')
df['month']= df['Order_Date'].dt.month.astype('int64')
df['day']= df['Order_Date'].dt.day.astype('int64')


# Time_Order_picked-Time_Orderd
df['Time_Order_picked'] = df['Time_Order_picked'].astype(str)
df['Time_Orderd'] = df['Time_Orderd'].astype(str)

df['Time_Order_picked'] = df['Time_Order_picked'].apply(lambda x: x.split(" ")[-1])
df['Time_Orderd'] = df['Time_Orderd'].apply(lambda x: x.split(" ")[-1])


df['Time_Order_picked_Hour'] = df['Time_Order_picked'].str.split(":", expand=True)[0].astype('int64')
df['Time_Order_picked_Min'] = df['Time_Order_picked'].str.split(":", expand=True)[1].astype('int64')



df['Time_Orderd_Hour']=df['Time_Orderd'].str.split(':',expand=True)[0]

df['Time_Orderd_Min']=df['Time_Orderd'].str.split(':',expand=True)[1]
df['Time_Orderd_Hour']=df['Time_Orderd_Hour'].astype('int64')
df['Time_Orderd_Min']=df['Time_Orderd_Min'].astype('int64')


calculate_preparation_time(df)

# Day

df['day_zone'] = df['Time_Order_picked_Hour'].apply(time_of_day)

df['day_name'] = df['Order_Date'].dt.day_name()





# Columns
df.columns = df.columns.str.upper()

df.rename(columns={'WEATHERCONDITIONS': 'WEATHER',
                   'ROAD_TRAFFIC_DENSITY': 'TRAFFIC_DENSITY',
                   'TYPE_OF_CITY': 'CITY_TYPE',
                   'TIME_TAKEN(MIN)': 'DELIVERY_TIME',
                   'AVG_RATING_BY_WEATHER': 'WEATHER_RATING',
                   'AVG_RATING_BY_TRAFFIC': 'TRAFFIC_RATING',
                   'AVG_RATING_BY_CITY': 'CITY_RATING',
                   'DAY_ZONE': 'DAY_TIME_ZONE',
                   'PREP_TIME': 'PREPARATION_TIME'}, inplace=True)

# Drop
df.drop(['ID', 'DELIVERY_PERSON_ID', 'ORDER_DATE', 'TIME_ORDERD', 'TIME_ORDER_PICKED'], axis=1, inplace=True)

# Veri setinin son halini kayıt etme
df.to_csv("data/processed/veri_seti_yeni.csv", index=False)




