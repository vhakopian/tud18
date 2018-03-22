# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 10:48:02 2018

@author: Theo
"""

#Linear regression

import numpy as np
import statsmodels.formula.api as sm
from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error
from contributors import *


#Data preprocessing 


def split(X, y):
    #return : X_train, X_test, y_train, y_test
    return train_test_split(X, y, test_size=0.2, random_state=6)

def regression(X, y):
    
    
    #verifying that the first column is only composed of ones
    one = True
    for i in range (len(X)):
        if X[i, 0] != 1:
            one = False    
    if not one :
        print('changement')
        X = np.append(arr= np.ones((len(X), 1)).astype(int), values=X, axis=1)
        
    regressor_OLS = sm.OLS(endog = y, exog = X).fit()
    return(regressor_OLS)
    


    
def models(X, y):
    #Data preprpcessing
    X = np.append(arr= np.ones((len(X), 1)).astype(int), values=X, axis=1)
    
    #Splitting the dataset
    X_train, X_test, y_train, y_test = split(X,y)
        
    R = []
    MSE_train = []
    MSE_test = []
    
    #1) BASE
    X1_train = X_train[:, 0:2]
    X1_test = X_test[:, 0:2]
    regressor1 = regression(X1_train, y_train)
    R1 = regressor1.rsquared
    R.append(R1)
    
    
    #Prediction
    y_trainpredict1 = regressor1.predict(X1_train)
    y_testpredict1 = regressor1.predict(X1_test)
    MSE_train1 = mean_squared_error(y_train, y_trainpredict1)
    MSE_test1 = mean_squared_error(y_test, y_testpredict1)
    MSE_train.append(MSE_train1)
    MSE_test.append(MSE_test1)
    
    #2) BASE + TOTAL
    X2_train = X_train[:, [0,1,4]]
    X2_test = X_test[:, [0,1,4]]
    regressor2 = regression(X2_train, y_train)
    R2 = regressor2.rsquared
    R.append(R2)
    
    #Prediction
    y_trainpredict2 = regressor2.predict(X2_train)
    y_testpredict2 = regressor2.predict(X2_test)
    MSE_train2 = mean_squared_error(y_train, y_trainpredict2)
    MSE_test2 = mean_squared_error(y_test, y_testpredict2)
    MSE_train.append(MSE_train2)
    MSE_test.append(MSE_test2)
    
    
    #3) BASE + MINOR
    X3_train = X_train[:, 0:3]
    X3_test = X_test[:, 0:3]
    regressor3 = regression(X3_train, y_train)
    R3 = regressor3.rsquared
    R.append(R3)
    
    #Prediction
    y_trainpredict3 = regressor3.predict(X3_train)
    y_testpredict3 = regressor3.predict(X3_test)
    MSE_train3 = mean_squared_error(y_train, y_trainpredict3)
    MSE_test3 = mean_squared_error(y_test, y_testpredict3)
    MSE_train.append(MSE_train3)
    MSE_test.append(MSE_test3)
    
    #4) BASE + MINOR + MAJOR
    X4_train = X_train[:, 0:4]
    X4_test = X_test[:, 0:4]
    regressor4 = regression(X4_train, y_train)
    R4 = regressor4.rsquared
    R.append(R4)
    
    #Prediction
    y_trainpredict4 = regressor4.predict(X4_train)
    y_testpredict4 = regressor4.predict(X4_test)
    MSE_train4 = mean_squared_error(y_train, y_trainpredict4)
    MSE_test4 = mean_squared_error(y_test, y_testpredict4)
    MSE_train.append(MSE_train4)
    MSE_test.append(MSE_test4)
    
    #5) BASE + MINOR + MAJOR +OWNERSHIP
    X5_train = X_train[:, [0, 1, 2, 3, 5]]
    X5_test = X_test[:, [0, 1, 2, 3, 5]]
    regressor5 = regression(X5_train, y_train)
    R5 = regressor5.rsquared
    R.append(R5)
    
    #Prediction
    y_trainpredict5 = regressor5.predict(X5_train)
    y_testpredict5 = regressor5.predict(X5_test)
    MSE_train5 = mean_squared_error(y_train, y_trainpredict5)
    MSE_test5 = mean_squared_error(y_test, y_testpredict5)
    MSE_train.append(MSE_train5)
    MSE_test.append(MSE_test5)
    
    
    return R, MSE_train, MSE_test
    
def main():
    X, y = load_data('save_bootstrap.pkl')
    regressor = regression(X, y)
    print(models(X, y))
    
    
    

if __name__ == "__main__":
    main()
    
"""

#Splitting the dataset
from sklearn.cross_validation import train_test_split
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state= 0 )


#Plotting the graphs
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
#regressor.fit(X_train, y_train)


for i in range (0, np.size(X, 1)):
    #plt.plot(X_train[:, i], y)
   # plt.show()
"""