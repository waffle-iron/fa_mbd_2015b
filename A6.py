import pandas as pd
import numpy as np


dev = pd.read_csv('https://dl.dropboxusercontent.com/u/28535341/dev.csv') 

while True: 
    tv = input("Enter name of target variable (type e to exit):  ")   
    if tv in dev.columns:
        print("Perfect! Thanks") 
        break
    elif tv == 'e': 
        break  
while True: 
    id_var = input("Enter name of id variable (type e if none or to exit):  ")   
    if id_var in dev.columns:
        print("Perfect! Thanks")   
        break
    elif id_var == 'e':  
        break

a = dev[tv] 
to_drop = [tv,id_var] #Drop id 
to_drop  = [i for i in td1 if i != 'e']   
to_drop = [x for x in td if len(x) > 0]
in_model = dev.drop(to_drop, axis=1)    


for var_name in in_model:
    dev[var_name] = (dev[var_name]- dev[var_name].mean()) / (dev[var_name].max() - dev[var_name].min()) #normalize vble


b = in_model.as_matrix().astype(np.float) #New matrix b


from sklearn.cross_validation import KFold
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier as ADA
from sklearn.ensemble import GradientBoostingClassifier as GBC
from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.linear_model import SGDClassifier as SGDC


def cv(b, a, clf_class, **kwargs):
    kf = KFold(len(a), n_folds=10, shuffle=True)
    apr = a.copy() 
    for train_index, test_index in kf:
        b_train, b_test = b[train_index], b[test_index]
        atr = a[train_index]
        clf = clf_class(**kwargs)
        clf.fit(b_train,atr)
        apr[test_index] = clf.predict(b_test)
    return apr #Kfold 


def pct_correct(a_true,apr):
    return np.mean(a_true == apr) #Calculating accuracy



def model_select(): 
    name = ["Support Vector Machines","Random Forest","K-Nearest-Neighbors","AdaBoost","Gradient Boosting","Stochastic Gradient Descent"]
    model = [SVC,RF,KNN,ADA,GBC,SGDC]
    num = len(model) #Numbers to iterate
    list = []
    for index in range(num):
        list.append({'Model Name': name[index], '% Correct': pct_correct(a, cv(b, a, model[index]))}) #Models accuracy
    dev = pd.DataFrame(list)
    sorted_models = dev.sort_values(by='% Correct', ascending=False) #Accuracy order
    return(print(sorted_models))  


model_select()

