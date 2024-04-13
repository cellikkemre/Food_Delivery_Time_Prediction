

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
import pandas as pd


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





########### Enlem-Boylam ###########














