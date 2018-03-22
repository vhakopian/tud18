import matplotlib.pyplot as plt 


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
        
        (m,M) = min(X[:,k]), max(X[:,k])
   
        X_reg = array([zeros(n) for k in range(101)])
        
        
        X_reg[:,k] = [m+(M-m)*k/100 for k in range(101)]
        y_reg = regressor(X_reg)
        
        ax.plot(X_reg[:,k],y_reg,c = 'b',markersize=1)
        
        ax.set_xlabel(label[k])
        ax.set_ylabel('no. of bugs')
    
    plt.show()