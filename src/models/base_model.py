from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error


dff = df.copy()

dff.drop(["ID", "Delivery_person_ID"], axis=1, inplace=True)
dff.drop(["Order_Date","Time_Orderd","Time_Order_picked"],axis=1, inplace=True)

cat_cols, cat_but_car, num_cols = grab_col_names(dff)

cat_cols = [col for col in cat_cols if col not in ["Time_taken(min)"]]
cat_cols

def label_encoder(dataframe, binary_col):
    labelencoder = LabelEncoder()
    dataframe[binary_col] = labelencoder.fit_transform(dataframe[binary_col])
    return dataframe

binary_cols = [col for col in df.columns if df[col].dtypes == "O" and len(df[col].unique()) == 2]

for col in binary_cols:
    label_encoder(dff, col)



def one_hot_encoder(dataframe, categorical_cols, drop_first=False):
    dataframe = pd.get_dummies(dataframe, columns=categorical_cols, drop_first=drop_first)
    return dataframe


cat_cols, cat_but_car, num_cols = grab_col_names(dff)

dff = one_hot_encoder(dff, cat_cols, drop_first=True)
dff = dff.replace({True: 1, False: 0})


dff.head()


train_df = dff[dff['Time_taken(min)'].notnull()]
test_df = dff[dff['Time_taken(min)'].isnull()]


y = train_df["Time_taken(min)"]
X = train_df.drop(["Time_taken(min)"], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=17)

models = [('LR', LinearRegression()),
          ("Ridge", Ridge()),
          ("Lasso", Lasso()),
          ("ElasticNet", ElasticNet()),
          ('KNN', KNeighborsRegressor()),
          ('CART', DecisionTreeRegressor()),
          ('RF', RandomForestRegressor()),
          ('SVR', SVR()),
          ('GBM', GradientBoostingRegressor()),
          ("XGBoost", XGBRegressor(objective='reg:squarederror')),
          ("LightGBM", LGBMRegressor()),
          ("CatBoost", CatBoostRegressor(verbose=False))]


for name, regressor in models:
    rmse = np.mean(np.sqrt(-cross_val_score(regressor, X, y, cv=5, scoring="neg_mean_squared_error")))
    print(f"RMSE: {round(rmse, 4)} ({name}) ")

"""
RMSE: 6.1136 (LR) 
RMSE: 6.1136 (Ridge) 
RMSE: 8.4142 (Lasso) 
RMSE: 8.3766 (ElasticNet) 
RMSE: 7.1633 (KNN) 
RMSE: 6.8524 (CART) 
RMSE: 5.0089 (RF) 
RMSE: 8.5332 (SVR) 
RMSE: 5.3192 (GBM) 
RMSE: 4.6999 (XGBoost)
RMSE: 4.8138 (LightGBM) 
RMSE: 4.6649 (CatBoost)  
"""

##### Log Dönşümlü #########

train_df = dff[dff['Time_taken(min)'].notnull()]
test_df = dff[dff['Time_taken(min)'].isnull()]

y = np.log1p(train_df['Time_taken(min)'])
X = train_df.drop(["Time_taken(min)"], axis=1)

for name, regressor in models:
    rmse = np.mean(np.sqrt(-cross_val_score(regressor, X, y, cv=5, scoring="neg_mean_squared_error")))
    print(f"RMSE: {round(rmse, 4)} ({name}) ")

"""
RMSE: 0.2417 (LR) 
RMSE: 0.2417 (Ridge) 
RMSE: 0.3556 (Lasso) 
RMSE: 0.3498 (ElasticNet) 
RMSE: 0.2744 (KNN) 
RMSE: 0.2762 (CART)
RMSE: 0.2015 (RF)
RMSE: 0.2553 (SVR) 
RMSE: 0.2125 (GBM) 
RMSE: 0.1885 (XGBoost)
RMSE: 0.1929 (LightGBM) 
RMSE: 0.1871 (CatBoost)    
"""




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

"""
linear Regression
 r2_score:  0.59
 MAE:   4.81
 MSE:   36.45
 rmse:  6.04
=========================
Ridge
 r2_score:  0.59
 MAE:   4.81
 MSE:   36.45
 rmse:  6.04
=========================
Random Forest
 r2_score:  0.72
 MAE:   3.85
 MSE:   24.38
 rmse:  4.94
=========================
Gradient Boosting
 r2_score:  0.68
 MAE:   4.16
 MSE:   27.89
 rmse:  5.28
=========================
XGBRegressor
 r2_score:  0.75
 MAE:   3.71
 MSE:   21.89
 rmse:  4.68
=========================
Decision Tree
 r2_score:  0.47
 MAE:   5.13
 MSE:   47.04
 rmse:  6.86
 
 =========================
SVM
 r2_score:  0.18
 MAE:   6.74
 MSE:   72.57
 rmse:  8.52
=========================
 



"""

