import matplotlib.pyplot as plt 
from numpy import *


def plot_regression(X,y,regressor):
    

    
    colors = ['g', 'r', 'c', 'm', 'y', 'k']
    
    fig = plt.figure()
    
    fig.suptitle('Number of bugs', fontsize=14)
    
    label = ["size", "churn", "minor", "major", "total", "ownership"]
    
    n = 6
    
    for k in range(n):
        ax = fig.add_subplot(2,3,k+1)

        color = colors[k]
        
        ax.plot(X[:,k],y,'o', c = color,markersize=5)
        
        ax.set_xlabel(label[k])
        ax.set_ylabel('no. of bugs')
    
    plt.show()