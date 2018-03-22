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
        X = np.append(arr= np.ones((len(X), 1)).astype(int), values=X, axis=1)
        print('Ones column added for the regression')
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
    
    index = [[0,1], [0,1,4], [0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3, 4]]
    
    for i in range (0,5):
        current_Xtrain = X_train[:, index[i]]
        current_Xtest = X_test[:, index[i]]
        regressor = regression(current_Xtrain, y_train)
        R.append(regressor.rsquared)        
        y_trainpred = regressor.predict(current_Xtrain)
        y_testpred = regressor.predict(current_Xtest)
        MSE_train.append(mean_squared_error(y_train, y_trainpred))
        MSE_test.append(mean_squared_error(y_test, y_testpred))
    
    return R, MSE_train, MSE_test
    
def main():
    
    X, y = load_data('save_bootstrap.pkl')
    regressor = regression(X, y)
    print(models(X, y))
    
    
    
    

if __name__ == "__main__":
    main()
    

   
