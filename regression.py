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
from sklearn.preprocessing import StandardScaler


def split(X, y):
    #Split the dataset into a training dataset and a test dataset
    #return : X_train, X_test, y_train, y_test
    return train_test_split(X, y, test_size=0.2, random_state=6)

def regression(X, y):
    #This function returns a linear regressor based on X and y
    
    #Verifying that the first column is only composed of ones
    one = True
    for i in range (len(X)):
        if X[i, 0] != 1:
            one = False   
            
    #Features scaling and adding the ones column
    sc_X = StandardScaler()
    if not one :
        X = sc_X.fit_transform(X)
        X = np.append(arr= np.ones((len(X), 1)).astype(int), values=X, axis=1)
        print('Ones column added for the regression')
    else:
        X[:, 1:] = sc_X.fit_transform(X[:, 1:])
    sc_y = StandardScaler()
    y = y.reshape(-1, 1)
    y = sc_y.fit_transform(y)
    regressor_OLS = sm.OLS(endog = y, exog = X).fit()
    return(regressor_OLS)
    


    
def models(X, y):
    #Returns R-squared, MSE_train and MSE_test for each model
    print('size')
    print(str(size(X, axis=1)))
    #Data preprocessing
    X = np.append(arr= np.ones((len(X), 1)).astype(int), values=X, axis=1)
    #We had a ones column in order to add a constant to the regression
    print('size')
    print(str(size(X, axis=1)))
    #Splitting the dataset
    X_train, X_test, y_train, y_test = split(X,y)
        
    R = []
    MSE_train = []
    MSE_test = []
    
    #index used for the differents models
    index = [[0,1,2], [0,1,2,5], [0,1, 2, 3], [0,1, 2, 3, 4], [0,1, 2, 3, 4, 6]]
    #index = [[0,1], [0,1,4], [0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3, 4]]
    
    for i in range (0,5):
        print('model ' + str(i))
        current_Xtrain = X_train[:, index[i]]
        current_Xtest = X_test[:, index[i]]
        regressor = regression(current_Xtrain, y_train)
        
        sc_X = StandardScaler()
        current_Xtest[:, 1:] = sc_X.fit_transform(current_Xtest[:, 1:])
        
        sc_y = StandardScaler()
        y_test = y_test.reshape(-1, 1)
        y_test = sc_y.fit_transform(y_test)
        
        
        y_trainpred = regressor.predict(current_Xtrain)
        y_testpred = regressor.predict(current_Xtest)
        
        R.append(regressor.rsquared) 
        MSE_train.append(mean_squared_error(y_train, y_trainpred))
        MSE_test.append(mean_squared_error(y_test, y_testpred))
    
    return R, MSE_train, MSE_test
    
def main():
    
    X, y = load_data('save_bootstrap.pkl')
    print(models(X, y))
    print(regression(X,y).summary())
  

if __name__ == "__main__":
    main()
    

   
