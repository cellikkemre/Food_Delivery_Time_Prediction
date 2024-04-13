def check_df(dataframe):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(3))
    print("##################### Tail #####################")
    print(dataframe.tail(3))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())

    # Sadece sayısal sütunları seçme
    numeric_columns = dataframe.select_dtypes(include=np.number)
    print("##################### Quantiles #####################")
    print(numeric_columns.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)



def grab_col_names(dataframe, cat_th=10, car_th=25):
    """
    Verilen veri çerçevesi için sütun isimlerini alır ve kategorik, kategorik ancak kardinal ve sayısal değişkenleri belirler.

    Parametreler:
    dataframe (pandas.DataFrame): Sütun isimlerinin alınacağı veri çerçevesi.
    cat_th (int, optional): Kategorik değişken olarak kabul edilecek eşik değer. Varsayılan değer 10.
    car_th (int, optional): Kategorik ancak kardinal değişken olarak kabul edilecek eşik değer. Varsayılan değer 20.

    Returns:
    tuple: Kategorik değişkenlerin, kategorik ancak kardinal değişkenlerin ve sayısal değişkenlerin listelerini içeren bir tuple.

    Örnek:
    cat_cols, cat_but_car, num_cols = grab_col_names(dataframe)
    """

    cat_cols = [col for col in dataframe.columns if dataframe[col].dtypes == "O"]

    num_but_cat = [col for col in dataframe.columns if dataframe[col].nunique() < cat_th and
                   dataframe[col].dtypes != "O"]

    cat_but_car = [col for col in dataframe.columns if dataframe[col].nunique() > car_th and
                   dataframe[col].dtypes == "O"]

    cat_cols = cat_cols + num_but_cat
    cat_cols = [col for col in cat_cols if col not in cat_but_car]

    num_cols = [col for col in dataframe.columns if dataframe[col].dtypes != "O"]
    num_cols = [col for col in num_cols if col not in num_but_cat]

    print(f"Observations: {dataframe.shape[0]}")
    print(f"Variables: {dataframe.shape[1]}")
    print(f'cat_cols: {len(cat_cols)}')
    print(f'num_cols: {len(num_cols)}')
    print(f'cat_but_car: {len(cat_but_car)}')
    print(f'num_but_cat: {len(num_but_cat)}')

    # cat_cols + num_cols + cat_but_car = değişken sayısı.
    # num_but_cat cat_cols'un içerisinde zaten.
    # dolayısıyla tüm şu 3 liste ile tüm değişkenler seçilmiş olacaktır: cat_cols + num_cols + cat_but_car
    # num_but_cat sadece raporlama için verilmiştir.

    return cat_cols, cat_but_car, num_cols


def cat_summary(dataframe, col_name, plot=False):
    """
    Verilen kategorik bir değişkenin frekans tablosunu ve oranlarını yazdırır. Opsiyonel olarak, bu tabloyu bir grafik
    ile görselleştirebilir.

    Parametreler:
    dataframe (pandas.DataFrame): Kategorik değişkenin bulunduğu veri çerçevesi.
    col_name (str): Frekans tablosunun ve oranlarının alınacağı kategorik değişkenin adı.
    plot (bool, optional): Grafik gösterilsin mi? Varsayılan değer False.

    Returns:
    None

    Örnek:
    cat_summary(dataframe, "column_name", plot=True)
    """

    # Kategorik değişkenin frekans tablosunu ve oranlarını oluşturur
    summary = pd.DataFrame({col_name: dataframe[col_name].value_counts(),
                            "Ratio (%)": 100 * dataframe[col_name].value_counts() / len(dataframe)})

    # Frekans tablosunu yazdırır
    print(summary)

    # Opsiyonel olarak, grafik gösterir
    if plot:
        sns.countplot(x=dataframe[col_name], data=dataframe)
        plt.show()


def num_summary(dataframe, numerical_col, plot=False):
    """
    Verilen sayısal bir değişken için temel istatistiklerin özetini yazdırır ve isteğe bağlı olarak bir histogram görseli oluşturur.

    Parametreler:
    dataframe (pandas.DataFrame): Sayısal değişkenin bulunduğu veri çerçevesi.
    numerical_col (str): Temel istatistiklerin alınacağı sayısal değişkenin adı.
    plot (bool, optional): Histogram gösterilsin mi? Varsayılan değer False.

    Returns:
    None

    Örnek:
    num_summary(dataframe, "column_name", plot=True)
    """

    # Sayısal değişken için temel istatistiklerin özetini oluşturur ve yazdırır
    quantiles = [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99]
    print(dataframe[numerical_col].describe(quantiles).T)

    # Opsiyonel olarak, histogram görseli oluşturur ve gösterir
    if plot:
        dataframe[numerical_col].hist(bins=50)
        plt.xlabel(numerical_col)
        plt.title(numerical_col)
        plt.show()

    print("#####################################")


def outlier_thresholds(dataframe, variable, low_quantile=0.05, up_quantile=0.95):
    """
    Verilen sayısal bir değişken için alt ve üst sınır eşik değerlerini hesaplar.

    Parametreler:
    dataframe (pandas.DataFrame): Sınır eşik değerlerinin hesaplanacağı veri çerçevesi.
    variable (str): Eşik değerlerinin hesaplanacağı sayısal değişkenin adı.
    low_quantile (float, optional): Alt sınır eşik değeri için kullanılacak çeyreklik. Varsayılan değer 0.05.
    up_quantile (float, optional): Üst sınır eşik değeri için kullanılacak çeyreklik. Varsayılan değer 0.95.

    Returns:
    tuple: Alt ve üst sınır eşik değerleri.

    Örnek:
    low_limit, up_limit = outlier_thresholds(dataframe, "column_name")
    """
    quantile_one = dataframe[variable].quantile(low_quantile)
    quantile_three = dataframe[variable].quantile(up_quantile)
    interquantile_range = quantile_three - quantile_one
    up_limit = quantile_three + 1.5 * interquantile_range
    low_limit = quantile_one - 1.5 * interquantile_range
    return low_limit, up_limit


def check_outlier(dataframe, col_name):
    """
    Verilen sayısal bir değişken için aykırı değer kontrolü yapar.

    Parametreler:
    dataframe (pandas.DataFrame): Aykırı değer kontrolü yapılacak veri çerçevesi.
    col_name (str): Aykırı değer kontrolü yapılacak sayısal değişkenin adı.

    Returns:
    bool: Değişkenin aykırı değer içerip içermediği durumunu döndürür.

    Örnek:
    is_outlier = check_outlier(dataframe, "column_name")
    """
    low_limit, up_limit = outlier_thresholds(dataframe, col_name)
    if (dataframe[(dataframe[col_name] > up_limit) | (dataframe[col_name] < low_limit)] != pd.Timestamp(0)).any(axis=None):
        return True
    else:
        return False


def missing_values_table(dataframe, na_name=False):
    """
    Verilen veri çerçevesindeki eksik değerleri analiz eder ve eksik değer tablosunu yazdırır.

    :param dataframe: pandas.DataFrame, Eksik değerlerin analiz edileceği veri çerçevesi.
    :param na_name: bool, Opsiyonel, Eksik değer bulunan sütunların isimlerini döndürsün mü? Varsayılan değer False.

    :return: list, Eksik değer bulunan sütunların isimleri (opsiyonel, na_name=True durumunda).

    Örnek:
    missing_values_table(dataframe)
    missing_values_table(dataframe, na_name=True)
    """
    # Eksik değer bulunan sütunların listesini oluşturur
    na_columns = [col for col in dataframe.columns if dataframe[col].isnull().sum() > 0]

    # Her sütundaki eksik değerlerin sayısını hesaplar ve büyükten küçüğe sıralar
    n_miss = dataframe[na_columns].isnull().sum().sort_values(ascending=False)

    # Her sütundaki eksik değerlerin oranını hesaplar ve büyükten küçüğe sıralar
    ratio = (dataframe[na_columns].isnull().sum() / dataframe.shape[0] * 100).sort_values(ascending=False)

    # Eksik değer tablosunu oluşturur
    missing_df = pd.concat([n_miss, np.round(ratio, 2)], axis=1, keys=['n_miss', 'ratio'])

    # Eksik değer tablosunu yazdırır
    print(missing_df, end="\n")

    # Opsiyonel olarak, eksik değer bulunan sütunların isimlerini döndürür
    if na_name:
        return na_columns


def quick_missing_imp(data, num_method="median", cat_length=20, target="Time_taken(min)"):
    """
    Verilen veri çerçevesindeki eksik değerleri hızlı bir şekilde doldurur.

    Parametreler:
    data (pandas.DataFrame): Eksik değerlerin doldurulacağı veri çerçevesi.
    num_method (str, optional): Sayısal değişkenler için kullanılacak doldurma yöntemi. "mean" veya "median" olabilir.
                                Varsayılan değer "median".
    cat_length (int, optional): Kategorik değişken olarak kabul edilecek sınıf sayısı. Varsayılan değer 20.
    target (str, optional): Hedef değişkenin adı. Varsayılan değer "Time_taken(min)".

    Returns:
    pandas.DataFrame: Eksik değerlerin doldurulmuş hali.

    Örnek:
    df = quick_missing_imp(dataframe, num_method="median", cat_length=20)
    """
    # Eksik değerlere sahip değişkenlerin listesi oluşturulur
    variables_with_na = [col for col in data.columns if data[col].isnull().sum() > 0]

    # Hedef değişken geçici olarak saklanır
    temp_target = data[target]

    print("# BEFORE")
    print(data[variables_with_na].isnull().sum(), "\n\n")  # Uygulama öncesi değişkenlerin eksik değerlerinin sayısı

    # Kategorik değişkenler için eksik değerler mode ile doldurulur (eğer sınıf sayısı belirli bir eşik değerden düşük veya eşitse)
    data = data.apply(lambda x: x.fillna(x.mode()[0]) if (x.dtype == "O" and len(x.unique()) <= cat_length) else x, axis=0)

    # Sayısal değişkenler için eksik değerler num_method parametresine göre doldurulur
    if num_method == "mean":
        data = data.apply(lambda x: x.fillna(x.mean()) if x.dtype != "O" else x, axis=0)
    elif num_method == "median":
        data = data.apply(lambda x: x.fillna(x.median()) if x.dtype != "O" else x, axis=0)

    # Hedef değişken eski haline getirilir
    data[target] = temp_target

    print("# AFTER \n Imputation method is 'MODE' for categorical variables!")
    print(" Imputation method is '" + num_method.upper() + "' for numeric variables! \n")
    print(data[variables_with_na].isnull().sum(), "\n\n")

    return data





def rare_analyser(dataframe, target, cat_cols):
    """
    Verilen kategorik değişkenlerin nadir sınıflarını analiz eder.

    Parametreler:
    dataframe (pandas.DataFrame): Kategorik değişkenlerin analiz edileceği veri çerçevesi.
    target (str): Hedef değişkenin adı.
    cat_cols (list): Analiz edilecek kategorik değişkenlerin adlarını içeren liste.

    Returns:
    None

    Örnek:
    rare_analyser(dataframe, "target_variable", ["categorical_col1", "categorical_col2"])
    """
    # Her bir kategorik değişken için nadir sınıfları ve ilgili istatistikleri yazdırır
    for col in cat_cols:
        print(col, ":", len(dataframe[col].value_counts()))
        print(pd.DataFrame({"COUNT": dataframe[col].value_counts(),
                            "RATIO": dataframe[col].value_counts() / len(dataframe),
                            "TARGET_MEAN": dataframe.groupby(col)[target].mean()}), end="\n\n\n")







def label_encoder(dataframe, binary_col):
    """
    Verilen kategorik bir değişkenin ikili sınıflarını 0 ve 1'e dönüştürür.

    Parametreler:
    dataframe (pandas.DataFrame): Etiket kodlama yapılacak veri çerçevesi.
    binary_col (str): İkili sınıflarına dönüştürülecek kategorik değişkenin adı.

    Returns:
    pandas.DataFrame: Etiket kodlaması yapılmış veri çerçevesi.

    Örnek:
    dataframe = label_encoder(dataframe, "binary_column")
    """
    # LabelEncoder nesnesi oluşturulur
    labelencoder = LabelEncoder()

    # İkili sınıfların etiket kodlaması yapılır
    dataframe[binary_col] = labelencoder.fit_transform(dataframe[binary_col])

    return dataframe


# İkili kategorik değişkenlerin listesi oluşturulur
binary_cols = [col for col in df.columns if df[col].dtypes == "O" and len(df[col].unique()) == 2]



def one_hot_encoder(dataframe, categorical_cols, drop_first=False):
    """
    Verilen kategorik değişkenleri one-hot kodlama ile dönüştürür.

    Parametreler:
    dataframe (pandas.DataFrame): One-hot kodlama yapılacak veri çerçevesi.
    categorical_cols (list): One-hot kodlama yapılacak kategorik değişkenlerin adlarını içeren liste.
    drop_first (bool, optional): İlk sütunun düşürülüp düşürülmeyeceği. Varsayılan değer False.

    Returns:
    pandas.DataFrame: One-hot kodlaması yapılmış veri çerçevesi.

    Örnek:
    dataframe = one_hot_encoder(dataframe, ["cat_column1", "cat_column2"], drop_first=True)
    """
    # Verilen kategorik değişkenleri one-hot kodlama ile dönüştürür
    dataframe = pd.get_dummies(dataframe, columns=categorical_cols, drop_first=drop_first)

    return dataframe




