df.rename(columns={'city': 'type_of_city'}, inplace=True)

# ID
df.drop('ID', axis=1, inplace=True)




########### Delivery_Personel_ID ###########

# -Şehir isimlerini ayırma
def extract_and_expand_city(id):
    """
    Bu fonksiyon, bir teslimat personeli kimliğinden şehrin adını çıkarır ve uzun haliyle değiştirir.

    Parametreler:
        id: Teslimat personeli kimliği.

    Dönüş Değeri:
        Şehrin uzun hali.
    """
    res_index = id.find('RES')  # 'RES' kelimesinin indeksini bulun
    if res_index != -1:  # Eğer 'RES' kelimesi bulunduysa
        short_name = id[:res_index]  # 'RES' kelimesinin öncesini (şehir adını) alın
        city_names = {
            'JAP': 'Japura',
            'COIMB': 'Coimbatore',
            'INDO': 'Indore',
            'SUR': 'Surat',
            'CHEN': 'Chennai',
            'RANCHI': 'Ranchi',
            'MYS': 'Mysore',
            'PUNE': 'Pune',
            'HYD': 'Hyderabad',
            'MUM': 'Mumbai',
            'VAD': 'Vadodara',
            'BANG': 'Bangalore',
            'LUDH': 'Ludhiana',
            'KNP': 'Kanpur',
            'AGR': 'Agra',
            'ALH': 'Allahabad',
            'DEH': 'Dehradun',
            'KOC': 'Kochi',
            'AURG': 'Aurangabad',
            'BHP': 'Bhopal',
            'GOA': 'Goa',
            'KOL': 'Kolkata'
        }
        return city_names.get(short_name, None)  # Şehrin uzun halini döndür
    else:
        return None

# Fonksiyonu kullanarak City sütununu doldurun
df['City'] = df['Delivery_person_ID'].apply(extract_and_expand_city)



########### Delivery_person_Age ###########

# Veri tipini int çevirme
df["Delivery_person_Age"]=df["Delivery_person_Age"].astype(int)



########### Delivery_person_Rating ###########

# Hava koşullarına göre sürücü performansı



# Hava koşullarına göre sürücü performansı
def average_rating_by_weather(df):
    weather_conditions = df['Weatherconditions'].unique()
    avg_ratings_by_weather = {}
    for condition in weather_conditions:
        avg_rating = df[df['Weatherconditions'] == condition]['Delivery_person_Ratings'].mean()
        avg_ratings_by_weather[condition] = avg_rating
    return avg_ratings_by_weather


# Trafik yoğunluğuna göre sürücü performansı
def average_rating_by_traffic(df):
    traffic_conditions = df['Road_traffic_density'].unique()
    avg_ratings_by_traffic = {}
    for condition in traffic_conditions:
        avg_rating = df[df['Road_traffic_density'] == condition]['Delivery_person_Ratings'].mean()
        avg_ratings_by_traffic[condition] = avg_rating
    return avg_ratings_by_traffic


# Şehre göre sürücü performansı
def average_rating_by_city(df):
    cities = df['City'].unique()
    avg_ratings_by_city = {}
    for city in cities:
        avg_rating = df[df['City'] == city]['Delivery_person_Ratings'].mean()
        avg_ratings_by_city[city] = avg_rating
    return avg_ratings_by_city


# Ana veri setine yeni sütunları ekleyen fonksiyon
def add_rating_columns(df):
    # Hava koşullarına göre ortalama puanlar
    avg_ratings_weather = average_rating_by_weather(df)
    df['Avg_Rating_By_Weather'] = df['Weatherconditions'].map(avg_ratings_weather)

    # Trafik yoğunluğuna göre ortalama puanlar
    avg_ratings_traffic = average_rating_by_traffic(df)
    df['Avg_Rating_By_Traffic'] = df['Road_traffic_density'].map(avg_ratings_traffic)

    # Şehre göre ortalama puanlar
    avg_ratings_city = average_rating_by_city(df)
    df['Avg_Rating_By_City'] = df['City'].map(avg_ratings_city)

    return df

add_rating_columns(df)



########### Enlem-Boylam ###########



def calculate_distance(df):
    """
    Verilen bir veri çerçevesindeki restoran ve teslimat lokasyonları arasındaki mesafeyi hesaplar ve yeni bir sütun oluşturur.
    """
    distances = []
    for index, row in df.iterrows():
        restaurant_coords = (row['Restaurant_latitude'], row['Restaurant_longitude'])
        delivery_coords = (row['Delivery_location_latitude'], row['Delivery_location_longitude'])
        distance = geodesic(restaurant_coords, delivery_coords).kilometers
        distance_rounded = round(distance, 2)
        distances.append(distance_rounded)
    df['Distance'] = distances

calculate_distance(df)




##### Hava durumunu gruplara ayırma ####
def categorize_weather(condition):
    if condition in ['Windy', 'Stormy']:
        return 'Bad Weather'
    elif condition in ['Sunny', 'Cloudy']:
        return 'Good Weather'
    elif condition in ['Fog', 'Sandstorms']:
        return 'Moderate Weather'


df['weather_category'] = df['Weatherconditions'].apply(categorize_weather)

###### hava durumunda conditions kelimesini kaldırma ######
df['Weatherconditions'] = df['Weatherconditions'].str.replace('conditions ', '')



# günü aralılara bölme(sabah, öğle, akşam)
def time_of_day(x):
    if x in [4, 5, 6, 7, 8, 9, 10]:
        return "Morning"
    elif x in [11, 12, 13, 14, 15]:
        return "Afternoon"
    elif x in [16, 17, 18, 19]:
        return "Evening"
    elif x in [20, 21, 22, 23]:
        return "Night"
    else:
        return "Midnight"
df['day_zone'] = df['Time_Order_picked_Hour'].apply(time_of_day)



# gün bulma
df['day_name'] = df['Order_Date'].dt.day_name()




# Sipariş hazırlanma süresi

def calculate_preparation_time(df):
    # 'Time_Orderd' ve 'Time_Order_picked' sütunlarını timedelta olarak değiştirin
    df['Time_Orderd'] = pd.to_timedelta(df['Time_Orderd'])
    df['Time_Order_picked'] = pd.to_timedelta(df['Time_Order_picked'])

    # Teslimat hazırlanma süresini hesaplayın
    df['prep_time'] = np.where(df['Time_Order_picked'] < df['Time_Orderd'],
                                              df['Time_Order_picked'] - df['Time_Orderd'] + pd.Timedelta(days=1),
                                              df['Time_Order_picked'] - df['Time_Orderd'])

    # Teslimat hazırlanma süresini dakika cinsine dönüştürün
    df['prep_time'] = (df['prep_time'].dt.total_seconds() / 60).astype(int)

    return df
calculate_preparation_time(df)




### Yıl değişkenini kaldırma ###
df.drop('year', axis=1, inplace=True)










