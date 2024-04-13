cat_cols, cat_but_car, num_cols = grab_col_names(df)

cat_cols = [col for col in cat_cols if col not in ["Time_taken(min)"]]
cat_cols

def label_encoder(dataframe, binary_col):
    labelencoder = LabelEncoder()
    dataframe[binary_col] = labelencoder.fit_transform(dataframe[binary_col])
    return dataframe

binary_cols = [col for col in df.columns if df[col].dtypes == "O" and len(df[col].unique()) == 2]

for col in binary_cols:
    label_encoder(df, col)

def one_hot_encoder(dataframe, categorical_cols, drop_first=False):
    dataframe = pd.get_dummies(dataframe, columns=categorical_cols, drop_first=drop_first)
    return dataframe


cat_cols, cat_but_car, num_cols = grab_col_names(df)

df = one_hot_encoder(df, cat_cols, drop_first=True)
df = df.replace({True: 1, False: 0})






train_df = df[df['Time_taken(min)'].notnull()]
test_df = df[df['Time_taken(min)'].isnull()]


y = train_df["Time_taken(min)"]
X = train_df.drop(["Time_taken(min)"], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=17)

def scores(y_test,p):

    r2 = r2_score(y_test, p)
    MAE = mean_absolute_error(y_test, p)
    MSE = mean_squared_error(y_test, p)
    rmse = np.sqrt(mean_squared_error(y_test, p))
    print(' r2_score:  {:.2f}'.format(r2))
    print(' MAE:   {:.2f}'.format(MAE))
    print(' MSE:   {:.2f}'.format(MSE))
    print(' rmse:  {:.2f}'.format(rmse))
    print("=========================")

models = {
    "linear Regression": LinearRegression(),
    "Ridge":Ridge(),
    "Random Forest": RandomForestRegressor(),
    "Gradient Boosting": GradientBoostingRegressor(),
    "XGBRegressor": XGBRegressor(),
    "Decision Tree": DecisionTreeRegressor(),
    "SVM": SVR()
}
for i in range(len(list(models))):
    model = list(models.values())[i]
    model.fit(X_train, y_train)
    p=model.predict(X_test)
    print(list(models.keys())[i])
    scores(y_test, p)
df["City"].value_counts()